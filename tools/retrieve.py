from rag.retrieval import retrieval_chromadb
from pydantic import BaseModel

from chromadb.api.types import QueryResult

# might need thislater
class ContentSource(BaseModel):
    answer: str
    source: str

def retrieve_content(query: str): 
    # logging
    print(f"TOOL CALLED: retrieve_content with query: {query}")
    
    results: QueryResult = retrieval_chromadb(query)

    chunks_with_sources = []

    for i, doc in enumerate(results['documents'][0]):
        source = results['metadatas'][0][i]['source']
        chunks_with_sources.append(f'Docs: \n {doc} \n [Source: {source}]')

    context = '\n\n ----- \n\n'.join(chunks_with_sources)

    return context

tools = [
    {
        "type": "function",
        "name": "retrieve_content",
        "description": "Use this tool if you need to search within FastAPI documentation",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "A question about FastAPI which includes searches, how, where, when",
                },
            },
            "required": ["query"],
        },
    },
]