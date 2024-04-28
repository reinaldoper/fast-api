from datetime import datetime
from uuid import uuid4
from fastapi import APIRouter, HTTPException, status, Body
from pydantic import UUID4
from sqlalchemy import select
from workout_api.atleta.models import AtletaModel
from workout_api.atleta.schemas import Atleta, AtletaOut
from workout_api.categorias.models import CategoriaModel
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from workout_api.contrib.dependencies import DatabaseDepencies
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()


@router.post('/', summary="Adiciona novo atleta.", response_model=AtletaOut,
             status_code=status.HTTP_201_CREATED)
async def post(db_session: DatabaseDepencies, atleta_in: Atleta = Body(...)):
    categoria = (await db_session.execute(select(CategoriaModel).filter_by(nome=atleta_in.categoria.nome))).scalars().first()

    if not categoria:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Categoria not found")
    
    centro_treinamento = (await db_session.
                          execute(select(CentroTreinamentoModel).filter_by(nome=atleta_in.centro_treinamento.nome))).scalars().first()

    if not centro_treinamento:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Treinamento not found")
    
    try:
        atleta_out = AtletaOut(id=uuid4(), created_at=datetime.utcnow(), **atleta_in.model_dump())
        atleta_model = AtletaModel(**atleta_out.model_dump(exclude={'categoria', 'centro_treinamento'}))
        atleta_model.categoria_id = categoria.pk_id
        atleta_model.centro_treinamento_id = centro_treinamento.pk_id
        db_session.add(atleta_model)
        await db_session.commit()
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_303_SEE_OTHER, detail=f"Já existe um atleta cadastrado com o cpf: {atleta_in.cpf}")
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error occurred")
   
    return atleta_out


@router.get('/', summary='Retornar todos os atletas',
            status_code=status.HTTP_200_OK,
            response_model=list[AtletaOut])
async def query(db_session: DatabaseDepencies,
                offset: int = 0, limit: int = 10) -> list[AtletaOut]:

    async with db_session as session:
        return await paginate(session, offset, limit)


@router.get('/{id}', summary='Retornar uma categoria pelo id',
            status_code=status.HTTP_200_OK, response_model=AtletaOut)
async def query_id(id: UUID4, db_session: DatabaseDepencies) -> AtletaOut:
    categoria: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalars().first()
    if not categoria:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Atleta not found")
    return categoria


@router.get('/query', summary='Retornar uma categoria pelo nome ou cpf', 
            status_code=status.HTTP_200_OK, response_model=AtletaOut)
async def query_atleta(nome: str | None, cpf: str | None,
                       db_session: DatabaseDepencies) -> AtletaOut:
    if not nome and not cpf:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Forneça nome ou cpf")
    
    query = await select(AtletaModel)
    if nome:
        query = await query.filter(AtletaModel.nome == nome)
    if cpf:
        query = await query.filter(AtletaModel.cpf == cpf)

    categoria: AtletaOut = (await db_session.execute(query)).scalars().first()
    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Atleta not found")
    
    return categoria


async def paginate(db: AsyncSession,
                   offset: int | None = None,
                   limit: int | None = None) -> list[AtletaOut]:
    async with db as session:
        async with session.begin():
            stmt = select(AtletaModel).offset(offset).limit(limit)
            result = await session.execute(stmt)
            return [row for row in result.scalars()]
