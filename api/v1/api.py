from fastapi import APIRouter
from api.v1.endpoints import usuario
from api.v1.endpoints import predicao

api_router = APIRouter()

api_router.include_router(usuario.router, prefix='/usuarios', tags=['usuarios'])
api_router.include_router(predicao.router, prefix='/predicoes', tags=['predicoes'])