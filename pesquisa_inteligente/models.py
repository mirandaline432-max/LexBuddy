from database import db
from datetime import datetime

class ConsultaJuridica(db.Model):
    __tablename__ = 'consultas_juridicas'
    
    id = db.Column(db.Integer, primary_key=True)
    pergunta_advogado = db.Column(db.Text, nullable=False)
    data_consulta = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Resposta final fundamentada gerada pela IA
    resposta_copiloto = db.Column(db.Text, nullable=False)
    
    # Trecho exato da lei ou jurisprudência real que serviu de fonte (RAG)
    fonte_verificada = db.Column(db.Text, nullable=True)