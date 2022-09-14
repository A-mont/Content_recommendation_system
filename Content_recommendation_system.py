# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 15:00:53 2021

@author: monte
"""


#Librería de manipulación del marco de datos
import pandas as pd
#Funciones matemáticas, necesitaremos la función sqrt para importar sólo lo necesario
from math import sqrt
import numpy as np
import matplotlib.pyplot as plt

#Ahora carguemos cada archivo en su propio marco de datos:


#Guardando la información de las películas dentro del marco de datos pandas
movies_df = pd.read_csv('movies.csv')
#Guardando la información del usuario dentro del marco de datos pandas
ratings_df = pd.read_csv('ratings.csv')
#Head es una función que obtiene los primeros N registros de un marco de datos. El valor por omision de N es 5.
movies_df.head()


#Utilizando expresiones regulares para encontrar un año guardado entre paréntesis
#Especificamos los paréntesis para no tener conflicto con las películas que tienen años como parte de su título
movies_df['year'] = movies_df.title.str.extract('(\(\d\d\d\d\))',expand=False)
#Eliminando los paréntesis
movies_df['year'] = movies_df.year.str.extract('(\d\d\d\d)',expand=False)
#Eliminando los años de la columna 'title'
movies_df['title'] = movies_df.title.str.replace('(\(\d\d\d\d\))', '')
#Aplicando la función strip para eliminar los caracteres blancos finales
movies_df['title'] = movies_df['title'].apply(lambda x: x.strip())
movies_df.head()

#Con ello, separemos los valores de la columna Genres y pongámoslo todos en list of Genres para simplificar una utilización que haremos después. Esto también se puede lograr la función split string de Python dentro de la columna que corresponde.


#Cada género está separado por un | para simplificar la llamada que se haga solo a |
movies_df['genres'] = movies_df.genres.str.split('|')
movies_df.head()



#Copiando el marco de datos de la pelicula en uno nuevo ya que no necesitamos la información del género por ahora.
moviesWithGenres_df = movies_df.copy()

#Para cada fila del marco de datos, iterar la lista de géneros y colocar un 1 en la columna que corresponda
for index, row in movies_df.iterrows():
    for genre in row['genres']:
        moviesWithGenres_df.at[index, genre] = 1
#Completar los valores NaN con 0 para mostrar que una película no tiene el género de la columna
moviesWithGenres_df = moviesWithGenres_df.fillna(0)
moviesWithGenres_df.head()



ratings_df.head()


#La sentencia Drop elimina la fila o columna señalada del marco de datos
ratings_df = ratings_df.drop('timestamp', 1)
ratings_df.head()




#Sistema de recomendación Basado en Contenido

userInput = [
            {'title':'Breakfast Club, The', 'rating':5},
            {'title':'Toy Story', 'rating':3.5},
            {'title':'Jumanji', 'rating':2},
            {'title':"Pulp Fiction", 'rating':5},
            {'title':'Akira', 'rating':4.5}
         ] 
inputMovies = pd.DataFrame(userInput)
inputMovies



#Filtrar las películas por título
inputId = movies_df[movies_df['title'].isin(inputMovies['title'].tolist())]
#Luego juntarlas para obtener el movieId. Implícitamente, lo está uniendo por título.
inputMovies = pd.merge(inputId, inputMovies)
#Eliminando información que no utilizaremos del dataframe de entrada
inputMovies = inputMovies.drop('genres', 1).drop('year', 1)
#Dataframe de entrada final
#Si una película que se agregó no se encuentra, entonces podría no estar en el dataframe 
#original o podría estar escrito de otra forma, por favor revisar mayúscula o minúscula.
inputMovies



#Descartando las películas de la entrada de datos
userMovies = moviesWithGenres_df[moviesWithGenres_df['movieId'].isin(inputMovies['movieId'].tolist())]
userMovies

#Inicializando el índice para evitar problemas a futuro
userMovies = userMovies.reset_index(drop=True)
#Eliminando problemas innecesarios para ahorrar memoria y evitar conflictos
userGenreTable = userMovies.drop('movieId', 1).drop('title', 1).drop('genres', 1).drop('year', 1)
userGenreTable

inputMovies['rating']


#Producto escalar para obtener los pesos
userProfile = userGenreTable.transpose().dot(inputMovies['rating'])
#Perfil del usuario
userProfile

#Ahora llevemos los géneros de cada película al marco de datos original
genreTable = moviesWithGenres_df.set_index(moviesWithGenres_df['movieId'])
#Y eliminemos información innecesaria
genreTable = genreTable.drop('movieId', 1).drop('title', 1).drop('genres', 1).drop('year', 1)
genreTable.head()

genreTable.shape


#Multiplicando los géneros por los pesos para luego calcular el peso promedio
recommendationTable_df = ((genreTable*userProfile).sum(axis=1))/(userProfile.sum())
recommendationTable_df.head()


#Ordena nuestra recomendación en orden descendente
recommendationTable_df = recommendationTable_df.sort_values(ascending=False)
#Miremos los valores
recommendationTable_df.head()


#Tabla de recomendaciones final
print(movies_df.loc[movies_df['movieId'].isin(recommendationTable_df.head(20).keys())])
