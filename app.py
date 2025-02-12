import streamlit as st
from streamlit_chat import message
from dotenv import load_dotenv
from PyPDF2 import PdfReader  
import tempfile  
import os  

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
load_dotenv()

from tools.parsers.generic_parses import parsear_archivo


if "vector_db" not in st.session_state:
    st.session_state["vector_db"] = None

if "interactions" not in st.session_state:
    st.session_state["interactions"] = []

#if "answers" not in st.session_state:
#    st.session_state["answers"] = []

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

#st.warning('This is a warning', icon="⚠️")
st.logo(
    "https://trascendex.ai/wp-content/uploads/2024/06/logo-trascendex-svg.svg",
    link="https://streamlit.io/gallery",
    icon_image="https://images.creativefabrica.com/products/previews/2024/04/19/ofJzgKblx/2fVkWPH9ZMUsnUMcRFPzRL2tnh3-desktop.jpg",
)


# Configurar el nombre de la pestaña del navegador  
st.set_page_config(  
    page_title="Habla con tu PDF",  # Título de la pestaña  
    page_icon="📊",  # Ícono de la pestaña (opcional)  
    layout="wide",  # Diseño de la página (opcional)  
    initial_sidebar_state="expanded"  # Estado inicial de la barra lateral (opcional)  
) 

from dotenv import load_dotenv, set_key, find_dotenv

load_dotenv()

# Whitelist of allowed environment variables
ALLOWED_VARS = [
    "OPENAI_API_KEY",
    "UNSTRUCTURED_API_KEY",
    "GOOGLE_API_KEY",
    "BEDROCK_REGION",
    "BEDROCK_MODEL_ID",
    "GOOGLE_DOCUMENT_AI_PROJECT_ID",
    "GOOGLE_DOCUMENT_AI_LOCATION",
    "GOOGLE_DOCUMENT_AI_PROCESSOR_ID",
    "GOOGLE_DOCUMENT_AI_PROCESSOR_VERSION",
    "LLAMA_CLOUD_API_KEY",
]

# --- Sidebar ---
with st.sidebar:
    st.header("Set Environment Variables")

    var_name = st.selectbox("Variable Name", options=ALLOWED_VARS)
    # Use text_input with type="password" for secure input
    var_value = st.text_input("Variable Value", type="password")

    if st.button("Set Variable"):
        if var_name in ALLOWED_VARS:
            set_key(find_dotenv(), var_name, var_value)
            os.environ[var_name] = var_value #Set value in session
            st.success(f"Environment variable '{var_name}' set and saved.")
        else:
            st.error("Invalid variable name.")

    # --- Display ONLY variable names (values are hidden) ---
    st.header("Set Environment Variables")
    st.write("The following environment variables are set:")
    dotenv_path = find_dotenv()
    if dotenv_path:
      with open(dotenv_path) as f:
        for line in f:
            if line.strip() and not line.startswith("#"):
                key, _ = line.strip().split("=", 1) # Split on the first =
                if key in ALLOWED_VARS:
                    st.write(f"- {key}")  # Only display the variable name
    else:
        st.write("No custom environment variables set yet.")

class interacion:
    mensaje: str
    tipo: str

col1, col2, col3, col4, col5, col6, col7 = st.columns(7)  # Create 3 columns

with col1:
    parsers_bedrock = st.checkbox("BEDROCK",value=True, key="parsers_bedrock")
with col2:
    parsers_unstructured = st.checkbox("UNSTRUCTURED",value=False, key="parsers_unstructured")
with col3:
    parsers_llamaindex = st.checkbox("LLAMA INDEX",value=True,key="parsers_llamaindex")
with col4:
    parsers_llamaparse = st.checkbox("LLAMAPARSE", value=True, key="parsers_llamaparse")
with col5:
    parsers_google_layout = st.checkbox("GOOGLE LAYOUT", value=True, key="parsers_google_layout")
