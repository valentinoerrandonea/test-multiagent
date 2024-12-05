# modules/content_composer.py

from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from config.settings import OPENAI_API_KEY
from modules.utils import calcular_tokens, resumir_texto

def componer_contenido(descripcion, datos_usuario):
    """
    Utiliza LangChain para componer el contenido basado en la descripción, los datos del usuario y el contenido previo almacenado en Elasticsearch.
    """
    # Crear el mensaje del sistema
    system_message_content = f"Eres un experto en {datos_usuario['industry']}."
    system_message = SystemMessage(content=system_message_content)

    # Si hay contenido previo, incluirlo en el prompt
    if contenido_previos:
        # Si el contenido previo es muy largo, resumirlo
        max_length_contenido_previos = 1500  # Ajusta según sea necesario
        if calcular_tokens(contenido_previos) > max_length_contenido_previos:
            print("Resumiendo contenido previo para ajustarlo al prompt.")
            contenido_previos = resumir_texto(contenido_previos, datos_usuario)

        contenido_previos = f"\n\nContenido previo relevante:\n{contenido_previos}"
    else:
        contenido_previos = ""

    # Crear el mensaje del usuario
    human_message_content = f"""
Utilizando la siguiente información, escribe un contenido en {datos_usuario['language']} que aborde la descripción proporcionada. El contenido debe ser **muy detallado**, **explicativo** y **justificar todos los puntos mencionados**. Asegúrate de proporcionar **ejemplos**, **datos relevantes** y **análisis profundos** que ayuden a comprender completamente el tema.

Antes de escribir, revisa el contenido previo para evitar redundancias y asegurar coherencia en el documento.{contenido_previos}

Descripción:
{descripcion}

Datos del usuario:
- Nombre de la empresa: {datos_usuario['company_name']}
- País de la empresa: {datos_usuario['company_country']}
- País objetivo: {datos_usuario['target_country']}
- Industria: {datos_usuario['industry']}
- Objetivo: {datos_usuario['objective']}
"""
    human_message = HumanMessage(content=human_message_content)
    messages = [system_message, human_message]

    # Calcular el número de tokens en el prompt
    prompt_tokens = calcular_tokens(system_message_content + human_message_content, modelo="gpt-4")
    max_total_tokens = 8192  # Límite total de tokens para GPT-4
    max_response_tokens = max_total_tokens - prompt_tokens - 500  # Deja un margen de 500 tokens

    # Verificar si el prompt es demasiado grande
    if max_response_tokens <= 0:
        print("El prompt es demasiado grande para el modelo. Reduciendo contenido previo.")
        # Puedes implementar lógica para reducir o resumir el contenido previo
        contenido_previos = ""
        # Recalcular human_message_content y prompt_tokens después de reducir
        human_message_content = f"""
Utilizando la siguiente información, escribe un contenido en {datos_usuario['language']} que aborde la descripción proporcionada. El contenido debe ser **muy detallado**, **explicativo** y **justificar todos los puntos mencionados**. Asegúrate de proporcionar **ejemplos**, **datos relevantes** y **análisis profundos** que ayuden a comprender completamente el tema.

Descripción:
{descripcion}

Datos del usuario:
- Nombre de la empresa: {datos_usuario['company_name']}
- País de la empresa: {datos_usuario['company_country']}
- País objetivo: {datos_usuario['target_country']}
- Industria: {datos_usuario['industry']}
- Objetivo: {datos_usuario['objective']}
"""
        human_message = HumanMessage(content=human_message_content)
        messages = [system_message, human_message]
        prompt_tokens = calcular_tokens(system_message_content + human_message_content, modelo="gpt-4")
        max_response_tokens = max_total_tokens - prompt_tokens - 500

    # Configurar el modelo de lenguaje con max_tokens ajustado
    llm = ChatOpenAI(
        openai_api_key=OPENAI_API_KEY,
        model_name="gpt-4",
        temperature=0.1,
        max_tokens=max_response_tokens,  # Ajustar max_tokens según el espacio disponible
    )

    try:
        # Generar el contenido usando LangChain y ChatOpenAI
        respuesta = llm(messages)
        contenido = respuesta.content.strip()
        return contenido
    except Exception as e:
        print(f"Error al generar contenido con LangChain: {e}")
        return ""