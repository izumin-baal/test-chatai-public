#!/opt/minsys-chatai/.venv_minsys-chatai/bin/python
# -*- coding: utf-8 -*-
"""
Bot sample
"""
import os
import sys
import discord
from dotenv import load_dotenv

load_dotenv('../.env')

DISCORD_BOT_CHATAI_CLIENT_SECRET = os.getenv('DISCORD_BOT_CHATAI_CLIENT_SECRET')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('test'):
        await message.channel.send('Test!')

client.run(DISCORD_BOT_CHATAI_CLIENT_SECRET)
