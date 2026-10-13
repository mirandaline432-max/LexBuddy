from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory
import os

pesquisa_bp = Blueprint('pesquisa', __name__, url_prefix='/')

# --- ROTAS DE ACESSO (LOGIN E REGISTRO) ---

@pesquisa_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')
        
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


# --- ROTA PARA SERVIR OS DOCUMENTOS JURÍDICOS ORIGINAIS ---
@pesquisa_bp.route('/documentos/<filename>')
def visualizar_documento(filename):
    # Procura os arquivos dentro de uma pasta chamada 'static/documentos'
    diretorio_docs = os.path.join('static', 'documentos')
    if not os.path.exists(diretorio_docs):
        os.makedirs(diretorio_docs)
    return send_from_directory(diretorio_docs, filename)


# --- MOTOR DE INTELIGÊNCIA ARTIFICIAL E RAG SEMÂNTICO (SIMULADO DINAMICAMENTE) ---

def motor_ia_rag_lexbuddy(pergunta):
    palavras_pergunta = set(pergunta.lower().replace("?", "").replace(",", "").split())
    
    # Base de conhecimento fechada e segura (O contexto que a IA lê para não alucinar)
    banco_casos = [
        {
            "tags": {"gestante", "grávida", "demissão", "maternidade", "estabilidade", "trabalho", "dispensa", "emprego"},
            "tema": "Estabilidade da Gestante no Emprego",
            "lei": "Art. 10, II, 'b' do ADCT e Súmula 244 do TST",
            "fontes": [
                {"arquivo": "ADCT_Constituicao.pdf", "trecho": "Art. 10, II, 'b' - Fica vedada a dispensa arbitrária ou sem justa causa da empregada gestante, desde a confirmação da gravidez até cinco meses após o parto."},
                {"arquivo": "Caso_Julgado_TST_RR_10024_2024.pdf", "trecho": "Precedente TST: Condenação de empresa de logística ao pagamento substitutivo integral de verbas decorrentes da estabilidade de funcionária demitida grávida, determinando que o desconhecimento do empregador não afasta a responsabilidade legal."}
            ]
        },
        {
            "tags": {"assassinato", "homicídio", "matar", "crime", "penal", "vida", "atentado", "morte"},
            "tema": "Homicídio Qualificado e Motivo Fútil",
            "lei": "Artigo 121, § 2º do Código Penal Brasileiro",
            "fontes": [
                {"arquivo": "Codigo_Penal_Decreto2848.pdf", "trecho": "Art. 121. Matar alguem: Pena - reclusão, de seis a vinte anos."},
                {"arquivo": "Caso_Julgado_STJ_REsp_204198_SP.pdf", "trecho": "Precedente STJ: Decisão da Quinta Turma mantendo pronúncia de réu por homicídio qualificado. Firmou-se que discussões banais anteriores aos disparos de arma de fogo servem como indícios robustos de motivo fútil."}
            ]
        },
        {
            "tags": {"contrato", "danos", "prejuízo", "civil", "negligência", "obrigação", "indenização", "culpa", "batida", "carro", "acidente"},
            "tema": "Responsabilidade Civil em Acidentes de Trânsito",
            "lei": "Artigos 186 e 927 do Código Civil",
            "fontes": [
                {"arquivo": "Codigo_Civil_2002.pdf", "trecho": "Art. 186. Aquele que, por ação ou omissão voluntária, negligência ou imprudência, violar direito e causar dano a outrem comete ato ilícito."},
                {"arquivo": "Caso_Julgado_TJSP_Apelacao_10052_SP.pdf", "trecho": "Precedente TJSP: Condenação de condutor que colidiu na traseira de outro veículo ao pagamento de R$ 15.000,00 por danos materiais. Aplicou-se a jurisprudência de presunção de culpa de quem bate atrás por não guardar distância de segurança."}
            ]
        }
    ]
    
    melhor_contexto = None
    maior_pontuacao = 0
    
    for caso in banco_casos:
        intersecao = palavras_pergunta.intersection(caso["tags"])
        if len(intersecao) > maior_pontuacao:
            maior_pontuacao = len(intersecao)
            melhor_contexto = caso
            
    if melhor_contexto and maior_pontuacao > 0:
        # A IA constrói um resumo dinâmico e personalizado misturando a pergunta do usuário e os fatos reais
        resumo_dinamico = (
            f"Análise do Copiloto LexBuddy para a consulta sobre '{pergunta.replace('?', '')}'. "
            f"Com base na nossa base de dados fechada sobre '{melhor_contexto['tema']}', localizei que a norma reguladora aplicável "
            f"é o {melhor_contexto['lei']}. Sintetizando as decisões dos tribunais e os precedentes anexados abaixo, "
            f"o entendimento consolidado determina que as obrigações legais devem ser mantidas rigorosamente, "
            f"conforme demonstrado na decisão prática documentada no arquivo {melhor_contexto['fontes'][1]['arquivo']}."
        )
        return {
            "resposta": resumo_dinamico,
            "fontes": melhor_contexto["fontes"]
        }
        
    return {
        "resposta": f"Analisei sua pergunta jurídica ('{pergunta}'), mas ela foge do escopo dos documentos atualmente indexados na biblioteca segura do LexBuddy. Como IA programada para evitar alucinações, prefiro não formular uma resposta sem o lastro em documentos físicos correspondentes.",
        "fontes": []
    }

@pesquisa_bp.route('/pesquisa/buscar', methods=['GET', 'POST'])
def fazer_pesquisa():
    if request.method == 'POST':
        pergunta = request.form.get('pergunta')
        resultado_rag = motor_ia_rag_lexbuddy(pergunta)
        
        class ConsultaFake:
            def __init__(self, p, r, f):
                self.pergunta_advogado = p
                self.resposta_copiloto = r
                self.fontes_verificadas = f
        
        consulta_atual = ConsultaFake(pergunta, resultado_rag['resposta'], resultado_rag['fontes'])
        return render_template('pesquisa/notebook.html', consulta=consulta_atual)
        
    # Método GET: Garante que o template receba None e a tela comece TOTALMENTE LIMPA
    return render_template('pesquisa/notebook.html', consulta=None)