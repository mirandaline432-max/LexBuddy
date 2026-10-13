from database import db
from datetime import datetime

class AnaliseContrato(db.Model):
    __tablename__ = 'analises_contratos'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo_contrato = db.Column(db.String(150), nullable=False)
    data_analise = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Resumo das cláusulas abusivas ou brechas identificadas
    riscos_detectados = db.Column(db.Text, nullable=True)
    
    # Prazo crítico identificado no contrato que o advogado precisa cumprir
    prazo_critico = db.Column(db.Date, nullable=True)
    status_prazo = db.Column(db.String(20), nullable=False, default='em_dia') # em_dia ou atrasado
