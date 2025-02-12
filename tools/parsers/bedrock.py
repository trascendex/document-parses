
import boto3
import json
import os
import re  # Import the 're' module

BEDROCK_REGION = os.environ.get("BEDROCK_REGION")  # Use a region that supports Bedrock AND your model.
#MODEL_ID = "anthropic.claude-3-5-sonnet-20240620-v1:0"
MODEL_ID = os.environ.get("BEDROCK_MODEL_ID")

# Create the Bedrock client *once*, globally.
bedrock = boto3.client(service_name='bedrock-runtime', region_name=BEDROCK_REGION)

def semantic_chunk_with_titan(text, model_id=MODEL_ID):
    """Performs semantic chunking using an Amazon Titan Text model on Bedrock."""
    # Use the global bedrock client.  No need to create it again.

    prompt = f"""Divide the following text into semantically coherent chunks.  Each chunk should represent a single topic or idea. Return the chunks as a numbered list, starting with "1. ". Do not include any additional text.

Text:
{text}
"""

    body = json.dumps({
        "prompt": prompt,
        "maxTokenCount": 2048,
        "temperature": 0.1,
    })

    try:
        response = bedrock.invoke_model(
            body=body,
            modelId=model_id,
            accept="application/json",
            contentType="application/json"
        )
        response_body = json.loads(response.get('body').read())
        completion = response_body['results'][0]['outputText']

        # Split the response into chunks
        chunks = re.split(r'\n\s*\d+\.\s*', completion)
        chunks = [c.strip() for c in chunks if c.strip()]
        return chunks

    except Exception as e:
        print(f"Error during Bedrock invocation: {e}")
        # Improved error reporting:
        print(f"Model ID: {model_id}")
        print(f"Request body: {body}")
        if 'response_body' in locals():
            print(f"Response body: {response_body}")
        else:
            print("Response body: N/A (Error before response)")
        return []
    
def semantic_chunk_with_claude(text, model_id=MODEL_ID):
    """Performs semantic chunking using Anthropic Claude 3 on Bedrock."""

    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": """You are a helpful document processing assistant.  Your task is to divide the following text into semantically meaningful chunks.

                    Guidelines:

                    * Each chunk should represent a coherent topic or idea.
                    * Chunks do NOT need to be the same length.  Prioritize semantic meaning over fixed size.
                    * Aim for chunks that are roughly paragraph-sized, but this is a guideline, not a strict rule.
                    * Return the chunks as a numbered list, starting with "1. ".
                    * Do NOT include any introductory or concluding text. Only return the numbered list.

                    Text to chunk:
                    """ + text # Put the text directly into the first message
                }
            ]
        }
    ]

    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",  # REQUIRED for Claude 3
        "messages": messages,
        "max_tokens": 4096,
        "temperature": 0.1,
        "top_p": 1,
    })


    try:
        response = bedrock.invoke_model(
            body=body,
            modelId=model_id,
            accept="application/json",
            contentType="application/json"
        )
        response_body = json.loads(response.get('body').read())
        completion = response_body['content'][0]['text']

        # Split the response into chunks
        chunks = re.split(r'\n\s*\d+\.\s*', completion)
        chunks = [c.strip() for c in chunks if c.strip()]
        return chunks

    except Exception as e:
        print(f"Error during Bedrock invocation: {e}")
        print(f"Model ID: {model_id}")
        print(f"Request body: {body}")  # Print the FULL request body
        if 'response_body' in locals():
            print(f"Response body: {response_body}")
        else:
            print("Response body: N/A (Error before response)")
        return []