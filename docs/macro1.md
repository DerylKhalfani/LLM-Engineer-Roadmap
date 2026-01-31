# Chunking

## Scraping source
Look at fastapi source docs 
https://github.com/fastapi/fastapi/tree/master/docs/en/docs


## Vector Databases
Use ChromaDB for its cheap use

### reference link and ideas
source code for chromaDB:
https://docs.trychroma.com/docs/collections/add-data
https://docs.langchain.com/oss/python/integrations/document_loaders/unstructured_markdown

ideas from:
https://medium.com/@iraj.hedayati/building-a-private-local-rag-chatbot-using-chroma-and-markdown-documents-147cae7f8e4a

### Chunking workflow

- Initialize the vector database, using persistentclient since i want the database to stay on my local file
- Initialize the embedding model with text-embedding-3-large, if not mini lv6 model is used
- Initialize the text splitter (RecursiveCharacterTextSplitter) splitting text recursively with 1000 size and 200 characters overlapping within each chunk
- MarkdownHeaderTextSplitter splits on each specific header and its content
- Initialize vector database with .create_collection() using the embedding model created

- list_files_os_walk function iterate through all the files, including folder within the fastapi/docs (fastapi md docs) returning the file path

- do a for loop for each md file which then read using with open() -> raw_text
- use MarkdownHeaderTextSplitter for each raw_text to get their metadata and page_content -> document_header: List[Document]
- do a for loop for each Document (document_header)
- and do a for loop for each Document page_content by splitting the text (RecursiveCharacterTextSplitter) -> chunk
- append the chunk to a list (chunked_documents)
- some of the header_doc may not have metadata thus some Document has default metadatas = {'Header 1': 'None'}
- each header_doc metadata also consists the source = markdown_path for easier tracking
- append the header_doc metadata to a list (chunked_metadatas)

- Create unique ids for each chunk

- then add it to the vector databases by batches (100)




### Tips and Notes during chunking
- UnstructuredMarkdownLoader strips markdown formatting therefore it can remove context
- Document is a class object consist of metadatas, id, embeddings
- OpenAI has a 300,000 token limit per request therefore i add it by batches


