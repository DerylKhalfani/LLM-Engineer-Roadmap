from fastapi import FastAPI

from rag.generation import llm_generation

# initialize fastapi instance
app = FastAPI()

@app.get('/')
async def root():
    return {'message': 'hello'}

@app.get('/query')
async def generate(query: str):
    response = llm_generation(query)
    return response