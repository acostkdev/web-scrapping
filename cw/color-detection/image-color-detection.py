import cv2
import numpy as np
from pathlib import Path

def get_full_path(nombre_archivo, directorio_base="."):
    # 1. Definimos el punto de partida (Directorio actual por defecto)
    root = Path(directorio_base).resolve()
    # 2. Buscamos de forma recursiva (**) el nombre del archivo
    # Usamos next() para obtener la primera coincidencia y no cargar todo en memoria
    try:
        ruta_encontrada = next(root.rglob(nombre_archivo))
        return ruta_encontrada.resolve()
    except StopIteration:
        return None




# Main
archivo_buscado = "frutas.png"
path = get_full_path(archivo_buscado)

if not path:
    print("-- Archivo no localizado. --")
    exit()

img = cv2.imread(path)
height = img.shape[0]
width = img.shape[1]

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) # Convertir la Iimagen al espacio de color HSV

color_ranges = { # Definir rangos de colores en HSV
    'red': (np.array([0, 100, 50]), np.array([20, 255, 255])),
    'green': (np.array([35, 100, 50]), np.array([85, 255, 255])),
    'yellow': (np.array([20, 100, 50]), np.array([35, 255, 255])),
    'purple': (np.array([130, 100, 50]), np.array([170, 255, 255])),
}

masks = {} # Crear máscaras para cada color
for color_name, (lowerColor, upperColor) in color_ranges.items():
    masks[color_name] = cv2.inRange(hsv, lowerColor, upperColor)

# Realizar el conteo de pixeles de cada color
#Inicializaciones
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

print("Porcentaje de pixeles por color:", percetage_colors)


# Aplicar la máscara a la imagen original
index = 0
for mask in masks.values():
    result = cv2.bitwise_and(img, img, mask=mask)
    # La imagen con el color detectado
    # cv2.imshow("Color Detectado " + str(index), result)
    index += 1

# Mostrar la imagen original
cv2.imshow("Imagen Original", img)
cv2.waitKey(0)
cv2.destroyAllWindows()