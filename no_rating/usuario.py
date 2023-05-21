from dataclasses import dataclass, field
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn import preprocessing
import pandas as pd

# import re
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

    def __post_init__(self):
        self.df_ratedmovies = pd.read_csv("data/user_ratedmovies.csv")
        self.df_ratedcountries = pd.read_csv("data/movie_countries.csv")
        self.df_ratedactors = pd.read_csv("data/movie_actors.csv")
        self.df_rateddirectores = pd.read_csv("data/movie_directors.csv")
        self.df_ratedgenres = pd.read_csv("data/movie_genres.csv")

        self.get_userMovies()
        self.get_top10Actors()
        self.get_top10Genres()
        self.get_top10Directors()
        self.get_top10Countries()
        self.get_arrayuser()

    def normalise(self, data):
        factor = 1.0 / math.fsum(data.values())

        for k in data:
            data[k] = data[k] * factor

        key_for_max = max(data.items(), key=itemgetter(1))[0]
        diff = 1.0 - math.fsum(data.values())
        print("discrepancy = " + str(diff))
        data[key_for_max] += diff

    def get_userMovies(self):
        cols = ["userID", "movieID", "rating"]

        df = self.df_ratedmovies.loc[(self.df_ratedmovies["userID"] == self.id)]

        for movie in df["movieID"]:
            rating = df.loc[(df["movieID"] == movie)]
            for rate in rating["rating"]:
                self.lista_filmes[movie] = rate

        for movieid, score in nlargest(
            10, self.lista_filmes.items(), key=itemgetter(1)
        ):
            self.lista_10filmes[movieid] = score

        # print(self.lista_10filmes)
        self.normalise(self.lista_10filmes)
        # print(self.lista_10filmes)
        # print(math.fsum(self.lista_10filmes.values()))

    def get_top10Actors(self):
        lista_ator = dict()
        for movie in self.lista_filmes:
            atores = self.df_ratedactors.loc[(self.df_ratedactors["movieID"] == movie)]

            for ator in atores["actorID"]:
                if ator not in lista_ator.keys():
                    lista_ator[ator] = 1
                #   print(f"adicionou a lista {ator}")

                else:
                    lista_ator[ator] += 1

        for actorid, score in nlargest(10, lista_ator.items(), key=itemgetter(1)):
            self.lista_10ator[actorid] = score

        self.normalise(self.lista_10ator)
        return self.lista_10ator

    def get_top10Genres(self):
        lista_genero = dict()

        for movie in self.lista_filmes:
            genres = self.df_ratedgenres.loc[(self.df_ratedgenres["movieID"] == movie)]

            for genre in genres["genre"]:
                if genre not in lista_genero.keys():
                    lista_genero[genre] = 1

                else:
                    lista_genero[genre] += 1

        for genre, score in nlargest(10, lista_genero.items(), key=itemgetter(1)):
            self.lista_10genero[genre] = score

        self.normalise(self.lista_10genero)
        return self.lista_genero

    def get_top10Directors(self):
        lista_diretor = dict()
        for movie in self.lista_filmes:
            directores = self.df_rateddirectores.loc[
                (self.df_rateddirectores["movieID"] == movie)
            ]

            for director in directores["directorID"]:
                if director not in lista_diretor.keys():
                    lista_diretor[director] = 1

                else:
                    lista_diretor[director] += 1

        for director, score in nlargest(10, lista_diretor.items(), key=itemgetter(1)):
            self.lista_10diretores[director] = score

        self.normalise(self.lista_10diretores)
        return self.lista_10diretores

    def get_top10Countries(self):
        lista_pais = dict()
        for movie in self.lista_filmes:
            countries = self.df_ratedcountries.loc[
                (self.df_ratedcountries["movieID"] == movie)
            ]

            for country in countries["country"]:
                if country not in lista_pais.keys():
                    lista_pais[country] = 1

                else:
                    lista_pais[country] += 1

        for country, score in nlargest(10, lista_pais.items(), key=itemgetter(1)):
            self.lista_10pais[country] = score

        self.normalise(self.lista_10pais)
        return self.lista_10pais

    def get_arrayuser(self):
        for movie in self.lista_filmes:
            genres = self.df_ratedgenres.loc[(self.df_ratedgenres["movieID"] == movie)]

            self.array_nota[movie] = {}
            for key in ["genre", "actor", "diretor", "pais"]:
                self.array_nota[movie][key] = 0

            for genre in genres["genre"]:
                if genre in self.lista_10genero.keys():
                    self.array_nota[movie]["genre"] += self.lista_10genero[genre]

            atores = self.df_ratedactors.loc[(self.df_ratedactors["movieID"] == movie)]

            for ator in atores["actorID"]:
                if ator in self.lista_10ator.keys():
                    self.array_nota[movie]["actor"] += self.lista_10ator[ator]

            diretores = self.df_rateddirectores.loc[
                (self.df_rateddirectores["movieID"] == movie)
            ]

            for diretor in diretores["directorID"]:
                if diretor in self.lista_10diretores.keys():
                    self.array_nota[movie]["diretor"] += self.lista_10diretores[diretor]

        # paises = self.df_ratedcountries.loc[(self.df_ratedcountries['movieID'] == movie)]

        # for pais in paises['country']:
        #     if pais in self.lista_10pais.keys():
        #         self.array_nota[movie]['pais'] += self.lista_10pais[pais]

        # print(self.array_nota)
        for movie in self.array_nota.keys():
            nota = 0
            for keys in self.array_nota[movie].keys():
                nota += self.array_nota[movie][keys]
            nota /= 4
            print(f"nota filme {movie} = {nota} ")
            print(self.array_nota[movie])

    #  Para cada usuário gerar um array
    #  filme, notagenero, notaator, notadiretor, notapais
