from typing import List
from pathlib import Path

from unstructured.partition.pdf import partition_pdf
from unstructured.chunking.title import chunk_by_title
from llama_index.core.schema import TextNode
from llama_index.core.readers import Document


def semantic_chunk_unstructured(
    pdf_path: str,
    strategy: str = "hi_res",
    include_page_breaks: bool = False,
    infer_table_structure: bool = True,
    chunking_strategy: str = "by_title",
    max_characters: int = 1500,
    new_after_n_chars: int = 1400,
    combine_text_under_n_chars: int = 500,
) -> List[TextNode]:
    """
    Performs semantic chunking on a PDF document using Unstructured.

    Args:
        pdf_path: The path to the PDF file.
        strategy: The partitioning strategy ("auto", "hi_res", "fast", "ocr_only").
        include_page_breaks: Whether to include page break elements.
        infer_table_structure: Whether to infer table structure.
        chunking_strategy: Chunking strategy ("by_title").
        max_characters: Maximum characters per chunk.
        new_after_n_chars: Start new chunk after n characters.
        combine_text_under_n_chars: Combine small text chunks.

    Returns:
        A list of LlamaIndex TextNode objects.
    """
    try:
        elements = partition_pdf(
            filename=pdf_path,
            strategy=strategy,
            include_page_breaks=include_page_breaks,
            infer_table_structure=infer_table_structure,
            chunking_strategy=chunking_strategy,
            max_characters=max_characters,
            new_after_n_chars=new_after_n_chars,
            combine_text_under_n_chars=combine_text_under_n_chars
        )

    except FileNotFoundError:
        print(f"Error: File not found at {pdf_path}")
        return []
    except Exception as e:
        print(f"Error during Unstructured partitioning: {e}")
        return []
    
    chunks = chunk_by_title(elements)
    nodes = []
    for i, chunk in enumerate(chunks):
            metadata = {}
            if chunk.metadata.page_number:
                metadata["page_number"] = chunk.metadata.page_number
            if chunk.metadata.filename:
                metadata["filename"] = chunk.metadata.filename
            if chunk.metadata.section: # Section metadata if available
                metadata["section"] = chunk.metadata.section
            if chunk.metadata.category_depth: # Depth in the hierarchy
              metadata["category_depth"] = chunk.metadata.category_depth
            if chunk.metadata.parent_id: # Parent ID
                metadata["parent_id"] = chunk.metadata.parent_id

            node = TextNode(
                text=str(chunk.text),
                id_= chunk.id,
                metadata = metadata,
                excluded_embed_metadata_keys=list(metadata.keys()),
                excluded_llm_metadata_keys=list(metadata.keys())
            )
            nodes.append(node)

    return nodes
