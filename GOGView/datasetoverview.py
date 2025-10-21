import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import ast

df = pd.read_csv('GOGView\data\gog_games_dataset.csv')

#Prints iniciais
#print(df.head())
#print(df.info())

#Filtros
df = df[df['type'].isin([1])]  # Manter apenas jogos
df = df[df['isInDevelopment'] == False]  # Remover jogos em desenvolvimento
df = df[df['isComingSoon'] == False]  # Remover jogos que ainda não foram lançados

#Derrubar colunas irrelevantes
df = df.drop(columns=['category','isComingSoon', 'availability','isInDevelopment','isDiscounted_main', 'type', 'isGame','isMod','supportUrl','releaseDate', 'gallery', 'video', 'isTBA', 'forumUrl', 'worksOn', 'originalCategory','isMovie', 'slug', 'isWishlistable','boxImage', 'promoId', 'filteredAvgRating', 'isReviewable', 'reviewPages', 'globalReleaseDate', 'dateReleaseDate'])

#Ajustar tipos de dados
df['dateGlobal'] = pd.to_datetime(df['dateGlobal'], errors='coerce')

#Adicionar colunas
df['YearGlobal'] = df['dateGlobal'].dt.year
df['MonthGlobal'] = df['dateGlobal'].dt.month

#Novas bases de dados
#Generos
df['genres'] = df['genres'].apply(ast.literal_eval)
all_genres = df['genres'].explode()
unique_genres = pd.Series(all_genres.unique())
#print(unique_genres.head())

#Sistemas operacionais
df['supportedOperatingSystems'] = df['supportedOperatingSystems'].apply(ast.literal_eval)
all_os = df['supportedOperatingSystems'].explode()
unique_os = pd.Series(all_os.unique())
#print(unique_os.head())

print(df.info())
print(df['salesVisibility'].unique())