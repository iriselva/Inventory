from fastapi.security.api_key import APIKeyHeader, HTTPException
from fastapi import status, Depends
from models import db

api_key_header = APIKeyHeader(name='X-API-Key', auto_error=True)

def check_api_key(x_api_key: str = Depends(api_key_header)):
    try:
        user = db.users.find_one({'api_key': x_api_key})
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid API key'
        )
