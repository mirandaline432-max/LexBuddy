import os
import chromadb
import pypdf  # Se der erro de falta desta biblioteca, rode: pip install pypdf

# 1. Conecta ao banco vetorial persistente (mesmo caminho do projeto)
caminho_vetorial = os.path.abspath(os.path.join(os.path.dirname(__file__), 'instance', 'chroma_db'))
chroma_client = chromadb.PersistentClient(path=caminho_vetorial)
colecao = chroma_client.get_or_create_collection(name="base_juridica_fechada")

# 2. Caminho da pasta de origem dos PDFs
PASTA_DOCS = os.path.join(os.path.dirname(__file__), 'documentos_fontes')

def extrair_texto_pdf(caminho_pdf):
    """Lê um arquivo PDF e extrai todo o texto contido nele"""
    texto_completo = ""
    try:
        with open(caminho_pdf, 'rb') as f:
            leitor = pypdf.PdfReader(f)
            for pagina in leitor.pages:
                texto_completo += pagina.extract_text() + "\n"
    except Exception as e:
        print(f"Erro ao ler o PDF {caminho_pdf}: {e}")
    return texto_completo.strip()

def indexar_documentos():
    if not os.path.exists(PASTA_DOCS):
        os.makedirs(PASTA_DOCS)
        print(f"Pasta '{PASTA_DOCS}' criada. Adicione arquivos PDF nela e execute o script novamente.")
        return

    arquivos = [f for f in os.listdir(PASTA_DOCS) if f.endswith('.pdf')]
    
    if not arquivos:
        print("Nenhum arquivo PDF encontrado na pasta 'documentos_fontes'.")
        return

    print(f"Encontrados {len(arquivos)} arquivos para indexação...")

    for idx, nome_arquivo in enumerate(arquivos):
        caminho_completo = os.path.join(PASTA_DOCS, nome_arquivo)
        texto = extrair_texto_pdf(caminho_completo)
        
        if not texto:
            print(f"Aviso: Não foi possível extrair texto de {nome_arquivo}. Pulando...")
            continue
            
        # Adiciona o texto ao banco de dados vetorial
        # O metadado 'arquivo' vincula o trecho ao PDF original para exibição em tela
        colecao.add(
            documents=[texto],
            metadatas=[{"arquivo": nome_arquivo}],
            ids=[f"doc_{idx}_{nome_arquivo}"]
        )
        print(f"Sucesso: {nome_arquivo} foi indexado com sucesso no ChromaDB!")

if __name__ == "__main__":
    indexar_documentos()
