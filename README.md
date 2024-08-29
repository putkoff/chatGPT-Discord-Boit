---

# Discord Bot with Abstract AI Integration

This repository contains a Discord bot that integrates with the `abstract_ai` module, providing advanced AI-driven interactions within Discord. The bot uses gpt-ALL functionalities managed by the `abstract_ai` framework to deliver intelligent and dynamic responses.

## Features

- **gpt-ALL Integration**: Utilizes the gpt-ALL model through the `abstract_ai` module for generating responses.
- **Complex Query Handling**: Manages queries, responses, and interactions using various managers such as `GptManager`, `ApiManager`, and `ResponseManager`.
- **Custom Commands**: Supports custom Discord commands to interact with the gpt-ALL model and other features.
- **Dynamic Personalities**: Adjusts the bot's personality based on channel settings and specific keywords.
- **Context-Aware Responses**: Generates contextually relevant responses based on personality and message content.
  
## Components

### abstract_ai Module

The `abstract_ai` module provides a structured framework to interact with the gpt-ALL model. Key components include:

- **GptManager**: Central class for managing interactions with gpt-ALL.
- **ApiManager**: Manages API keys and headers.
- **ModelManager**: Handles model selection and querying.
- **PromptManager**: Manages prompt generation and token distribution.
- **ResponseManager**: Handles and processes responses from gpt-ALL.

#### GptManager

- **update_response_mgr**: Updates the `ResponseManager` instance.
- **get_query**: Retrieves responses from gpt-ALL.
- **update_all**: Synchronizes all managers.
- **submit_query**: Manages sending and receiving queries.

#### ApiManager

- **get_openai_key**: Retrieves API key from environment variables.
- **get_header**: Constructs necessary headers for API requests.

#### PromptBuilder

- **get_token_calcs**: Calculates token distribution for prompts and completions.
- **get_token_distributions**: Distributes tokens across chunks based on prompt needs.

#### ResponseManager

- **re_initialize_query**: Resets query attributes.
- **post_request**: Sends requests to the AI model.
- **get_response**: Formats and retrieves responses.

### Personality Management

The bot adjusts personalities based on channel settings and message content. Key functionalities:

- **Channel-Based Personalities**: Personalities assigned to channels.
- **Keyword-Based Overrides**: Keywords in messages can override channel-based personalities.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/discord-bot-with-abstract-ai.git
   ```

2. **Navigate to the project directory**:
   ```bash
   cd discord-bot-with-abstract-ai
   ```

3. **Install dependencies**:
   Create a `.env` file in the root directory with the following keys:
   ```plaintext
   darnell_open_ai=your_openai_api_key
   darnell_public_key=your_discord_public_key
   darnell_application_id=your_discord_application_id
   darnell_client_secret=your_discord_client_secret
   darnell_client_id=your_discord_client_id
   darnell_token=your_discord_token
   ```
   Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

   `requirements.txt` should include:
   ```plaintext
   discord.py
   openai
   asgiref
   python-dotenv
   abstract_utilities
   abstract_ai
   aiofiles
   abstract_security
   collections
   logging
   requests
   ```

4. **Run the bot**:
   Execute the bot script:
   ```bash
   python3 main.py
   ```

## `main.py` Script

Here's the setup for the bot:

```python
import json, os, sys, requests, discord, re, asyncio
from discord.ext import commands
from discord import app_commands
from asgiref.sync import sync_to_async
from abstract_utilities import *
from abstract_security import *
from src.utils.log import setup_logger
from src.chat import handle_response

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
        self.darnell_id = client_id

    async def on_message(self, message):
        # Don't respond to the bot's own messages
        if message.author == self.user:
            return
        # Check if 'darnell' is mentioned
        if self.darnell_id in [user.id for user in message.mentions]:
            async with message.channel.typing():
                # Simulate processing time
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
```
---

## Usage

The bot responds to commands and messages, and can be queried by mentioning its name:
- **Mention the Bot**: To interact with the bot, mention it using `@bot_name`. For example, `@darnell ask <question>` will send the question to GPT-All and return a response.
---

## Contributing

Contributions are welcome! Open issues or submit pull requests to enhance the bot. Refer to our [contributing guidelines](CONTRIBUTING.md) for more information.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

## Contact

For questions or issues, open a new issue on our [GitHub repository](https://github.com/putkoff/chatGPT-Discord-Bot/new/main).

---

Feel free to make any adjustments or add more details as needed.
