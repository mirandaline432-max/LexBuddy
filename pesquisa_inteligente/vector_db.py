import chromadb
import os

# Configura o armazenamento persistente dos julgados e jurisprudências
caminho_diretorio = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'instance', 'chroma_db'))
cliente_chroma = chromadb.PersistentClient(path=caminho_diretorio)

def obter_colecao_juridica():
    """Retorna a coleção pronta para indexar ou buscar PDFs do judiciário"""
    return cliente_chroma.get_or_create_collection(name="base_juridica_fechada")
