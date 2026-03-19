# Misión 2: HSV (Canal Value)

## Qué Hace

Convierte la imagen a espacio HSV (Hue, Saturation, Value) y esconde el mensaje en los LSB del canal **Value** (brillo).

## Por Qué HSV es Diferente

En RGB, cada canal tiene un impacto directo en el color final. En HSV:
- **Hue:** tono (0-179, circular)
- **Saturation:** saturación/intensidad del color
- **Value:** brillo (0-255)

Modificar el canal Value afecta solo el brillo percibido, no el color en sí. Es una alternativa interesante al LSB directo en RGB.

## Trade-offs

| Técnica | Modificaciones | Recuperación | Visibilidad |
|---------|---------------|-------------|------------|
| LSB en RGB (Misión 1) | 0.23% | 100% | Imperceptible |
| LSB en HSV (Misión 2) | ~41% | 100% | Más notable |

El HSV modifica más píxeles porque cambiar el Value se traduce en cambios en los 3 canales al convertir de vuelta a BGR. Es menos óptimo que LSB directo, pero demuestra cómo se puede aplicar esteganografía en diferentes espacios de color.

## Cómo se Usa

```python
# codificar
encoded = encode_hsv(imagen_bgr, mensaje)
cv2.imwrite("imagen_secreta.png", encoded)

# decodificar
recovered = decode_hsv(encoded)
print(recovered)
```
