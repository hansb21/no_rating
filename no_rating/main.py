from dataclasses import dataclass, field 
import numpy as np
import pandas as pd 
#import re 
from heapq import nlargest
from operator import itemgetter
import math


@dataclass
class usuario:
    """description"""
    id: int
    lista_filmes: dict = field(default_factory=dict)
    lista_10filmes: dict = field(default_factory=dict)
    lista_ator: dict = field(default_factory=dict)
    lista_10ator: dict = field(default_factory=dict)
    lista_genero: dict = field(default_factory=dict)
    lista_10genero: dict = field(default_factory=dict)
    lista_diretor: dict = field(default_factory=dict)
    lista_10diretores: dict = field(default_factory=dict)
    lista_pais: dict = field(default_factory=dict)
    lista_10pais: dict = field(default_factory=dict)

    ano: int = 0000
    total_genero: int = 0
    
    def normalise(self, data):
        factor = 1.0 / math.fsum(data.values())
        
        for k in data:
            data[k] = data[k] * factor 

        key_for_max = max(data.items(), key=itemgetter(1))[0]
        diff = 1.0 - math.fsum(data.values())
        print("discrepancy = " + str(diff))
        data[key_for_max] += diff 

    def get_userMovies(self):
        cols = ['userID', 'movieID', 'rating']
        df_ratedmovies = pd.read_csv('data/user_ratedmovies.csv')

        df = df_ratedmovies.loc[(df_ratedmovies['userID'] == self.id)]
        
        for movie in df['movieID']:
           rating = df.loc[(df['movieID'] == movie)]
           for rate in (rating['rating']):
                    self.lista_filmes[movie] = rate

        for movieid, score in nlargest(10, self.lista_filmes.items(), key=itemgetter(1)):
           self.lista_10filmes[movieid] = score
        
        print(self.lista_10filmes)
        self.normalise(self.lista_10filmes)
        print(self.lista_10filmes)
        print(math.fsum(self.lista_10filmes.values()))

    def get_top10Actors(self):
        df_ratedactors = pd.read_csv('data/movie_actors.csv')
        for movie in self.lista_filmes:
            atores = df_ratedactors.loc[(df_ratedactors['movieID'] == movie)]
            
            for ator in atores['actorID']:

                if ator not in self.lista_ator.keys():
                    self.lista_ator[ator] = 1
                 #   print(f"adicionou a lista {ator}")
    
                else: 
                    self.lista_ator[ator] += 1

        for actorid, score in nlargest(10, self.lista_ator.items(), key=itemgetter(1)):
                   self.lista_10ator[actorid] = score
        
        print(self.lista_10ator)
        self.normalise(self.lista_10ator)
        print(self.lista_10ator)
        print(math.fsum(self.lista_10ator.values()))
        return self.lista_10ator

    def get_top10Genres(self):
        df_ratedgenres = pd.read_csv('data/movie_genres.csv')
        for movie in self.lista_filmes:
            genres = df_ratedgenres.loc[(df_ratedgenres['movieID'] == movie)]
            
            for genre in genres['genre']:

                if genre not in self.lista_genero.keys():
                    self.lista_genero[genre] = 1
    
                else: 
                    self.lista_genero[genre] += 1

        for genre, score in nlargest(10, self.lista_genero.items(), key=itemgetter(1)):
                   self.lista_10genero[genre] = score
        
        print(self.lista_10genero)
        self.normalise(self.lista_10genero)
        print(self.lista_10genero)
        print(math.fsum(self.lista_10genero.values()))
        return self.lista_genero

    def get_top10Directors(self):
        df_rateddirectores = pd.read_csv('data/movie_directors.csv')
        for movie in self.lista_filmes:
            directores = df_rateddirectores.loc[(df_rateddirectores['movieID'] == movie)]
            
            for director in directores['directorID']:

                if director not in self.lista_diretor.keys():
                    self.lista_diretor[director] = 1
    
                else: 
                    self.lista_diretor[director] += 1

        for director, score in nlargest(10, self.lista_diretor.items(), key=itemgetter(1)):
                   self.lista_10diretores[director] = score
        print(self.lista_10diretores)
        self.normalise(self.lista_10diretores)
        print(self.lista_10diretores)
        print(math.fsum(self.lista_10diretores.values()))
        return self.lista_10diretores 
  
    def get_top10Countries(self):
        df_ratedcountries = pd.read_csv('data/movie_countries.csv')
        for movie in self.lista_filmes:
            countries = df_ratedcountries.loc[(df_ratedcountries['movieID'] == movie)]
            
            for country in countries['country']:

                if country not in self.lista_pais.keys():
                    self.lista_pais[country] = 1
    
                else: 
                    self.lista_pais[country] += 1

        for country, score in nlargest(10, self.lista_pais.items(), key=itemgetter(1)):
                   self.lista_10pais[country] = score
        print(self.lista_10pais)
        self.normalise(self.lista_10pais)
        print(self.lista_10pais)
        print(math.fsum(self.lista_10pais.values()))
        return self.lista_10pais

    def get_topYear(self):
        return self.ano 

    
    def get_arrayuser(self):
        for movie in self.lista_filmes:
            pass 
        
     #  Para cada usuário gerar um array
     #  filme, notagenero, notaator, notadiretor, notapais

user = usuario(id=int(input("entre id: ")))
user.get_userMovies()
user.get_top10Actors()
user.get_top10Genres()
user.get_top10Directors()
user.get_top10Countries()

