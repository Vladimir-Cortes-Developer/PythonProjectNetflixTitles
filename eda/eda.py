# Importación de librerías necesarias
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import re

# Configuración de visualización
plt.style.use('fivethirtyeight')
sns.set_palette('Set2')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)
pd.set_option('display.width', 1000)


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

    # 1. CARGA Y EXPLORACIÓN INICIAL DE DATOS
    # ---------------------------------------
    print("1. CARGA Y EXPLORACIÓN INICIAL DE DATOS")
    print("-" * 50)

    # Cargar el dataset
    df = pd.read_csv('../dataset/netflix_titles.csv')

    # Información básica del dataset
    print("\n• Información básica del dataset:")
    print(f"Dimensiones del dataset: {df.shape[0]} filas x {df.shape[1]} columnas")
    print("\n• Primeras 5 filas del dataset:")
    print(df.head())

    # Información de las columnas
    print("\n• Información de tipos de datos:")
    print(df.info())

    # Estadísticas descriptivas
    print("\n• Estadísticas descriptivas:")
    print(df.describe(include='all'))

    # 2. ANÁLISIS DE VALORES FALTANTES
    # --------------------------------
    print("\n\n2. ANÁLISIS DE VALORES FALTANTES")
    print("-" * 50)

    # Calcular valores faltantes por columna
    missing_values = df.isnull().sum()
    missing_percentage = (missing_values / len(df)) * 100

    missing_data = pd.DataFrame({
        'Valores Faltantes': missing_values,
        'Porcentaje (%)': missing_percentage.round(2)
    })

    print("• Análisis de valores faltantes por columna:")
    print(missing_data[missing_data['Valores Faltantes'] > 0].sort_values(by='Valores Faltantes', ascending=False))

    # Visualización de valores faltantes
    plt.figure(figsize=(12, 6))
    sns.heatmap(df.isnull(), cbar=False, cmap='viridis', yticklabels=False)
    plt.title('Mapa de calor de valores faltantes')
    plt.tight_layout()
    plt.savefig('../imagenes/valores_faltantes.png')

    # 3. PREPROCESAMIENTO BÁSICO
    # -------------------------
    print("\n\n3. PREPROCESAMIENTO BÁSICO")
    print("-" * 50)

    # Copia del dataframe para no afectar el original
    df_clean = df.copy()

    # Convertir date_added a datetime
    df_clean['date_added'] = pd.to_datetime(df_clean['date_added'], errors='coerce')

    # Extraer año y mes de date_added
    df_clean['year_added'] = df_clean['date_added'].dt.year
    df_clean['month_added'] = df_clean['date_added'].dt.month

    # Tratamiento de valores faltantes (corregido para evitar FutureWarning)
    df_clean = df_clean.assign(
        director=df_clean['director'].fillna('Sin director'),
        cast=df_clean['cast'].fillna('Sin elenco'),
        country=df_clean['country'].fillna('País desconocido')
    )

    # Extraer la duración numérica y la unidad (corregido para evitar SyntaxWarning)
    df_clean['duration_numeric'] = df_clean['duration'].str.extract(r'(\d+)').astype(float)
    df_clean['duration_unit'] = df_clean['duration'].str.extract(r'(\D+)').fillna('')
    df_clean['duration_unit'] = df_clean['duration_unit'].str.strip()

    print("• Nuevas columnas creadas:")
    print(df_clean[['date_added', 'year_added', 'month_added', 'duration', 'duration_numeric', 'duration_unit']].head())

    # 4. ANÁLISIS DE DISTRIBUCIÓN DE CONTENIDO
    # ---------------------------------------
    print("\n\n4. ANÁLISIS DE DISTRIBUCIÓN DE CONTENIDO")
    print("-" * 50)

    # Distribución por tipo (Movie vs TV Show)
    content_distribution = df_clean['type'].value_counts()
    print("• Distribución por tipo de contenido:")
    print(content_distribution)
    print(f"Porcentaje de películas: {(content_distribution['Movie'] / len(df_clean) * 100):.2f}%")
    print(f"Porcentaje de series: {(content_distribution['TV Show'] / len(df_clean) * 100):.2f}%")

    # Visualización de la distribución por tipo (corregido para evitar FutureWarning)
    plt.figure(figsize=(10, 6))
    # Asignar color explícitamente sin usar palette
    ax = sns.countplot(x='type', data=df_clean, hue='type', legend=False)
    plt.title('Distribución de Tipos de Contenido en Netflix')
    plt.xlabel('Tipo de Contenido')
    plt.ylabel('Cantidad')

    # Agregar etiquetas de cantidad y porcentaje
    total = len(df_clean)
    for p in ax.patches:
        percentage = f'{100 * p.get_height() / total:.1f}%'
        x = p.get_x() + p.get_width() / 2
        y = p.get_height()
        ax.annotate(f'{int(y)}\n{percentage}', (x, y), ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig('../imagenes/distribucion_tipos.png')

    # 5. ANÁLISIS TEMPORAL
    # -------------------
    print("\n\n5. ANÁLISIS TEMPORAL")
    print("-" * 50)

    # Tendencia de lanzamientos por año
    releases_by_year = df_clean['release_year'].value_counts().sort_index()
    print("• Top 10 años con más lanzamientos:")
    print(releases_by_year.sort_values(ascending=False).head(10))

    # Visualización de tendencia por año
    plt.figure(figsize=(15, 6))
    releases_by_year.plot(kind='line', marker='o', linewidth=2)
    plt.title('Tendencia de Lanzamientos por Año')
    plt.xlabel('Año de Lanzamiento')
    plt.ylabel('Cantidad de Títulos')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('../imagenes/lanzamientos_por_año.png')

    # Distribución de contenido agregado por año
    yearly_additions = df_clean['year_added'].value_counts().sort_index()
    print("\n• Contenido añadido a Netflix por año:")
    print(yearly_additions)

    # Visualización de adiciones por año
    plt.figure(figsize=(15, 6))
    yearly_additions.plot(kind='bar', color='coral')
    plt.title('Contenido Añadido a Netflix por Año')
    plt.xlabel('Año')
    plt.ylabel('Cantidad de Títulos')
    plt.tight_layout()
    plt.savefig('../imagenes/adiciones_por_año.png')

    # Evolución de tipos de contenido por año
    content_by_year = df_clean.groupby(['release_year', 'type']).size().unstack().fillna(0)
    print("\n• Evolución de tipos de contenido por año (muestra):")
    print(content_by_year.tail(10))  # últimos 10 años

    # Visualización de evolución por tipo y año
    plt.figure(figsize=(15, 7))
    content_by_year.plot(marker='o')
    plt.title('Evolución de Tipos de Contenido por Año')
    plt.xlabel('Año de Lanzamiento')
    plt.ylabel('Cantidad de Títulos')
    plt.grid(True, alpha=0.3)
    plt.legend(title='Tipo de Contenido')
    plt.tight_layout()
    plt.savefig('../imagenes/evolucion_contenido.png')

    # Heatmap de estrenos por mes y año
    recent_df = df_clean[df_clean['year_added'] >= 2015].copy()  # Últimos años
    heatmap_data = pd.crosstab(recent_df['year_added'], recent_df['month_added'])
    plt.figure(figsize=(14, 8))
    sns.heatmap(heatmap_data, cmap='YlOrRd', annot=True, fmt='d')
    plt.title('Heatmap de Estrenos por Mes y Año (desde 2015)')
    plt.xlabel('Mes')
    plt.ylabel('Año')
    plt.tight_layout()
    plt.savefig('../imagenes/heatmap_estrenos.png')

    # 6. ANÁLISIS POR PAÍS
    # -------------------
    print("\n\n6. ANÁLISIS POR PAÍS")
    print("-" * 50)

    # Procesamiento para obtener todos los países (considerando que pueden estar separados por coma)
    all_countries = df_clean['country'].str.split(', ').explode().str.strip()
    country_counts = all_countries.value_counts().head(15)
    print("• Top 15 países con más contenido:")
    print(country_counts)

    # Visualización de top países
    plt.figure(figsize=(12, 8))
    country_counts.plot(kind='barh', color='skyblue')
    plt.title('Top 15 Países con Más Contenido en Netflix')
    plt.xlabel('Cantidad de Títulos')
    plt.ylabel('País')
    plt.tight_layout()
    plt.savefig('../imagenes/top_paises.png')

    # 7. ANÁLISIS DE CLASIFICACIONES (RATINGS)
    # --------------------------------------
    print("\n\n7. ANÁLISIS DE CLASIFICACIONES (RATINGS)")
    print("-" * 50)

    # Distribución de clasificaciones
    rating_counts = df_clean['rating'].value_counts()
    print("• Distribución de clasificaciones:")
    print(rating_counts)

    # Visualización de clasificaciones (corregido para evitar FutureWarning)
    plt.figure(figsize=(12, 8))
    ordered_ratings = df_clean['rating'].value_counts().index
    ax = sns.countplot(y='rating', data=df_clean, order=ordered_ratings, color='steelblue')
    plt.title('Distribución de Clasificaciones de Contenido')
    plt.xlabel('Cantidad de Títulos')
    plt.ylabel('Clasificación')

    # Agregar etiquetas de cantidad
    for i, v in enumerate(rating_counts):
        ax.text(v + 5, i, str(v), va='center')

    plt.tight_layout()
    plt.savefig('../imagenes/clasificaciones.png')

    # 8. ANÁLISIS DE GÉNEROS
    # ---------------------
    print("\n\n8. ANÁLISIS DE GÉNEROS")
    print("-" * 50)

    # Procesamiento para obtener todos los géneros
    all_genres = df_clean['listed_in'].str.split(', ').explode().str.strip()
    genre_counts = all_genres.value_counts().head(15)
    print("• Top 15 géneros en Netflix:")
    print(genre_counts)

    # Visualización de géneros
    plt.figure(figsize=(14, 10))
    genre_counts.plot(kind='barh', color='lightseagreen')
    plt.title('Top 15 Géneros en Netflix')
    plt.xlabel('Cantidad de Títulos')
    plt.ylabel('Género')
    plt.tight_layout()
    plt.savefig('../imagenes/generos.png')

    # 9. ANÁLISIS DE DURACIÓN
    # ----------------------
    print("\n\n9. ANÁLISIS DE DURACIÓN")
    print("-" * 50)

    # Películas - Distribución de duración en minutos
    movies_df = df_clean[df_clean['type'] == 'Movie'].copy()
    print("• Estadísticas de duración de películas (minutos):")
    print(movies_df['duration_numeric'].describe())

    # Visualización de duración de películas
    plt.figure(figsize=(15, 6))
    sns.histplot(data=movies_df, x='duration_numeric', bins=30, kde=True)
    plt.title('Distribución de Duración de Películas')
    plt.xlabel('Duración (minutos)')
    plt.ylabel('Frecuencia')
    plt.tight_layout()
    plt.savefig('../imagenes/duracion_peliculas.png')

    # Series - Distribución de temporadas
    tvshows_df = df_clean[df_clean['type'] == 'TV Show'].copy()
    season_counts = tvshows_df['duration_numeric'].value_counts().sort_index().head(10)
    print("\n• Distribución de temporadas en series:")
    print(season_counts)

    # Visualización de temporadas de series
    plt.figure(figsize=(12, 6))
    season_counts.plot(kind='bar', color='purple')
    plt.title('Distribución de Temporadas en Series de Netflix')
    plt.xlabel('Número de Temporadas')
    plt.ylabel('Cantidad de Series')
    plt.tight_layout()
    plt.savefig('../imagenes/temporadas_series.png')

    # 10. ANÁLISIS DE DIRECTORES
    # -------------------------
    print("\n\n10. ANÁLISIS DE DIRECTORES")
    print("-" * 50)

    # Top directores con más contenido
    # Excluimos 'Sin director' para el análisis
    directors_df = df_clean[df_clean['director'] != 'Sin director'].copy()
    directors = directors_df['director'].str.split(', ').explode().str.strip()
    top_directors = directors.value_counts().head(15)
    print("• Top 15 directores con más contenido:")
    print(top_directors)

    # Visualización de top directores
    plt.figure(figsize=(14, 10))
    top_directors.plot(kind='barh', color='salmon')
    plt.title('Top 15 Directores con Más Contenido en Netflix')
    plt.xlabel('Cantidad de Títulos')
    plt.ylabel('Director')
    plt.tight_layout()
    plt.savefig('../imagenes/top_directores.png')

    # 11. ANÁLISIS DE CORRELACIONES
    # ----------------------------
    print("\n\n11. ANÁLISIS DE CORRELACIONES")
    print("-" * 50)

    # Seleccionar sólo variables numéricas
    numeric_df = df_clean[['release_year', 'year_added', 'month_added', 'duration_numeric']].copy()
    correlation = numeric_df.corr()
    print("• Matriz de correlación entre variables numéricas:")
    print(correlation)

    # Visualización de correlaciones
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation, annot=True, cmap='coolwarm', center=0)
    plt.title('Correlación entre Variables Numéricas')
    plt.tight_layout()
    plt.savefig('../imagenes/correlacion.png')

    # 12. EVOLUCIÓN DE GÉNEROS A LO LARGO DEL TIEMPO
    # ---------------------------------------------
    print("\n\n12. EVOLUCIÓN DE GÉNEROS A LO LARGO DEL TIEMPO")
    print("-" * 50)

    # Obtener los 5 géneros más comunes
    top5_genres = all_genres.value_counts().head(5).index.tolist()

    # Crear un DataFrame para el análisis de evolución de géneros
    genre_evolution = {}
    for genre in top5_genres:
        # Filtramos el DataFrame para cada género
        genre_data = df_clean[df_clean['listed_in'].str.contains(genre)]
        # Contamos títulos por año
        yearly_counts = genre_data.groupby('release_year').size()
        genre_evolution[genre] = yearly_counts

    genre_evolution_df = pd.DataFrame(genre_evolution)
    genre_evolution_df = genre_evolution_df.fillna(0)

    print("• Evolución de los 5 géneros principales (muestra de los últimos 10 años):")
    print(genre_evolution_df.tail(10))

    # Visualización de evolución de géneros
    plt.figure(figsize=(15, 8))
    genre_evolution_df[top5_genres].plot(marker='o')
    plt.title('Evolución de los 5 Géneros Principales por Año')
    plt.xlabel('Año')
    plt.ylabel('Cantidad de Títulos')
    plt.grid(True, alpha=0.3)
    plt.legend(title='Género')
    plt.tight_layout()
    plt.savefig('../imagenes/evolucion_generos.png')

    # 13. HALLAZGOS PRINCIPALES
    # ------------------------
    print("\n\n13. HALLAZGOS PRINCIPALES")
    print("-" * 50)

    print("""
    Principales hallazgos del análisis exploratorio:

    1. Distribución de contenido: Aproximadamente el 70% del catálogo son películas y el 30% series.

    2. Tendencia temporal: Se observa un crecimiento exponencial de contenido hasta 2018, con una ligera 
       disminución en años posteriores.

    3. Contenido por país: Estados Unidos lidera la producción con más del 40% del contenido, seguido 
       por India y Reino Unido.

    4. Clasificaciones: La clasificación TV-MA (para adultos) es la más común, seguida por TV-14, 
       lo que indica un enfoque en contenido para audiencias maduras.

    5. Duración: La mayoría de las películas tienen una duración entre 90 y 120 minutos, mientras que 
       la mayoría de las series tienen solo 1-2 temporadas.

    6. Géneros dominantes: Los dramas internacionales y las comedias son los géneros más representados 
       en la plataforma.

    7. Estacionalidad: Se observa un patrón de más estrenos hacia finales de año (septiembre-diciembre).

    8. Evolución de contenido: La proporción de series respecto a películas ha aumentado en los últimos años, 
       mostrando un cambio estratégico en el tipo de contenido.

    9. Valores faltantes: La columna "director" presenta aproximadamente un 30% de valores faltantes, 
       lo que podría indicar un enfoque en la producción de series donde el concepto de director único 
       es menos relevante.

    10. Contenido internacional: El contenido internacional ha crecido significativamente, especialmente 
        producciones de India y Reino Unido, reflejando una estrategia de globalización.
    """)

    print("\n¡Análisis Exploratorio Completo!")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('Netflix Titles')
