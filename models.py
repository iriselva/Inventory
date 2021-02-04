from email_validator import validate_email, EmailNotValidError
from pydantic import BaseModel, Field
from fastapi import HTTPException
from pymongo import MongoClient
from typing import Optional
from bson import ObjectId
import datetime
import os

# hide MONGODB_URI in Environment Variables
client = MongoClient(os.environ['MONGODB_URI'])
db = client.database

MONGO_ID = "_id"
   
# checks whether an item ID is a valid MongoDB object ID string
def validate_item_id(item_id: str):
    if not ObjectId.is_valid(item_id):
        raise HTTPException(400, 'Invalid item id')

# checks whether a user ID is a valid MongoDB object ID string
def validate_user_id(user_id: str):
     if not ObjectId.is_valid(user_id):
        raise HTTPException(400, 'Invalid user id')

# checks whether an email is a valid email or not
def validate_user_email(email: str):
    try:
        # Validate
        valid = validate_email(email)

        # Update with the normalized form.
        email = valid.email
    except EmailNotValidError as e:
        # email is not valid, exception message is human-readable
        raise HTTPException(400, str(e))

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    # The method validate is used to check if the data received is actually valid for this class.
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    # modify schema is to avoid an error when accessing the documentation
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')

# MongoDB expects a field with the name _id, but Pydantic does not accept any field that starts with _. 
# Then we create an alias so Pydantic can understand our document.

# a pydantic user model to validate user requests
class User(BaseModel):
    id: Optional[PyObjectId] = Field(alias=MONGO_ID)
    username: str
    email: str
    password: str

    # The inner class Config is used to define some configuration for the model. 
    # Here we tell Pydantic that we are using a custom type (by arbitrary_types_allowed) 
    # and also a mapping for JSON serialization (by json_encoders).
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
        schema_extra = {
            "example": {
                "username": "str",
                "email": "str",
                "password": "str"
            }
        }

class UserOut(BaseModel):
    username: str
    email: str

# a pydantic item model to validate user requests
class Item(BaseModel):
    id: Optional[PyObjectId] = Field(alias=MONGO_ID)
    item: str 
    date: str
    description: str
    itemType: str
    amount: int
    user_id: Optional[str]
    image: str
    location: str
    price: str

    # The inner class Config is used to define some configuration for the model. 
    # Here we tell Pydantic that we are using a custom type (by arbitrary_types_allowed) 
    # and also a mapping for JSON serialization (by json_encoders).
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
        schema_extra = {
            "example": {
                "item": "Item name",
                "date": "2010-11-12",
                "description": "This is a description of the item",
                "itemType": "Painting",
                "amount": 1,
                "image": "string",
                "location": "In the gallery",
                "price": "1000 kr"
            }
        }



# a pydantic model for the access token
class Token(BaseModel):
    access_token: str
    token_type: str

# a pydantic model for access token data
class TokenData(BaseModel):
    user_id: Optional[str] = None
    username: Optional[str] = None
