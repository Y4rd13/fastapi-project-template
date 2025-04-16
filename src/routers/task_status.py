from celery.result import AsyncResult
from fastapi import APIRouter

router = APIRouter()

@router.get("/status/{task_id}", summary="Check task status", description="Check the status of a task using its ID.")
async def get_task_status(task_id: str):
    """
    Endpoint to get the status of any task using its task_id.
    """
    task_result = AsyncResult(task_id)
    return {
        "task_id": task_id,
        "status": task_result.status,
        "result": task_result.result
    }