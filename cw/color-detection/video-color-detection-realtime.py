import cv2 as cv
import numpy as np
import time

cap = cv.VideoCapture(0)
i=0
color_ranges = { # Definir rangos de colores en HSV
    'red': (np.array([0, 100, 50]), np.array([20, 255, 255])),
    'green': (np.array([35, 100, 50]), np.array([85, 255, 255])),
    'yellow': (np.array([20, 100, 50]), np.array([35, 255, 255])),
    'purple': (np.array([130, 100, 50]), np.array([170, 255, 255])),
}

last_calculation = time.time()

while(True):
    ret, img = cap.read()
    if ret:
        cv.imshow('video', img)
        k = cv.waitKey(1) & 0xFF
        if k == 27:
            break

        current_time = time.time()
        
        if current_time - last_calculation >= 5:  # Cada 10 segundos
            height = img.shape[0]
            width = img.shape[1]
            hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
            
            masks = {}
            for color_name, (lowerColor, upperColor) in color_ranges.items():
                masks[color_name] = cv.inRange(hsv, lowerColor, upperColor)

            pixel_counts = {color_name: 0 for color_name in masks.keys()}
            total_color_pixels = 0

            for color_name, mask in masks.items():
                for y in range(height):
                    for x in range(width):
                        if mask[y, x] > 0:
                            pixel_counts[color_name] += 1
                            total_color_pixels += 1

            percetage_colors = {}
            for color_name, count in pixel_counts.items():
                percentage = (count / total_color_pixels) * 100 if total_color_pixels > 0 else 0
                percetage_colors[color_name] = percentage

            print("Porcentaje de pixeles por color:", percetage_colors)
            last_calculation = current_time

    else:
        break
   
cap.release()
cv.destroyAllWindows()