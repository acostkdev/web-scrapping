"""
Mision 3: El Cifrado Cromatico (Reto Hibrido HSV + LSB)
Bloque 3 - Esteganografia
Usa mascara de color en HSV combinado con extraccion LSB.
"""

import cv2
import numpy as np


def bits_a_bytes(bits):
    chars = []
    for i in range(0, len(bits) - 7, 8):
        byte = 0
        for j in range(8):
            byte = (byte << 1) | bits[i + j]
        chars.append(chr(byte))
    return "".join(chars)


def decodificar_lsb_con_mascara(imagen_ruta):
    try:
        img = cv2.imread(imagen_ruta)
        if img is None:
            raise FileNotFoundError(f"No se encontro la imagen: {imagen_ruta}")

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        bajo = np.array([15, 100, 100])
        alto = np.array([20, 255, 255])
        mascara = cv2.inRange(hsv, bajo, alto)

        v_channel = hsv[:, :, 2]
        pixeles_validos = v_channel[mascara > 0]

        if len(pixeles_validos) == 0:
            print("No se encontraron pixeles amarillo-pardo en la imagen.")
            return

        bits_extraidos = []
        mensaje = ""
        for valor in pixeles_validos:
            bits_extraidos.append(int(valor) & 1)
            if len(bits_extraidos) >= 8 and len(bits_extraidos) % 8 == 0:
                letra = bits_a_bytes(bits_extraidos)
                if "###FIN###" in letra:
                    mensaje = letra.replace("###FIN###", "")
                    break

        if mensaje:
            print("MENSAJE RECUPERADO:")
            print(mensaje)
        else:
            print("No se encontro el delimitador ###FIN### en los datos extraidos.")
            print("Bits extraidos hasta ahora:", len(bits_extraidos))

        print(f"\nPixeles con amarillo-pardo: {len(pixeles_validos)}")
        print(f"Bits extraidos: {len(bits_extraidos)}")

    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Asegurate de que evidencia_3.png esta en la misma carpeta.")
    except Exception as e:
        print(f"Ocurrio un error inesperado: {e}")


if __name__ == "__main__":
    import os
    ruta = os.path.join(os.path.dirname(__file__), "..", "color-detection", "color-detection-acertijo", "evidencia_3.png")
    decodificar_lsb_con_mascara(os.path.normpath(ruta))
