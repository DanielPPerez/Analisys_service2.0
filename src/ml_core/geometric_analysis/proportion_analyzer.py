# src/ml_core/geometric_analysis/proportion_analyzer.py

import cv2
import numpy as np
from typing import Dict, Any
from ..utils.image_preprocessor import find_main_contour

def analyze_proportion(user_image_bin: np.ndarray, template_image_bin: np.ndarray) -> Dict[str, Any]:
    """
    Analiza y diagnostica la proporción (relación de aspecto) de una letra
    en comparación con una plantilla.

    Args:
        user_image_bin: Imagen binarizada del usuario (letra blanca, fondo negro).
        template_image_bin: Imagen binarizada de la plantilla de referencia.

    Returns:
        Un diccionario con métricas de diagnóstico detalladas.
    """
    user_contour = find_main_contour(user_image_bin)
    template_contour = find_main_contour(template_image_bin)

    # Valores por defecto en caso de fallo
    default_response = {
        "score": 0.0,
        "user_aspect_ratio": 0.0,
        "template_aspect_ratio": 0.0,
        "deviation_code": "no_contour_found"
    }

    if user_contour is None or template_contour is None:
        return default_response

    # Calcular relación de aspecto para el usuario
    _, _, uw, uh = cv2.boundingRect(user_contour)
    user_aspect_ratio = uw / uh if uh > 0 else 0.0

    # Calcular relación de aspecto para la plantilla
    _, _, tw, th = cv2.boundingRect(template_contour)
    template_aspect_ratio = tw / th if th > 0 else 0.0

    if template_aspect_ratio == 0:
        return default_response # No se puede comparar con una plantilla sin dimensiones

    # Calcular el error porcentual y el código de desviación
    error = (user_aspect_ratio - template_aspect_ratio) / template_aspect_ratio
    
    deviation_code = "optima"
    if error > 0.25:  # Más de un 25% más ancha que la plantilla
        deviation_code = "demasiado_ancha"
    elif error < -0.25: # Más de un 25% más estrecha que la plantilla
        deviation_code = "demasiado_estrecha"

    # Convertir el error absoluto en una puntuación (0.0 a 1.0)
    # Un error del 100% (el doble o la mitad de ancha) se considera una puntuación de 0.
    score = max(0.0, 1.0 - abs(error))
    
    return {
        "score": round(score * 100), # Puntuación en escala 0-100
        "user_aspect_ratio": round(user_aspect_ratio, 3),
        "template_aspect_ratio": round(template_aspect_ratio, 3),
        "deviation_code": deviation_code
    }