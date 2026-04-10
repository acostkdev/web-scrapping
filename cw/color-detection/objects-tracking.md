# Investigación: Algoritmos de Detección y Localización de Objetos mediante Segmentación de Color

## 1. Introducción a la Segmentación de Color
En el análisis de imágenes, la segmentación por color es una técnica de visión computacional que permite aislar objetos de interés basándose en sus propiedades cromáticas. A diferencia de la detección por redes neuronales (como YOLO), este enfoque es computacionalmente ligero y determinista, ideal para entornos con recursos limitados o condiciones de iluminación controladas.

## 2. El Proceso de Segmentación (Pipeline Arquitectónico)
Para que un sistema de detección sea robusto y siga principios, debemos separar las responsabilidades:

1. **Preprocesamiento:** Conversión de espacios de color (de BGR/RGB a HSV/LAB para mayor robustez ante cambios de luz).
2. **Umbralización (Thresholding):** Creación de una máscara binaria donde los píxeles que cumplen el criterio son blancos (1) y el resto negros (0).
3. **Operaciones Morfológicas:** Aplicación de erosión y dilatación (no reinventar filtros, usar kernels estándar) para eliminar ruido.
4. **Extracción de Características:** Localización de contornos y cálculo de momentos.

## 3. Localización del Objeto: El Centroide
Una vez obtenida la máscara binaria del objeto específico, el método matemático estándar para hallar su centro de masa es mediante **Momentos de Imagen**.

### Fundamentación Matemática
El momento de una imagen $I(x,y)$ se define como:
$$M_{ij} = \sum_{x} \sum_{y} x^i y^j I(x,y)$$

Para una imagen binaria, el centroide $(\bar{x}, \bar{y})$ se calcula utilizando los momentos de orden cero y primer orden:
$$\bar{x} = \frac{M_{10}}{M_{00}}, \quad \bar{y} = \frac{M_{01}}{M_{00}}$$
Donde $M_{00}$ representa el área del objeto.

### Implementación en Python (OpenCV)
Siguiendo buenas prácticas, encapsulamos la lógica en una función pura para facilitar pruebas unitarias.

```python
import cv2
import numpy as np

def get_object_centroid(binary_mask: np.ndarray) -> tuple:
    """
    Calcula el centroide de la masa blanca en una máscara binaria.'.
    """
    moments = cv2.moments(binary_mask)
    
    # Evitar división por cero si no hay objeto detectado
    if moments["m00"] == 0:
        return (0, 0)
    
    cX = int(moments["m10"] / moments["m00"])
    cY = int(moments["m01"] / moments["m00"])
    
    return (cX, cY)