from fastapi import APIRouter
from workout_api.atleta.controller import router as atletas
from workout_api.categorias.controller import router as categorias
from workout_api.centro_treinamento.controller import router as centro_treinamento


api_router = APIRouter()
api_router.include_router(atletas, prefix='/atletas', tags=['atletas'])
api_router.include_router(categorias, prefix='/categorias', tags=['categorias'])
api_router.include_router(centro_treinamento, prefix='/centro', tags=['centro-treinamento'])