with col6:
    parsers_llamaparse_gemini = st.checkbox("LLAMAPARSE GEMINI", value=True, key="parsers_llamaparse_gemini")
with col7:
    parsers_recursive_character_text_splitter = st.checkbox("RECURSIVE CHARACTER TEXT SPLITTER", value=False, key="parsers_recursive_character_text_splitter")


import time
processed_files = []  
def cargar_archivos():
    if st.session_state.file_uploader is not None:  
        # Guardar el archivo en un directorio temporal  
        # print(st.session_state.file_uploader.uploaded_file  )
        uploaded_file = st.session_state.file_uploader 
        
        if isinstance(uploaded_file, list):
             for archivo in uploaded_file:
                procesar_achivo(archivo)
        else:
            procesar_achivo(uploaded_file)
        # Esto es para cuando acepta mas de un archivo
        

def procesar_achivo(archivo:any):
    print(archivo)
    st.write(f"Archivo seleccionado: {archivo.name}")  
    st.write(f"Tamaño del archivo: {archivo.size} bytes")  
    # Procesar el archivo  
    file_contents = archivo.getvalue()  

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:  
        tmp_file.write(archivo.getvalue())  
        tmp_file_path = tmp_file.name  
    
    # Guardar tmp_file_path en el directorio files
    if not os.path.exists("files"):
        os.makedirs("files")

    #RUTA DEL ARCHIVO

    # GUARDAR EN UNA VARIABLE LA FECHA EN FORMATO YYYYDDMM_mm
    import datetime

    now = datetime.datetime.now()

    date_string = now.strftime("%Y%d%m_%H%M%S")
    file_path = f"files/{date_string}_{archivo.name}"


    with open(file_path, "wb") as f:
        f.write(file_contents)

    processed_files.append({  
        'name': file_path,  
        'data': file_contents  
    }) 

    from tools.parsers.generic_parses import parsear_archivo
    parsear_archivo(file_path)

load_button_container = st.container()

def upload_button(): 
    with load_button_container:
        pdf_file = st.file_uploader("Cargar archivos",key="file_uploader", type=["pdf"], accept_multiple_files=False, on_change= cargar_archivos)

input_container = st.container()

with input_container:
    #with st.form(key="my_form",clear_on_submit=True):
        #query = st.text_area("Hazme una pregunta!", key="input", height=80)
        query = st.chat_input("Hazme una pregunta")
        with st.container():
            #submit_button = st.form_submit_button(label="Enviar")
            upload_button()
        if query: #and submit_button:
            #st.session_state["questions"].append(query)
            _interaccion = interacion()
            _interaccion.mensaje = query
            _interaccion.tipo = "user"
            st.session_state["interactions"].append(_interaccion)
            with st.chat_message("Rodrigo", avatar=":material/face:"):
                st.write(query)
                #st.line_chart(np.random.randn(30, 3))
            vector_db = st.session_state["vector_db"]

            ## prompt 
            prompt = """
                        You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.
                        Question: {question} 
                        Context: {context} 
                        Answer:
            """
            prompt_template = PromptTemplate(
                template=prompt,
                #input_variables=["question","context"]
            )

            llm_openai = ChatOpenAI(model="gpt-4")

            if vector_db:
                retriever_db = vector_db.as_retriever()

                retriever_qa = RetrievalQA.from_chain_type(
                    llm=llm_openai,
                    retriever=retriever_db,
                    chain_type="stuff"
                )

                answer = retriever_qa.invoke(query)["result"]
            else:
                answer = llm_openai.invoke(query).content


            ## save in st memory
            message = st.chat_message("ai",avatar=":material/network_intelligence:")
            message.write(answer)
            #message.bar_chart(np.random.randn(30, 3))
            #st.session_state["answers"].append(answer)
            _interaccion = interacion()
            _interaccion.mensaje = answer
            _interaccion.tipo = "system"
            st.session_state["interactions"].append(_interaccion)



