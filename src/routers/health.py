from fastapi import APIRouter
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta

router = APIRouter()
start_time = datetime.now()

@router.get("/health", summary="Check API health", description="Returns the API status and uptime.")
async def health_check():
    """
    Checks if the API is running and returns the uptime.
    """
    current_time = datetime.now()
    uptime = current_time - start_time
    health_status = {
        "status": "ok",
        "message": "API is up and running",
        "uptime": str(timedelta(seconds=uptime.total_seconds()))
    }
    return JSONResponse(content=health_status)