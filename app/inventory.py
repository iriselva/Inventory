import requests
from app.models import db, Item, validate_item_id, validate_user_id, MONGO_ID
from bson import ObjectId
from fastapi import HTTPException
import traceback
import logging

# enpoints 

def add_inventory_routes(app):

    # create item POST
    @app.post('/inventory/{user_id}', status_code=201)
    # making type annotations making a variable for fastapi
    async def create_item(user_id: str, item: Item):
        
        if hasattr(item, 'id'):
            delattr(item, 'id')
            
        validate_user_id(user_id)
                
        user = db.users.find_one({MONGO_ID: ObjectId(user_id)})
        if user is None:
            raise HTTPException(404, 'User not found')

        item.user_id = user_id

        result = db.inventory.insert_one(item.dict(by_alias=True))
        if not result.acknowledged:
            raise HTTPException(400, 'Unable to create item')

        item.id = result.inserted_id
        return item


    # get all inventory items by user
    @app.get('/inventory/{user_id}')
    async def get_inventory(user_id: str):
        validate_user_id(user_id)

        #Validate that user exists
        user = db.users.find_one({MONGO_ID: ObjectId(user_id)})
        if user is None:
            raise HTTPException(404, "User not found")

        items = []
        for item in db.inventory.find({'user_id': user_id}):
            items.append(Item(**item))
    
        return items    


    @app.patch('/inventory/{user_id}/{item_id}', status_code=201)
    # making type annotations making a variable for fastapi
    async def update_item(user_id: str, item_id: str, item: Item):
        validate_item_id(item_id)

        if hasattr(item, 'id'):
            delattr(item, 'id')
            
        # finding item to update in the database to validate that it exists
        stored_item = db.inventory.find_one({MONGO_ID: ObjectId(item_id), 'user_id': user_id})
        if stored_item is None:
            raise HTTPException(404, "Item not found")

        # Add user_id to the update object so it wont get overwritten
        update = item.dict(by_alias=True)
        update["user_id"] = user_id
        
        #need to tell mongo what to do, $set makes it update all values that match update object
        result = db.inventory.update_one({MONGO_ID: ObjectId(item_id)}, { "$set": update})
        
        if not result.acknowledged:
            raise HTTPException(400, 'Unable to update item')
            
        item.id = ObjectId(item_id)
        item.user_id = user_id

        return item    

    @app.delete('/inventory/{user_id}/{item_id}', status_code=204)
    async def delete_item(user_id: str, item_id: str):
        
        validate_item_id(item_id)

        stored_item = db.inventory.find_one({MONGO_ID: ObjectId(item_id), 'user_id': user_id})
        if stored_item is None:
            raise HTTPException(404, "Item not found")

        result = db.inventory.delete_one({MONGO_ID: ObjectId(item_id)})

        if result.deleted_count == 0:
          raise HTTPException(400, 'Unable to delete item')






                