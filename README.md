# Recommender System Project


Este projeto implementa um sistema de recomendação utilizando várias abordagens, incluindo recomendações colaborativas simples, baseadas em conteúdo, híbridas e de popularidade. O sistema foi desenvolvido utilizando Python, Flask e Streamlit.

## Funcionalidades

- **Recomendações Colaborativas**: Baseadas nas preferências de usuários similares.
- **Recomendações Baseadas em Conteúdo**: Utilizam as características dos itens para fazer recomendações.
- **Recomendações Híbridas**: Combinação das abordagens colaborativa e baseada em conteúdo.
- **Recomendações de Popularidade**: Itens mais populares são recomendados.
- **Visualizações**: Gráficos que ajudam a entender melhor as recomendações.



## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/recommender_system_project.git
   cd recommender_system_project
## Ambiente virtual

python3 -m venv venv
source venv/bin/activate

# Dependencias
pip install -r requirements.txt

## Execução
## API
Inicie a API Flask:
python run_api.py
A API estará disponível em http://127.0.0.1:5000/.

## Interface Streamlit
Execute a aplicação Streamlit:
streamlit run src/visualizations/app.py

## Estrutura do Projeto
recommender_system_project/
│
├── api/
│    └── init.py 
|    └── routes.py
│
|
├── data/
│ └── Genre.csv
│ └── Movies.csv
│ └── Rating.csv
├── recommender_system_project.egg-info/
                                      └── dependency_links.txt
                                      └── entry_points
                                      └── PKG_INFO
                                      └── requires.txt
                                      └── SOURCES.txt
                                      └── top_leves.txt
├── src/
│ └── visulaizations/
                    └── init.py
                    └── app.py
                    └──visualization
│ └── data_loader
│ └── recommender
│
├── tests/
│ └── init.py
│ └── test_recommender.py
│
├── init.py
├── create_app
├── README.md
├── requirements.txt
└── run.api.py
└── setup.py

## Contribuições
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.

# Licença
Este projeto está licenciado sob a Licença MIT.


# Com essa estrutura, qualquer pessoa interessada no projeto terá todas as informações necessárias para instalá-lo, configurá-lo e executá-lo corretamente. Além disso, eles terão um entendimento claro da estrutura do projeto e de como contribuir.
