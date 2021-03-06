from models import db, User, UserOut, validate_user_email, MONGO_ID
from mysecurity import get_current_user, get_password_hash
from fastapi import HTTPException, Depends

def add_users_routes(app):
    # create user
    @app.post('/users', tags=["Users"], response_model=UserOut, status_code=201, 
              description="Creats a new user.<br><br>"
              "Responds with HTTP status code 409 if username or email already exists.")
    async def create_user(user: User):
        # remove empty ID from user model
        if hasattr(user, 'id'):
            delattr(user, 'id')

        # check if email is valid
        validate_user_email(user.email)
        # check if email is already in use
        try:
            email_user = db.users.find_one({'email': user.email})
        except Exception as e:
            raise HTTPException(500, "Internal Server Error")
        if email_user:
            raise HTTPException(409, "This email is already in use")
        
        # check if username is already in use
        try:
            username = db.users.find_one({'username': user.username})
        except Exception as e:
            raise HTTPException(500, "Internal Server Error")
        if username:
            raise HTTPException(409, "This username is already in use")

        # hash password
        user.password = get_password_hash(user.password)

        # insert user into MongoDB
        try:
            db.users.insert_one(dict(user))
        except Exception as e:
            raise HTTPException(500, "Internal Server Error")

        # return the newly created user to the client
        return dict(user)

    # get current user
    @app.get('/users', tags=["Users"], status_code=200, 
             description="Gets information about the logged in user.")
    async def get_user(user: User = Depends(get_current_user)):
        # convert object ID to string
        user['id'] = str(user['_id'])
        del user['_id']

        # remove hashed password from result
        del user['password']

        return user

    # delete a user
    @app.delete('/users', tags=["Users"], status_code=200, 
                 description="Deletes the currently logged in user.<br><br>")
    async def delete_user(user: User = Depends(get_current_user)):
        result = db.users.delete_one({MONGO_ID: user[MONGO_ID]})

        if result.deleted_count == 0:
            raise HTTPException(500, 'Unable to delete user')
