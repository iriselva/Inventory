from fastapi import FastAPI
from models import db, User, Item
from bson import ObjectId
# import requests
import traceback, logging
from routes.inventory import add_inventory_routes
app = FastAPI()

@app.get('/')
async def index():
    return 'Hello there!'

@app.get('/users')
async def list_users():
    users = []
    try:
        for user in db.users.find():
            users.append(User(**user))
        return {'users': users}    
    except Exception as e:
        logging.error("An exception occurred", e)
        logging.error(traceback.format_exc())
        # TODO: return status code 500 or something idk

    return {'users': []}

@app.get('/users/{user_id}')
async def get_user(user_id: str):
    try:
        user = db.users.find_one({'_id': ObjectId(user_id)})
    except Exception as e:
        logging.error("An exception occurred", e)
        logging.error(traceback.format_exc())
        # TODO: return status code 500 or something idk

    return {'user': User(**user)}

# to create a user
@app.post('/users', status_code=201)
# making type annotations making a variable for fastapi
async def create_user(user: User):
    # TODO: return status code 409 if email is already in use
    if hasattr(user, 'id'):
        delattr(user, 'id')

    try:
        result = db.users.insert_one(user.dict(by_alias=True))
    except Exception as e:
        logging.error("An exception occurred", e)
        logging.error(traceback.format_exc())
        # TODO: return status code 500 or something idk

    user.id = result.inserted_id
    return {'user': user}

# to delete a user
@app.delete('/users/{user_id}')
async def delete_user(user_id: str):
    try:
        db.users.delete_one({'_id': ObjectId(user_id)})
    except Exception as e:
        logging.error("An exception occurred", e)
        logging.error(traceback.format_exc())
        # TODO: return status code 500 or something idk

add_inventory_routes(app)