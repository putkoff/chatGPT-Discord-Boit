import json,os,sys,requests,discord,re,asyncio
from discord.ext import commands
from discord import app_commands
from asgiref.sync import sync_to_async
from abstract_utilities import *
from abstract_security import *
from src.utils.log import setup_logger
from src.chat import handle_response
# Adjust the import statement based on actual directory structure
bot_name = 'darnell'
my_open_ai_key = get_env_value(f'{bot_name}_open_ai')
my_discord_token = get_env_value(f'{bot_name}_token')
application_id = get_env_value(f'{bot_name}_application_id')
client_id = get_env_value(f'{bot_name}_client_id')
client_secret = get_env_value(f'{bot_name}_client_secret')
public_key = get_env_value(f'{bot_name}_public_key')
logger = setup_logger(__name__)
class AIChatBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        intents = discord.Intents.default()
        intents.message_content = True  # Enabling privileged message content intent
        self.api_key = my_open_ai_key
        self.is_private = False
        self.darnell_id = 1199838929256456232
    async def on_message(self, message):
        # Don't respond to the bot's own messages
        if message.author == self.user:
            return
        # Check if 'darnell' is mentioned
        if self.darnell_id in [user.id for user in message.mentions]:
            async with message.channel.typing():
                # Simulate some processing time
                channel_id = message.channel.id
                await asyncio.sleep(2)  # Replace with actual processing call
                response = await handle_response(channel_id, message.content)

                # Split response into parts of 2000 characters each
                max_length = 2000
                for i in range(0, len(response), max_length):
                    part = response[i:i + max_length]
                    await message.channel.send(part)
    async def on_ready(self):
        await bot.tree.sync()  # Sync an empty command tree
        logger.info(f'{self.user} has connected to Discord!')
# Create an instance of AIChatBot
if __name__ == "__main__":
    intents = discord.Intents.default()
    intents.messages = True
    intents.message_content = True
    # Create an instance of AIChatBot
    bot = AIChatBot(command_prefix='/', intents=intents)
  # Get token from environment variable
    bot.run(my_discord_token)
