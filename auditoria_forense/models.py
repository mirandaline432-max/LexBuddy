from database import db
from datetime import datetime

class AnaliseForense(db.Model):
    __tablename__ = 'analises_forenses'
    
    id = db.Column(db.Integer, primary_key=True)
    nome_arquivo = db.Column(db.String(255), nullable=False)
    data_analise = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Armazena os dados técnicos extraídos do arquivo
    software_criador = db.Column(db.String(150), nullable=True)
    data_modificacao_oculta = db.Column(db.String(50), nullable=True)
    
    # Nível de alerta gerado automaticamente: 'seguro', 'suspeito' ou 'critico'
    status_risco = db.Column(db.String(20), nullable=False, default='seguro')
    detalhes_fraude = db.Column(db.Text, nullable=True)