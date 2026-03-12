

## Qué es LSB

LSB (Least Significant Bit) es la técnica de esteganografía más básica. Cada píxel de una imagen tiene valores de color (RGB). Si cambiamos el último bit de cada valor, el color cambia en 1 unidad de 256, que el ojo no nota.

Por ejemplo:
- Pixel original: (200, 150, 100)
- Pixel modificado: (200, 151, 100) — el cambio en el verde es invisible

Cada píxel tiene 3 canales (RGB) = 3 bits para almacenar información. Una imagen de 400x100 tiene 120,000 canales = podemos guardar hasta 15 KB de texto.

## Cómo funciona el código

1. **Codificar:** convertir el mensaje a bits, meter un bit en el LSB de cada canal de píxel
2. **Header:** primeros 32 bits almacenan la longitud del mensaje
3. **Decodificar:** leer los LSBs, reconstruir bits → texto

## Resultados

```
Imagen: 400x100, 120,000 bytes
Mensaje: 64 caracteres
Píxeles modificados: 279 / 120,000 (0.23%)
Recuperación exitosa
```

## Ejercicio
 `cw-bloque3-mision1-esteganografia-lsb.py`

---

