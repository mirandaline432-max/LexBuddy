from flask_sqlalchemy import SQLAlchemy

# Cria a instância centralizada do banco de dados
db = SQLAlchemy()

def inicializar_banco(app):
    """Inicializa o banco de dados e cria as tabelas automaticamente"""
    db.init_app(app)
    with app.app_context():
        db.create_all()