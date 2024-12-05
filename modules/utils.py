# modules/utils.py

import tiktoken
from langchain_openai.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from config.settings import OPENAI_API_KEY
def calcular_tokens(texto, modelo="gpt-4"):
    """
    Calcula el número de tokens en un texto dado para el modelo especificado.
    """
    encoding = tiktoken.encoding_for_model(modelo)
    num_tokens = len(encoding.encode(texto))
    return num_tokens

def resumir_texto(texto, datos_usuario):
    """
    Resume el texto proporcionado utilizando el modelo GPT-4.
    """
    llm = ChatOpenAI(
        openai_api_key=OPENAI_API_KEY,
        model_name="gpt-4",
        temperature=0.1,
        max_tokens=500,
    )
    prompt = f"Por favor, resume el siguiente texto en {datos_usuario['language']} en no más de 1500 caracteres:\n\n{texto}"
    try:
        respuesta = llm.invoke([HumanMessage(content=prompt)])
        resumen = respuesta.content.strip()
        return resumen
    except Exception as e:
        print(f"Error al resumir el texto: {e}")
        return texto  # En caso de error, devuelve el texto original