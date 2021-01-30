
from fastapi import FastAPI
from inventory import add_inventory_routes
from users import add_users_routes

app = FastAPI()

@app.get('/')
async def index():
    return 'Hello there!'

add_users_routes(app)
add_inventory_routes(app)

print('BEFORE MAIN')
if __name__ == "__main__":
    print('AFTER MAIN')
    uvicorn.run("app:main", host='0.0.0.0')