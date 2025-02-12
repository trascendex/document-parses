import nest_asyncio
import os
from typing import List
from llama_index.core.node_parser import MarkdownElementNodeParser
from llama_index.core.schema import TextNode
from llama_index.core.readers import Document
from llama_index.core.node_parser import SentenceSplitter
from llama_parse import LlamaParse

def parseDocument(document:any):

    nest_asyncio.apply()

    node_parser = MarkdownElementNodeParser(num_workers=8)
    nodes = node_parser.get_nodes_from_documents(document)

    return nodes


# os.environ["GOOGLE_API_KEY"] = os.environ.get("GOOGLE_API_KEY")  # Replace with your actual API key

def semantic_chunk_pdf(pdf_path: str, parsing_instruction: str = None) -> List[TextNode]:
    """
    Parses a PDF document using LlamaParse and a hypothetical "Gemini 2.0 Flash" model
    for semantic chunking.

    Args:
        pdf_path: The path to the PDF file.
        parsing_instruction:  Optional.  A custom instruction string to guide the
            parsing process. If None, a default instruction is used.

    Returns:
        A list of LlamaIndex TextNode objects representing the semantically chunked content.
    """

    # --- Default Parsing Instruction (if none is provided) ---
    if parsing_instruction is None:
        parsing_instruction = (
            "Extract the key sections and concepts from this document. "
            "Maintain the hierarchical structure (e.g., sections, subsections). "
            "Represent each meaningful chunk of text as a separate block. "
            "Include any relevant tables or figures within their respective sections."
        )

    # --- LlamaParse Setup (with the hypothetical model) ---
    parser = LlamaParse(
        result_type="markdown",  # Request Markdown output
        use_vendor_multimodal_model=True,
        vendor_multimodal_model_name="gemini-2.0-flash-001",  # The hypothetical model
        invalidate_cache=True,  # Force a fresh parse
        parsing_instruction=parsing_instruction,
    )

    # --- Parse the PDF and get JSON result ---
    print(" --- Parse the PDF and get JSON result ---")
    try:
        json_objs = parser.get_json_result(pdf_path)
    except Exception as e:
        print(f"Error parsing PDF with LlamaParse: {e}")
        return []  # Return an empty list on error

    # --- Check for empty results---
    print(" --- Check for empty results---")
    if not json_objs:
        print("LlamaParse returned an empty result.")
        return []

    # --- Extract page data ---
    print(" --- Extract page data ---")
    json_list = json_objs[0].get("pages", [])  # Use .get() to handle missing "pages" key
    if not json_list:
        print("No pages found in the parsed JSON.")
        return []

    # --- Helper Function to Extract Text Nodes ---
    def _get_text_nodes_from_page(page_data: dict) -> List[TextNode]:
        """
        Extracts TextNode objects from a single page's parsed data.
        Handles different content types (text, tables, etc.)
        """
        nodes = []
        page_num = page_data.get("page", -1)  # Page number

        # The key change is here:  Iterate through "items", not "blocks"
        for item in page_data.get("items", []):  # Use "items", not "blocks"
            item_type = item.get("type")
            item_text = item.get("md", "")   # Use "md" (Markdown) instead of "text"

            if item_type in ("text", "heading") and item_text.strip():  # Include "heading"
                # Create TextNode for text blocks.
                node = TextNode(
                    text=item_text,
                    metadata={"page_number": page_num, "item_type": item_type},
                    excluded_embed_metadata_keys=["page_number", "item_type"],
                    excluded_llm_metadata_keys=["page_number", "item_type"],
                )
                nodes.append(node)

            elif item_type == "table" and item_text.strip():  #Keep table, just in case
                node = TextNode(
                    text=item_text,
                    metadata={"page_number": page_num, "item_type": item_type},
                    excluded_embed_metadata_keys=["page_number", "item_type"],
                    excluded_llm_metadata_keys=["page_number", "item_type"],
                )
                nodes.append(node)

            # You might need to add more conditions here for other item types,
            # like lists, images (if you want to handle them).

        return nodes

    # --- Process all pages ---
    print(" --- Process all pages ---")
    all_nodes = []
    for page_data in json_list:
        all_nodes.extend(_get_text_nodes_from_page(page_data))
    print(json_list)
    return all_nodes