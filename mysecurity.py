from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from passlib.context import CryptContext
from models import db, TokenData
from jose import JWTError, jwt
from typing import Optional
from bson import ObjectId
import os

# hide Secret Key in Environment Variables
# the secret key is used to sign the access token
SECRET_KEY = os.environ['SECRET_KEY']

# Signing algorithm is used to sign tokens issued for your application or API. 
# A signature is part of a JWT and is used to verify that the sender of 
# the token is who it says it is and to ensure that the message wasn't changed along the way.
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# CryptContext manages hashes and related policy configuration
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# configure FastAPI to use OAuth2 Password Bearer authentication method
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

# find user by its username in database
def get_user_by_username(username: str):
    user = db.users.find_one({'username': username})
    return user

# find user by its ID in database
def get_user_by_id(id: str):
    user = db.users.find_one({'_id': ObjectId(id)})
    return user

# compare plain text password to a hashed password when logging in
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# hash a password with the pwd_context (bcrypt)
def get_password_hash(password):
    return pwd_context.hash(password)

# authenticate user when logging in with the inputted username and password
def authenticate_user(username: str, password: str):
    user = get_user_by_username(username)
    if not user:
        return False
    if not verify_password(password, user['password']):
        return False
    return user

# generate a new access token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    # copy the token (by value) data to a new variable
    to_encode = data.copy()

    # set token expiration if specified
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # default token expiration timer is 15 minutes
        expire = datetime.utcnow() + timedelta(minutes=15)

    # insert expiration timer to token
    to_encode.update({'exp': expire})

    # encode and sign the token with secret key and decryption algorithm
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

# get user by his/her ID (which is stored in the token)
async def get_current_user(token: str = Depends(oauth2_scheme)):
    # if token is invalid, return an HTTP error
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        # Decode the received token, verify it with secret key, and return the current user
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    
        user_id: str = payload.get('sub')
        username: str = payload.get('username')
    
        if user_id is None:
            raise credentials_exception

        token_data = TokenData(user_id=user_id, username=username)
    except JWTError:
        raise credentials_exception

    # get user by his/her ID (that came from the token) from the database
    user = get_user_by_id(token_data.user_id)
    if user is None:
        raise credentials_exception

    return user
    