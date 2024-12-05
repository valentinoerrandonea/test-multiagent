# modules/content_saver.py

import os

def inicializar_archivo_salida(nombre_archivo="reporte_completo.md"):
    """
    Inicializa el archivo de salida. Si el archivo existe, lo elimina para empezar de nuevo.
    """
    if os.path.exists(nombre_archivo):
        os.remove(nombre_archivo)
    print(f"Archivo de salida inicializado: {nombre_archivo}")

def guardar_contenido(titulo_seccion, contenido, nombre_archivo="reporte_completo.md", nivel_encabezado=1):
    """
    Guarda el contenido generado en un archivo Markdown único, agregando el contenido de cada sección.
    """
    encabezado = '#' * nivel_encabezado  # Genera '#' según el nivel de encabezado
    try:
        with open(nombre_archivo, 'a', encoding='utf-8') as f:
            f.write(f"{encabezado} {titulo_seccion}\n\n")
            f.write(f"{contenido}\n\n")
        print(f"Contenido de la sección '{titulo_seccion}' guardado en {nombre_archivo}")
    except Exception as e:
        print(f"Error al guardar el contenido: {e}")