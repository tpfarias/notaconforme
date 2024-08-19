from typing import Optional, List
from pydantic import BaseModel
from schemas.usuario_schema import UsuarioSchema

class GrupoSchema(BaseModel):
    id: Optional[int] = None
    nome: str

    class Config:
        from_attributes = True

class GrupoSchemaUsuarios(GrupoSchema):
    usuarios: Optional[List[UsuarioSchema]]

