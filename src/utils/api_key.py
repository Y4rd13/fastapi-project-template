from fastapi import Header, HTTPException
from starlette.status import HTTP_403_FORBIDDEN
from core.config import settings

async def get_api_key(api_key: str = Header(..., alias="X-API-KEY")):
    if api_key != settings.API_KEY:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Invalid API Key"
        )
    return api_key