import os

class Config:
    # Chave de segurança para controle de sessões de usuários no Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'lexbuddy-chave-secreta-super-protegida-123'
    
    # Configuração do caminho do banco de dados SQLite local
    SQLALCHEMY_DATABASE_URI = 'sqlite:///lexbuddy.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Espaço reservado para a chave da IA (OpenAI / Groq)
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY') or 'sua-chave-api-aqui'