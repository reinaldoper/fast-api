from pydantic import UUID4
from sqlalchemy.future import select
from uuid import uuid4
from fastapi import APIRouter, HTTPException, status, Body
from fastapi_pagination import Page, paginate, add_pagination
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from workout_api.centro_treinamento.schemas import CentroTreinamento, CentroTreinamentoOut
from workout_api.contrib.dependencies import DatabaseDepencies
from fastapi import FastAPI


app = FastAPI(title="Pagination atleta", debug=True)

router = APIRouter()


@router.post('/', summary='Adicionar treinamento', status_code=status.HTTP_201_CREATED, response_model=CentroTreinamentoOut)
async def post(db_session: DatabaseDepencies, treinamento_in: CentroTreinamento = Body(...)) -> CentroTreinamentoOut:
    centro_treinamento_out = CentroTreinamentoOut(id=uuid4(), **treinamento_in.model_dump())
    treinamento_model = CentroTreinamentoModel(**centro_treinamento_out.model_dump())
    db_session.add(treinamento_model)
    await db_session.commit()
   
    return centro_treinamento_out
   

@router.get('/', summary='Retornar todos os centros treinamentos', status_code=status.HTTP_200_OK, response_model=Page[list[CentroTreinamentoOut]])
async def query(db_session: DatabaseDepencies) -> list[CentroTreinamentoOut]:
    treinamentos: list[CentroTreinamentoOut] = (await db_session.execute(select(CentroTreinamentoModel))).scalars().all()
    return paginate(treinamentos)

 
@router.get('/{id}', summary='Retornar uma centro treinamento pelo id', status_code=status.HTTP_200_OK, response_model=CentroTreinamentoOut)
async def query_id(id: UUID4, db_session: DatabaseDepencies) -> CentroTreinamentoOut:
    treinamento: CentroTreinamentoOut = (await db_session.execute(select(CentroTreinamentoModel).filter_by(id=id))).scalars().first()
    if not treinamento:
        raise HTTPException(404, detail="Training center not found")
    return treinamento


add_pagination(app)