import matplotlib.pyplot as plt
import streamlit as st
from  sklearn.manifold import TSNE
import numpy as np
import pandas as pd
import requests
import seaborn as sns
from src.recommender import (
    recommend_items_content,recommend_items_hybrid,recommend_items_popularity,
recommend_items_collaborative,get_movie_titles,calculate_similarity_matrices)
from src.data_loader import Load_and_pepare_data
from api.routes import api_routes

movies_path = r'/data/Movies.csv'
ratings_path = r'/data/Rating.csv'
genres_path = r'/data/Genre.csv'




def get_recommendations(user_index,rating_path,movies_path):
    # Calculando matrizes de similaridade
    user_similarity, content_similarity = calculate_similarity_matrices(rating_matrix, movies_df)


    _,recommended_items_collab = recommend_items_collaborative(user_index, rating_matrix, user_similarity)
    _,recommended_items_content = recommend_items_content(user_index, rating_matrix, content_similarity)
    _,recommended_items_hybrid = recommend_items_hybrid(user_index, rating_matrix, user_similarity, content_similarity)
    _,recommended_items_popularity = recommend_items_popularity(rating_matrix)


    recommendations = {
        'collab': recommended_items_collab,
        'content': recommended_items_content,
        'hybrid': recommended_items_hybrid,
        'popularity': recommended_items_popularity
    }

    return recommendations
# Plotagem simples de todas as recomendacoes com os filmes

#def plot_recommendation(ax, data, title,movies_df=None):
    #if isinstance(data, np.ndarray) and data.size > 0:# Verifica se data é um array não vazio
        #movie_titles = get_movie_titles(data, movies_df)
        #ax.barh(range(len(data)), np.ones(len(data)))  # Use uma lista de 1s para eixo y temporariamente
        #ax.set_yticks(range(len(data)))
        #ax.set_yticklabels(movie_titles)
        #ax.invert_yaxis() # Coloca o primeiro item no topo
        #ax.set_title(title)
    #else:
        #ax.text(0.5, 0.5, 'No Data', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
        #ax.set_title(title)




def plot_recommendations(recommendations, movies_df):
    fig, axs = plt.subplots(2, 2, figsize=(15, 10))
    plot_recommendation(axs[0, 0], recommendations.get('collab'), 'Collaborative Recommendations', movies_df)
    plot_recommendation(axs[0, 1], recommendations.get('content'), 'Content Recommendations', movies_df)
    plot_recommendation(axs[1, 0], recommendations.get('hybrid'), 'Hybrid Recommendations', movies_df)
    plot_recommendation(axs[1, 1], recommendations.get('popularity'), 'Popularity Recommendations', movies_df)
    plt.tight_layout()
    st.pyplot(fig)

# Interface do Streamlit
st.title('Movie Recommendation System')


# Função para plotar a similaridade dos usuários
def plot_user_Random_similarity(user_similarity):
    tsne = TSNE(n_components=2, perplexity=8, random_state=42)
    user_embeddings = tsne.fit_transform(user_similarity)

    plt.figure(figsize=(10, 8))
    plt.scatter(user_embeddings[:, 0], user_embeddings[:, 1])
    plt.title('User Similarity')
    plt.xlabel('Component 1')
    plt.ylabel('Component 2')
    plt.grid(True)
    st.pyplot(plt)

# Endpoint da API
api_url = 'http://127.0.0.1:5000'

