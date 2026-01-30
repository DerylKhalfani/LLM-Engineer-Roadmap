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
chroma_client = chromadb.Client()

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

for markdown_path in list_files_os_walk('../docs/fastapi'):

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
            chunked_metadatas.append(header_doc.metadata)

# list of unique ids
uuids = [str(uuid4()) for _ in range(len(chunked_documents))]

# adding documents to vector
collection.add(ids=uuids, documents=chunked_documents, metadatas=chunked_metadatas)

# if __name__ == "__main__":                                         
#       # Test with single file                                        
#       test_path = '../docs/macro1.md'                                
                                                                     
#       print(f"Testing with: {test_path}\n")                          
                                                                     
#       # Load and split    
#       with open(test_path, 'r', encoding='utf-8') as f:
#            raw_text = f.read()                                                                                                                           
                                                                     
#       # Split by headers                                             
#       header_docs = markdown_text_splitter.split_text(raw_text)           
#       print(f"Split into {len(header_docs)} header sections\n")      
                                                                     
#       # Show first header section                                    
#       if header_docs:                                                
#           print("First header section:")                             
#           print(f"  Metadata: {header_docs[0].metadata}")            
#           print(f"  Content preview: {header_docs[0].page_content[:200]}...\n")                         
                                                                     
#       # Now split into chunks                                        
#       test_chunks = []                                               
#       test_metas = []                                                
                                                                     
#       for header_doc in header_docs:                                 
#           chunks = text_splitter.split_text(header_doc.page_content) 
#           for chunk in chunks:                                       
#               test_chunks.append(chunk)                              
#               test_metas.append(header_doc.metadata)                 
                                                                     
#       print(f"Total chunks created: {len(test_chunks)}")             
#       print(f"\nFirst chunk preview:")                               
#       print(f"  Text: {test_chunks[0][:200]}...")                    
#       print(f"  Metadata: {test_metas[0]}")                 