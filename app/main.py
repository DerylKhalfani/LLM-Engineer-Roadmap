from fastapi import FastAPI

from rag.generation import llm_response_with_guardrail

# initialize fastapi instance
app = FastAPI()

@app.get('/')
async def root():
    return {'message': 'hello'}

@app.get('/query')
async def generate(query: str):
    response = await llm_response_with_guardrail(query)
    return response