from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(document:any):
    text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            is_separator_regex=False,
        )
    chunks = text_splitter.split_documents(document)
    return chunks