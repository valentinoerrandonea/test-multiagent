# modules/processor.py

from modules.content_composer import componer_contenido
from modules.validator import validar_contenido
from modules.formatter import formatear_contenido
from modules.content_saver import guardar_contenido, inicializar_archivo_salida

def procesar_guia(guia, datos_usuario):
    # Inicializar el archivo de salida
    nombre_archivo_salida = "reporte_completo.md"
    inicializar_archivo_salida(nombre_archivo=nombre_archivo_salida)

    for titulo_guia, secciones in guia.items():
        print(f"Procesando guía: {titulo_guia}")

        # Reemplazar {company} y {market} en el título de la guía
        titulo_guia = titulo_guia.replace("{company}", datos_usuario['company_name'])
        titulo_guia = titulo_guia.replace("{market}", datos_usuario['target_country'])

        for titulo_seccion, contenido_seccion in secciones.items():
            print(f"\nProcesando sección: {titulo_seccion}")

            # Verificar si la sección tiene subsecciones
            if 'description' in contenido_seccion:
                # La sección tiene una descripción y se puede procesar
                procesar_seccion(titulo_seccion, contenido_seccion, datos_usuario, nombre_archivo_salida, nivel_encabezado=1)
            else:
                # La sección no tiene descripción, pero puede tener subsecciones
                for subtitulo_seccion, subcontenido_seccion in contenido_seccion.items():
                    print(f"\nProcesando subsección: {subtitulo_seccion}")

                    # Reemplazar marcadores en el subtítulo y descripción
                    subtitulo_seccion_formateado = subtitulo_seccion.replace("{company}", datos_usuario['company_name'])
                    subtitulo_seccion_formateado = subtitulo_seccion_formateado.replace("{market}", datos_usuario['target_country'])

                    descripcion = subcontenido_seccion.get('description', '')
                    if not descripcion:
                        print(f"La subsección '{subtitulo_seccion}' no tiene una descripción. Se omitirá.")
                        continue

                    descripcion = descripcion.replace("{company}", datos_usuario['company_name'])
                    descripcion = descripcion.replace("{market}", datos_usuario['target_country'])
                    descripcion = descripcion.replace("{objective}", datos_usuario['objective'])

                    # Procesar la subsección
                    procesar_seccion(subtitulo_seccion_formateado, {'description': descripcion}, datos_usuario, nombre_archivo_salida, nivel_encabezado=2)
    print("\nProcesamiento de la guía completado.")

def procesar_seccion(titulo_seccion, contenido_seccion, datos_usuario, nombre_archivo_salida, nivel_encabezado=1):
    descripcion = contenido_seccion.get('description', '')
    if not descripcion:
        print(f"La sección '{titulo_seccion}' no tiene una descripción. Se omitirá.")
        return

    # Reemplazar marcadores en la descripción
    descripcion = descripcion.replace("{company}", datos_usuario['company_name'])
    descripcion = descripcion.replace("{market}", datos_usuario['target_country'])
    descripcion = descripcion.replace("{objective}", datos_usuario['objective'])

    # Componer contenido sin resultados de búsqueda
    contenido = componer_contenido(descripcion, datos_usuario)

    if not contenido:
        print(f"No se pudo generar contenido para la sección '{titulo_seccion}'.")
        return

    # Validar contenido
    contenido_validado = validar_contenido(contenido, datos_usuario)

    # Formatear contenido
    contenido_formateado = formatear_contenido(contenido_validado, datos_usuario)

    # Validación final
    contenido_final = validar_contenido(contenido_formateado, datos_usuario)

    # Guardar contenido en el archivo único
    guardar_contenido(titulo_seccion, contenido_final, nombre_archivo=nombre_archivo_salida, nivel_encabezado=nivel_encabezado)