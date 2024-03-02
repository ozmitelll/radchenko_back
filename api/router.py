from fastapi import APIRouter

from api import (
    user,
    order
)
api_router = APIRouter()
api_router.include_router(user.auth, prefix="/auth", tags=["Authentication"])
api_router.include_router(user.router, prefix="/user", tags=["User"])
api_router.include_router(order.router, prefix='/orders', tags=["Orders"])

