# modules/guia_loader.py

import json
import os

def cargar_guia():
    """
    Carga el archivo 'guia.json' desde el directorio 'data'.

    Returns:
        dict: El contenido de la guía en formato de diccionario.
    """
    ruta_guia = os.path.join('data', 'guia.json')
    try:
        with open(ruta_guia, 'r', encoding='utf-8') as archivo:
            guia = json.load(archivo)
        return guia
    except FileNotFoundError:
        print(f"Error: El archivo '{ruta_guia}' no se encontró.")
        exit(1)
    except json.JSONDecodeError as e:
        print(f"Error al decodificar el archivo '{ruta_guia}': {e}")
        exit(1)