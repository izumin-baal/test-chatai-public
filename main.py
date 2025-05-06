#!/opt/minsys-chatai/.venv_minsys-chatai/bin/python
# -*- coding: utf-8 -*-
"""
minsys CHAT AI
ネットワーク関連の様々な機能を提供しており、ユーザーが自由テキストで求める情報を回答することができる。
ネットワークエンジニアの業務をサポートするためのAIアシスタント。
"""
import os
import sys
import datetime
import json
import re
import discord
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

from functions.tools import TOOLS
from functions.peeringdb import get_peeringdb_net_info
from functions.bgpinfo import show_route, show_route_detail, show_route_as_regex

# Discord Setup
DISCORD_BOT_CHATAI_CLIENT_SECRET = os.getenv('DISCORD_BOT_CHATAI_CLIENT_SECRET')
DISCORD_MAX_MESSAGE_LENGTH = 1800

intents = discord.Intents.default()
intents.message_content = True
discord_client = discord.Client(intents=intents)

# OpenAI Setup
OPENAI_CHATAI_API_KEYS = os.getenv('OPENAI_CHATAI_API_KEYS')
OPENAI_MODEL = "gpt-4.1-mini"
INSTRUCTIONS_FILE = "./instructions/instruction_chatai.txt"
CHAT_LOG_FILE = "./logs/chat_log.txt"
MEMORY_FILE = "./logs/memory.txt"
CHAT_LOG_MAX_LINES = 20
openai_client = OpenAI(api_key=OPENAI_CHATAI_API_KEYS)

try:
    with open(INSTRUCTIONS_FILE, "r", encoding="utf-8") as f:
        instructions = f.read()
except FileNotFoundError:
    print(f"Error: The file {INSTRUCTIONS_FILE} was not found.")
    sys.exit(1)

# Function
def save_chat_log_to_file(message, author):
    """
    Save chat log to a file with a timestamp.
    Only CHAT_LOG_MAX_LINES lines are saved.
    If the file exceeds this limit, the oldest lines are removed.
    """
    now = datetime.datetime.now()
    formatted_message = format_line_break_to_space(message)
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

    lines = get_chat_log()
    if not lines:
        lines = []
    
    if len(lines) >= CHAT_LOG_MAX_LINES:
        lines = lines[1:]
    
    lines.append(f"[{timestamp}] {author}: {formatted_message}\n")

    try:
        with open(CHAT_LOG_FILE, "w", encoding="utf-8") as f:
            f.writelines(lines)
    except Exception as e:
        print(f"Error writing to file: {e}")

