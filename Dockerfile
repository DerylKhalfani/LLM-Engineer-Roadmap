FROM python:3.12

WORKDIR /llm-engineer

COPY ./requirements.txt /llm-engineer/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /llm-engineer/requirements.txt

COPY ./app /llm-engineer/app 
COPY ./docs /llm-engineer/docs 
COPY ./eval /llm-engineer/eval 
COPY ./infra /llm-engineer/infra 
COPY ./ops /llm-engineer/ops 
COPY ./rag /llm-engineer/rag 
COPY ./tools /llm-engineer/tools 
COPY ./chroma_db /llm-engineer/chroma_db

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]