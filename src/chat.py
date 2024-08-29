from abstract_ai import ApiManager,PromptManager,ModelManager,InstructionManager,ResponseManager
from asgiref.sync import sync_to_async
from .personality import *
from .utils.utils import *
from abstract_security import *
import requests
api_mgr = ApiManager(api_key=get_env_value(path="/home/solcatcher/bots/darnell/.env", key='darnell_open_ai'))


def create_message(message,personality=None):
    
    instructions_template = f"""
    ----------------------------------------
    INSTRUCTIONS
    ----------------------------------------
    Please embody the personality described below and reply thoughtfully and descriptively to the inquiry.
    
    Personality Description:
    {personality.get('abstract').replace('^%','').replace('%^','')}\n\n{personality.get('personality').replace('^%','').replace('%^','')}

    temperment:
    {makeTemperment(personality.get('temperment')).replace('^%','').replace('%^','')}
    
    User Inquiry:
    {message}
    ----------------------------------------
    """
    return instructions_template

def get_prompt(message, role='assistant'):
    model, message, max_tokens, endpoint = determine_tokens(message=message, role=role, model_mgr=model_mgr)
    return {"model": model, "messages": message, "max_tokens": max_tokens}

def get_response_content(output):
    response = get_any_value(safe_json_loads(output), "response")
    choices = get_any_value(safe_json_loads(response), "choices")[0]
    content = safe_json_loads(get_any_value(safe_json_loads(choices), "content"))
    return content

async def get_query(model='gpt-4',prompt='',personality=''):
  model_mgr=ModelManager(model)
  instruction_mgr=InstructionManager()
  instruction_mgr.add_instructions({"bool_values":{'api_response':True},"text_values":{"instructions":''},"text":""})
  prompt_mgr=PromptManager(prompt_data=[prompt],request_data=[''],instruction_data=[{"bool_values":{'api_response':True},"text_values":{"api_response":"place response to prompt here"},"text":""}],chunk_token_distribution_number=0,completion_percentage=40,instruction_mgr=instruction_mgr,notation=None,model_mgr=model_mgr,chunk_number=0,chunk_type="CODE")
  response_mgr = ResponseManager(prompt_mgr=prompt_mgr,api_mgr=api_mgr)
  return response_mgr.initial_query()

async def handle_response(channel_id, message) -> str:
    print('responding...')
    personality = await checkKeyWords(message)
    if personality == None:
        personality = await get_personality(channel_id=channel_id)
    personality = personality or get_default_personality(name=None)

    # Handle response asynchronously

    response = await get_query(prompt=create_message(message,personality))
    return get_any_value(get_any_value(response, 'choices'), 'content')

def determine_tokens(message, role='assistant', model_mgr=None, endpoint=None, max_tokens=None):
    model_mgr = model_mgr or model_mgr
    model = model_mgr.selected_model_name
    endpoint = endpoint or model_mgr.selected_endpoint
    max_tokens = max_tokens or model_mgr.selected_max_tokens
    
    message = [{"role": role, "content": message}]
    max_tokens = model_mgr.selected_max_tokens - int(num_tokens_from_string(message) + 10)
    
    return model, message, max_tokens, endpoint
