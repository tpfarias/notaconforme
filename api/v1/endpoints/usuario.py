from typing import List, Optional, Any

from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from models.usuario_model import UsuarioModel
from schemas.usuario_schema import UsuarioSchema, UsuarioSchemaCreate, UsuarioSchemaUpdate
from core.deps import get_session, get_current_user
from core.security import gerar_hash_senha
from core.auth import autenticar, criar_token_acesso


router = APIRouter()


# GET Logado
@router.get('/logado', response_model=UsuarioSchema)
def get_logado(usuario_logado: UsuarioModel = Depends(get_current_user)):
    return usuario_logado


# POST / Signup
@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=UsuarioSchema)
async def post_usuario(usuario: UsuarioSchemaCreate, db: AsyncSession = Depends(get_session)):
    novo_usuario: UsuarioModel = UsuarioModel(
        nome=usuario.nome,
        email=usuario.email,
        senha=gerar_hash_senha(usuario.senha),
        ativo=usuario.ativo,
        grupo_id=usuario.grupo_id
    )

    async with db as session:
        try:
            session.add(novo_usuario)
            await session.commit()

            return novo_usuario
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail='Já existe um usuário com este email cadastrado.')


# GET Usuarios
@router.get('/', response_model=List[UsuarioSchema])
async def get_usuarios(db: AsyncSession = Depends(get_session), usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(UsuarioModel)
        result = await session.execute(query)
        usuarios: List[UsuarioSchema] = result.scalars().unique().all()

        return usuarios


# GET Usuario
@router.get('/{usuario_id}', response_model=UsuarioSchema, status_code=status.HTTP_200_OK)
async def get_usuario(usuario_id: int, db: AsyncSession = Depends(get_session), usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario: UsuarioSchema = result.scalars().unique().one_or_none()

        if usuario:
            return usuario
        else:
            raise HTTPException(detail='Usuário não encontrado.',
                                status_code=status.HTTP_404_NOT_FOUND)


# PUT Usuario
@router.put('/{usuario_id}', response_model=UsuarioSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_usuario(usuario_id: int, usuario: UsuarioSchemaUpdate, db: AsyncSession = Depends(get_session), usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario_update: UsuarioSchema = result.scalars().unique().one_or_none()

        if usuario_update:
            if usuario.nome:
                usuario_update.nome = usuario.nome
            if usuario.email:
                usuario_update.email = usuario.email
            if usuario.ativo:
                usuario_update.ativo = usuario.ativo
            if usuario.senha:
                usuario_update.senha = gerar_hash_senha(usuario.senha)
            await session.commit()
            return usuario_update

        else:
            raise HTTPException(detail='Usuário não encontrado.',
                                status_code=status.HTTP_404_NOT_FOUND)


# DELETE usuario
@router.delete('/{usuario_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_usuario(usuario_id: int, db: AsyncSession = Depends(get_session), usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario_delete: UsuarioSchema = result.scalars().unique().one_or_none()

        if usuario_delete:
            await session.delete(usuario_delete)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='Usuário não encontrado.',
                                status_code=status.HTTP_404_NOT_FOUND)


# POST Login
@router.post('/login')
async def login(
            form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    usuario = await autenticar(email=form_data.username, senha=form_data.password, db=db)

    if not usuario:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Dados de acesso incorretos.')

    return JSONResponse(content={"access_token": criar_token_acesso(sub=usuario.id), "token_type": "bearer"}, status_code=status.HTTP_200_OK)
