"""
Funciones auxiliares para PiLearn
"""


def validar_respuesta_texto(texto):
    """
    Validar que el texto de respuesta sea válido
    
    Args:
        texto: texto a validar
    
    Returns:
        tuple: (es_valido: bool, mensaje_error: str)
    """
    if not texto or not texto.strip():
        return False, "Por favor, escribe una respuesta"
    
    texto = texto.strip()
    
    caracteres_prohibidos = ['<', '>', ';', '&', '|', '`', '$']
    for char in caracteres_prohibidos:
        if char in texto:
            return False, "Caracteres no permitidos en la respuesta"
    
    if len(texto) > 100:
        return False, "La respuesta es demasiado larga (máximo 100 caracteres)"
    
    return True, ""


def formatear_tiempo(segundos):
    """
    Formatear tiempo en formato legible
    
    Args:
        segundos: cantidad de segundos
    
    Returns:
        str: tiempo formateado (ej: "2:30")
    """
    minutos = int(segundos // 60)
    segs = int(segundos % 60)
    return f"{minutos}:{segs:02d}"


def calcular_precision(correctas, total):
    """
    Calcular precisión porcentual
    
    Args:
        correctas: cantidad de respuestas correctas
        total: total de respuestas
    
    Returns:
        float: precisión en porcentaje
    """
    if total == 0:
        return 0.0
    return (correctas / total) * 100


def obtener_mensaje_motivacional(precision):
    """
    Obtener mensaje motivacional según precisión
    
    Args:
        precision: porcentaje de precisión
    
    Returns:
        str: mensaje motivacional
    """
    if precision >= 90:
        return "🌟 ¡EXCELENTE! ¡Eres un maestro!"
    elif precision >= 70:
        return "🎉 ¡MUY BIEN! Vas por buen camino"
    elif precision >= 50:
        return "👍 ¡BIEN HECHO! Sigue practicando"
    else:
        return "💪 ¡SIGUE INTENTANDO! La práctica hace al maestro"
