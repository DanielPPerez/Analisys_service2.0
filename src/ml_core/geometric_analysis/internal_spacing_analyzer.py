# src/ml_core/geometric_analysis/internal_spacing_analyzer.py

import cv2
import numpy as np
from typing import Dict, Any, Tuple

def _get_hole_properties(image_bin: np.ndarray) -> Tuple[int, float]:
    """Encuentra los "agujeros" (contornos internos) y calcula su área total."""
    contours, hierarchy = cv2.findContours(image_bin, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    hole_count, total_hole_area = 0, 0.0
    if hierarchy is None: return 0, 0.0
    for i, _ in enumerate(contours):
        if hierarchy[0][i][3] != -1: # Si tiene un padre, es un agujero
            hole_count += 1
            total_hole_area += cv2.contourArea(contours[i])
    return hole_count, total_hole_area

def analyze_internal_spacing(user_image_bin: np.ndarray, template_image_bin: np.ndarray) -> Dict[str, Any]:
    """
    Analiza y diagnostica el espaciado interno ("agujeros") de una letra.

    Args:
        user_image_bin: Imagen binarizada del usuario (letra blanca, fondo negro).
        template_image_bin: Imagen binarizada de la plantilla de referencia.

    Returns:
        Un diccionario con métricas de diagnóstico detalladas.
    """
    user_holes, user_hole_area = _get_hole_properties(user_image_bin)
    template_holes, template_hole_area = _get_hole_properties(template_image_bin)

    # Si la plantilla no tiene agujeros, no hay nada que analizar
    if template_holes == 0:
        score = 100.0 if user_holes == 0 else 0.0
        return {"score": score, "deviation_code": "no_holes_expected" if user_holes > 0 else "optima"}

    # Penalización si el número de agujeros no coincide
    if user_holes != template_holes:
        return {"score": 0.0, "user_holes": user_holes, "template_holes": template_holes, "deviation_code": "wrong_hole_count"}

    # Calcular área total de la letra (píxeles blancos) para normalizar
    user_total_area = cv2.countNonZero(user_image_bin)
    template_total_area = cv2.countNonZero(template_image_bin)
    if user_total_area == 0 or template_total_area == 0:
        return {"score": 0.0, "deviation_code": "no_content"}

    # Calcular la proporción del área de los agujeros respecto al área de la letra
    user_hole_ratio = user_hole_area / user_total_area
    template_hole_ratio = template_hole_area / template_total_area

    # Calcular error y código de desviación
    error = (user_hole_ratio - template_hole_ratio) / template_hole_ratio
    deviation_code = "optima"
    if error > 0.4: # Agujeros un 40% más grandes de lo esperado
        deviation_code = "circulo_demasiado_abierto"
    elif error < -0.4: # Agujeros un 40% más pequeños de lo esperado
        deviation_code = "circulo_casi_cerrado"
        
    score = max(0.0, 1.0 - abs(error))

    return {
        "score": round(score * 100),
        "user_internal_area_ratio": round(user_hole_ratio, 3),
        "template_internal_area_ratio": round(template_hole_ratio, 3),
        "deviation_code": deviation_code
    }