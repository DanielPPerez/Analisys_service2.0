# augment_dataset.py
import os
import cv2
import albumentations as A
import numpy as np

print("Iniciando la aumentación del dataset...")

# --- CONFIGURACIÓN ---
INPUT_DIR = "dataset/plantillas"
OUTPUT_DIR = "dataset/variations"
NUM_VARIATIONS_PER_TEMPLATE = 800 

# Definir el pipeline de aumentación de datos
# Estas son transformaciones potentes para simular la escritura a mano
transform = A.Compose([
    A.Rotate(limit=15, p=0.8, border_mode=cv2.BORDER_CONSTANT, value=[255, 255, 255]),
    A.ShiftScaleRotate(shift_limit=0.05, scale_limit=0.1, rotate_limit=0, p=0.8, border_mode=cv2.BORDER_CONSTANT, value=[255, 255, 255]),
    A.ElasticTransform(p=0.7, alpha=120, sigma=120 * 0.05, alpha_affine=120 * 0.03),
    A.GridDistortion(p=0.5),
    A.OpticalDistortion(p=0.5, distort_limit=0.5, shift_limit=0.2),
])

def main():
    """
    Función principal que orquesta la aumentación de datos.
    """
    if not os.path.exists(INPUT_DIR):
        print(f"Error: El directorio de plantillas '{INPUT_DIR}' no existe.")
        print("Por favor, ejecuta 'generate_templates.py' primero.")
        return

    template_files = [f for f in os.listdir(INPUT_DIR) if f.endswith('.png')]
    
    if not template_files:
        print(f"No se encontraron plantillas en '{INPUT_DIR}'.")
        return
        
    print(f"Se encontraron {len(template_files)} plantillas. Generando {NUM_VARIATIONS_PER_TEMPLATE} variaciones para cada una...")

    for template_file in template_files:
        # Extraer el nombre del caracter para usarlo como nombre de la subcarpeta
        character_name = template_file.replace('_template.png', '')
        char_output_dir = os.path.join(OUTPUT_DIR, character_name)
        
        # Crear la subcarpeta para el caracter si no existe
        if not os.path.exists(char_output_dir):
            os.makedirs(char_output_dir)
        
        # Cargar la imagen de la plantilla
        template_path = os.path.join(INPUT_DIR, template_file)
        image = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
        
        if image is None:
            print(f"Advertencia: No se pudo leer la imagen {template_path}")
            continue

        # Generar y guardar las imágenes aumentadas
        for i in range(NUM_VARIATIONS_PER_TEMPLATE):
            augmented = transform(image=image)
            augmented_image = augmented['image']
            
            output_filename = os.path.join(char_output_dir, f"{character_name}_{i+1}.png")
            cv2.imwrite(output_filename, augmented_image)
    
    print("-" * 30)
    print("¡Aumentación de datos completada!")
    print(f"Las imágenes generadas se han guardado en: {OUTPUT_DIR}")
    print("-" * 30)

if __name__ == "__main__":
    main()