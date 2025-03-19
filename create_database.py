from core.config import settings
from core.database import engine, SessionLocal
from models.usuario_model import UsuarioModel  # Importe o modelo de usuário
from core.security import gerar_hash_senha
from passlib.context import CryptContext


async def create_tables() -> None:
    import models.__all_models
    print('Criando as tabelas no banco de dados')

    async with engine.begin() as conn:
        await conn.run_sync(settings.DBBaseModel.metadata.drop_all)
        await conn.run_sync(settings.DBBaseModel.metadata.create_all)
    print('Tabelas criadas com sucesso...')

    # Criar usuário padrão
    await create_default_user()


async def create_default_user():
    db = SessionLocal()
    try:
        # Verificar se o usuário já existe
        if not db.query(UsuarioModel).filter_by(email="admin@email.com").first():
            hashed_password = gerar_hash_senha("admin123")  # Senha segura
            user = UsuarioModel(nome="Admin", email="admin@email.com", senha=hashed_password, ativo=True)
            db.add(user)
            db.commit()
            print("Usuário padrão criado com sucesso.")
        else:
            print("Usuário padrão já existe.")
    except Exception as e:
        print(f"Erro ao criar usuário padrão: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == '__main__':
    import asyncio

    asyncio.run(create_tables())
