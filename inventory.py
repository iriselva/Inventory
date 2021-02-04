from models import db, Item, validate_item_id, MONGO_ID
from fastapi import HTTPException, Depends
from mysecurity import get_current_user
from bson import ObjectId
from models import User

def add_inventory_routes(app):
    # create item
    @app.post('/inventory', tags=["Inventory"], status_code=201)
    async def create_item(item: Item, user: User = Depends(get_current_user)):
        # remove empty ID from inventory model
        if hasattr(item, 'id'):
            delattr(item, 'id')

        # add user ID to item
        item.user_id = str(user['_id'])

        # convert datetime variable to string
        item.date = str(item.date)

        # insert item to database
        result = db.inventory.insert_one(item.dict(by_alias=True))
        if not result.acknowledged:
            raise HTTPException(400, 'Unable to create item')

        # add newly generated ID to the item
        item.id = result.inserted_id
        return item
    
    # get an inventory item by its ID
    @app.get('/inventory/{item_id}', tags=['Inventory'], description='Get an inventory item by its ID', status_code=200)
    async def get_item(item_id: str, user: User = Depends(get_current_user)):
        validate_item_id(item_id)
        
        # get item from database
        item = db.inventory.find_one({'_id': ObjectId(item_id), 'user_id': str(user['_id'])})
        if not item:
            raise HTTPException(404, "Item not found")
    
        # convert object ID to string
        item['id'] = str(item['_id'])
        del item['_id']  # delete object ID

        return item

    # update inventory item
    @app.patch('/inventory/{item_id}', tags=["Inventory"], description="", status_code=201)
    async def update_item(item_id: str, item: Item, user: User = Depends(get_current_user)):
        validate_item_id(item_id)

        # remove empty ID from inventory model
        if hasattr(item, 'id'):
            delattr(item, 'id')
            
        # find item to update in the database to validate that it exists
        stored_item = db.inventory.find_one({MONGO_ID: ObjectId(item_id), 'user_id': str(user['_id'])})
        if stored_item is None:
            raise HTTPException(404, "Item not found")

        # add user_id to the update object so it wont get overwritten
        update = item.dict(by_alias=True)
        update["user_id"] = str(user['_id'])
        update['date'] = str(item.date)
        
        # need to tell mongo what to do, $set makes it update all values that match update object
        result = db.inventory.update_one({MONGO_ID: ObjectId(item_id)}, { "$set": update})
        if not result.acknowledged:
            raise HTTPException(400, 'Unable to update item')

        # add ID and user ID to result
        item.id = item_id
        item.user_id = str(user['_id'])

        return item

    # delete item
    @app.delete('/inventory/{item_id}', tags=["Inventory"], description="", status_code=200)
    async def delete_item(item_id: str, user: User = Depends(get_current_user)):
        validate_item_id(item_id)

        # get item from database by its ID to check if it exists
        stored_item = db.inventory.find_one({MONGO_ID: ObjectId(item_id), 'user_id': str(user['_id'])})
        if stored_item is None:
            raise HTTPException(404, "Item not found")

        # delete item from database
        result = db.inventory.delete_one({MONGO_ID: ObjectId(item_id)})
        if result.deleted_count == 0:
          raise HTTPException(400, 'Unable to delete item')

    # get all inventory items by user
    @app.get('/inventory', tags=["Inventory"], description="A more detailed description goes here.....")
    async def get_inventory(user: User = Depends(get_current_user)):
        items = []
        # find all items in database by user ID and append them to the items list
        for item in db.inventory.find({'user_id': str(user['_id'])}):
            # change item ID from object ID to string
            item['id'] = str(item['_id'])
            del item['_id']  # delete object ID
            items.append(item)
        return items    
