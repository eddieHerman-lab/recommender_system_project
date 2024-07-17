from setuptools import setup, find_packages

setup(
    name='recommender_system_project',  # Nome do pacote
    version='0.1.0',  # Versão do pacote
    packages=find_packages(where='src'),  # Inclui todos os pacotes encontrados automaticamente
    package_dir={'':'src'},
    install_requires=[  # Dependências necessárias
        'numpy',
        'matplotlib',
        'scikit-learn',
        'pandas',
        'flask',
        'streamlit',
        'pytest'
    ],
    entry_points={  # Pontos de entrada para scripts de console
        'console_scripts': [
            'recommender_system_project=app:main',
        ],
    },
    author='Eduardo Hermanson',  # Seu nome como autor do pacote
    author_email='eduardowhermanson@gmail.com',  # Seu email
    description='Projeto de Sistema de Recomendação',  # Breve descrição do projeto
    long_description=open('README.md').read(),  # Descrição longa do README.md
    long_description_content_type='text/markdown',  # Tipo de conteúdo do README
    url='https://github.com/seu_usuario/recommender_system_project',  # URL do repositório GitHub
    classifiers=[  # Classificações do pacote
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7'
)
