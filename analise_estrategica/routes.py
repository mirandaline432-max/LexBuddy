from flask import Blueprint, render_template, request, redirect, url_for, flash
from database import db
from analise_estrategica.models import AnaliseContrato
from datetime import datetime, date

analise_bp = Blueprint('analise', __name__, url_prefix='/analise')

def simular_extracao_contrato():
    """Simula a extração de informações de um contrato de prestação de serviços via IA"""
    # Mapeia um prazo estipulado no documento fictício (ex: 20 de Outubro de 2026)
    prazo_extraido = date(2026, 10, 20)
    hoje = date.today()
    
    status = 'atrasado' if prazo_extraido < hoje else 'em_dia'
    
    return {
        'titulo': 'Contrato de Prestação de Serviços Tecnológicos.pdf',
        'riscos': 'Alerta de Risco: Cláusula 7ª estabelece multa rescisória abusiva de 50%, violando o limite de razoabilidade do Código Civil.',
        'prazo': prazo_extraido,
        'status': status
    }

@analise_bp.route('/contratos', methods=['GET', 'POST'])
def analisar_contrato():
    if request.method == 'POST':
        titulo = request.form.get('titulo_documento') or 'Contrato Desconhecido'
        
        # Executa o motor de inteligência artificial de extração
        dados = simular_extracao_contrato()
        
        # Salva o relatório estratégico no SQLite unificado
        nova_analise = AnaliseContrato(
            titulo_contrato=dados['titulo'],
            riscos_detectados=dados['riscos'],
            prazo_critico=dados['prazo'],
            status_prazo=dados['status']
        )
        db.session.add(nova_analise)
        db.session.commit()
        
        flash('Contrato interpretado e prazos mapeados!', 'success')
        return render_template('analise/contratos.html', contrato=nova_analise)
        
    return render_template('analise/contratos.html', contrato=None)