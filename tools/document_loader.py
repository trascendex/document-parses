from llama_index.core import SimpleDirectoryReader  
from typing import List  
import os  

def load_path(path:str):
    documents = SimpleDirectoryReader(path).load_data()

    archivos_leidos = []
    for document in documents:
        if document.metadata["file_name"] not in archivos_leidos:
            archivos_leidos.append(document.metadata["file_name"])
    
    return documents

def load_file(file_name: str) -> List:  
    """  
    Carga un archivo usando SimpleDirectoryReader e incluye el raw_content en los documentos.  
    
    Args:  
        file_name (str): Ruta al archivo a cargar  
        
    Returns:  
        List: Lista de documentos con raw_content incluido  
    """  
    try:  
        # Verificar que el archivo existe y tenemos permisos  
        if not os.path.exists(file_name):  
            raise FileNotFoundError(f"No se encontró el archivo: {file_name}")  
        
        if not os.access(file_name, os.R_OK):  
            raise PermissionError(f"No hay permisos de lectura para el archivo: {file_name}")  
        
        # Leer el raw_content  
        with open(file_name, 'rb') as file:  
            raw_content = file.read()  
        
        # Cargar con LlamaIndex usando la ruta absoluta del archivo  
        file_path = os.path.abspath(file_name)  
        documents = SimpleDirectoryReader(input_files=[file_path]).load_data()  
        
        # Incluir raw_content en cada documento  
        #for doc in documents:  
        #    doc.metadata['raw_content'] = raw_content  
        
        return documents  
        
    except PermissionError as e:  
        print(f"Error de permisos: {str(e)}")  
        print("Por favor, verifica que tienes permisos de lectura para el archivo y el directorio")  
        raise  
    except Exception as e:  
        print(f"Error inesperado: {str(e)}")  
        raise  