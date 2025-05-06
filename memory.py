#!/opt/minsys-chatai/.venv_minsys-chatai/bin/python
# -*- coding: utf-8 -*-
"""
minsys CHAT AIの記憶を管理するプログラム
10秒ごとにログを参照して会話があった場合は記憶を更新する。
"""
import os
import sys
import time
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# OpenAI Setup
OPENAI_CHATAI_API_KEYS = os.getenv('OPENAI_CHATAI_API_KEYS')
OPENAI_MODEL = "gpt-4.1"
INSTRUCTIONS_FILE = "./instructions/instruction_memory.txt"
CHAT_LOG_FILE = "./logs/chat_log.txt"
MEMORY_FILE = "./logs/memory.txt"
openai_client = OpenAI(api_key=OPENAI_CHATAI_API_KEYS)

try:
    with open(INSTRUCTIONS_FILE, "r", encoding="utf-8") as f:
        instructions = f.read()
except FileNotFoundError:
    print(f"Error: The file {INSTRUCTIONS_FILE} was not found.")
    sys.exit(1)

# Function
def get_latest_message():
    """
    最新のメッセージを取得する関数
    """
    try:
        with open(CHAT_LOG_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
            if lines:
                return lines[-1].strip()
            else:
                return None
    except FileNotFoundError:
        print(f"Error: The file {CHAT_LOG_FILE} was not found.")
        return None

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

def format_openai_input_message():
    """
    Format the input message for OpenAI's API.
    """
    memory = get_memory()
    chat_log = get_chat_log()

    mem_lines  = "\n".join(line.rstrip("\n") for line in memory)
    chat_lines = "\n".join(line.rstrip("\n") for line in chat_log)

    core = (
        "<memory>\n"
        f"{mem_lines}\n"
        "</memory>\n\n"
        "<chat_log>\n"
        f"{chat_lines}\n"
        "</chat_log>\n\n"
    )

    return f"```xml\n{core}\n```"

def update_memory():
    input_message = format_openai_input_message()
    if not input_message:
        return None
    try:
        response = openai_client.responses.create(
            model=OPENAI_MODEL,
            instructions=instructions,
            input=input_message,
        )
        if response.output_text:
            with open(MEMORY_FILE, "w", encoding="utf-8") as f:
                f.write(response.output_text + "\n")
    except Exception as e:
        print(f"Error getting OpenAI response: {e}")
        return None

def main():
    latest_message = None
    while True:
        if latest_message is None:
            latest_message = get_latest_message()
        
        if latest_message != get_latest_message():
            # 最新のメッセージが更新された場合
            latest_message = get_latest_message()
            update_memory()
            
        time.sleep(10)

main()
