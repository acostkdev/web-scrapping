"""
Misión 1: Esteganografía LSB (Least Significant Bit)
Bloque 3 - Esteganografía

Oculta un mensaje en los bits menos significativos de una imagen.
Cambiar el último bit de cada canal de color es invisible al ojo humano.
"""

import cv2
import numpy as np


def str_to_bits(texto):
    """Convierte string a lista de enteros (bits)."""
    bits = []
    for c in texto:
        for i in range(7, -1, -1):
            bits.append((ord(c) >> i) & 1)
    return bits


def bits_to_str(bits):
    """Convierte lista de bits de vuelta a string."""
    chars = []
    for i in range(0, len(bits) - 7, 8):
        byte = 0
        for j in range(8):
            byte = (byte << 1) | bits[i + j]
        if byte == 0:
            break
        chars.append(chr(byte))
    return "".join(chars)


def int_to_bits_32(n):
    """Entero de 0-2^32 a 32 bits (big-endian)."""
    return [(n >> i) & 1 for i in range(31, -1, -1)]


def bits_32_to_int(bits):
    """32 bits de vuelta a entero."""
    n = 0
    for b in bits:
        n = (n << 1) | int(b)
    return n


def make_image():
    """Imagen de prueba con textura."""
    np.random.seed(42)
    return np.random.randint(0, 256, (100, 400, 3), dtype=np.uint8)


def cargar_o_crear_imagen(ruta=None):
    """Carga imagen desde ruta o crea una de prueba."""
    if ruta:
        img = cv2.imread(ruta)
        if img is None:
            raise FileNotFoundError(f"No se pudo cargar: {ruta}")
        return img
    return make_image()


def encode_lsb(img, msg):
    """Codifica msg en los LSB de la imagen."""
    h, w, c = img.shape
    flat = img.copy().ravel()
    
    bits = str_to_bits(msg)
    header = int_to_bits_32(len(msg))
    bits_total = header + bits
    
    max_chars = (flat.size - 32) // 8
    if len(msg) > max_chars:
        raise ValueError(f"Mensaje muy largo. Máximo {max_chars} caracteres")
    
    for i in range(len(bits_total)):
        # & 0xFE limpia el LSB, | bits_total[i] lo setea
        flat[i] = (flat[i] & 0xFE) | bits_total[i]
    
    return flat.reshape(h, w, c)


def decode_lsb(img):
    """Extrae mensaje desde los LSB de la imagen."""
    flat = img.ravel()
    
    # leer header: 32 bits = longitud del mensaje
    hbits = [int(flat[i] & 1) for i in range(32)]
    msg_len = bits_32_to_int(hbits)
    
    if msg_len <= 0 or msg_len * 8 + 32 > flat.size:
        return ""
    
    # leer los bits del mensaje
    mbits = [int(flat[32 + i] & 1) for i in range(msg_len * 8)]
    return bits_to_str(mbits)


def ejecutar(ruta_imagen=None):
    print("=" * 70)
    print("MISIÓN 1: ESTEGANOGRAFÍA LSB")
    print("=" * 70)
    print()
    
    img = cargar_o_crear_imagen(ruta_imagen)
    print(f"📷 Imagen: {img.shape[1]}x{img.shape[0]}, {img.size} bytes")
    if ruta_imagen:
        print(f"   Cargada desde: {ruta_imagen}")
    else:
        print("   Generada sintéticamente")
    print()
    
    msg = "Mensaje oculto en LSB. Solo quien sabe dónde mirar lo encuentra."
    print(f"📝 Mensaje ({len(msg)} chars): \"{msg}\"")
    print()
    
    print("🔒 Codificando...")
    encoded = encode_lsb(img, msg)
    
    diff = cv2.absdiff(img, encoded)
    mods = np.count_nonzero(diff)
    print(f"  Píxeles modificados: {mods} / {img.size} ({100*mods/img.size:.2f}%)")
    print()
    
    print("🔓 Decodificando...")
    recovered = decode_lsb(encoded)
    ok = recovered == msg
    print(f"  Mensaje: \"{recovered}\"")
    print(f"  {'✅ OK' if ok else '❌ FALLÓ'}")
    print()
    
    # demo visual
    print("📊 Primeros 24 píxeles - cambios en LSB:")
    print("  i  ant  nuevo  LSB?")
    for i in range(24):
        a = int(img.ravel()[i])
        d = int(encoded.ravel()[i])
        ch = "✓" if (a & 1) != (d & 1) else "·"
        print(f"  {i:>2}  {a:>3}   {d:>3}    {ch}")
    print()
    
    print("=" * 70)
    print("FIN M1")
    print("=" * 70)


if __name__ == "__main__":
    import sys
    ruta = sys.argv[1] if len(sys.argv) > 1 else None
    ejecutar(ruta)
