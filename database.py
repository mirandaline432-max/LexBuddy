from flask_sqlalchemy import SQLAlchemy
import chromadb
import os

# 1. Banco de Dados Relacional (SQLite) para Usuários e Logs
db = SQLAlchemy()

# 2. Banco de Dados Vetorial (ChromaDB) para Documentos Jurídicos
# Define o caminho de salvamento dentro da pasta padrão 'instance' do Flask
caminho_vetorial = os.path.join(os.path.dirname(__file__), 'instance', 'chroma_db')
chroma_client = chromadb.PersistentClient(path=caminho_vetorial)

def inicializar_banco(app):
    """Inicializa os bancos de dados do LexBuddy"""
    # Inicializa o SQLite
    db.init_app(app)
    with app.app_context():
        db.create_all()
        
    # Inicializa e garante a existência da coleção jurídica no ChromaDB
    # Essa instância 'base_juridica' será importada pelas suas rotas de pesquisa
    app.config['CHROMA_COLLECTION'] = chroma_client.get_or_create_collection(name="base_juridica_fechada")
