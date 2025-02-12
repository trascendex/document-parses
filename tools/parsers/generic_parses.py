import streamlit as st
import os

if "settings.llm" not in st.session_state:
    st.session_state["settings.llm"] = None

if "settings.embed_model" not in st.session_state:
    st.session_state["settings.embed_model"] = None 

class respuesta:
    file_name:str
    tokens:any

def parsear_archivo(file_name:str):
    from tools.document_loader import load_file
    document = load_file(file_name)
    placeholder = st.empty()
    with placeholder.container():
        st.write(f"Parseando archivo : {file_name}")
        print(document[0].text)
        #print(document[0].id_)
        
        respuesta = []

        from tools.parsers.llamaindex import parseDocument as llamaindex_parser
        import time

        if st.session_state.parsers_recursive_character_text_splitter:
            st.write("################### PROCESANDO CON RECURSIVE CHARACTER TEXT SPLITTER ###########################")
            print("################### PROCESANDO CON RECURSIVE CHARACTER TEXT SPLITTER ###########################")
        
            from tools.parsers.recursive_character_text_splitter import split_documents as recursive_chunker
            start_time = time.time()
            recursive_chunks = recursive_chunker(document)
            end_time = time.time()
            respuesta.append({
                "parser": "recursive_character_text_splitter",
                "comentarios":"",
                "tiempo": end_time - start_time,
                "first_node": recursive_chunks[0] if recursive_chunks else None,
                "second_node": recursive_chunks[1] if len(recursive_chunks) > 1 else None,
                "third_node": recursive_chunks[2] if len(recursive_chunks) > 2 else None,
                "nodes": recursive_chunks
            })

        if st.session_state.parsers_bedrock:
            st.write("################### PROCESANDO CON AMAZON BEDROCK ###########################")
            print("################### PROCESANDO CON AMAZON BEDROCK ###########################")
            # --- Ejemplo de uso ---

            from tools.parsers.bedrock import semantic_chunk_with_claude as bedrock_parser
            start_time = time.time()
            chunks = bedrock_parser(document[0].text)
            end_time = time.time()
            respuesta.append({
                "parser": "bedrock",
                "comentarios":"",
                "tiempo": end_time - start_time,
                "first_node": chunks[0] if chunks else None,
                "second_node": chunks[1] if len(chunks) > 1 else None,
                "third_node": chunks[2] if len(chunks) > 2 else None,
                "nodes": chunks
            })

        if st.session_state.parsers_unstructured and 1==2:
            st.write("################### PROCESANDO CON UNSTRUCTURED ###########################")
            print("################### PROCESANDO CON UNSTRUCTURED ###########################")
            from tools.parsers.unstructured import semantic_chunk_unstructured as unstructured_parser

            start_time = time.time()
            chunks_unstructured = unstructured_parser(file_name)
            end_time = time.time()
            respuesta.append({
                "parser": "unstructured",
                "comentarios":"",
                "tiempo": end_time - start_time,
                "first_node": chunks_unstructured[0] if chunks_unstructured else None,
                "second_node": chunks_unstructured[1] if len(chunks_unstructured) > 1 else None,
                "third_node": chunks_unstructured[2] if len(chunks_unstructured) > 2 else None,
                "nodes": chunks_unstructured
            })

        if st.session_state.parsers_llamaindex:
            st.write("################### PROCESANDO CON LLAMAINDEX ###########################")
            print("################### PROCESANDO CON LLAMAINDEX ###########################")
            start_time = time.time()
            nodes_llamaindex = llamaindex_parser(document)
            end_time = time.time()
            respuesta.append({  
                "parser": "llamaindex",  
                "comentarios":"",
                "tiempo": end_time - start_time,
                "first_node": nodes_llamaindex[0] if nodes_llamaindex else None,  
                "second_node": nodes_llamaindex[1] if len(nodes_llamaindex) > 1 else None,  
                "third_node": nodes_llamaindex[2] if len(nodes_llamaindex) > 2 else None,  
                "nodes": nodes_llamaindex  
            })
    
        if st.session_state.parsers_llamaparse:
            st.write("################### PROCESANDO CON LLAMAPARSE ###########################")
            print("################### PROCESANDO CON LLAMAPARSE ###########################")
            from tools.parsers.llamaparse import parseDocument as llamaparse_parser
            start_time = time.time()
            nodes_llamaparse = llamaparse_parser(document)
            end_time = time.time()
            # Convertir los nodos a diccionarios con la información que quieres mostrar  
            respuesta.append({  
                "parser": "llamaparse_default", 
                "comentarios":"",
                "tiempo": end_time - start_time, 
                "first_node": nodes_llamaparse[0] if nodes_llamaparse else None,  
                "second_node": nodes_llamaparse[1] if len(nodes_llamaparse) > 1 else None,  
                "third_node": nodes_llamaparse[2] if len(nodes_llamaparse) > 2 else None,  
                "nodes": nodes_llamaparse  
            })
    
        if st.session_state.parsers_llamaparse_gemini:
            st.write("################### PROCESANDO CON LLAMAPARSE GEMINI ###########################")
            print("################### PROCESANDO CON LLAMAPARSE GEMINI ###########################")
            from tools.parsers.llamaparse import semantic_chunk_pdf as llamaparse_parser_gemini
            start_time = time.time()
            nodes_llamaparse_gemini = llamaparse_parser_gemini(file_name)
            end_time = time.time()
            # Convertir los nodos a diccionarios con la información que quieres mostrar  
            respuesta.append({  
                "parser": "llamaparse_gemini", 
                "comentarios":"Limite 15 páginas",
                "tiempo": end_time - start_time, 
                "first_node": nodes_llamaparse_gemini[0] if nodes_llamaparse_gemini else None,  
                "second_node": nodes_llamaparse_gemini[1] if len(nodes_llamaparse_gemini) > 1 else None,  
                "third_node": nodes_llamaparse_gemini[2] if len(nodes_llamaparse_gemini) > 2 else None,  
                "nodes": nodes_llamaparse_gemini  
            })

        if st.session_state.parsers_google_layout:
            st.write("################### PROCESANDO CON GOOGLE LAYOUT ###########################")
            print("################### PROCESANDO CON GOOGLE LAYOUT ###########################")
            from tools.parsers.google_layout import parseDocument as google_layout_parser

            start_time = time.time()

            respuesta_google_ai = google_layout_parser(file_name)

            end_time = time.time()

            document_object = respuesta_google_ai.document
            
            nodes_google_layout = document_object.document_layout.blocks

            for block in document_object.document_layout.blocks:
                print(block.text_block.text)
                if hasattr(block.text_block, 'blocks'):
                    for block2 in block.text_block.blocks:
                        print(block2.text_block.text)
                        if hasattr(block2.text_block, 'blocks'):
                            for block3 in block2.text_block.blocks:
                                print(block3.text_block.text)
            
            respuesta.append({  
                "parser": "google_layout", 
                "comentarios":"",
                "tiempo": end_time - start_time, 
                "first_node": nodes_google_layout[0] if nodes_google_layout else None,  
                "second_node": nodes_google_layout[1] if len(nodes_google_layout) > 1 else None,  
                "third_node": nodes_google_layout[2] if len(nodes_google_layout) > 2 else None,  
                "nodes": document_object.document_layout.blocks  
            })

    
        display_parsed_results(respuesta=respuesta)
    return respuesta


