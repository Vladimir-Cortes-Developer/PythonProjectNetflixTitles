## Análisis Exploratorio de Datos: Dataset Netflix Titles
## Chatbot Netflix
## Bootcamp en Inteligencia artificial (Talento Tech)
## Nivel: Explorador - Básico-2025-5-L2-G47
## Realizado por:  Víctor C. Vladimir Cortés A.


# API de Películas Netflix

Esta es una API desarrollada con FastAPI que permite acceder a una base de datos de películas y series de Netflix. La API ofrece funcionalidades para listar, buscar por ID, filtrar por categoría y un chatbot que encuentra películas por palabras clave.

## Estructura del Proyecto

El proyecto consiste en un archivo principal `main.py` que implementa la API utilizando FastAPI y un conjunto de datos de Netflix almacenado en `dataset/netflix_titles.csv`.

## Requisitos

Para ejecutar esta API necesitas:

- Python 3.13.3+
- FastAPI
- Uvicorn (servidor ASGI)
- Pandas
- NLTK

## Instalación

```bash
# Crear un entorno virtual
python -m venv .venv

# Activar el entorno virtual
# En Windows:
.venv\Scripts\activate
# En Linux/Mac:
source .venv/bin/activate

# Instalar dependencias
pip install fastapi uvicorn pandas nltk

# Descargar los recursos de NLTK
python -c "import nltk; nltk.download('punkt'); nltk.download('wordnet')"
```

## Código Explicado

```python
# Importamos las herramientas necesarias para contruir nuestra API
from fastapi import FastAPI, HTTPException # FastAPI nos ayuda a crear la API, HTTPException maneja errores.
from fastapi.responses import HTMLResponse, JSONResponse # HTMLResponse nos permite responder con HTML, JSONResponse nos permite responder con JSON.
import pandas as pd # Pandas nos ayuda a manejar datos en tablasm como si fuera una hoja de cálculo.
import nltk # NLTK es una librería para procesar texto y analizar palabras.
from nltk.tokenize import word_tokenize # Se usa para dividir un texto en palabras individuales.
from nltk.corpus import wordnet # Nos ayuda a encontrar sinonimos de palabras.


# Configuración de NLTK - Descargamos los recursos necesarios
try:
    # Descargamos directamente sin especificar ruta para evitar problemas
    nltk.download('punkt')
    nltk.download('wordnet')
except Exception as e:
    print(f"Error al configurar NLTK: {e}")

def load_movies():
    # Leemos el archivo que contiene información de películas y seleccionamos las columnas más importantes
    df = pd.read_csv('./dataset/netflix_titles.csv')[['show_id','title','release_year','listed_in','description','rating']]

    # Renombramos las columnas para que sean más faciles de entender.
    df.columns = ['id','title','year','category','rating','overview']
    # Llenamos los espacios vacios con texto vacío y convertimos los datos en una lista de diccionarios
    return df.fillna('').to_dict(orient = 'records')

# Cargamos las películas al iniciar la API para no leer el archivo cada vez que alguien pregunte por ellas.
movies_list = load_movies()

# Función para encontrar sinónimos de una palabra (word)
def get_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name().lower())
    return synonyms

# Creamos la aplicación FastAPI, que será el motor de nuestra API
app = FastAPI(title="Mi aplicación de Películas", version="1.0.0")

# Ruta de inicio: Cuando alguien entra a la API sin especificar nada, verá un mensaje de bienvenda
@app.get('/', tags=['Home'])
def home():
# Cuando entremos en el navegador a http://127.0.0.1:8000/ veremos un mensaje de bienvenida.
    return HTMLResponse('<h1>Bienvenido a la API de Películas</h1>')

# Ruta para obtener todas las películas disponibles
@app.get('/movies', tags=['Movies'])
def get_movies():
    # Si hay películas, las enviamos, si no, mostramos un error
    return movies_list or HTTPException(status_code=500, detail="No hay datos de películas disponibles")

# Ruta para obtener una película específica según su ID
@app.get('/movies/{id}', tags=['Movies'])
def get_movie(id : str):
    # Buscamos en la lista de películas la que tenga el mismo ID
    return next((m for m in movies_list if m['id'] == id), {"detalle": "película no encontrada"})

# Ruta del chatbot que responde con películas según palabras clave de la categoría
@app.get("/chatbot", tags=["Chatbot"])
def chatbot(query: str):
    try:
        # Intentamos tokenizar con word_tokenize
        query_words = word_tokenize(query.lower())
    except LookupError:
        # Si falla, usamos un método más simple
        query_words = query.lower().split()

    # Obtenemos sinónimos para cada palabra
    synonyms = {word for q in query_words for word in get_synonyms(q)} | set(query_words)

    # Validamos que la película tenga categoría y buscamos coincidencias
    results = [m for m in movies_list if any(s in m["title"].lower() for s in synonyms)]

    return JSONResponse(content={
        "respuesta": "Aquí tienes algunas películas relacionadas." if results else "No encontré películas en esa categoría.",
        "películas": results
    })

# Ruta para buscar películas por categoría específica
@app.get ('/movies/by_category/', tags=['Movies'])
def get_movies_by_category(category: str):
    # Filtramos la lista de películas según la categoría ingresada
    return [m for m in movies_list if category.lower() in m['category'].lower()]
```

## Ejecución

Para iniciar la API, ejecuta:

```bash
uvicorn main:app --reload
```

Esto iniciará el servidor en `http://127.0.0.1:8000`.

## Endpoints Disponibles

La API ofrece los siguientes endpoints:

### Home
- `GET /`: Página de inicio con mensaje de bienvenida

### Películas
- `GET /movies`: Obtener todas las películas disponibles
- `GET /movies/{id}`: Obtener una película por su ID
- `GET /movies/by_category/?category={category}`: Obtener películas por categoría

### Chatbot
- `GET /chatbot?query={query}`: Buscar películas usando palabras clave en el título

## Documentación Interactiva

FastAPI genera automáticamente documentación interactiva. Puedes acceder a ella en:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Notas

- La función `chatbot` busca coincidencias en el título de las películas, no en la categoría como sugiere el comentario original.
- Los datos se cargan en memoria al iniciar la aplicación para mejorar el rendimiento.
- Se utiliza NLTK para procesamiento de lenguaje natural, específicamente para tokenización y búsqueda de sinónimos.
