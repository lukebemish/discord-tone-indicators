# bot.py
import os

import discord
from dotenv import load_dotenv
import random

load_dotenv(dotenv_path=".envvars")
TOKEN = os.getenv('DISCORD_TOKEN')

activity=discord.Game(name='Not sure what /s means? Confused by all the /hj\'s?\r\nReact to a message with "❔" to find out what it\'s all about!\r\n(That\'s the :grey_question: emoji)')

client = discord.Client(activity=activity)

key = {
    "j":"joking",
    "hj":"half-joking",
    "s":"sarcastic",
    "srs":"serious",
    "p":"platonic",
    "r":"romantic",
    "l":"lyrics",
    "ly":"lyrics",
    "t":"teasing",
    "nm":"not mad",
    "nc":"negative connotation",
    "pc":"positive connotation",
    "neg":"negative connotation",
    "pos":"positive connotation",
    "lh":"lighthearted",
    "nbh":"nobody here",
    "m":"metaphorically",
    "li":"literally",
    "rh":"rhetorical question",
    "rt":"rhetorical question",
    "gen":"genuine question",
    "hyp":"hyperbole",
    "c":"copypasta",
    "sx":"sexual intent",
    "x":"sexual intent",
    "nsx":"non-sexual intent",
    "nx":"non-sexual intent",
    "th":"threat",
    "cb":"clickbait",
    "f":"fake",
    "g":"genuine"
    
}

def text_parser(message):
    text = message.content
    inside_slash = False
    parsed = []
    parsing = ""
    for j,i in enumerate(text):
        if i == '/':
            inside_slash = True
            parsing = ""
        elif inside_slash:
            if i.isalnum():
                parsing+=i
            else:
                if (i==',' or i==' ') and ((parsing in key.keys()) or parsing==''):
                    if parsing in key.keys():
                        parsed.append(parsing)
                    parsing = ''
                else:
                    inside_slash = False
    if parsing in key.keys():
        parsed.append(parsing)
    if len(parsed)==0:
        return getRealName(message) + " wasn't using any tone indicators that I know of!"
    return getRealName(message)+" was using tone indicators: "+', '.join(key[e].capitalize() for e in set(parsed))

def getRealName(event):
    try:
        if event.author.nick != None:
            return event.author.nick
        else:
            return event.author.name
    except:
        return event.author.name

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_raw_reaction_add(payload):
    channel = client.get_guild(payload.guild_id).get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    #print(payload.emoji.name)
    if payload.emoji.name == "❔":
        await message.channel.send(text_parser(message),reference=message)
        reactions = [i for i in message.reactions if i.emoji=="❔"]
        print(reactions)
        if len(reactions)>0:
            await reactions[0].clear()

client.run(TOKEN)
