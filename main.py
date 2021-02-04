from mysecurity import authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from fastapi.openapi.utils import get_openapi
from inventory import add_inventory_routes
from users import add_users_routes
from datetime import timedelta
from models import Token

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
)

# custom schema for the FastAPI - Swagger UI 
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Our Inventory API",
        version="1.0.0",
        description="This is the OpenAPI schema for our Module 5 Project.<br>" 
        "The panel below displays documentation for all endpoints, <br>parameters and error messages available to the API.<br><br>"
        "<b>Getting Started</b><br><br>"
        "To start using the API you must first create a user using the POST /users endpoint.<br>After you've created a user you get an OAuth2 access token by sending a POST request <br>"
        "to /token with the newly created credentials. To use the API you must place this token <br>in an Authorization header of all requests."
        " This token remains valid for 30 minutes.",
        routes=app.routes
    )

    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# redirects users to docs, is hidden in swagger
@app.get('/', include_in_schema=False)
async def index():
    response = RedirectResponse(url='/docs')
    return response

# login for access token
@app.post('/token', tags=["Login"], response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # authenticate user by username and password
    user = authenticate_user(form_data.username, form_data.password)

    # if user not found then return 401 HTTP status code
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},  # tell user how to authenticate
        )

    # create access token containing the user's ID and username,
    # and make it expire in ACCESS_TOKEN_EXPIRE_MINUTES
    access_token = create_access_token(
        data={'sub': str(user['_id']), 'username': user['username']},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    # return the access token to the user
    return {'access_token': access_token, 'token_type': 'bearer'}

# add routes to the API
add_users_routes(app)
add_inventory_routes(app)
from mysecurity import authenticate_user, create_access_token
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from mysecurity import ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from fastapi.openapi.utils import get_openapi
from inventory import add_inventory_routes
from users import add_users_routes
from datetime import timedelta
from models import Token

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Our Inventory API",
        version="1.0.0",
        description="This is the OpenAPI schema for our Module 5 Project",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.get('/', tags=["Root"])
async def index():
    response = RedirectResponse(url='/docs')
    return response

@app.post('/token', response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': str(user['_id']), 'username': user['username']},
        expires_delta=access_token_expires
    )
    return {'access_token': access_token, 'token_type': 'bearer'}

add_users_routes(app)
add_inventory_routes(app)
