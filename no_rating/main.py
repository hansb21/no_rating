from dataclasses import dataclass
import numpy as np
import pandas as pd 

@dataclass
class usuario:
    """description"""
    id: int
    lista_ator: list[tuple]
    lista_genero: list[tuple]
    total_genero: int = 0

df_topex = pd.read_csv('data/ratings.csv') 
df_movies = pd.read_csv('data/movies.xls')
#print(df_topex['item id'])
user = dict()

def getWatched(userId):
    filmes = {userId: list()}
    for movie in df_topex['movieId'].where(df_topex['userId'] == userId).dropna():
        filmes[userId].append(movie)

    return filmes
def getMovieGenre(movieId):

    genres = {movieId: list()}
    movies = df_movies['genres'].where(df_movies['movieId'] == movieId).dropna()
    for k in movies:
        for genre in k.split("|"):
            genres[movieId].append(genre) 
            print(genres)
                #print(filmes[i][j])
    return genres 
def getUserGenres(userId):
    total = 0
    userGenres = {userId: dict()}
    filmes = getWatched((userId))
    for movie in filmes[userId]:
        genres = getMovieGenre(movie)
        for genre in genres[movie]:
            if genre not in userGenres[userId]:
                total += 1
                print(f" adicionou genero = {genre} ")
                userGenres[userId][genre] = 1 
            else:
                userGenres[userId][genre] += 1 

    return userGenres, total 

#print(user[42])
usergenre, total_genero = getUserGenres((42))
norm = 0
nota = 0
rate = getMovieGenre((165)) #df_movies['genres'].where(df_movies['movieId'] == '110').dropna()

for genres in usergenre[42].keys():
    print(genres)
    for rating in rate.values():
        print(f"={rating}")
        print(f"genres = {genres}")
        print(nota)
        if genres in rating:
            print("estava em rating")
            print(f"={usergenre[42][genres]}/{total_genero}")
            norm += usergenre[42][genres]/total_genero
            nota += usergenre[42][genres]/total_genero
print(f"nota = {nota}")
nota = nota / 2
nota = nota * 4 
print(f"nota = {nota}")
nota += 1 

print(f"nota = {nota}")
print(f"norm = {norm}")
