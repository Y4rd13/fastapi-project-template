from fastapi import FastAPI, Depends
from routers import (
    health, 
    task_status, 
    auth,
    your_service_route
)
from utils.auth_utils import get_current_user
from src.core.logger_func import logger
#from scripts.test_cuda import check_cuda

app = FastAPI(
    title="Project Template API",
    description="Project Template API Service",
    version="1.0.0",
    docs_url="/swagger",
    redoc_url="/redoc"
)

app.include_router(health.router, tags=["health"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])

# Test routes without JWT
#app.include_router(your_service_route.router, prefix="/test/v1", tags=["test-service"])

v1_routers = [
    your_service_route.router,
    task_status.router,
]

for router in v1_routers:
    app.include_router(router, prefix="/api/v1", tags=["v1"], dependencies=[Depends(get_current_user)])

@app.on_event("startup")
def startup_event():
    logger.info("-" * 50)
    logger.info("Starting API...")
    #logger.info("Checking for CUDA support on the system...")
    #check_cuda()
    logger.info("Application setup complete.")
    logger.info("-" * 50)