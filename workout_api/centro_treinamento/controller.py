from pydantic import UUID4
from sqlalchemy import select
from uuid import uuid4
from fastapi import APIRouter, HTTPException, status, Body
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from workout_api.centro_treinamento.schemas import CentroTreinamento, CentroTreinamentoOut
from workout_api.contrib.dependencies import DatabaseDepencies
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post('/', summary='Adicionar treinamento',
             status_code=status.HTTP_201_CREATED,
             response_model=CentroTreinamentoOut)
async def post(db_session: DatabaseDepencies,
               treinamento_in: CentroTreinamento = Body(...)) -> CentroTreinamentoOut:
    centro_treinamento_out = CentroTreinamentoOut(id=uuid4(), **treinamento_in.model_dump())
    treinamento_model = CentroTreinamentoModel(**centro_treinamento_out.model_dump())
    db_session.add(treinamento_model)
    await db_session.commit()
   
    return centro_treinamento_out
   

@router.get('/', summary='Retornar todos os centros treinamentos', 
            status_code=status.HTTP_200_OK,
            response_model=list[CentroTreinamentoOut])
async def query(db_session: DatabaseDepencies,
                offset: int = 0, limit: int = 10) -> list[CentroTreinamentoOut]:
    async with db_session as session:
        return await paginate(session, offset, limit)

 
@router.get('/{id}', summary='Retornar uma centro treinamento pelo id', status_code=status.HTTP_200_OK, response_model=CentroTreinamentoOut)
async def query_id(id: UUID4, db_session: DatabaseDepencies) -> CentroTreinamentoOut:
    treinamento: CentroTreinamentoOut = (await db_session.execute(select(CentroTreinamentoModel).filter_by(id=id))).scalars().first()
    if not treinamento:
        raise HTTPException(404, detail="Training center not found")
    return treinamento


async def paginate(db: AsyncSession,
                   offset: int | None = None,
                   limit: int | None = None) -> list[CentroTreinamentoOut]:
    async with db as session:
        async with session.begin():
            stmt = select(CentroTreinamentoModel).offset(offset).limit(limit)
            result = await session.execute(stmt)
            return [row for row in result.scalars()]
