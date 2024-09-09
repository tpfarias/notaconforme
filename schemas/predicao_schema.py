from pydantic import BaseModel

class PredicaoSchema(BaseModel):
    id: int
    discriminacao: str

#    class Config:
#        orm_mode = True


class PredicaoSchemaResponse(BaseModel):
    id: int
    cnae: str