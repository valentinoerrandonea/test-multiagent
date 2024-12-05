# modules/user_input.py

def obtener_datos_usuario():
    """
    Solicita al usuario los datos necesarios para generar el reporte.

    Returns:
        dict: Un diccionario con los datos proporcionados por el usuario.
    """
    print("Por favor, ingrese los siguientes datos para generar el reporte:\n")

    datos_usuario = {
        'company_name': input("Ingrese el nombre de la empresa: ").strip(),
        'company_country': input("Ingrese el país de la empresa: ").strip(),
        'target_country': input("Ingrese el país objetivo: ").strip(),
        'industry': input("Ingrese la industria: ").strip(),
        'objective': input("Ingrese el objetivo: ").strip(),
        'language': input("Ingrese el idioma para el reporte: ").strip().lower()
    }

    # Validar que ningún campo esté vacío
    for key, value in datos_usuario.items():
        if not value:
            print(f"El campo '{key}' no puede estar vacío.")
            exit(1)

    return datos_usuario