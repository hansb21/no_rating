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
    lista_10filmes: dict = field(default_factory=dict)
    lista_10ator: dict = field(default_factory=dict)
    lista_10genero: dict = field(default_factory=dict)
    lista_10diretores: dict = field(default_factory=dict)
    lista_10pais: dict = field(default_factory=dict)
    
    #!TODO remove this, turn into a local variable in every function
    lista_filmes: dict = field(default_factory=dict)
    lista_ator: dict = field(default_factory=dict)
    lista_genero: dict = field(default_factory=dict)
    lista_diretor: dict = field(default_factory=dict)
    lista_pais: dict = field(default_factory=dict)
    array_nota: dict = field(default_factory=dict)

    ano: int = 0000
    total_genero: int = 0
    
    df_ratedmovies = pd.read_csv('data/user_ratedmovies.csv')
    df_ratedcountries = pd.read_csv('data/movie_countries.csv')
    df_ratedactors = pd.read_csv('data/movie_actors.csv')
    df_rateddirectores = pd.read_csv('data/movie_directors.csv')
    df_ratedgenres = pd.read_csv('data/movie_genres.csv')
    
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

        df = self.df_ratedmovies.loc[(self.df_ratedmovies['userID'] == self.id)]
        
        for movie in df['movieID']:
           rating = df.loc[(df['movieID'] == movie)]
           for rate in (rating['rating']):
                    self.lista_filmes[movie] = rate

        for movieid, score in nlargest(10, self.lista_filmes.items(), key=itemgetter(1)):
           self.lista_10filmes[movieid] = score
        
        #print(self.lista_10filmes)
        self.normalise(self.lista_10filmes)
        #print(self.lista_10filmes)
        #print(math.fsum(self.lista_10filmes.values()))

    def get_top10Actors(self):
        for movie in self.lista_filmes:
            atores = self.df_ratedactors.loc[(self.df_ratedactors['movieID'] == movie)]
            
            for ator in atores['actorID']:

                if ator not in self.lista_ator.keys():
                    self.lista_ator[ator] = 1
                 #   print(f"adicionou a lista {ator}")
    
                else: 
                    self.lista_ator[ator] += 1

        for actorid, score in nlargest(10, self.lista_ator.items(), key=itemgetter(1)):
                   self.lista_10ator[actorid] = score
        
        #print(self.lista_10ator)
        self.normalise(self.lista_10ator)
        #print(self.lista_10ator)
        #print(math.fsum(self.lista_10ator.values()))
        return self.lista_10ator

    def get_top10Genres(self):
        for movie in self.lista_filmes:
            genres = self.df_ratedgenres.loc[(self.df_ratedgenres['movieID'] == movie)]
            
            for genre in genres['genre']:

                if genre not in self.lista_genero.keys():
                    self.lista_genero[genre] = 1
    
                else: 
                    self.lista_genero[genre] += 1

        for genre, score in nlargest(10, self.lista_genero.items(), key=itemgetter(1)):
                   self.lista_10genero[genre] = score
        
        #print(self.lista_10genero)
        self.normalise(self.lista_10genero)
        #print(self.lista_10genero)
        #print(math.fsum(self.lista_10genero.values()))
        return self.lista_genero

    def get_top10Directors(self):
        for movie in self.lista_filmes:
            directores = self.df_rateddirectores.loc[(self.df_rateddirectores['movieID'] == movie)]
            
            for director in directores['directorID']:

                if director not in self.lista_diretor.keys():
                    self.lista_diretor[director] = 1
    
                else: 
                    self.lista_diretor[director] += 1

        for director, score in nlargest(10, self.lista_diretor.items(), key=itemgetter(1)):
                   self.lista_10diretores[director] = score
        #print(self.lista_10diretores)
        self.normalise(self.lista_10diretores)
        #print(self.lista_10diretores)
        #print(math.fsum(self.lista_10diretores.values()))
        return self.lista_10diretores 
  
    def get_top10Countries(self):
        for movie in self.lista_filmes:
            countries = self.df_ratedcountries.loc[(self.df_ratedcountries['movieID'] == movie)]
            
            for country in countries['country']:

                if country not in self.lista_pais.keys():
                    self.lista_pais[country] = 1
    
                else: 
                    self.lista_pais[country] += 1

        for country, score in nlargest(10, self.lista_pais.items(), key=itemgetter(1)):
                   self.lista_10pais[country] = score
       # print(self.lista_10pais)
        self.normalise(self.lista_10pais)
       # print(self.lista_10pais)
       # print(math.fsum(self.lista_10pais.values()))
        return self.lista_10pais

    def get_topYear(self):
        return self.ano 
    
    def get_arrayuser(self):
        for movie in self.lista_filmes:
            self.array_nota[movie] = {}
            genres = self.df_ratedgenres.loc[(self.df_ratedgenres['movieID'] == movie)] 
            
            self.array_nota[movie]['genre'] = 0
            self.array_nota[movie]['actor'] = 0
            self.array_nota[movie]['diretor'] = 0
            self.array_nota[movie]['pais'] = 0
            for genre in genres['genre']:
                if genre in self.lista_10genero.keys():
                    self.array_nota[movie]['genre'] += self.lista_10genero[genre]

            atores = self.df_ratedactors.loc[(self.df_ratedactors['movieID'] == movie)]
            
            for ator in atores['actorID']:
                if ator in self.lista_10ator.keys():
                    self.array_nota[movie]['actor'] += self.lista_10ator[ator]

            diretores = self.df_rateddirectores.loc[(self.df_rateddirectores['movieID'] == movie)]

            for diretor in diretores['directorID']:
                if diretor in self.lista_10diretores.keys():
                    self.array_nota[movie]['diretor'] += self.lista_10diretores[diretor]

            paises = self.df_ratedcountries.loc[(self.df_ratedcountries['movieID'] == movie)]

            for pais in paises['country']:
                if pais in self.lista_10pais.keys():
                    self.array_nota[movie]['pais'] += self.lista_10pais[pais]

        #print(self.array_nota)
        for movie in self.array_nota.keys():
            nota = 0
            for keys in self.array_nota[movie].keys():
                nota += self.array_nota[movie][keys]
            print(f"nota filme = {nota} ")
     #  Para cada usuário gerar um array
     #  filme, notagenero, notaator, notadiretor, notapais

user = usuario(id=int(input("entre id: ")))
user.get_userMovies()
user.get_top10Actors()
user.get_top10Genres()
user.get_top10Directors()
user.get_top10Countries()
user.get_arrayuser()

