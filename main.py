"""
Imagina que esta API es una biblioteca de películas:
La función load_movies() es como un bibliotecario que carga el catálogo de libros (películas) cuando se abre la biblioteca.
La función get_movies() muestra todo el catálogo cuando alguien lo pide.
La función get_movie(id) es como si alguien preguntara por un libro específico por su código de identificación.
La función chatbot (query) es un asistente que busca libros según palabras clave y sinónimo.
La función get_movies_by_category (cagory) ayuda a encontrar películas según su género (acción, comedia, etc.).
"""

# Importamos las herramientas necesarias para contruir nuestra API
from fastapi import FastAPI, HTTPException # FastAPI nos ayuda a crear la API, HTTPException maneja errores.	I
from fastapi.responses import HTMLResponse, JSONResponse # HTMLResponse nos permite responder con HTML, JSONResponse nos permite responder con JSON.
import pandas as pd # Pandas nos ayuda a manejar datos en tablasm como si fuera una hoja de cálculo.
import nltk # NLTK es una librería para procesar texto y analizar palabras.
from nltk.tokenize import word_tokenize # Se usa para dividir un texto en palabras individuales.
from nltk.corpus import wordnet # Nos ayuda a encontrar sinonimos de palabras.

# Configuración de NLTK
try:
    nltk.data.path.append(r"C:\Users\User001\PycharmProjects\Talentotech2\PythonProjectNetflixTitles\.venv\nltk_data")
    nltk.download("punkt", download_dir=nltk.data.path[0], quiet=True)
    nltk.download("wordnet", download_dir=nltk.data.path[0], quiet=True)
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

# Función para encontrar sinónimos de una palabra
def get_synonyms(word):
    # Usamos WordNet para obtener distintas palabras que significan lo mismo.
    return{lemma.name().lower() for syn in wordnet.synsets(word) for lemma in syn.lemmas()}








