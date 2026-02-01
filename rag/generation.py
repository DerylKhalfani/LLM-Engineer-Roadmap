from openai import OpenAI
import os
from dotenv import load_dotenv
from rag.retrieval import retrieval_chromadb

from pydantic import BaseModel
from typing import List
from chromadb.api.types import QueryResult

load_dotenv()

client = OpenAI()

class ContentSource(BaseModel):
    answer: str
    source: str

def llm_generation(query: str) -> str:
    # retrieve from vector database
    result: QueryResult = retrieval_chromadb(query)

    # take the content and source (contains 5 source)
    chunks_with_sources = []
    for i, doc in enumerate(result['documents'][0]):
        source = result['metadatas'][0][i]['source']
        chunks_with_sources.append(f'Docs: \n {doc} \n [Source: {source}]')
    
    context = '\n\n ---- \n\n'.join(chunks_with_sources)

    response = client.responses.parse(
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
        reasoning= {'effort': 'minimal'},
        text_format=ContentSource
    )

    print(response)

    response = response.output[1].content[0].parsed

    print(type(response))

    print(response)

    answer = response.answer
    source = response.source

    return answer, source

# query = 'How do i connect backend to frontend in fastapi?'
# response = llm_generation(query= query)

# print(response)



