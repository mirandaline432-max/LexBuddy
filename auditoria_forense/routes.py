from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
import google.generativeai as genai
import os
import pypdf

auditoria_bp = Blueprint('auditoria', __name__, url_prefix='/auditoria')

# Configura a IA utilizando a variável de ambiente que já definimos no Ubuntu
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def extrair_texto_pdf(arquivo_storage):
    """Extrai texto do arquivo PDF enviado via formulário"""
    texto = ""
    try:
        leitor = pypdf.PdfReader(arquivo_storage)
        for pagina in leitor.pages:
            texto += pagina.extract_text() + "\n"
    except Exception as e:
        print(f"Erro ao ler PDF na auditoria: {e}")
    return texto.strip()

@auditoria_bp.route('/analisar', methods=['GET', 'POST'])
def analisar_fraude():
    if request.method == 'POST':
        # 1. Captura o arquivo ou o texto colado enviado pelo usuário
        arquivo = request.files.get('documento')
        texto_inserido = request.form.get('texto_processo', '')
        
        texto_para_auditoria = ""
        
        if arquivo and arquivo.filename.endswith('.pdf'):
            texto_para_auditoria = extrair_texto_pdf(arquivo)
        else:
            texto_para_auditoria = texto_inserido

        if not texto_para_auditoria or len(texto_para_auditoria.strip()) < 10:
            flash('Por favor, insira um texto válido ou faça o upload de um PDF legível.', 'danger')
            return redirect(url_for('auditoria.analisar_fraude'))

        try:
            # 2. Engenharia de Prompt especializada em Forense e Fraudes
            prompt_auditoria = f"""
            Você é um Perito Forense Computacional e Auditor Jurídico sênior integrado ao LexBuddy.
            Analise rigorosamente o documento ou o extrato processual fornecido abaixo com o objetivo de detectar indícios de fraudes, inconsistências crônicas ou anomalias documentais.

            Sua resposta deve conter de forma estruturada:
            1. RESUMO DA ANÁLISE: Uma visão técnica geral sobre a integridade do texto.
            2. ALERTAS DE RISCO OU ANOMALIAS: Liste em tópicos padrões suspeitos encontrados (ex: incoerências em datas, contradições textuais flagrantes, valores sem lastro ou formatação atípica). Se não houver, indique conformidade.
            3. DIRETRIZES DE INVESTIGAÇÃO: Recomendações práticas para o advogado aprofundar a auditoria deste caso.

            DOCUMENTO SUBMETIDO PARA AUDITORIA FORENSE:
            {texto_para_auditoria}
            """

            # 3. Executa a análise usando o modelo multimodal veloz
            model = genai.GenerativeModel('gemini-1.5-flash')
            resposta_pericia = model.generate_content(prompt_auditoria)

            # Estrutura um objeto simulado contendo o resultado real da IA para alimentar o template
            class ResultadoAuditoria:
                def __init__(self, analise, texto_original):
                    self.relatorio_pericial = analise
                    self.documento_auditado = texto_original

            resultado_atual = ResultadoAuditoria(resposta_pericia.text, texto_para_auditoria)
            return render_template('auditoria/forense.html', resultado=resultado_atual)

        except Exception as e:
            flash(f'Erro crítico ao acionar o motor de auditoria forense: {str(e)}', 'danger')
            return redirect(url_for('auditoria.analisar_fraude'))

    # Método GET: Renderiza a página limpa aguardando o envio do caso
    return render_template('auditoria/forense.html', resultado=None)