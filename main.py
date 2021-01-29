
from fastapi import FastAPI, Security
from models import db, User, Item
from fastapi import FastAPI, HTTPException
from models import db, User, Item, validate_user_id
from bson import ObjectId
import traceback, logging

from routes.inventory import add_inventory_routes
from uuid import uuid4
from mysecurity import check_api_key
from inventory import add_inventory_routes

app = FastAPI()

@app.get('/')
async def index():
    return 'Hello there!'

@app.get('/users', dependencies=[Security(check_api_key)])

async def list_users():
    users = []
   
    for user in db.users.find():
        users.append(User(**user))

    return users    


@app.get('/users/{user_id}')
async def get_user(user_id: str):

    validate_id(user_id)

    user = db.users.find_one({'_id': ObjectId(user_id)})
    
    if user is None:
        raise HTTPException(404, "User not found")

    return User(**user)


# to create a user
@app.post('/users', status_code=201)
# making type annotations making a variable for fastapi
async def create_user(user: User):
    # TODO: return status code 409 if email is already in use

    # get user dict from pydantic model
    user_data = dict(user)

    # remove empty ID from dict
    del user_data['id']

    # generate new API key and add to dict
    user_data['api_key'] = str(uuid4())

    try:
        # insert user into MongoDB
        db.users.insert_one(user_data)
    except Exception as e:
        logging.error("An exception occurred", e)
        logging.error(traceback.format_exc())
        # TODO: return status code 500 or something idk

    # convert ObjectID '_id' to string
    user_data['id'] = str(user_data['_id'])

    # remove '_id' (but keep 'id') because it can't be serialized to JSON
    del user_data['_id']

    # return the newly created user to the client
    return {'user': user_data}

# to delete a user
@app.delete('/users/{user_id}', status_code=204)
async def delete_user(user_id: str):

    validate_id(user_id)
    
    user = db.users.find_one({'_id': ObjectId(user_id)})
    if user is None:
        raise HTTPException(404, "User not found")

    result = db.users.delete_one({'_id': ObjectId(user_id)})

    if result.deleted_count == 0:
        raise HTTPException(400, 'Unable to delete')


add_inventory_routes(app)
