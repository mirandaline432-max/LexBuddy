from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory
import google.generativeai as genai
import chromadb
import os

pesquisa_bp = Blueprint('pesquisa', __name__, url_prefix='/')

# --- CONFIGURAÇÃO DA IA REAL E BANCO VETORIAL ---
# Inicializa o cliente do ChromaDB apontando para a pasta local permanente
caminho_vetorial = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'instance', 'chroma_db'))
chroma_client = chromadb.PersistentClient(path=caminho_vetorial)

# Configura a API do Gemini utilizando variáveis de ambiente
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


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
    diretorio_docs = os.path.join('static', 'documentos')
    if not os.path.exists(diretorio_docs):
        os.makedirs(diretorio_docs)
    return send_from_directory(diretorio_docs, filename)


# --- MOTOR DE INTELIGÊNCIA ARTIFICIAL E RAG REAL ---

def motor_ia_rag_lexbuddy_real(pergunta):
    try:
        # 1. Acessa a coleção persistente do ChromaDB
        colecao = chroma_client.get_or_create_collection(name="base_juridica_fechada")
        
        # 2. Faz a consulta vetorial por similaridade baseado na pergunta
        resultados = colecao.query(
            query_texts=[pergunta],
            n_results=2  # Busca os 2 trechos de documentos mais relevantes
        )
        
        # Estrutura os documentos encontrados para o Prompt e para a exibição em tela
        contexto_textos = []
        fontes_formatadas = []
        
        if resultados and resultados['documents'] and resultados['documents'][0]:
            for i in range(len(resultados['documents'][0])):
                texto_trecho = resultados['documents'][0][i]
                # Metadados opcionais (como o nome do arquivo original) salvos no Chroma
                meta = resultados['metadatas'][0][i] if resultados['metadatas'] else {}
                nome_arquivo = meta.get('arquivo', 'Documento_Indexado.pdf')
                
                contexto_textos.append(texto_trecho)
                fontes_formatadas.append({
                    "arquivo": nome_arquivo,
                    "trecho": texto_trecho
                })
        
        # Se o banco de dados vetorial estiver completamente vazio ou sem correspondências
        if not contexto_textos:
            return {
                "resposta": f"Analisei sua pergunta jurídica ('{pergunta}'), mas ela foge do escopo dos documentos atualmente indexados na biblioteca segura do LexBuddy. Como uma IA programada para evitar alucinações, prefiro não formular uma resposta sem o lastro em documentos correspondentes.",
                "fontes": []
            }
            
        # 3. Engenharia de Prompt para o Gemini (Estilo NotebookLM)
        contexto_consolidado = "\n\n".join(contexto_textos)
        prompt_sistema = f"""
        Você é o LexBuddy, um assistente de IA especializado no ecossistema jurídico.
        Baseando-se estritamente nos documentos de contexto fornecidos abaixo, responda à pergunta do usuário de forma analítica e profissional.
        Se a resposta não puder ser obtida por meio do texto abaixo, diga explicitamente que não possui a informação na base fechada e evite alucinar.

        DOCUMENTOS DE CONTEXTO JURÍDICO:
        {contexto_consolidado}

        PERGUNTA DO USUÁRIO:
        {pergunta}
        """
        
        # 4. Envia o prompt estruturado para o modelo LLM real
        model = genai.GenerativeModel('gemini-1.5-flash')
        resposta_ia = model.generate_content(prompt_sistema)
        
        return {
            "resposta": resposta_ia.text,
            "fontes": fontes_formatadas
        }
        
    except Exception as e:
        # Caso ocorra um erro de conexão ou de banco, retorna uma mensagem amigável de erro técnico
        return {
            "resposta": f"Erro interno no processamento do motor de IA: {str(e)}",
            "fontes": []
        }


@pesquisa_bp.route('/pesquisa/buscar', methods=['GET', 'POST'])
def fazer_pesquisa():
    if request.method == 'POST':
        pergunta = request.form.get('pergunta')
        
        # Chama a nova função conectada ao ChromaDB e Gemini
        resultado_rag = motor_ia_rag_lexbuddy_real(pergunta)
        
        # Mantém a mesma classe simulada que o seu template HTML espera receber para renderizar a tela
        class ConsultaFake:
            def __init__(self, p, r, f):
                self.pergunta_advogado = p
                self.resposta_copiloto = r
                self.fontes_verificadas = f
        
        consulta_atual = ConsultaFake(pergunta, resultado_rag['resposta'], resultado_rag['fontes'])
        return render_template('pesquisa/notebook.html', consulta=consulta_atual)
        
    return render_template('pesquisa/notebook.html', consulta=None)