def get_chat_log():
    """
    Get the chat log from the file.
    """
    try:
        with open(CHAT_LOG_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = []
    except Exception as e:
        print(f"Error reading file: {e}")
        lines = []
    
    return lines

def get_memory():
    """
    Get the memory from the file.
    """
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = []
    except Exception as e:
        print(f"Error reading file: {e}")
        lines = []
    
    return lines

def get_openai_response(message, tools=None):
    """
    Get a response from OpenAI's API.
    """

    if not message:
        return None

    try:
        response = openai_client.responses.create(
            model=OPENAI_MODEL,
            input=message,
            instructions=instructions,
            tools=tools,
            temperature=0.3,
        )
        return response
    except Exception as e:
        print(f"Error getting OpenAI response: {e}")
        return None

def format_openai_input_message(message):
    """
    Format the input message for OpenAI's API.
    """
    memory = get_memory()
    chat_log = get_chat_log()
    request = message.strip()

    mem_lines  = "\n".join(line.rstrip("\n") for line in memory)
    chat_lines = "\n".join(line.rstrip("\n") for line in chat_log)

    core = (
        "<memory>\n"
        f"{mem_lines}\n"
        "</memory>\n\n"
        "<chat_log>\n"
        f"{chat_lines}\n"
        "</chat_log>\n\n"
        "<request>\n"
        f"{request}\n"
        "</request>"
    )

    return f"```xml\n{core}\n```"


def format_line_break_to_space(message):
    """
    Replace line breaks with spaces.
    """
    return re.sub(r'[\r\n]+', ' ', message)

def format_discord_message(message):
    """
    Split the message into chunks of DISCORD_MAX_MESSAGE_LENGTH characters or less.
    """
    if len(message) <= DISCORD_MAX_MESSAGE_LENGTH:
        return [message]
    
    chunks = []
    while len(message) > DISCORD_MAX_MESSAGE_LENGTH:
        split_index = max(message.rfind('。', 0, DISCORD_MAX_MESSAGE_LENGTH), message.rfind('？', 0, DISCORD_MAX_MESSAGE_LENGTH), message.rfind(' ', 0, DISCORD_MAX_MESSAGE_LENGTH))
        if split_index == -1:
            split_index = DISCORD_MAX_MESSAGE_LENGTH
        
        chunks.append(message[:split_index])
        message = message[split_index:]
    
    if message:
        chunks.append(message)
    
    return chunks
    

# Discord Bot Event
@discord_client.event
async def on_ready():
    print(f'Start App {discord_client.user}')

@discord_client.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == discord_client.user:
        return
    
    # Ignore messages from other channels
    if message.channel.name != 'chatai':
        return

    # Save the message to a log file
    save_chat_log_to_file(message.content, message.author)

    # Get the OpenAI response
    input_message = format_openai_input_message(message.content)
    response = get_openai_response(input_message, TOOLS)
    if response:
        if not response.output_text == "":
            # 通常のメッセージ
            save_chat_log_to_file(response.output_text, "CHAT AI")
            response_message = format_discord_message(response.output_text)
            for line in response_message:
                if line:
                    await message.channel.send(line)
        elif response and hasattr(response, 'output'):
            # ツールの実行結果
            for tool_call in response.output:
                type = tool_call.type
                name = tool_call.name
                call_id = tool_call.call_id
                args = json.loads(tool_call.arguments)
                await message.channel.send(f"Function_Call実行します: {name}")
                if type == "function_call":
                    if name == "get_peeringdb_net_info":
                        asn = args.get("asn")
                        name = args.get("name")
                        result = get_peeringdb_net_info(asn=asn, name=name)
                        input_items = [{
                            "role": "user",
                            "content": format_openai_input_message(message.content),
                        }]
                        input_items.append(tool_call)
                        input_items.append({
                            "type": "function_call_output",
                            "call_id": call_id,
                            "output": str(result),
                        })
                        response = get_openai_response(input_items)
                        if not response.output_text == "":
                            save_chat_log_to_file(response.output_text, "CHAT AI")
                            response_message = format_discord_message(response.output_text)
                            for line in response_message:
                                if line:
                                    await message.channel.send(line)
                    if name == "show_route" or name == "show_route_detail":
                        prefix = args.get("prefix")
                        if name == "show_route":
                            result = show_route(prefix=prefix)
                        elif name == "show_route_detail":
                            result = show_route_detail(prefix=prefix)
                        show_command_output = result[1]
                        if len(show_command_output) > DISCORD_MAX_MESSAGE_LENGTH:
                            show_command_output = show_command_output[:DISCORD_MAX_MESSAGE_LENGTH] + "\n\nsnip..."
                        await message.channel.send('```\n' + show_command_output + '```')
                        input_items = [{
                            "role": "user",
                            "content": format_openai_input_message(message.content),
                        }]
                        input_items.append(tool_call)
                        input_items.append({
                            "type": "function_call_output",
                            "call_id": call_id,
                            "output": str(result),
                        })
                        response = get_openai_response(input_items)
                        if not response.output_text == "":
                            save_chat_log_to_file(response.output_text, "CHAT AI")
                            response_message = format_discord_message(response.output_text)
                            for line in response_message:
                                if line:
                                    await message.channel.send(line)
                    if name == "show_route_as-regex":
                        asn_regex = args.get("asn_regex")
                        result = show_route_as_regex(asn_regex=asn_regex)
                        show_command_output = result[1]
                        if len(show_command_output) > DISCORD_MAX_MESSAGE_LENGTH:
                            show_command_output = show_command_output[:DISCORD_MAX_MESSAGE_LENGTH] + "\n\nsnip..."
                        await message.channel.send('```\n' + show_command_output + '```')
                        input_items = [{
                            "role": "user",
                            "content": format_openai_input_message(message.content),
                        }]
                        input_items.append(tool_call)
                        input_items.append({
                            "type": "function_call_output",
                            "call_id": call_id,
                            "output": str(result),
                        })
                        response = get_openai_response(input_items)
                        if not response.output_text == "":
                            save_chat_log_to_file(response.output_text, "CHAT AI")
                            response_message = format_discord_message(response.output_text)
                            for line in response_message:
                                if line:
                                    await message.channel.send(line)
            

discord_client.run(DISCORD_BOT_CHATAI_CLIENT_SECRET)
