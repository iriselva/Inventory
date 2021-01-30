
from fastapi import FastAPI
from inventory import add_inventory_routes
from users import add_users_routes
import uvicorn



app = FastAPI()

@app.get('/')
async def index():
    return 'Hello there!'

add_users_routes(app)
add_inventory_routes(app)

if __name__ == "__main__":
    uvicorn.run("server.app:app", host="0.0.0.0", port=8000, reload=True)