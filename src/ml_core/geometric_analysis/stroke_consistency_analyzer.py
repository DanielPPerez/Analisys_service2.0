# src/ml_core/geometric_analysis/stroke_consistency_analyzer.py

import cv2
import numpy as np
from typing import Dict, Any

def _skeletonize(image_bin: np.ndarray) -> np.ndarray:
    """Realiza la esqueletización de una imagen binarizada."""
    skeleton = np.zeros(image_bin.shape, np.uint8)
    element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    while True:
        eroded = cv2.erode(image_bin, element)
        temp = cv2.dilate(eroded, element)
        temp = cv2.subtract(image_bin, temp)
        skeleton = cv2.bitwise_or(skeleton, temp)
        image_bin = eroded.copy()
        if cv2.countNonZero(image_bin) == 0:
            break
    return skeleton

def analyze_stroke_consistency(user_image_bin: np.ndarray) -> Dict[str, Any]:
    """
    Analiza y diagnostica la consistencia del grosor del trazo de una letra.

    Args:
        user_image_bin: Imagen binarizada del usuario (letra blanca, fondo negro).

    Returns:
        Un diccionario con métricas de diagnóstico detalladas.
    """
    if cv2.countNonZero(user_image_bin) == 0:
        return {"score": 0.0, "thickness_variance": -1.0, "deviation_code": "no_content"}

    dist_transform = cv2.distanceTransform(user_image_bin, cv2.DIST_L2, 5)
    skeleton = _skeletonize(user_image_bin)
    thickness_values = dist_transform[skeleton > 0]

    if len(thickness_values) < 5:
        return {"score": 50.0, "thickness_variance": -1.0, "deviation_code": "not_enough_data"}

    mean_thickness = np.mean(thickness_values)
    std_thickness = np.std(thickness_values)

    if mean_thickness == 0:
        return {"score": 0.0, "thickness_variance": -1.0, "deviation_code": "no_thickness"}

    # Coeficiente de variación: una medida de variabilidad relativa
    coeff_of_variation = std_thickness / mean_thickness
    
    deviation_code = "optima"
    if coeff_of_variation > 0.3: # Si la desviación es más del 30% de la media
        deviation_code = "trazo_inconsistente"

    # Convertir la variación en una puntuación
    # Un coeficiente de 0.5 (50%) o más se considera una puntuación de 0.
    score = max(0.0, 1.0 - coeff_of_variation / 0.5)

    return {
        "score": round(score * 100), # Puntuación en escala 0-100
        "thickness_variation_coeff": round(coeff_of_variation, 3),
        "deviation_code": deviation_code
    }