# generate_templates.py
import os
from PIL import Image, ImageDraw, ImageFont

print("Iniciando la generación de plantillas de caracteres...")

# --- CONFIGURACIÓN ---
OUTPUT_DIR = "dataset/plantillas"
IMG_SIZE = (128, 128)
BACKGROUND_COLOR = "white"
TEXT_COLOR = "black"
FONT_SIZE = 90

# Lista completa de caracteres a generar
CHARACTERS = list("abcdefghijklmnopqrstuvwxyz") + \
             list("ABCDEFGHIJKLMNOPQRSTUVWXYZ") + \
             list("0123456789") + \
             ['ñ', 'Ñ', 'Ch', 'ch', 'Ll', 'll']

# Intenta encontrar una fuente.
try:
    font = ImageFont.truetype("arial.ttf", FONT_SIZE)
except IOError:
    print(f"Fuente 'arial.ttf' no encontrada. Usando fuente por defecto.")
    print("Asegúrate de tener una fuente .ttf disponible o cambia la ruta en el script.")
    font = ImageFont.load_default()


def generate_character_image(character, filename):
    """
    Genera y guarda una imagen para un único caracter.
    """
    # Crear una imagen en blanco
    img = Image.new('L', IMG_SIZE, color=BACKGROUND_COLOR) # 'L' para escala de grises
    draw = ImageDraw.Draw(img)

    # Calcular la posición para centrar el texto
    try:
        # Versión moderna de Pillow para calcular el bounding box
        _, _, text_width, text_height = draw.textbbox((0, 0), character, font=font)
    except AttributeError:
        # Fallback para versiones más antiguas de Pillow
        text_width, text_height = draw.textsize(character, font=font)
    
    x = (IMG_SIZE[0] - text_width) / 2
    y = (IMG_SIZE[1] - text_height) / 2

    # Dibujar el texto en la imagen
    draw.text((x, y), character, fill=TEXT_COLOR, font=font)
    
    # Guardar la imagen
    img.save(filename)


def main():
    """
    Función principal que orquesta la creación de las plantillas.
    """
    # Crear el directorio de salida si no existe
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Directorio creado: {OUTPUT_DIR}")

    print(f"Generando {len(CHARACTERS)} plantillas de caracteres...")
    
    for char in CHARACTERS:
        # Crear un nombre de archivo seguro
        char_identifier = f"{char}_ord{ord(char[0])}"
        output_path = os.path.join(OUTPUT_DIR, f"{char_identifier}_template.png")
        generate_character_image(char, output_path)

    print("-" * 30)
    print("¡Generación de plantillas completada!")
    print(f"Las imágenes se han guardado en la carpeta: {OUTPUT_DIR}")
    print("-" * 30)


if __name__ == "__main__":
    main()