import os

def parseDocument(file_name:str):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './google_credentials.json'

    documentai_doc = process_document_layout_sample(project_id,location,processor_id,processor_version,file_name,mime_type)
    return documentai_doc

from typing import Optional, Sequence

from google.api_core.client_options import ClientOptions
from google.cloud import documentai

project_id = os.environ.get("GOOGLE_DOCUMENT_AI_PROJECT_ID")
location = os.environ.get("GOOGLE_DOCUMENT_AI_LOCATION")
processor_id = os.environ.get("GOOGLE_DOCUMENT_AI_PROCESSOR_ID")
processor_version = os.environ.get("GOOGLE_DOCUMENT_AI_PROCESSOR_VERSION")
#file_path = "./CoralCloudResortFAQs.pdf"
mime_type = "application/pdf"

def process_document_layout_sample(
    project_id: str,
    location: str,
    processor_id: str,
    processor_version: str,
    file_path: str,
    mime_type: str,
) -> documentai.Document:
    process_options = documentai.ProcessOptions(
        layout_config=documentai.ProcessOptions.LayoutConfig(
            chunking_config=documentai.ProcessOptions.LayoutConfig.ChunkingConfig(
                chunk_size=1000,
                include_ancestor_headings=True,
            )
        )
    )

    document = process_document(
        project_id,
        location,
        processor_id,
        processor_version,
        file_path,
        mime_type,
        process_options=process_options,
    )

    #print("Document Layout Blocks")
    #for block in document.document_layout.blocks:
    #    print(block)

    #print("Document Chunks")
    #for chunk in document.chunked_document.chunks:
    #    print(chunk)

    return document


def process_document(
    project_id: str,
    location: str,
    processor_id: str,
    processor_version: str,
    file_path: str,
    mime_type: str,
    process_options: Optional[documentai.ProcessOptions] = None,
) -> documentai.Document:
    # You must set the `api_endpoint` if you use a location other than "us".
    client = documentai.DocumentProcessorServiceClient(
        client_options=ClientOptions(
            api_endpoint=f"{location}-documentai.googleapis.com"
        )
    )

    # The full resource name of the processor version, e.g.:
    # `projects/{project_id}/locations/{location}/processors/{processor_id}/processorVersions/{processor_version_id}`
    # You must create a processor before running this sample.
    name = client.processor_version_path(
        project_id, location, processor_id, processor_version
    )

    # Crear el raw document  
    with open(file_path, 'rb') as file:  
        content = file.read()  

    raw_document = documentai.RawDocument(  
        content=content,  
        mime_type='application/pdf'  # Ajusta el mime_type según el tipo de archivo  
    )  
    
    
    # Crear la solicitud  
    request = documentai.ProcessRequest(  
        name=name,  
        raw_document=raw_document  
    )  

    # For a full list of `Document` object attributes, reference this page:
    # https://cloud.google.com/document-ai/docs/reference/rest/v1/Document
    try:  
        response = client.process_document(request=request)  
        #print("########################### response #####################################")
        #import pickle
        #nombre_archivo = "response.json"
        #with open(nombre_archivo, 'wb') as archivo:
            # Serializamos el objeto y lo guardamos en el archivo
            #pickle.dump(response, archivo)
        #print("########################### /response #####################################")
        return response  
    except Exception as e:  
        print(f"Error procesando documento: {str(e)}")  
        raise  