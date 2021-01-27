from fastapi import FastAPI
import requests
from models import db, User
import traceback
import logging
# importin the models.py file (object-id)
#from models import db, User

app = FastAPI()


@app.get('/')
async def index():
    return{'key': 'value'}

@app.get('/users')
async def list_users():
    users = []
    try:
        for user in db.users.find():
            users.append(User(**user))
        return {'users': users}    
    except Exception as e:
        print("An exception occurred", e)
        logging.error(traceback.format_exc())

    return {'users': []}

@app.get('/users/{user_id}')
def get_user(user_id: str):
    user = db.users.find({'_id':user_id})
    print(user)
    return {'user': User(**user)}


# to create a user
@app.post('/users')
# making type annotations making a variable for fastapi
async def create_user(user: User):
    if hasattr(user, 'id'):
        delattr(user, 'id')
    ret = db.users.insert_one(user.dict(by_alias=True))
    user.id = ret.inserted_id
    return {'user': user}

# to delete a user
@app.delete('/users/{user_id}')
def delete_user(user_id: int):
    db.pop(user_id-1)
    return{}
