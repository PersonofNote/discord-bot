# bot.py

# data formatting imports
import os
from dotenv import load_dotenv
import pandas as pd
import requests
import json
from datetime import date
import random
import time
from operator import itemgetter

# third-party data api libraries
import discord
#import tweepy

# modules
import generate_users as u
from data_collection import *


load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')

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
    response = f"Hello, @channel! I am collecting messages from this channel. They will be collected in a .csv file. \n If you have questions or feedback, please ping (user or channel)"
    if message.content == 'a':
        # Restrict to this channel for testing. message.content.split([0] should be the command, after that is args)
        message_array = []
        if (message.channel.name in ALLOWED_CHANNELS):
            # TODO: get limit arg from message
            #messages = await get_all_messages(client, message.channel.id)
            allmessages = []

            #make initial request for most recent tweets (200 is the maximum allowed count)
            new_messages = await message.channel.history(limit=100).flatten()
            print (len(new_messages))
            print(new_messages)
            #pretty_print_messages(messages)
            #await message.channel.send(response)


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

#before=date.today(), after=False

def get_all_messages(channel, token):
    headers = {"Authorization": f"Bot {token}"}
    channel_path = f'https://discord.com/api/channels/{channel}/messages?limit=100'

    allmessages = []
    try:
        new_messages = requests.get(channel_path, headers=headers).json() 
        allmessages.extend(new_messages)
        print(allmessages[-1])
        #save the id of the oldest tweet less one
        oldest = int(allmessages[-1]['id']) - 1

        #keep grabbing messages until there are no messages left to grab
        while len(new_messages) > 0:
            print(f"getting messages before {oldest}")
            channel_path = f'https://discord.com/api/channels/{test_channel_id}/messages?limit=100&before={oldest}'
            new_messages = requests.get(channel_path, headers=headers).json() 

            allmessages.extend(new_messages)

            print(f"...{len(allmessages)} messages downloaded so far")

            try:
                oldest = int(allmessages[-1]['id']) - 1
            except:
                print("Done")
                break
        message_arr = [[m['id'], m['timestamp'], m['author']['username'], m['content']] for m in allmessages]
        return message_arr
    except Exception as e: print(e)

    #message_arr = [[m['id'], m['timestamp'], m['content']]
                #for m in allmessages]
                
    #messages_df = pd.DataFrame(message_arr,
                            #columns=["Id", "Date", "content"])
    #message_arr = 
    '''
    print(len(allmessages))
    for m in allmessages:
        if type(m) == dict:
            print(m['content'])
        else:
            print(type(m))
    '''





#data = json.dumps(params)  
#print(type(data))

test_channel_id = 885948250253848588
test_guild_id = 647140436686667776

'''
testDiscord = DiscordCollection(TOKEN)
discord_messages = testDiscord.get_channel_messages(885948250253848588, count=2)
discord_arr = testDiscord.make_arr(discord_messages)
discord_df = testDiscord.make_df(discord_arr)
'''


test_twitter = TwitterCollection(TWITTER_BEARER_TOKEN)
print(test_twitter.token)
tw_user = test_twitter.get_user(screen_name="Person_of_note")
tw_user_id = tw_user.json()['data']['id']
print(tw_user_id)
test_tweets = test_twitter.get_tweets(tw_user_id, num=2)
print(test_tweets.json())



# TODO: Map random avatars to random users
'''
for x in range(1, 3):
    params = {
    'username': random.choice(usernames),
    'avatar_url': random.choice(avatar_list),
    'content': random.choice(text)
    }
    r = requests.post('https://discord.com/api/webhooks/931256796348301343/wTicpzl4unTyJZ57zEGEL4lntMotqPK1PsIc56uX682X8FixBy8_J8G8D_U-DHkjFWUc', headers=headers, data=params)
    time.sleep(random.randrange(2, 5))
'''





#get_all_messages(test_channel_id, TOKEN)

client.run(TOKEN)



# TODO Proper:
'''
    - Make a db or a bucket with various files where you can store avatars and tweets, then pick a random one

'''
