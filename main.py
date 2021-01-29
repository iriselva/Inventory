from fastapi import FastAPI, HTTPException
from models import db, User, Item, validate_user_id
from bson import ObjectId
# import requests
import traceback, logging
from inventory import add_inventory_routes
app = FastAPI()

@app.get('/')
async def index():
    return 'Hello there!'


@app.get('/users')
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
    if hasattr(user, 'id'):
        delattr(user, 'id')

    result = db.users.insert_one(user.dict(by_alias=True))

    if not result.acknowledged:
        raise HTTPException(400, 'Unable to create user')

    user.id = result.inserted_id
    return user


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