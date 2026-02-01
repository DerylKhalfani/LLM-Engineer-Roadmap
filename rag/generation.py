from openai import OpenAI
import os
from dotenv import load_dotenv
from rag.retrieval import retrieval_chromadb

from chromadb.api.types import QueryResult

load_dotenv()

client = OpenAI()

def llm_generation(query: str) -> str:
    # retrieve from vector database
    result: QueryResult = retrieval_chromadb(query)

    # take the content and source (contains 5 source)
    chunks_with_sources = []
    for i, doc in enumerate(result['documents'][0]):
        source = result['metadatas'][0][i]['source']
        chunks_with_sources.append(f'[Source: {source}] \n Docs: \n {doc}')
    
    context = '\n\n ---- \n\n'.join(chunks_with_sources)

    response = client.responses.create(
        model= 'gpt-5-nano',
        instructions = f"""
        Generate text, (question and answer style) based on these retrieved documents:
        
        {context}
        Choose the content that is more similar in context with the input.

        CONSTRAINTS:
        - Keep it straightforward and under 200 words
        - Cite the Sources you used
        """,
        input= query,
        reasoning= {'effort': 'minimal'}
    )

    return response.output[1].content[0].text

query = 'How do i connect backend to frontend in fastapi?'
response = llm_generation(query= query)

print(response)



