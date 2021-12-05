from fastapi import APIRouter

from .endpoints import test, images, common

api_v1_router = APIRouter()
api_v1_router.include_router(test.router, prefix='/test')
api_v1_router.include_router(images.router, prefix='/images')
api_v1_router.include_router(common.router, prefix='/common')
