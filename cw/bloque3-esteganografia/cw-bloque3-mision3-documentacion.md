# Mision 3: El Cifrado Cromatico (Reto Hibrido HSV + LSB)

## Que hicimos

En esta mision combinamos tecnicas de las misiones 1 y 2 para crear
un metodo hibrido. Primero aplicamos una mascara de color en HSV para
encontrar solo los pixeles de un tono especifico (amarillo-pardo), y
despues extraemos el LSB unicamente de esos pixeles. Esto hace que el
mensaje sea invisible incluso si sabes que hay esteganografia, porque
los pixeles que contienen el mensaje son solo los del color indicado.

## Por que HSV

HSV nos permite aislar colores de manera mas natural que RGB. Aca
definimos un rango de tono amarillo-pardo (H entre 15 y 20, S y V
minimos de 100). Con la funcion inRange de OpenCV creamos una mascara
binaria que marca solo los pixeles dentro de ese rango. Esto es clave
porque si no usamos mascara, estariamos leyendo LSB de todo la imagen
y el mensaje se perderia entre el ruido.

## Como funciona el enfoque hibrido

1. Cargar la imagen evidencia_3.png
2. Convertir a HSV
3. Crear mascara de amarillo-pardo con inRange
4. Extraer el canal V (Value) y filtrar solo los pixeles validos
5. Leer el bit menos significativo de cada valor V
6. Agrupar bits en bytes y convertirlos a caracteres ASCII
7. Parar cuando encontramos el delimitador ###FIN###

## Que aprendimos

Aprendimos que combinar tecnicas de esteganografia hace que el mensaje
sea mucho mas dificil de detectar. No solo estamos ocultando en LSB,
sino que ademas limitamos la escritura a un subconjunto especifico de
pixeles basados en color. Un atacante tendria que saber:
- Que hay esteganografia
- Que se uso HSV
- Que rango de color exacto se uso como mascara

Sin esa informacion, el mensaje es practicamente imposible de recuperar.

## Resultados

El script busca el archivo evidencia_3.png en la misma carpeta y si no
existe atrapa el error con try/except. Es importante tener la imagen
correcta para que funcione.
