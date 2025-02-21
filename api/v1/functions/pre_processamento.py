import nltk
from nltk.corpus import stopwords
import unicodedata
import re
import pandas as pd
from pathlib import Path

csv_dicionario_stopwords = Path(__file__).resolve().parent.parent / "datas" / "dicionario_stopwords.csv"
csv_dicionario_palavras_tratadas = Path(__file__).resolve().parent.parent / "datas" / "dicionario_palavras_tratadas.csv"



nltk.download('stopwords')
stop_words = stopwords.words('portuguese')

# Stopwords adicionais - Dicionário de palavras
df_stopwords_add = pd.read_csv(csv_dicionario_stopwords)
df_stopwords_add['palavra'] = df_stopwords_add['palavra'].str.lower()
stopwords_add = df_stopwords_add['palavra'].tolist()
stop_words.extend(stopwords_add)


# Função para remover stopwords de um texto
def remove_stopwords(texto):
    palavras = texto.split()
    palavras_filtradas = [palavra for palavra in palavras if palavra.lower() not in stop_words]
    return ' '.join(palavras_filtradas)

# Remove acentuação
def remove_acentuacao(text):
    text = ''.join(
        c for c in unicodedata.normalize('NFKD', text) if not unicodedata.combining(c)
    )
    return text

def limpa_texto(text):
    # Remover caracteres especiais e números, mantendo apenas letras e espaços
    text = re.sub(r'[^A-Za-z\s]', ' ', text)
    # Remove espaços excessivos
    text = " ".join(text.split())
    return text

# Remover letras isoladas
def remove_letras_isoladas(text):
    text = re.sub(r'\b[A-Za-z]\b', '', text)
    return text


# Separar palavras de acordo com dicionario

def separar_palavras(texto):
    palavras_corrigidas = []

    vocabulario_df = pd.read_csv(csv_dicionario_palavras_tratadas)
    vocabulario = set(vocabulario_df['palavra'].str.lower())

    for palavra in texto.split():
        palavra_corrigida = palavra.lower()

        for ref_palavra in vocabulario:
            if palavra_corrigida.startswith(ref_palavra):
                palavra_corrigida = ref_palavra + " " + palavra_corrigida[len(ref_palavra):]
                break
            elif palavra_corrigida.endswith(ref_palavra):
                palavra_corrigida = palavra_corrigida[:-len(ref_palavra)] + " " + ref_palavra
                break

        palavras_corrigidas.append(palavra_corrigida)

    return ' '.join(palavras_corrigidas)


def preprocessar_texto(texto):
    texto = texto.lower()
    texto = remove_acentuacao(texto)
    texto = limpa_texto(texto)
    texto = separar_palavras(texto)
    texto = remove_letras_isoladas(texto)
    texto = remove_stopwords(texto)

    return texto