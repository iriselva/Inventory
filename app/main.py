
from fastapi import FastAPI
from app.inventory import add_inventory_routes
from app.users import add_users_routes

app = FastAPI()

@app.get('/')
async def index():
    return 'Hello there!'

add_users_routes(app)
add_inventory_routes(app)

if __name__ == "__main__":
    uvicorn.run("app:main", host='0.0.0.0')