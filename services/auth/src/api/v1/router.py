from fastapi import APIRouter
from src.api.v1 import auth
from src.api.v1 import health

router = APIRouter(prefix="/v1")

router.include_router(auth.router)
router.include_router(health.router)
