from pydantic import BaseModel
from typing import Dict, Any

class PredicaoSchema(BaseModel):
    discriminacao: str
    #campos_dinamicos: Dict[str, Any] = {}

    class Config:
       extra = "allow"


