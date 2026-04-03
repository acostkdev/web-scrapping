import cv2
import glob
import numpy as np
from pathlib import Path

# Busqueda del path de la carpeta
def get_folder_path(nombre_carpeta, directorio_base="."):
    root = Path(directorio_base).resolve()
    search_generator = (p for p in root.rglob(nombre_carpeta) if p.is_dir())
    try:
        return next(search_generator).resolve()
    except StopIteration:
        return None

# Inicio. Obtener rutas de archivos y comprobar su existencia
nombre_carpeta='color-detection-imagelist'
carpeta = get_folder_path(nombre_carpeta)
ruta_imagenes = glob.glob(str(carpeta / '*.png')) if carpeta else []
if len(ruta_imagenes) == 0:
    print("-- Error al obtener imágenes. --")
    exit()


# Leer imágenes y aplicar máscaras de color
imagenes = []
color_ranges = { # Definir rangos de colores en HSV
    'red': (np.array([0, 100, 50]), np.array([20, 255, 255])),
    'green': (np.array([35, 100, 50]), np.array([85, 255, 255])),
    'yellow': (np.array([20, 100, 50]), np.array([35, 255, 255])),
    'purple': (np.array([130, 100, 50]), np.array([170, 255, 255])),
}
for ruta in ruta_imagenes:
    img = cv2.imread(ruta)
    if img is not None:
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        masks = {}
        for color_name, (lowerColor, upperColor) in color_ranges.items():
            masks[color_name] = cv2.inRange(hsv, lowerColor, upperColor)
        imagenes.append({'image': img, 'masks': masks})

index = 0
for imagen in imagenes:
    img = imagen['image']
    height, width = img.shape[:2]
    masks = imagen['masks']
    pixel_counts = {}
    total_color_pixels = 0
    for color_name, mask in masks.items():
        pixel_counts[color_name] = 0

    for color_name, mask in masks.items(): #Conteos
        for y in range(height):
            for x in range(width):
                if mask[y, x] > 0:
                    pixel_counts[color_name] = pixel_counts[color_name] + 1
                    total_color_pixels = total_color_pixels + 1

    percetage_colors = {}
    for color_name, count in pixel_counts.items():
        percentage = (count / total_color_pixels) * 100 if total_color_pixels > 0 else 0
        percetage_colors[color_name] = percentage
    print(f"Imagen {index}: Porcentaje de pixeles por color en {percetage_colors}")
    index += 1