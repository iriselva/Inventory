from fastapi import FastAPI, Security, HTTPException
from models import db, User, UserOut, validate_user_id, validate_user_email, MONGO_ID
from bson import ObjectId
from uuid import uuid4
from mysecurity import check_api_key
import bcrypt

def add_users_routes(app):
  @app.get('/users')
  async def get_user(user: str = Security(check_api_key)):
      user = db.users.find_one({MONGO_ID: user[MONGO_ID]})
      
      if user is None:
          raise HTTPException(404, "User not found")

      return User(**user)

  # to create a user
  @app.post('/users', response_model=UserOut, status_code=201)
  # making type annotations making a variable for fastapi
  async def create_user(user: User):
      # TODO: return status code 409 if email is already in use
      validate_user_email(user.email)
      # get user dict from pydantic model
      user_data = dict(user)

      # remove empty ID from dict
      del user_data['id']

      # generate new API key and add to dict
      user_data['api_key'] = str(uuid4())

      # change password to bytes string before we hash it
      user_data['password'] = bytes(user_data['password'], 'utf-8')

      # hash password with bcrypt
      user_data['password'] = bcrypt.hashpw(user_data['password'], bcrypt.gensalt())

      # change hashed password to bytes string to string
      user_data['password'] = str(user_data['password'])

      try:
          # insert user into MongoDB
          db.users.insert_one(user_data)
      except Exception as e:
          raise HTTPException(500, "Internal Server Error")

      # convert ObjectID '_id' to string
      user_data['id'] = str(user_data['_id'])

      # remove '_id' (but keep 'id') because it can't be serialized to JSON
      del user_data['_id']

      # return the newly created user to the client
      return {'user': user_data}

  # to delete a user
  @app.delete('/users', status_code=200)
  async def delete_user(user: str = Security(check_api_key)):
    result = db.users.delete_one({MONGO_ID: user[MONGO_ID]})

    if result.deleted_count == 0:
        raise HTTPException(400, 'Unable to delete')
