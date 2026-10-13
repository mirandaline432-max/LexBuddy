from flask import Blueprint, render_template, request, redirect, url_for, flash

pesquisa_bp = Blueprint('pesquisa', __name__, url_prefix='/pesquisa')

def simular_motor_rag_juridico(pergunta):
    """Simula o funcionamento do RAG Avançado na base de dados fechada"""
    pergunta_min = pergunta.lower()
    
    if 'demissão' in pergunta_min or 'grávida' in pergunta_min:
        return {
            'resposta': "De acordo com o Art. 10, II, 'b' do ADCT, a empregada gestante possui estabilidade provisória desde a confirmação da gravidez até cinco meses após o parto. A jurisprudência do TST (Súmula 244) estende essa garantia mesmo em contratos de experiência ou tempo determinado.",
            'fonte': "Artigo 10, Inciso II, alínea 'b' do Ato das Disposições Constitucionais Transitorias (ADCT) e Súmula 244 do Tribunal Superior do Trabalho (TST)."
        }
    elif 'fraude' in pergunta_min or 'prova' in pergunta_min:
        return {
            'resposta': "A utilização de prova documental com metadados adulterados viola o princípio da boa-fé processual (Art. 5º do CPC). Uma vez comprovada a manipulação digital por perícia forense, a prova é considerada ilícita e deve ser desentranhada dos autos.",
            'fonte': "Artigo 5º do Código de Processo Civil (CPC) e Artigo 157 do Código de Processo Penal (CPP)."
        }
    else:
        return {
            'resposta': "Com base na pesquisa semântica na biblioteca do LexBuddy, verificou-se a necessidade de analisar o nexo de causalidade conforme as diretrizes do Código Civil.",
            'fonte': "Artigos 186 e 927 do Código Civil Brasileiro."
        }

@pesquisa_bp.route('/buscar', methods=['GET', 'POST'])
def fazer_pesquisa():
    if request.method == 'POST':
        pergunta = request.form.get('pergunta')
        
        if not pergunta:
            flash('Por favor, digite uma dúvida ou caso para pesquisar!')
            return redirect(request.url)
            
        resultado_rag = simular_motor_rag_juridico(pergunta)
        
        # Importação local para evitar a importação circular que travou o terminal [1]
        from database import db
        from pesquisa_inteligente.models import ConsultaJuridica
        
        nova_consulta = ConsultaJuridica(
            pergunta_advogado=pergunta,
            resposta_copiloto=resultado_rag['resposta'],
            fonte_verificada=resultado_rag['fonte']
        )
        db.session.add(nova_consulta)
        db.session.commit()
        
        return render_template('pesquisa/notebook.html', consulta=nova_consulta)
        
    return render_template('pesquisa/notebook.html', consulta=None)