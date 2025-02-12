# Comparador de document parsers
La solución permite comparar distintos parsers y cuál es el resultado para cada uno. 
Compara:
Tiempo de ejecución, el primer, segundo y tercer nodo, y muestra una lista de nodos.


Parsers Implementados:
## RECURSIVE CHARACTER TEXT SPLITTER ![Status](https://img.shields.io/badge/Status-IMPLEMENTADO%20PERO%20NO%20FUNCIONA-red)

## BEDROCK CON anthropic.claude-3-sonnet-20240229-v1:0 ![Status](https://img.shields.io/badge/Status-FUNCIONANDO%20OK-green)
  NECESITA LAS VARIABLES DE ENTORNO **BEDROCK_REGION**, **BEDROCK_MODEL_ID** (Si se corre en local con un aws profile configurado. Falta agregarle la opción de que tome **AWS_ACCESS_KEY_ID** y **AWS_SECRET_KEY** o algún otro método de autenticación)
 
## UNSTRUCTURED ![Status](https://img.shields.io/badge/Status-IMPLEMENTADO%20PERO%20NO%20FUNCIONA-red)

## LLAMA INDEX ![Status](https://img.shields.io/badge/Status-FUNCIONANDO%20OK-green)

## LLAMA PARSE ![Status](https://img.shields.io/badge/Status-FUNCIONANDO%20OK-green)

NECESITA LA VARIABLE DE ENTORNO **LLAMA_CLOUD_API_KEY**
 
## LLAMA PARSE CON GEMINI ![Status](https://img.shields.io/badge/Status-FUNCIONANDO%20OK-green)
NECESITA LA VARIABLE DE ENTORNO **GOOGLE_API_KEY**

## GOOGLE DOCUMENT AI LAYOUT ![Status](https://img.shields.io/badge/Status-FUNCIONANDO%20OK-green)
NECESITA LAS VARIABLES DE ENTORNO **GOOGLE_DOCUMENT_AI_PROJECT_ID**, **GOOGLE_DOCUMENT_AI_LOCATION**,**GOOGLE_DOCUMENT_AI_PROCESSOR_ID**, **GOOGLE_DOCUMENT_AI_PROCESSOR_VERSION**

## CONCLUSIONES:
https://drive.google.com/file/d/1R59uhBAjpGxHyj_IfLZ5dIVeK3eOY1l2/view?usp=sharing