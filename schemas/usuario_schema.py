from typing import Optional
from pydantic import BaseModel, EmailStr
#from schemas.grupo_schema import GrupoSchema


class UsuarioSchema(BaseModel):
    id: Optional[int] = None
    nome: str
    email: EmailStr
    ativo: bool = True
    grupo_id: Optional[int]
#    grupo_nome: Optional[GrupoSchema.nome]

    class Config:
        from_attributes = True

class UsuarioSchemaCreate(UsuarioSchema):
    senha: str

class UsuarioSchemaUpdate(UsuarioSchema):
    nome: Optional[str]
    email: Optional[EmailStr]
    senha: Optional[str]
    ativo: Optional[bool]
    grupo_id: Optional[int]

