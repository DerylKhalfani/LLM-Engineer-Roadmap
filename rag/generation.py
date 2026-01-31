from openai import OpenAI
import os
from dotenv import load_dotenv
from retrieval import retrieval_chromadb

from chromadb.api.types import QueryResult

load_dotenv()

client = OpenAI()

def llm_generation(query: str) -> str:
    # retrieve from vector database
    result: QueryResult = retrieval_chromadb(query)

    # take the content and source
    content = result['documents']
    source = result['metadatas'][0][0]['source']

    response = client.responses.create(
        model= 'gpt-5-nano',
        instructions = f"""
        Generate text, (question and answer style) based on the content: {content} \n and source: {source}.
        Choose the content that is more similar in context with the input and include the source.

        CONSTRAINTS:
        - Keep it straightforward and under 200 words
        """,
        input= query,
        reasoning= {'effort': 'minimal'}
    )

    return response.output[1].content[0].text

query = 'How do i connect backend to frontend in fastapi?'
response = llm_generation(query= query)

print(response)



