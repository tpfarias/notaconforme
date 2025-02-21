from pydantic import BaseModel
from typing import Dict, Any

class PredicaoSchema(BaseModel):
    discriminacao: str
#    id:int
    #campos_dinamicos: Dict[str, Any] = {}

    class Config:
       extra = "allow"


