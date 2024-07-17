from flask import Blueprint, jsonify, request
import matplotlib.pyplot as plt
from src.data_loader import Load_and_pepare_data

from src.recommender import (
calculate_similarity_matrices, recommend_items_collaborative,
recommend_items_content,recommend_items_hybrid,recommend_items_popularity,Show_history,get_movie_titles
)
import pandas as pd
import numpy as np

api_routes = Blueprint('api_routes', __name__)

# Definir os caminhos para os arquivos CSV
movies_path = r'/data/Movies.csv'
ratings_path = r'/data/Rating.csv'
genres_path = r'/data/Genre.csv'
# Carregar e preparar dados reais
movies_df, ratings_df = Load_and_pepare_data(movies_path, ratings_path,genres_path)

# Verificar se a coluna rating esta presente
if 'Rating' in ratings_df.columns:
    # Verificar e tratar valores NaN na coluna de ratings
    if ratings_df['Rating'].isnull().sum() > 0:
        # Preencher NaN com a média dos ratings
        ratings_df['Rating'].fillna(ratings_df['Rating'].mean(), inplace=True)
        ratings_df.rename(columns={'movieId': 'MovieID'},inplace=True)
    rating_matrix = ratings_df.pivot_table(index='UserId', columns='MovieID',values='Rating',aggfunc='mean').fillna(0).values
else:
    raise ValueError("Nenhuma coluna de 'Rating  encontrada no DataFrame de ratings.")
user_similarity, content_similarity= calculate_similarity_matrices(rating_matrix, movies_df)

def create_rating_matrix(ratings_df):
    n_users = ratings_df['userId'].max() + 1
    n_movies = ratings_df['movieId'].max() + 1
    rating_matrix = np.zeros((n_users, n_movies))
    for row in ratings_df.itertuples():
        rating_matrix[row.userId, row.movieId] = row.rating
    return rating_matrix

def get_recommendations(user_index):
    # Recomendação para o usuário de índice user_index
    collab_scores, recommended_items_collab = recommend_items_collaborative(user_index, rating_matrix, user_similarity)
    popularity_scores, recommended_items_popularity = recommend_items_popularity(rating_matrix)
    content_scores, recommended_items_content = recommend_items_content(user_index, rating_matrix, content_similarity)
    hybrid_scores, recommended_items_hybrid = recommend_items_hybrid(user_index, rating_matrix, user_similarity, content_similarity)



    recommended_items_collab = [item for item in recommended_items_collab if item not in history_indices]
    recommended_items_content = [item for item in recommended_items_content if item not in history_indices]
    recommended_items_hybrid = [item for item in recommended_items_hybrid if item not in history_indices]
    recommended_items_popularity = [item for item in recommended_items_popularity if item not in history_indices]


    recommendations = {
        'collab': recommended_items_collab,
        'content': recommended_items_cntent ,
        'hybrid': recommended_items_hybrid,
        'popularity': recommended_items_popularity
    }
    #Retornar recommendations para uso do Streamlit posteriormente

    return recommendations

@api_routes.route('/recommend/<int:user_index>', methods=['GET'])
def recommend(user_index):
    user_history,history_indices = Show_history(user_index, rating_matrix, movies_df)
    # Recomendação para o usuário de índice user_index
    collab_scores, recommended_items_collab = recommend_items_collaborative(user_index, rating_matrix, user_similarity)
    popularity_scores, recommended_items_popularity = recommend_items_popularity(rating_matrix)
    content_scores, recommended_items_content = recommend_items_content(user_index, rating_matrix, content_similarity)
    hybrid_scores, recommended_items_hybrid = recommend_items_hybrid(user_index, rating_matrix, user_similarity,content_similarity)



    recommended_items_collab = [item for item in recommended_items_collab if item not in history_indices]
    recommended_items_content = [item for item in recommended_items_content if item not in history_indices]
    recommended_items_hybrid = [item for item in recommended_items_hybrid if item not in history_indices]
    recommended_items_popularity = [item for item in recommended_items_popularity if item not in history_indices]



    #Buscar os filmes recomendados
    collab_titles = get_movie_titles(recommended_items_collab, movies_df)
    content_titles = get_movie_titles(recommended_items_content, movies_df)
    hybrid_titles = get_movie_titles(recommended_items_hybrid, movies_df)
    popularity_titles = get_movie_titles(recommended_items_popularity, movies_df)

    user_titles =user_history

    # Imprimir recomendações colaborativas e populares
    response = {
        'Collaborative Recommendations':   collab_titles,
        'Popularity-based Recommendations':  popularity_titles,
        'Content Recommendations':  content_titles,
        'Hibrid Recommendations':   hybrid_titles,
        'User History':        user_titles,


    }

    return jsonify(response)



