import chromadb
from chromadb.api.types import QueryResult

from dotenv import load_dotenv

load_dotenv()

client = chromadb.PersistentClient(path='./chroma_db')

collection = client.get_collection(name='fastapi_docs')

# Query Result includes ids, embeddings, documents, metadatas

def retrieval_chromadb(texts: str) -> QueryResult:
    results: QueryResult = collection.query(
        query_texts=[f'{texts}'],
        n_results = 5
    )

    return results

# result = retrieval_chromadb('How do i add a middleware')

# print(type(result['documents']))
# print(type(result['metadatas']))
# print(type(result['metadatas'][0]))
# print(type(result['metadatas'][0][0]))
# print(result['metadatas'][0][0]['source'])