# Carregar rating_matrix e movies_df usando funções do data_loader
movies_df, ratings_df = Load_and_pepare_data(movies_path, ratings_path, genres_path)
rating_matrix = ratings_df.pivot(index='UserId', columns='MovieID', values='Rating').fillna(0).values
# Selecionar o índice do usuário
def plot_user_similarity(user_index, rating_matrix, movies_df):
    user_similarity, _ = calculate_similarity_matrices(rating_matrix, movies_df)
    # Verifica se o user_index está dentro dos limites válidos
    if user_index >= user_similarity.shape[0]:
        st.error(f'Erro: O índice do usuário {user_index} está fora dos limites.')
        return

    # Defina o perplexity adequado aqui
    perplexity = min(5, user_similarity.shape[0] - 1)


    tsne = TSNE(n_components=2, perplexity=perplexity, random_state=42)
    user_embeddings = tsne.fit_transform(user_similarity) # Transforma para 2D

    plt.figure(figsize=(10, 8))
    plt.scatter(user_embeddings[:, 0], user_embeddings[:, 1])
    plt.title(f'User {user_index} Similarity')
    plt.xlabel('Component 1')
    plt.ylabel('Component 2')
    plt.grid(True)
    st.pyplot(plt)




def calculate_correlation(recommendations):
    df = pd.DataFrame(recommendations)
    correlation_matrix = df.corr()
    return correlation_matrix

def plot_correlation_heatmap(correlation_matrix):
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', ax=ax)
    ax.set_title('Correlation Between Recommendation Methods')
    st.pyplot(fig)

def get_recommendations_with_scores(user_index, rating_matrix, movies_df):
    user_similarity, content_similarity = calculate_similarity_matrices(rating_matrix, movies_df)

    _, recommended_items_collab = recommend_items_collaborative(user_index, rating_matrix, user_similarity)
    _, recommended_items_content = recommend_items_content(user_index, rating_matrix, content_similarity)
    _, recommended_items_hybrid = recommend_items_hybrid(user_index, rating_matrix, user_similarity, content_similarity)
    _, recommended_items_popularity = recommend_items_popularity(rating_matrix)


    # Exemplo de atribuição de pontuações fictícias
    recommendations = {
        'collab': {item: np.random.rand() for item in recommended_items_collab},
        'content': {item: np.random.rand() for item in recommended_items_content},
        'hybrid': {item: np.random.rand() for item in recommended_items_hybrid},
        'popularity': {item: np.random.rand() for item in recommended_items_popularity}
    }
    # Cria um DataFrame para facilitar o cálculo da correlação
    recommendations_df = pd.DataFrame.from_dict(recommendations, orient='index').transpose().dropna(axis=1, how='all')




    return recommendations_df

def plot_pie_recommendation(recommendations_df):
    if recommendations_df.empty:
        st.write("Não há dados suficientes para calcular a interseção das recomendações.")
        return


    intersection = set(recommendations_df.index)
    for column in recommendations_df.columns:
        column_indices = set(recommendations_df[column].dropna().index)
        intersection = set.intersection( column_indices)


    if len(recommendations_df.index) == 0:
        st.write("Não há dados suficientes no DataFrame para calcular a porcentagem.")
        return




    common_percentage = len(intersection) / len(recommendations_df.index) * 100
    # Plotar o gráfico de pizza
    labels = ['Presente em todas as recomendações', 'Não presente em todas as recomendações']
    sizes = [common_percentage, 100 - common_percentage]
    colors = ['#ff9999', '#66b3ff']
    explode = (0.1, 0)  # explode 1st slice
    fig,ax= plt.subplots()
    ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    ax.axis('equal')# Aspecto igual ao ratio que o grafico representa no circulo
    ax.set_title('Filmes Presentes em Todas as Recomendações')
    st.pyplot(fig)




def plot_recommendation_comparison(recommendations_df):
    correlation_matrix = calculate_correlation(recommendations_df)
    plot_correlation_heatmap(correlation_matrix)

# Inicializa o estado do Streamlit
if 'user_index' not in st.session_state:
    st.session_state.user_index = 0

# Atualiza o estado do índice do usuário
def update_user_index():
    st.session_state.user_index = st.session_state.user_input


max_user_index= rating_matrix.shape[0]-1

#Ajustar o valor user index para garantir que esteja dentro do limite do valor maximo

def validate_user_index():
    if st.session_state.user_index > max_user_index:
        st.session_state.user_index = max_user_index
