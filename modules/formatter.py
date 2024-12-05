# modules/formatter.py

from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from config.settings import OPENAI_API_KEY
from modules.utils import calcular_tokens


def formatear_contenido(contenido, datos_usuario):
    """
    Formatea el contenido para asegurar que sigue el estilo y formato deseado.
    """
    if not contenido:
        print("El contenido proporcionado está vacío.")
        return ""
    else:
        system_message_content = f"Eres un editor experto en {datos_usuario['industry']}."
        human_message_content = f"""
Por favor, formatea el siguiente contenido en {datos_usuario['language']} para que siga un estilo profesional y coherente. Asegúrate de que el texto fluya bien, que los encabezados y listas estén correctamente estructurados, y que se utilice una terminología consistente. **Si no hay cambios necesarios, devuelve el contenido original tal cual, sin agregar comentarios o explicaciones adicionales.**

Contenido a formatear:
{contenido}
"""
        system_message = SystemMessage(content=system_message_content)
        human_message = HumanMessage(content=human_message_content)
        messages = [system_message, human_message]

        # Calcular tokens y ajustar max_tokens
        prompt_tokens = calcular_tokens(system_message_content + human_message_content, modelo="gpt-4")
        max_total_tokens = 8192
        max_response_tokens = max_total_tokens - prompt_tokens - 500

        llm = ChatOpenAI(
            openai_api_key=OPENAI_API_KEY,
            model_name="gpt-4",
            temperature=0.1,
            max_tokens=max_response_tokens,
        )

        try:
            respuesta = llm.invoke(messages)
            contenido_formateado = respuesta.content.strip()
            return contenido_formateado
        except Exception as e:
            print(f"Error al formatear el contenido con LangChain: {e}")
            return contenido