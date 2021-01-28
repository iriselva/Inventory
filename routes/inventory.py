import requests
from models import db, Item
import traceback
import logging

# enpoints 

def add_inventory_routes(app):

    # create item POST
    @app.post('/inventory', status_code=201)
    # making type annotations making a variable for fastapi
    async def create_item(item: Item):
        # TODO: return status code 409 if email is already in use
        if hasattr(item, 'id'):
            delattr(item, 'id')

        try:
            # user validation
            user = db.users.find_one({'_id': ObjectId(item.user_id)})
            if user is None:
                logging.error("User was not found")
                return "Error: User not found"
            
            result = db.inventory.insert_one(item.dict(by_alias=True))
        except Exception as e:
            logging.error("An exception occurred", e)
            logging.error(traceback.format_exc())
            # TODO: return status code 500 or something idk

        item.id = result.inserted_id
        return {'item': item}

    # get all inventory items by user
    @app.get('/inventory/{user_id}')
    async def get_inventory(user_id: str):
        items = []
        try:
            user = db.users.find_one({'_id': ObjectId(user_id)})
            if user is None:
                logging.error("User was not found")
                return "Error: User not found"
            for item in db.inventory.find({'user_id': user_id}):
                items.append(Item(**item))
        except Exception as e:
            logging.error("An exception occurred", e)
            logging.error(traceback.format_exc())
            # TODO: return status code 500 or something idk

        return {'items': items}    

# updating item - still working on it
#   @app.patch('/inventory/{user_id}/{item_id}')
#   async def update_item(item_id: str):
#        try:
#            item = db.inventory.find_one({'_id' ObjectID(item_id)})
#            if user is None:
#                logging.error("User was not found")
#                return "Error: User not found"
#                #raise HTTPException(404)?
#            for item in db.inventory.update_one({'item_id': item_id}):
#                items.setattr(item, name, value)#item, date, description, type_of_item, amount, image, location
#            return item
                
                
        
