import joblib
from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response
from models.usuario_model import UsuarioModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from core.deps import get_session, get_current_user
from schemas.predicao_schema import PredicaoSchema
from api.v1.functions.pre_processamento import preprocessar_texto

#Modelo de Produção
#modelo_path = "MLModels/modelo_preditivo.joblib"
#vectorizer_path = "MLModels/vectorizer.pkl"

#Modelo Simulado - GitHUB
vectorizer_path = "MLModels/vectorizer_simulado.pkl"
modelo_path = "MLModels/modelo_preditivo_simulado.joblib"

vectorizer = joblib.load(vectorizer_path)
modelo_treinado = joblib.load(modelo_path)


router = APIRouter()

@router.post('/', status_code=status.HTTP_200_OK)
async def post_predicoes(request: List[PredicaoSchema], usuario_logado: UsuarioModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):

    response = []

    classes = [
        '0401', '0402', '0403', '0404', '0405', '0406', '0407', '0408',
        '0409', '0410', '0411', '0412', '0413', '0414', '0415', '0416',
        '0417', '0418', '0419', '0420', '0421', '1'
    ]

    discriminacoes_processadas = [preprocessar_texto(item.discriminacao) for item in request]
    discriminacoes_vetorizadas = vectorizer.transform(discriminacoes_processadas)
    cod_servicos = modelo_treinado.predict(discriminacoes_vetorizadas)

    for idx, item in enumerate(request):
        try:
            codigos_selecionados = [classes[i] for i in range(len(classes)) if cod_servicos[idx, i] == 1]
            response_data = {
                "servicos": codigos_selecionados
            }

            response_data.update(item.model_dump(exclude={"discriminacao"}))
            response.append(response_data)

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao processar a requisição: {str(e)}")

    return response



