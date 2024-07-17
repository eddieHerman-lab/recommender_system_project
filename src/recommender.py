import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import random

def calculate_similarity_matrices(rating_matrix, movies_df):
    vectorizer= CountVectorizer(tokenizer=lambda x: x.split())
    user_similarity = cosine_similarity(rating_matrix)
    item_features = vectorizer.fit_transform(movies_df['Genre']).toarray()
    content_similarity = cosine_similarity(item_features)
    return user_similarity, content_similarity



def recommend_items_collaborative(user_index, rating_matrix, user_similarity,top_n=30):
    user_ratings = rating_matrix[user_index]
    scores = user_similarity[user_index].dot(rating_matrix) / np.array([np.abs(user_similarity[user_index]).sum()])
    recommended_items = np.argsort(scores)[::-1]
    scores = np.nan_to_num(scores)  # Substituir NaNs por zeros
    recommended_items = np.argsort(scores)[::-1]

    return scores, recommended_items[:top_n]

def recommend_items_content(user_index, rating_matrix, content_similarity, top_n=30):
    user_ratings = rating_matrix[user_index, :]

    if content_similarity.shape[0] != rating_matrix.shape[1]:
        min_length = min(rating_matrix.shape[1],content_similarity.shape[0])
        content_similarity= content_similarity[:min_length, :min_length]
        rating_matrix= rating_matrix[:,:min_length]
        user_ratings = user_ratings[:min_length]

    print(f"user_ratings shape: {user_ratings.shape}")
    print(f"content_similarity shape: {content_similarity.shape}")


    scores = np.dot(content_similarity, user_ratings.T)  # Ajuste aqui
    scores = np.nan_to_num(scores)  # Substituir NaNs por zeros
    recommended_items = np.argsort(scores)[::-1]

    return scores, recommended_items[:top_n]


def recommend_items_hybrid(user_index, rating_matrix, user_similarity, content_similarity,alpha=0.5, top_n=30):
    collab_scores, _ = recommend_items_collaborative(user_index, rating_matrix, user_similarity,top_n)
    content_scores, _ = recommend_items_content(user_index, rating_matrix, content_similarity, top_n)

    hybrid_scores = alpha * collab_scores +(1-alpha) *content_scores
    recommended_items = np.argsort(hybrid_scores)[::-1]

    return hybrid_scores, recommended_items[:top_n]



def recommend_items_popularity(rating_matrix, top_n=30):
    item_popularity = np.sum(rating_matrix, axis=0)
    popular_items = np.argsort(item_popularity)[::-1]

    return item_popularity, popular_items[:top_n]



def get_movie_titles(movie_indices, movies_df):
    return movies_df.iloc[movie_indices]['Movie'].tolist()



def Show_history(user_index,rating_matrix,movies_df, min_watched=1,max_watched=30):
    # Número aleatório de filmes assistidos pelo usuário
    num_watched = random.randint(min_watched, max_watched)

    # Filmes aleatórios que o usuário assistiu (usando índices de filmes)
    watched_indices = random.sample(range(rating_matrix.shape[1]), num_watched)

    # Obtenha os títulos dos filmes assistidos pelo usuário
    watched_movies = movies_df.iloc[watched_indices]['Movie'].tolist()

    return watched_movies,watched_indices



