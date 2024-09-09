import joblib

from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response
from models.usuario_model import UsuarioModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.deps import get_session, get_current_user
from schemas.predicao_schema import PredicaoSchema, PredicaoSchemaResponse

vectorizer_path = "MLModels/vectorizer_PNL.pkl"
vectorizer = joblib.load(vectorizer_path)

modelo_path = "MLModels/model_ML.joblib"
modelo_treinado = joblib.load(modelo_path)

router = APIRouter()

@router.post('/', status_code=status.HTTP_200_OK, response_model=List[PredicaoSchemaResponse])
async def post_predicoes(request: List[PredicaoSchema], usuario_logado: UsuarioModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):

    response = []

    for item in request:
        try:
            discriminacao_vetorizada = vectorizer.transform([item.discriminacao.lower()])
            cnae = modelo_treinado.predict(discriminacao_vetorizada)
            response.append(PredicaoSchemaResponse(id=item.id, cnae=str(cnae)))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao processar a requisição: {str(e)}")

    return response






