#!/opt/minsys-chatai/.venv_minsys-chatai/bin/python
# -*- coding: utf-8 -*-
"""
ChatGPT sample
"""
import os
import sys
import json
import asyncio
from openai import OpenAI
from dotenv import load_dotenv
from pprint import pprint

load_dotenv('../.env')

OPENAI_CHATAI_API_KEYS = os.getenv('OPENAI_CHATAI_API_KEYS')
OPENAI_MODEL = "gpt-4.1-mini"
TOOLS = [
    {
        "type": "function",
        "name": "add_numbers",
        "description": "2つの数を加算する関数",
        "parameters": {
            "type": "object",
            "properties": {
                "number1": {
                    "type": "number",
                    "description": "1つ目の数",
                },
                "number2": {
                    "type": "number",
                    "description": "2つ目の数",
                },
            },
            "required": ["number1", "number2"],
        },
    },
]

client = OpenAI(api_key=OPENAI_CHATAI_API_KEYS)


def add_numbers(number1, number2):
    """
    2つの数を加算する関数
    """
    return number1 + number2

def send_message_to_openai(input_items):
    """
    OpenAIにメッセージを送信する関数
    """
    
    try:
        response = client.responses.create(
            model=OPENAI_MODEL,
            input=input_items,
            tools=TOOLS,
        )
        return response
    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    input_items = [{
        "role": "user",
        "content": "3と20を加算してください。",
    }]
    print("Input Text:")
    print(input_items[0]["content"])
    response = send_message_to_openai(input_items)
    if response and hasattr(response, 'output'):
        for tool_call in response.output:
            type = tool_call.type
            name = tool_call.name
            call_id = tool_call.call_id
            args = json.loads(tool_call.arguments)
            if type == "function_call":
                if name == "add_numbers":
                    number1 = args["number1"]
                    number2 = args["number2"]
                    result = add_numbers(number1, number2)
                    input_items.append(tool_call)
                    input_items.append({
                        "type": "function_call_output",
                        "call_id": call_id,
                        "output": str(result),
                    })
                    response = send_message_to_openai(input_items)
                    print("Output Text:")
                    print(response.output_text)
    elif response and hasattr(response, 'output_text'):
        print("Output Text:")
        print(response.output_text)
    


if __name__ == "__main__":
    main()
