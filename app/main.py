from fastapi import FastAPI

from rag.retrieval import retrieval_chromadb

# initialize fastapi instance
app = FastAPI()

@app.get('/')
async def root():
    return {'message': 'hello'}

@app.get('/query')
async def generate(query: str):
    response = retrieval_chromadb(query)
    return response