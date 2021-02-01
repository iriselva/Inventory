from fastapi.security.api_key import APIKeyHeader, HTTPException
from fastapi import status, Depends
from models import db

api_key_header = APIKeyHeader(name='X-API-Key', auto_error=True)

def check_api_key(x_api_key: str = Depends(api_key_header)):
    try:
        user = db.users.find_one({'api_key': x_api_key})
    except Exception:
        raise HTTPException(500, 'Internal Server Error')
    
    if not user:
        raise HTTPException(401, 'Invalid API key')

    return user
