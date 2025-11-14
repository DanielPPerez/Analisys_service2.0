import cv2
import numpy as np
from typing import Optional

def preprocess_image(image: np.ndarray) -> np.ndarray:
    """
    Preprocesa una imagen para que coincida con la entrada que espera el modelo siamés.
    """
    # 1. Redimensionar
    resized_img = cv2.resize(image, (128, 128))
    
    # 2. Convertir a escala de grises si es necesario
    if len(resized_img.shape) == 3 and resized_img.shape[2] == 3:
        gray_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY)
    else:
        gray_img = resized_img
        
    # 3. Normalizar los valores de los píxeles al rango [0, 1]
    normalized_img = gray_img.astype("float32") / 255.0
    
    # 4. Añadir la dimensión del lote y la del canal
    # El modelo espera una forma de (1, 128, 128, 1)
    expanded_img = np.expand_dims(normalized_img, axis=0)
    expanded_img = np.expand_dims(expanded_img, axis=-1)
    
    return expanded_img

def find_main_contour(image_bin: np.ndarray) -> Optional[np.ndarray]:
    """
    Encuentra el contorno más grande en una imagen binarizada.
    Se asume que la imagen contiene un solo objeto principal (la letra).

    Args:
        image_bin: Imagen binarizada (fondo negro, letra blanca).

    Returns:
        El contorno más grande encontrado, o None si no se encuentran contornos.
    """
    # RETR_EXTERNAL es más eficiente si solo queremos los contornos exteriores.
    contours, _ = cv2.findContours(image_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        return None
        
    # Devuelve el contorno con el área más grande
    return max(contours, key=cv2.contourArea)