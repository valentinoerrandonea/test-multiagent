# main.py

from modules.user_input import obtener_datos_usuario
from modules.guia_loader import cargar_guia
from modules.processor import procesar_guia

def main():
    try:
        # Obtener datos del usuario
        datos_usuario = obtener_datos_usuario()
        
        # Cargar la guía
        guia = cargar_guia()
        
        # Procesar la guía
        procesar_guia(guia, datos_usuario)
    except Exception as e:
        print(f"Ha ocurrido un error: {e}")

if __name__ == '__main__':
    main()