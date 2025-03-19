from core.config import settings
from core.database import engine, Session
from models.usuario_model import UsuarioModel
from core.security import gerar_hash_senha
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

async def create_default_user(session: AsyncSession):
    # Verificar se o usuário já existe
    async with session.begin():
        result = await session.execute(select(UsuarioModel).filter_by(email="admin@admin.com"))
        user = result.scalar_one_or_none()

        # Se o usuário não existir, criar um novo
        if user is None:
            hashed_password = gerar_hash_senha("admin1234")  # Senha padrão
            new_user = UsuarioModel(nome="Admin", email="admin@admin.com", senha=hashed_password)
            session.add(new_user)
            await session.commit()
            print("Usuário padrão 'admin' criado com sucesso.")


async def create_tables() -> None:
    import models.__all_models
    print('Criando as tabelas no banco de dados')

    async with engine.begin() as conn:
        await conn.run_sync(settings.DBBaseModel.metadata.drop_all)
        await conn.run_sync(settings.DBBaseModel.metadata.create_all)
    print('Tabelas criadas com sucesso...')


    async with AsyncSession(engine) as session:
        await create_default_user(session)


if __name__ == '__main__':
    import asyncio

    asyncio.run(create_tables())
