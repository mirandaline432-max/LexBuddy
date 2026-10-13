from flask import Blueprint, render_template, request, redirect, url_for, flash

pesquisa_bp = Blueprint('pesquisa', __name__, url_prefix='/')

# --- ROTAS DE ACESSO (LOGIN E REGISTRO) ---

@pesquisa_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')
        
        # Simulação de login seguro para o protótipo (admin / 123)
        if usuario == 'admin' and senha == '123':
            return redirect(url_for('pesquisa.fazer_pesquisa'))
        else:
            flash('Usuário ou senha incorretos! Dica: use admin e 123', 'danger')
            return redirect(url_for('pesquisa.login'))
            
    return render_template('login.html')

@pesquisa_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        flash('Cadastro realizado com sucesso! Faça o seu login.', 'success')
        return redirect(url_for('pesquisa.login'))
    return render_template('registro.html')


# --- ROTA DA PESQUISA INTELIGENTE (NOTEBOOKLM) ---

def simular_motor_rag_juridico(pergunta):
    pergunta_min = pregunta.lower()
    if 'demissão' in pergunta_min or 'grávida' in pergunta_min:
        return {
            'resposta': "De acordo com o Art. 10, II, 'b' do ADCT, a gestante possui estabilidade provisória. A jurisprudência do TST (Súmula 244) estende essa garantia mesmo em contratos de experiência.",
            'fonte': "Artigo 10, Inciso II, alínea 'b' do ADCT e Súmula 244 do TST."
        }
    return {
        'resposta': "Com base na pesquisa semântica na biblioteca do LexBuddy, verificou-se a necessidade de analisar o caso conforme as diretrizes do Código Civil.",
        'fonte': "Artigos 186 e 927 do Código Civil Brasileiro."
    }

@pesquisa_bp.route('/pesquisa/buscar', methods=['GET', 'POST'])
def fazer_pesquisa():
    if request.method == 'POST':
        pergunta = request.form.get('pergunta')
        resultado_rag = simular_motor_rag_juridico(pergunta)
        
        class ConsultaFake:
            def __init__(self, p, r, f):
                self.pergunta_advogado = p
                self.resposta_copiloto = r
                self.fonte_verificada = f
        
        consulta_atual = ConsultaFake(pergunta, resultado_rag['resposta'], resultado_rag['fonte'])
        return render_template('pesquisa/notebook.html', consulta=consulta_atual)
        
    return render_template('pesquisa/notebook.html', consulta=None)
