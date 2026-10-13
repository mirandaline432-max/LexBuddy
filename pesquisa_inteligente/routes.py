from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required

pesquisa_bp = Blueprint('pesquisa', __name__, url_prefix='/')

# --- ROTAS DE AUTENTICAÇÃO (LOGIN E REGISTRO) ---

@pesquisa_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nome_usuario = request.form.get('nomeUsuario')
        email = request.form.get('email')
        senha = request.form.get('senha')
        nome = request.form.get('nome')
        
        from database import db
        from pesquisa_inteligente.models import ConsultaJuridica # Usaremos a importação local segura
        # Código de salvamento do usuário simplificado para o protótipo
        flash('Cadastro realizado com sucesso! Faça o login.', 'success')
        return redirect(url_for('pesquisa.login'))
        
    return render_template('registro.html')

@pesquisa_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome_usuario = request.form.get('nomeUsuario')
        senha = request.form.get('senha')
        
        # Simulação de login bem-sucedido para o protótipo do grupo
        if nome_usuario == 'admin' and senha == '123':
            flash('Bem-vindo de volta ao LexBuddy!', 'success')
            return redirect(url_for('pesquisa.fazer_pesquisa'))
        else:
            flash('Usuário ou senha incorretos. Dica: use admin e 123', 'danger')
            return redirect(url_for('pesquisa.login'))
            
    return render_template('login.html')

@pesquisa_bp.route('/logout')
def logout():
    flash('Sessão encerrada com sucesso.', 'info')
    return redirect(url_for('home'))


# --- ROTA DA PESQUISA INTELIGENTE (NOTEBOOKLM) ---

def simular_motor_rag_juridico(pergunta):
    pergunta_min = pergunta.lower()
    if 'demissão' in pergunta_min or 'grávida' in pergunta_min:
        return {
            'resposta': "De acordo com o Art. 10, II, 'b' do ADCT, a empregada gestante possui estabilidade provisória. A jurisprudência do TST (Súmula 244) estende essa garantia mesmo em contratos de experiência.",
            'fonte': "Artigo 10, Inciso II, alínea 'b' do ADCT e Súmula 244 do TST."
        }
    return {
        'resposta': "Com base na pesquisa semântica na biblioteca do LexBuddy, analisou-se o caso de acordo com o Código Civil Brasileiro.",
        'fonte': "Artigos 186 e 927 do Código Civil."
    }

@pesquisa_bp.route('/buscar', methods=['GET', 'POST'])
def fazer_pesquisa():
    if request.method == 'POST':
        pergunta = request.form.get('pergunta')
        resultado_rag = simular_motor_rag_juridico(pergunta)
        
        from database import db
        # Criamos um objeto fictício para o template renderizar na tela
        class ConsultaFake:
            def __init__(self, p, r, f):
                self.pergunta_advogado = p
                self.resposta_copiloto = r
                self.fonte_verificada = f
        
        consulta_atual = ConsultaFake(pergunta, resultado_rag['resposta'], resultado_rag['fonte'])
        return render_template('pesquisa/notebook.html', consulta=consulta_atual)
        
    return render_template('pesquisa/notebook.html', consulta=None)