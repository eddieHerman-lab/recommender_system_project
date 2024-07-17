import pytest
import pandas as pd
import numpy as np
from src.recommender import (
    recommend_items_content, recommend_items_hybrid, recommend_items_popularity,
    recommend_items_collaborative, calculate_similarity_matrices
)
from src.data_loader import Load_and_pepare_data

# Caminhos dos arquivos
movies_path = r'/data/Movies.csv'
ratings_path = r'/data/Rating.csv'
genres_path = r'/data/Genre.csv'

# Carregar dados uma vez para os testes
movies_df, ratings_df = Load_and_pepare_data(movies_path, ratings_path, genres_path)
rating_matrix = ratings_df.pivot(index='UserId', columns='MovieID', values='Rating').fillna(0).values

@pytest.fixture
def user_index():
    return 0  # ou qualquer outro índice válido para testes

def test_calculate_similarity_matrices():
    user_similarity, content_similarity = calculate_similarity_matrices(rating_matrix, movies_df)
    assert user_similarity.shape == (rating_matrix.shape[0], rating_matrix.shape[0])
    assert content_similarity.shape == (movies_df.shape[0], movies_df.shape[0])

def test_recommend_items_collaborative(user_index):
    user_similarity, _ = calculate_similarity_matrices(rating_matrix, movies_df)
    scores, recommended_items = recommend_items_collaborative(user_index, rating_matrix, user_similarity)
    assert len(recommended_items) > 0

def test_recommend_items_content(user_index):
    _, content_similarity = calculate_similarity_matrices(rating_matrix, movies_df)
    scores, recommended_items = recommend_items_content(user_index, rating_matrix, content_similarity)
    assert len(recommended_items) > 0

def test_recommend_items_hybrid(user_index):
    user_similarity, content_similarity = calculate_similarity_matrices(rating_matrix, movies_df)
    scores, recommended_items = recommend_items_hybrid(user_index, rating_matrix, user_similarity, content_similarity)
    assert len(recommended_items) > 0

def test_recommend_items_popularity():
    scores, recommended_items = recommend_items_popularity(rating_matrix)
    assert len(recommended_items) > 0

if __name__ == "__main__":
    pytest.main()
