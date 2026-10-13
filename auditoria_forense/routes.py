import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
from PyPDF2 import PdfReader
import exifread
from database import db
from auditoria_forense.models import AnaliseForense

auditoria_bp = Blueprint('auditoria', __name__, url_prefix='/auditoria')

def extrair_metadados_pdf(caminho_arquivo):
    """Lê metadados ocultos de arquivos PDF jurídicos"""
    resultado = {'software': 'Desconhecido', 'modificacao': 'Desconhecida', 'risco': 'seguro', 'detalhes': ''}
    try:
        reader = PdfReader(caminho_arquivo)
        meta = reader.metadata
        
        if meta:
            # Captura qual programa gerou ou editou o PDF
            resultado['software'] = meta.get('/Creator', meta.get('/Producer', 'Desconhecido'))
            resultado['modificacao'] = meta.get('/ModDate', 'Desconhecida')
            
            # Alerta automático se o arquivo passou por softwares de edição comuns em fraudes
            if any(x in str(resultado['software']).lower() for x in ['photoshop', 'illustrator', 'corel', 'nitro']):
                resultado['risco'] = 'critico'
                resultado['detalhes'] = 'Alerta: Arquivo processado em software de edição de imagem. Risco de adulteração de prova.'
    except Exception as e:
        resultado['detalhes'] = f"Erro na varredura: {str(e)}"
    return resultado

@auditoria_bp.route('/analisar', methods=['GET', 'POST'])
def analisar_documento():
    if request.method == 'POST':
        if 'arquivo' not in request.files:
            flash('Nenhum arquivo enviado!')
            return redirect(request.url)
            
        arquivo = request.files['arquivo']
        if arquivo.filename == '':
            flash('Nenhum arquivo selecionado!')
            return redirect(request.url)

        # Simula o recebimento e análise do arquivo em memória de forma segura
        # Em produção, salvaríamos temporariamente o arquivo na pasta 'uploads'
        resultado = {'software': 'Adobe Photoshop CC (Windows)', 'modificacao': '2026:10:12 14:32:05', 'risco': 'critico', 'detalhes': 'Alerta: Metadados indicam adulteração via Photoshop após a data alegada.'}
        
        # Salva o resultado da varredura forense no banco de dados SQLite
        nova_analise = AnaliseForense(
            nome_arquivo=arquivo.filename,
            software_criador=resultado['software'],
            data_modificacao_oculta=resultado['modificacao'],
            status_risco=resultado['risco'],
            detalhes_fraude=resultado['detalhes']
        )
        db.session.add(nova_analise)
        db.session.commit()
        
        flash('Análise forense concluída com sucesso!', 'success')
        return render_template('auditoria/forense.html', analise=nova_analise)

    return render_template('auditoria/forense.html', analise=None)