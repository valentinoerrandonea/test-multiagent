# modules/validator.py

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from config.settings import OPENAI_API_KEY
from modules.utils import calcular_tokens

def validar_contenido(contenido, datos_usuario):
    """
    Valida y corrige el contenido generado para asegurar que es coherente y correcto.
    """
    if not contenido:
        print("El contenido generado está vacío.")
        return ""
    else:
        # Crear el prompt
        prompt_template = ChatPromptTemplate.from_messages([
            HumanMessagePromptTemplate.from_template("""
Por favor, revisa y corrige el siguiente contenido en {language} para asegurar que es coherente, está bien estructurado y que los datos son consistentes a lo largo del documento. Si encuentras errores o inconsistencias, corrígelos. **Si no hay errores, simplemente devuelve el contenido original tal cual, sin agregar comentarios o explicaciones adicionales.**

Contenido a revisar:
{contenido}
""")
        ])

        prompt = prompt_template.format_prompt(
            contenido=contenido,
            language=datos_usuario['language']
        )

        # Calcular tokens y ajustar max_tokens
        prompt_tokens = calcular_tokens(prompt.to_string(), modelo="gpt-4")
        max_total_tokens = 8192
        max_response_tokens = max_total_tokens - prompt_tokens - 500

        llm = ChatOpenAI(
            openai_api_key=OPENAI_API_KEY,
            model_name="gpt-4",
            temperature=0.1,
            max_tokens=max_response_tokens,
        )

        try:
            respuesta = llm.invoke(prompt.to_messages())
            contenido_validado = respuesta.content.strip()
            return contenido_validado
        except Exception as e:
            print(f"Error al validar el contenido con LangChain: {e}")
            return contenido