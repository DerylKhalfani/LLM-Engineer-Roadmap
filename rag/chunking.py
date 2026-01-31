import os
import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter, MarkdownTextSplitter
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_core.documents import Document
import chromadb.utils.embedding_functions as embedding_functions
from uuid import uuid4
from typing import List
from dotenv import load_dotenv

load_dotenv()

# initialize vector(chroma)
chroma_client = chromadb.PersistentClient(path = './chroma_db')

model_name = 'text-embedding-3-large'

# embedding model
embedding_model = embedding_functions.OpenAIEmbeddingFunction(
                api_key=os.getenv('OPENAI_API_KEY'),
                model_name=model_name
            )
text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000,
                                               chunk_overlap = 200,
                                               add_start_index = True)

headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
]

markdown_text_splitter = MarkdownHeaderTextSplitter(headers_to_split_on)


collection = chroma_client.create_collection(name = 'fastapi_docs', embedding_function = embedding_model)

### HELPER FUNCTIONS ###
def list_files_os_walk(directory: str) -> List[str]:
    """
    iterating thorugh all the files and folders of the fastapi
    """
    file_paths = []

    # os.walk directory does the magic
    for root, _, files in os.walk(directory):
        for file in files:

            # appending path from root to file
            file_paths.append(os.path.join(root, file))

    return file_paths
    
chunked_documents = []
chunked_metadatas = []

for markdown_path in list_files_os_walk('./docs/fastapi'):

    # skip non-md file
    if not markdown_path.endswith('.md'):
        continue
    
    with open(markdown_path, 'r', encoding='utf-8') as f:
        raw_text = f.read()

    # loading document in each loader and chunking
    # document is a Document object
    document_header: List[Document] = markdown_text_splitter.split_text(raw_text)
    
    # take per document header_doc: Document which consists of metadata ({header1...}) and page_content
    for header_doc in document_header:

        for chunk in text_splitter.split_text(header_doc.page_content):
            chunked_documents.append(chunk)

            if not header_doc.metadata:
                header_doc.metadata = {'Header 1': 'None'}
            
            header_doc.metadata['source'] = markdown_path

            chunked_metadatas.append(header_doc.metadata.copy())

# list of unique ids
uuids = [str(uuid4()) for _ in range(len(chunked_documents))]

print(f'Total documents to be added: {len(chunked_documents)}')

batch_size = 100

for i in range(0, len(chunked_documents), batch_size):
    batch_docs = chunked_documents[i:i+batch_size]
    batch_metas = chunked_metadatas[i:i+batch_size]
    batch_ids = uuids[i:i+batch_size]
    
    # adding documents to vector
    collection.add(ids=batch_ids, documents=batch_docs, metadatas=batch_metas)

print(f'Collection count: {collection.count()}')