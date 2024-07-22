import pandas as pd
import numpy as np
from src import recommender

movies_path= r'/data/Movies.csv'
rating_path= r'/data/Rating.csv'
genres_path = r'/data/Genre.csv'
def Load_and_pepare_data(movies_path, ratings_path,genres_path):

    movies_df= pd.read_csv(movies_path)
    ratings_df = pd.read_csv(ratings_path)
    genres_df=pd.read_csv(genres_path)

    movies_df=pd.concat([movies_df,genres_df],axis=1)

    movies_df['Genre'].fillna('Unknow', inplace=True)
    movies_df['Genre'] = movies_df['Genre'].apply(lambda x: 'Unknown' if x.strip() == '' else x)
    num_users = 500 # Definicao de usuarios ficticios
    ratings_df['UserId']=np.random.randint(0, num_users, ratings_df.shape[0])
    movies_df['Genre']= movies_df['Genre'].str.replace('','Unknow')

    # Atribuir um identificador único para cada filme
    ratings_df['MovieID'] = range(1, ratings_df.shape[0] + 1)  # Cria IDs únicos para cada filme
    # Verificar as primeiras linhas dos DataFrames para garantir que as colunas estão corretas


    return  movies_df, ratings_df

