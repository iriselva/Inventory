from fastapi import FastAPI
import requests
import main.py
from models import db, Item 

app = FastAPI()

# enpoints 
# create item POST
@app.post('/inventory', status_code=201)
# making type annotations making a variable for fastapi
async def create_item(item: Item):
    # TODO: return status code 409 if email is already in use
    if hasattr(item, 'id'):
        delattr(item, 'id')

    try:
        result = db.inventory.insert_one(item.dict(by_alias=True))
    except Exception as e:
        logging.error("An exception occurred", e)
        logging.error(traceback.format_exc())
        # TODO: return status code 500 or something idk

    item.id = result.inserted_id
    return {'item': item}
