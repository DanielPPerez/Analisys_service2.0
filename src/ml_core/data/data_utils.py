# src/ml_core/data_utils.py
import numpy as np

def create_pairs_from_data(images, labels):
    """
    Crea pares de índices a partir de datos ya cargados en memoria.
    
    Args:
        images (np.array): Array con todas las imágenes.
        labels (np.array): Array con todas las etiquetas numéricas.
        
    Returns:
        tuple: (pares_de_indices, etiquetas_de_pares)
    """
    print("Creando pares de índices a partir de datos en memoria...")
    
    num_classes = len(np.unique(labels))
    map_label_to_indices = {label: np.flatnonzero(labels == label) for label in range(num_classes)}
    
    pair_indices = []
    pair_labels = []
    
    num_images = len(images)
    for i in range(num_images):
        current_label = labels[i]
        
        # Par positivo
        pos_idx = i
        while pos_idx == i:
            pos_idx = np.random.choice(map_label_to_indices[current_label])
        pair_indices.append([i, pos_idx])
        pair_labels.append(1.0)
        
        # Par negativo
        neg_label = np.random.randint(0, num_classes)
        while neg_label == current_label:
            neg_label = np.random.randint(0, num_classes)
        neg_idx = np.random.choice(map_label_to_indices[neg_label])
        pair_indices.append([i, neg_idx])
        pair_labels.append(0.0)
        
    print(f"Se crearon {len(pair_indices)} pares de índices.")
    return np.array(pair_indices), np.array(pair_labels, dtype="float32")