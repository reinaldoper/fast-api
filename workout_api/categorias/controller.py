from pydantic import UUID4
from sqlalchemy.future import select
from uuid import uuid4
from fastapi import APIRouter, HTTPException, status, Body
from fastapi_pagination import Page, paginate, add_pagination
from workout_api.categorias.models import CategoriaModel
from workout_api.categorias.schemas import Categoria, CategoriaOut
from workout_api.contrib.dependencies import DatabaseDepencies
from fastapi import FastAPI


app = FastAPI(title="Pagination atleta", debug=True)

router = APIRouter()


@router.post('/', summary='Adicionar categoria', status_code=status.HTTP_201_CREATED, response_model=CategoriaOut)
async def post(db_session: DatabaseDepencies, categoria_in: Categoria = Body(...)) -> CategoriaOut:
    categorias_out = CategoriaOut(id=uuid4(), **categoria_in.model_dump())
    categoria_model = CategoriaModel(**categorias_out.model_dump())
    db_session.add(categoria_model)
    await db_session.commit()
   
    return categorias_out
   

@router.get('/', summary='Retornar todas as categorias', status_code=status.HTTP_200_OK, response_model=Page[list[CategoriaOut]])
async def query(db_session: DatabaseDepencies) -> list[CategoriaOut]:
    categorias: list[CategoriaOut] = (await db_session.execute(select(CategoriaModel))).scalars().all()
    return paginate(categorias)

 
@router.get('/{id}', summary='Retornar uma categoria pelo id', status_code=status.HTTP_200_OK, response_model=CategoriaOut)
async def query_id(id: UUID4, db_session: DatabaseDepencies) -> CategoriaOut:
    categoria: CategoriaOut = (await db_session.execute(select(CategoriaModel).filter_by(id=id))).scalars().first()
    if not categoria:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Categoria not found")
    return categoria


add_pagination(app)