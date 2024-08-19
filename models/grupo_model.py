from sqlalchemy import Integer, String, Column, Boolean
from sqlalchemy.orm import relationship

from core.config import settings


class GrupoModel(settings.DBBaseModel):
    __tablename__ = 'grupos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(300), nullable=True)

    usuarios = relationship(
        "UsuarioModel",
        back_populates="grupo",
        uselist=True,
        lazy="joined"
    )
