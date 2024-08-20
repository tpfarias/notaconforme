from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.grupo_model import GrupoModel
from models.usuario_model import UsuarioModel
from core.deps import get_session, get_current_user
from schemas.grupo_schema import GrupoSchema

router = APIRouter()

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=GrupoSchema)
async def post_grupos(grupo: GrupoSchema, db: AsyncSession = Depends(get_session)):
    novo_grupo: GrupoModel = GrupoModel(
        nome=grupo.nome,
    )

    db.add(novo_grupo)
    await db.commit()

    return novo_grupo


@router.get('/', response_model=List[GrupoSchema])
async def get_grupos(db: AsyncSession = Depends(get_session), usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(GrupoModel)
        result = await session.execute(query)
        grupos: List[GrupoModel] = result.scalars().unique().all()

        return grupos


@router.get('/{grupo_id}', response_model=GrupoSchema, status_code=status.HTTP_200_OK)
async def get_grupo(grupo_id: int, db: AsyncSession = Depends(get_session), usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(GrupoModel).filter(GrupoModel.id == grupo_id)
        result = await session.execute(query)
        grupo: GrupoModel = result.scalars().unique().one_or_none()

        if grupo:
            return grupo
        else:
            raise HTTPException(detail='Grupo de usuários não encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)


@router.put('/{grupo_id}', response_model=GrupoSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_grupo(grupo_id: int, grupo: GrupoSchema, db: AsyncSession = Depends(get_session), usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(GrupoModel).filter(GrupoModel.id == grupo_id)
        result = await session.execute(query)
        grupo_update: GrupoModel = result.scalars().unique().one_or_none()

        if grupo_update:
            if grupo.nome:
                grupo_update.nome = grupo.nome

            await session.commit()
            return grupo_update
        else:
            raise HTTPException(detail='Grupo de usuários não encontrado.',
                                status_code=status.HTTP_404_NOT_FOUND)


@router.delete('/{grupo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_grupo(grupo_id: int, db: AsyncSession = Depends(get_session), usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(GrupoModel).filter(GrupoModel.id == grupo_id)
        result = await session.execute(query)
        grupo_delete: GrupoModel = result.scalars().unique().one_or_none()

        if grupo_delete:
            await session.delete(grupo_delete)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='Grupo de usuário não encontrado.',
                                status_code=status.HTTP_404_NOT_FOUND)
