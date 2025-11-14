# src/ml_core/geometric_analysis/inclination_analyzer.py

import cv2
import numpy as np
from typing import Dict, Any
from ..utils.image_preprocessor import find_main_contour

def analyze_inclination(user_image_bin: np.ndarray) -> Dict[str, Any]:
    """
    Analiza y diagnostica la inclinación de una letra.
    El ángulo ideal se asume como vertical.

    Args:
        user_image_bin: Imagen binarizada del usuario (letra blanca, fondo negro).

    Returns:
        Un diccionario con métricas de diagnóstico detalladas.
    """
    user_contour = find_main_contour(user_image_bin)

    default_response = {
        "score": 0.0,
        "user_angle": 0.0,
        "deviation_code": "no_contour_found"
    }

    if user_contour is None:
        return default_response
    
    # El contorno debe tener al menos 5 puntos para que minAreaRect funcione
    if len(user_contour) < 5:
        default_response["deviation_code"] = "contour_too_small"
        return default_response

    # Obtener el rectángulo de área mínima para determinar el ángulo
    (x, y), (width, height), angle = cv2.minAreaRect(user_contour)

    # Normalizar el ángulo para una interpretación consistente.
    # 0 grados será vertical. Valores positivos se inclinan a la derecha, negativos a la izquierda.
    if width < height:
        deviation_angle = angle
    else:
        deviation_angle = angle - 90

    # Calcular el código de desviación
    deviation_code = "optima"
    if deviation_angle > 15: # Inclinación notable a la derecha
        deviation_code = "inclinacion_excesiva_derecha"
    elif deviation_angle < -15: # Inclinación notable a la izquierda
        deviation_code = "inclinacion_excesiva_izquierda"

    # Convertir la desviación en una puntuación
    # Una desviación de 45 grados o más se considera una puntuación de 0.
    score = max(0.0, 1.0 - abs(deviation_angle) / 45.0)

    return {
        "score": round(score * 100), # Puntuación en escala 0-100
        "user_angle": round(deviation_angle, 2), # Ángulo de desviación en grados
        "deviation_code": deviation_code
    }