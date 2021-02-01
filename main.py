from fastapi import FastAPI
from inventory import add_inventory_routes
from users import add_users_routes
from fastapi.openapi.utils import get_openapi
from starlette.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

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


add_users_routes(app)
add_inventory_routes(app)
