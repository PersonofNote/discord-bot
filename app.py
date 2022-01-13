# bot.py
import os

import discord
from dotenv import load_dotenv

import pandas as pd


load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

# Temp for singular server; will need to scale to multiple servers
SERVER = os.getenv('SERVER_NAME')

ALLOWED_CHANNELS = os.getenv('ALLOWED_CHANNELS')

client = discord.Client()

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == SERVER:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    guild = client.guilds[0]
    text_channel_list = []
    for channel in guild.text_channels:
        text_channel_list.append(channel)


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hello, {member.name}. This DM will hold copy about what Spacepost is, as well as useful links.'
    )

@client.event
async def on_message(message):
    # Disregard bot's own message
    if message.author == client.user:
        return
    print(message.channel.id)
    response = f"Hello, @channel! I am collecting messages from this channel. They will be collected in a .csv file. \n If you haves questions or feedback, please ping (user or channel)"
    if message.content == '!download_messages':
        # Restrict to this channel for testing. message.content.split([0] should be the command, after that is args)
        if (message.channel.name in ALLOWED_CHANNELS):
            # TODO: get limit arg from message
            messages = await message.channel.history(limit=100).flatten()
            pretty_print_messages(messages)
            await message.channel.send(response)


### HELPER FUNCTIONS ### 
def pretty_print_messages(messages):
    for x in messages:
        print(x)

def make_csv(messages):
    # Adapt from notebook
    pass

def process_csv(file_path):
    # Adapt from notebook
    pass

client.run(TOKEN)
