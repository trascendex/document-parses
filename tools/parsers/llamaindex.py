from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

def parseDocument(document:any):
    from llama_index.core.node_parser import SentenceSplitter 
    from typing import List  

    # 2. Crear el splitter  
    text_splitter = SentenceSplitter(chunk_size=1024, chunk_overlap=200)  

    # 3. Dividir el documento  
    nodes = text_splitter.get_nodes_from_documents(document)  
    
    return nodes