import json  
from typing import List, Dict, Any 

def node_to_dict(node):  
    """  
    Convierte un nodo a diccionario serializable  
    """  
    if node is None:  
        return None  
    
    # Convertir el nodo a un diccionario con los campos que nos interesan  
    return {  
        'text': node.text if hasattr(node, 'text') else str(node),  
        'node_id': node.node_id if hasattr(node, 'node_id') else None,  
        'metadata': {  
            k: str(v) for k, v in node.metadata.items()  
        } if hasattr(node, 'metadata') else {}  
    }  

def display_parsed_results(respuesta: list):  
    """  
    Muestra los resultados del parseo en una tabla formateada  
    """  
    import streamlit as st  
    import pandas as pd  
    import json  

    def serialize_node(node):  
        """Serializa un nodo a JSON"""  
        try:  
            return json.dumps(node_to_dict(node), indent=2)  
        except Exception as e:  
            return str({"error": f"Error serializando nodo: {str(e)}"})  

    def serialize_nodes(nodes):  
        """Serializa lista de nodos a JSON"""  
        try:  
            return json.dumps([node_to_dict(node) for node in nodes], indent=2)  
        except Exception as e:  
            return str({"error": f"Error serializando lista de nodos: {str(e)}"})  

    # Preparar datos para la tabla  
    data = []  
    for i, item in enumerate(respuesta):  
        try:  
            data.append({  
                'ID_NODO': i,  
                'PARSER': item['parser'], 
                'TIME': item['tiempo'],
                'FIRST_NODE': serialize_node(item['first_node']),  
                'SECOND_NODE': serialize_node(item['second_node']),  
                'THIRD_NODE': serialize_node(item['third_node']),  
                'NODOS': serialize_nodes(item['nodes'])  
            })  
        except Exception as e:  
            st.error(f"Error procesando item {i}: {str(e)}")  
            continue  

    # Crear DataFrame  
    df = pd.DataFrame(data)  
    
    # Mostrar tabla con configuración personalizada  
    st.dataframe(  
        df,  
        column_config={  
            'ID_NODO': st.column_config.NumberColumn('ID'),  
            'PARSER': st.column_config.TextColumn('Parser'),  
            'FIRST_NODE': st.column_config.TextColumn(  
                'Primer Nodo',  
                width='medium'  
            ),  
            'SECOND_NODE': st.column_config.TextColumn(  
                'Segundo Nodo',  
                width='medium'  
            ),  
            'THIRD_NODE': st.column_config.TextColumn(  
                'Tercer Nodo',  
                width='medium'  
            ),  
            'NODOS': st.column_config.TextColumn(  
                'Todos los Nodos',  
                width='large'  
            )  
        },  
        hide_index=True,  
        use_container_width=True  
    )  


#parsear_archivo("files/CV_Sebastian_Iannini.pdf")