validate_user_index()
user_input = st.number_input('Enter User Index', min_value=0,max_value=max_user_index, value=st.session_state.user_index, step=1, on_change=update_user_index, key='user_input')


st.sidebar.header('Entendendo Sistemas de Recomendacoes!')
st.sidebar.write("""
    Sistemas de Recomendação (SR) são conjuntos de algoritmos capazes analisar e identificar
    padrões de comportamento dos usuários de determinada plataforma, com objetivo de fornecer
    sugestões personalizadas, com base em seus interesses e histórico de navegação.
    Existem varios tipos de sistemas de recomendações dentre eles os mais comuns:
        
    **Colaborativo:** Baseado na similariedade dos usuarios.
    - **Contéudo:** Baseado em topicos de contéudo.
    - **Hibrido:** Baseado numa abordagem hibrida entre conteudo e colaborativo.
    - **Popularidade:** Baseado nos itens mais populares.
         
     """)
st.sidebar.write("Desenvolvido com [Streamlit](https://streamlit.io/)")
response = requests.get(f'{api_url}/recommend/{user_input}')
if response.status_code == 200:
    recommendations = response.json()
    st.write(recommendations)  # Verifique o conteúdo retornado
else:
    st.write("Failed to get recommendations")

if st.button('Plot Random User Similarity'):
           st.sidebar.header('Entendendo o Gráfico de Similaridade de Usuários')
           st.sidebar.write("""
           **Componentes 1 e 2:**
           No gráfico de dispersão gerado pelo t-SNE, os componentes 1 e 2 são as coordenadas das projeções dos usuários no plano 2D. Essas coordenadas são derivadas de uma transformação dos dados de similaridade original para um espaço bidimensional mais fácil de visualizar.

           **Interpretação:**
           - **Proximidade:** Usuários que estão próximos no gráfico têm perfis de avaliação mais semelhantes.
           - **Clusters:** Pode-se observar se há agrupamentos de usuários com preferências semelhantes para filmes.
           - **Dispersão:** Usuários dispersos indicam maior variabilidade nas preferências de filmes.
           """)
           st.sidebar.write("Desenvolvido com [Streamlit](https://streamlit.io/)")
           # Obter a matriz de similaridade dos usuários da API (substitua isso pela sua lógica)
           user_similarity = np.random.rand(20, 20)  # Exemplo de dados aleatórios
           plot_user_Random_similarity(user_similarity)
           plot_user_similarity(user_input, rating_matrix, movies_df)

if st.button('Recommendations Plotting'):
    recommendations = get_recommendations(user_input, rating_matrix, movies_df)
    #plot_recommendations(recommendations, movies_df)
    recommendations_df = get_recommendations_with_scores(user_input, rating_matrix, movies_df)
    #st.write(recommendations_df)  # Mostrar o DataFrame para verificação
    st.write("Recomendações carregadas com sucesso!.")
    plot_pie_recommendation(recommendations_df)


if st.button('Plot Correlation between Recommendations Methods:'):
    st.sidebar.header('Entendendo a Correlação entre Métodos de Recomendação')
    st.sidebar.write("""
    **Correlação entre Métodos de Recomendação:**
    A correlação entre diferentes métodos de recomendação indica como as recomendações feitas por cada método se relacionam. Se a correlação entre dois métodos é alta (próxima de 1), significa que eles tendem a recomendar itens semelhantes. Se a correlação é baixa (próxima de 0) ou negativa, significa que eles recomendam itens diferentes.


    **Interpretação do Heatmap de Correlação:**
    - **Cores Mais Escuras:** Alta correlação.
    - **Cores Mais Claras:** Baixa correlação.
    - **Anotações:** Os valores numéricos indicam o grau de correlação entre 0 e 1.
    """)


    recommendations_df = get_recommendations_with_scores(user_input, rating_matrix, movies_df)
    correlation_matrix = calculate_correlation(recommendations_df)
    plot_correlation_heatmap(correlation_matrix)

if __name__ == '__main__':
    st.write('STREAMLIT')