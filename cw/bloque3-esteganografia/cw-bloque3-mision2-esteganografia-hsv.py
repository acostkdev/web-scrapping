"""
Misión 2: Esteganografía en Canal HSV
Bloque 3 - Esteganografía

Oculta información en el canal Value del espacio HSV.
A diferencia de RGB, modificar el Value en HSV afecta solo el brillo percibido.
"""

import cv2
import numpy as np


def str_to_bits(t):
    return [(ord(c) >> i) & 1 for c in t for i in range(7, -1, -1)]


def bits_to_str(bits):
    chars = []
    for i in range(0, len(bits) - 7, 8):
        b = 0
        for j in range(8):
            b = (b << 1) | bits[i + j]
        if b == 0: break
        chars.append(chr(b))
    return "".join(chars)


def int32_bits(n):
    return [(n >> i) & 1 for i in range(31, -1, -1)]


def bits_int32(bits):
    n = 0
    for b in bits:
        n = (n << 1) | int(b)
    return n


def make_image():
    """Crea imagen con degradado."""
    img = np.zeros((150, 400, 3), dtype=np.uint8)
    for y in range(150):
        for x in range(400):
            img[y, x] = [(x * 3) % 256, (y * 5 + 30) % 256, (x + y * 2) % 256]
    return img


def cargar_o_crear(ruta=None):
    if ruta:
        img = cv2.imread(ruta)
        if img is None:
            raise FileNotFoundError(f"No se pudo cargar: {ruta}")
        return img
    return make_image()


def encode_hsv(img, msg):
    """
    Convierte a HSV, codifica bits en LSB del canal Value,
    convierte de vuelta a BGR.
    """
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    vf = hsv[:, :, 2].ravel().copy()  # Value channel
    
    bits = str_to_bits(msg)
    header = int32_bits(len(msg))
    all_bits = header + bits
    
    max_bits = min(len(all_bits), len(vf))
    if max_bits < len(all_bits):
        raise ValueError("Mensaje muy largo")
    
    for i in range(len(all_bits)):
        vf[i] = (vf[i] & 0xFE) | all_bits[i]
    
    hsv_cod = hsv.copy()
    hsv_cod[:, :, 2] = vf.reshape(hsv[:, :, 2].shape)
    return cv2.cvtColor(hsv_cod, cv2.COLOR_HSV2BGR)


def decode_hsv(img):
    """Lee los LSB del canal Value desde una imagen BGR."""
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    vf = hsv[:, :, 2].ravel()
    
    hbits = [int(vf[i] & 1) for i in range(32)]
    msg_len = bits_int32(hbits)
    
    if msg_len <= 0 or msg_len * 8 + 32 > len(vf):
        return ""
    
    mbits = [int(vf[32 + i] & 1) for i in range(msg_len * 8)]
    return bits_to_str(mbits)


def ejecutar(ruta_imagen=None):
    print("=" * 70)
    print("MISIÓN 2: ESTEGANOGRAFÍA HSV (VALUE)")
    print("=" * 70)
    print()
    
    img = cargar_o_crear(ruta_imagen)
    print(f"Imagen: {img.shape[1]}x{img.shape[0]}, {img.size} byte s")
    if ruta_imagen:
        print(f"   Cargada desde: {ruta_imagen}")
    else:
        print("   Generada sintéticamente")
    print()
    
    msg = "HSV Value hiding secret information dentro de los brightness bits."
    print(f"Mensaje ({len(msg)} chars): \"{msg}\"")
    print()
    
    print("codificando en Value channel (HSV)...")
    encoded = encode_hsv(img, msg)
    
    diff = cv2.absdiff(img, encoded)
    mods = np.count_nonzero(diff)
    print(f"  Píxeles modificados: {mods} / {img.size} ({100*mods/img.size:.2f}%)")
    print()
    
    print("decodificando...")
    recovered = decode_hsv(encoded)
    ok = recovered == msg
    print(f"  Mensaje: \"{recovered}\"")
    print(f"  {'OK' if ok else ' FALLÓ'}")
    print()
    
    print("=" * 70)
    print("FIN M2")
    print("=" * 70)


if __name__ == "__main__":
    import sys
    ruta = sys.argv[1] if len(sys.argv) > 1 else None
    ejecutar(ruta)
