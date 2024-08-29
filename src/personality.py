import os,json
import aiofiles
from .utils import *
from abstract_utilities import *

bot_name = 'darnell'

async def get_abs_file_name():
    return os.path.abspath(__file__)

async def get_abs_dir():
    return os.path.dirname(await get_abs_file_name())

async def create_abs_path(link):
    return os.path.join(await get_abs_dir(), link)

async def get_personalities_dir():
    return os.path.join(await get_abs_dir(), 'personalities')

async def create_personalities_path(link):
    return os.path.join(await get_personalities_dir(), link)

async def get_personality_description_path():
    return await create_personalities_path('personalityDescription.json')

async def safe_read_from_json(file_path):
    async with aiofiles.open(file_path, mode='r') as file:
        data = await file.read()
        return safe_json_loads(data)

async def get_personality_descriptions():
    return await safe_read_from_json(await get_personality_description_path())

async def get_channel_personalities_path():
    return await create_personalities_path('channelPersonalities.json')

async def get_channel_personalities():
    return await safe_read_from_json(await get_channel_personalities_path())

async def get_personality_short_descriptions_path():
    return await create_personalities_path('personalityShort.json')

async def get_personality_short_descriptions():
    return await safe_read_from_json(await get_personality_short_descriptions_path())

def get_default_personality(name=None):
    return {
        "abstract": f"you are {getName(name=name)}",
        "personality": 'Just a really good guy',
        "temperament": "Friendly, informative, and supportive."
    }

def makeTemperment(dict_obj):
    string = dict_obj
    if isinstance(dict_obj, dict):
        string = ''
        for key, value in dict_obj.items():
            string += f"{key}:\n{value}\n\n"
    return string

async def get_channel_personality(channel_id):
    channel_id = str(channel_id)
    channelPersonalities = await get_channel_personalities()
    for key, values in channelPersonalities.items():
        if [channel for channel in values['channels'] if str(channel) == channel_id]:
            return key

async def get_personaity_from_channel(channel_id, name=None):
    personalityKey = await get_channel_personality(channel_id)
    print(f"personality {personalityKey} for channel id {channel_id}")
    personalities = await get_personality_descriptions()
    return personalities.get(personalityKey or "solanaDeveloper", get_default_personality(name=name))

def getName(name=None):
    return name or bot_name or "Alex"

async def get_personality(name=None, personality=None, channel_id=None):
    return await get_personaity_from_channel(channel_id,)

async def checkKeyWords(message):
    personality = None
    channel_personalities = await get_channel_personalities()
    commandPersonality = get_keywords(str(message))
    if commandPersonality:
        personalityKeys = list(channel_personalities.keys())
        personality = [
            personalityKey for personalityKey in personalityKeys
            if str(commandPersonality[0]).lower() in str(personalityKey).lower()
        ]
        if personality:
            descriptions = await get_personality_descriptions()
            return descriptions.get(personality[0])
    
    personality = await get_keywordCount(message, channel_personalities)
    if personality:
        descriptions = await get_personality_descriptions()
        return descriptions.get(personality)
