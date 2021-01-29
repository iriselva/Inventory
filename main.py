
from fastapi import FastAPI
from inventory import add_inventory_routes
from users import add_users_routes

app = FastAPI()

@app.get('/')
async def index():
    return 'Hello there!'

add_users_routes(app)
add_inventory_routes(app)
