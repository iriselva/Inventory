import requests
from models import db, Item, validate_item_id, validate_user_id, MONGO_ID
from bson import ObjectId
from fastapi import HTTPException, Security
import traceback
import logging
from mysecurity import check_api_key

# enpoints 

def add_inventory_routes(app):

    # create item POST
    @app.post('/inventory', status_code=201)
    # making type annotations making a variable for fastapi
    async def create_item(item: Item, user: str = Security(check_api_key)):
        if hasattr(item, 'id'):
            delattr(item, 'id')

        item.user_id = str(user['_id'])

        result = db.inventory.insert_one(item.dict(by_alias=True))
        if not result.acknowledged:
            raise HTTPException(400, 'Unable to create item')

        item.id = result.inserted_id
        return item

    # get all inventory items by user
    @app.get('/inventory')
    async def get_inventory(user: str = Security(check_api_key)):
        items = []
        for item in db.inventory.find({'user_id': str(user['_id'])}):
            items.append(Item(**item))
    
        return items    

    @app.patch('/inventory/{item_id}', status_code=201)
    # making type annotations making a variable for fastapi
    async def update_item(item_id: str, item: Item, user: str = Security(check_api_key)):
        validate_item_id(item_id)

        if hasattr(item, 'id'):
            delattr(item, 'id')
            
        # finding item to update in the database to validate that it exists
        stored_item = db.inventory.find_one({MONGO_ID: ObjectId(item_id), 'user_id': str(user['_id'])})
        if stored_item is None:
            raise HTTPException(404, "Item not found")

        # Add user_id to the update object so it wont get overwritten
        update = item.dict(by_alias=True)
        update["user_id"] = str(user['_id'])
        
        #need to tell mongo what to do, $set makes it update all values that match update object
        result = db.inventory.update_one({MONGO_ID: ObjectId(item_id)}, { "$set": update})
        
        if not result.acknowledged:
            raise HTTPException(400, 'Unable to update item')
            
        item.id = ObjectId(item_id)
        item.user_id = user['_id']

        return item    

    @app.delete('/inventory/{item_id}', status_code=200)
    async def delete_item(item_id: str, user: str = Security(check_api_key)):
        
        validate_item_id(item_id)

        stored_item = db.inventory.find_one({MONGO_ID: ObjectId(item_id), 'user_id': str(user['_id'])})
        if stored_item is None:
            raise HTTPException(404, "Item not found")

        result = db.inventory.delete_one({MONGO_ID: ObjectId(item_id)})

        if result.deleted_count == 0:
          raise HTTPException(400, 'Unable to delete item')
