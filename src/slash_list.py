def getIntyeraction(*args,**kwargs):
    pass
import discord
from discord.ext import commands
intents = discord.Intents.default()  # Create a default set of intents
intents.typing = False  # You can customize which intents you need

# Initialize the bot with the specified intents and set the command prefix
bot = commands.Bot(command_prefix="/", intents=intents)

# Event handler for when the bot is ready
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} ({bot.user.id})")

# Define a slash command that switches text outputs
@bot.command()
async def switch(ctx, *, text_to_switch):
    # Delete the user's command message
    await ctx.message.delete()

    # Send the text to the channel
    await ctx.send(text_to_switch)
