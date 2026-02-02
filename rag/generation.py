from openai import OpenAI
import os
from dotenv import load_dotenv
import json

from tools.retrieve import tools, retrieve_content


from pydantic import BaseModel
from typing import List
from chromadb.api.types import QueryResult

load_dotenv()

client = OpenAI()

def llm_generation(query: str) -> str:

    input_list = [
        {'role':'user', 'content': f'{query}'}
    ]
    response = client.responses.parse(
        model= 'gpt-5-nano',
        instructions = f"""
        You are a FastAPI assistant.                                   
                                                                 
        CRITICAL: You MUST use the retrieve_content tool for ALL FastAPI questions.                                             
        Never answer from memory - always search the documentation first..
        Choose the content that is more similar in context with the input.

        CONSTRAINTS:
        - Keep it straightforward and under 200 words
        - IMPORTANT to Cite the Sources (.md file) IF you used the tool.
        """,
        input= input_list,
        reasoning= {'effort': 'minimal'},
        tools=tools
    )

    input_list += response.output

    # looping response.output and check if there is function_call
    function_calls = [item for item in response.output if item.type == 'function_call']

    # this is used to avoid calling the model twice if its a non-tool query
    if function_calls:
        for item in function_calls:
            if item.name == 'retrieve_content':
                    # Executing function logic
                    args = json.loads(item.arguments)
                    context = retrieve_content(args['query']) # extracting query

                    # provide function call results tpo the model
                    input_list.append({
                        'type': 'function_call_output',
                        'call_id': item.call_id,
                        'output': json.dumps({
                            'output': context
                        })
                        
                    })

        # print('fInal input: ')
        # print(input_list)

        response = client.responses.parse(
        model= 'gpt-5-nano',
        instructions = f"""
        You are a FastAPI assistant. that can engage in a conversational manner.                                  
                                                                 
        CRITICAL: 
        Use the retrieve_content tool ONLY for FastAPI-related questions.                   
        For general conversation, respond normally without tools.

        CONSTRAINTS:
        - Keep it straightforward and under 200 words
        - IMPORTANT to Cite the Sources (.md file) IF you used the tool.
        """,
        input= input_list,
        reasoning= {'effort': 'minimal'},
        tools=tools
        )

        # print('final response')
        # print(response)
        return response.output[1].content[0].text

    # no tool call
    else:
         # print('final response')
        # print(response)
         
         return response.output[1].content[0].text
    
# query = 'How do i connect backend to frontend in fastapi?'
# response = llm_generation(query= query)

# print(response)



