from openai import OpenAI
import os
from dotenv import load_dotenv
import json
import asyncio

from tools.retrieve import tools, retrieve_content


from pydantic import BaseModel
from typing import List
from chromadb.api.types import QueryResult

load_dotenv()

client = OpenAI()

class GuardRailResponse(BaseModel):
     allowed: bool
     reason: str

async def topical_guardrail(query):
    print('Checking topical guardrail')

    input_list = [
        {'role': 'system',
        'content': """
        You are assessing queries for a FastAPI          
        documentation assistant.                         
                                                   
        CONTEXT: Users are interacting with a FastAPI    
        assistant, so web development questions          
        should be interpreted as FastAPI-related unless  
        clearly about other frameworks.                  
                                                        
        ALLOWED:                                         
        - FastAPI questions and documentation            
        - General web development questions (assumed     
        FastAPI context)                                 
        - Normal conversation and greetings              
                                                        
        NOT ALLOWED:                                     
        - Questions explicitly about other frameworks    
        (Django, Flask, Express, etc.)                   
        - Questions completely unrelated to programming  
        - Spam or harmful content                        
                                                        
        Examples of ALLOWED queries:                     
        - "how to connect frontend and backend" (FastAPI 
        context)                                         
        - "what is CORS?"                                
        - "how do I handle file uploads?"                
                                                        
        Examples of NOT ALLOWED queries:                 
        - "how do I deploy a Django app?"                
        - "what's the weather today?"
         
         """
        },
        {'role': 'user', 'content': query}
    ]

    response = client.responses.parse(
         model='gpt-5-mini',
         input= input_list,
         text_format= GuardRailResponse
    )

    return response.output[1].content[0].parsed

async def llm_response(query: str) -> str:
    print('Getting LLM response')

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

# USING GUARDRAIL
async def llm_response_with_guardrail(query):
    
    # running two tasks in parallerl
    topical_guardrail_task = asyncio.create_task(topical_guardrail(query))
    llm_response_task = asyncio.create_task(llm_response(query))

    while True:
        # waiting for whichever finishes first
        # await asyncio.wait() pausing and wait
        # return_when=asyncio.FIRST_COMPLETED resume when atleast one task finishes
        # done set of tasks finished, _ -> running
        done, _ = await asyncio.wait(
              [topical_guardrail_task, llm_response_task], return_when=asyncio.FIRST_COMPLETED
        )


        if topical_guardrail_task in done:
            # getting GuardrailResponse object
            guardrail_response = topical_guardrail_task.result()

            if not guardrail_response.allowed:
                llm_response_task.cancel() # cancel the llm task
                print('Topical guardrail triggered')

                return """I'm a FastAPI assistant and can only help with FastAPI-related questions. Please ask me something about FastAPI!"""
            
            elif llm_response_task in done:
                 response = llm_response_task.result()
                 return response
        else:
             await asyncio.sleep(0.1) # sleep before checking tasks again
    
# query = 'How do i connect backend to frontend in fastapi?'
# response = llm_generation(query= query)

# print(response)



