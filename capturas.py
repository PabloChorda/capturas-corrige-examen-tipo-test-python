import os
from time import sleep
from PIL import Image
import pytesseract

# Paso 1: Leer el archivo de teoría
def leer_teoria(archivo):
    with open(archivo, 'r') as f:
        contenido = f.read()
    return contenido

# Paso 2: Capturar pantallazos
def capturar_pantallazo(n):
    os.system(f'screencapture -x ~/Desktop/screenshot_{n}.png')
    print(f"Pantallazo {n} guardado.")

# Capturar múltiples pantallazos con intervalo
def capturar_en_loop(cantidad):
    for i in range(cantidad):
        capturar_pantallazo(i)
        sleep(4)  # Ajusta el tiempo entre capturas si es necesario

# Paso 3: Extraer texto de los pantallazos
def procesar_pantallazo(n):
    imagen = Image.open(f'/Users/bigsur/Desktop/screenshot_{n}.png')
    return pytesseract.image_to_string(imagen, lang='spa')

# Paso 4: Buscar respuestas en el archivo de teoría
def buscar_respuesta_en_teoria(pregunta, teoria):
    # Simplificamos la pregunta para buscar palabras clave en la teoría
    palabras_clave = pregunta.lower().split()
    respuesta = ""
    for palabra in palabras_clave:
        if palabra in teoria.lower():
            # Encontramos una coincidencia en la teoría
            indice = teoria.lower().find(palabra)
            # Extraemos una parte cercana a la coincidencia como posible respuesta
            contexto = teoria[indice:indice+300]
            respuesta = contexto
            break
    
    if respuesta:
        # Analizar contexto para buscar opciones correctas
        if "correcta" in respuesta or "correcto" in respuesta:
            return "a" if "a" in respuesta else "b" if "b" in respuesta else "c" if "c" in respuesta else "d"
        else:
            return "No se encontró una respuesta clara."
    return "No se encontró una respuesta clara."

# Paso 5: Flujo principal
if __name__ == '__main__':
    # Leer la teoría desde un archivo de texto
    archivo_teoria = '/Users/bigsur/Desktop/teoria.txt'  # Cambia esta ruta si es necesario
    teoria = leer_teoria(archivo_teoria)

    # Capturar y procesar 8 pantallazos
    cantidad_pantallazos = 8
    capturar_en_loop(cantidad_pantallazos)

    # Conjunto para almacenar preguntas únicas
    preguntas_unicas = set()

    # Procesar cada pantallazo y obtener respuestas desde la teoría
    for i in range(cantidad_pantallazos):
        pregunta = procesar_pantallazo(i)

        # Limpiar el texto de la pregunta, eliminando contenido no relevante
        pregunta_limpia = "".join([c for c in pregunta if c.isalnum() or c.isspace()])
        
        # Verificar si la pregunta ya fue procesada
        if pregunta_limpia not in preguntas_unicas:
            preguntas_unicas.add(pregunta_limpia)  # Añadir pregunta al conjunto si es nueva
            print(f"Pregunta {i+1}:")
            
            # Buscar la respuesta en el archivo de teoría
            respuesta = buscar_respuesta_en_teoria(pregunta_limpia, teoria)
            print(f"Respuesta sugerida para la pregunta {i+1}: {respuesta}\n")
        else:
            print(f"Pregunta del pantallazo {i+1} omitida (duplicada).\n")















