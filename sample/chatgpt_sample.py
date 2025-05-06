#!/opt/minsys-chatai/.venv_minsys-chatai/bin/python
# -*- coding: utf-8 -*-
"""
ChatGPT sample
"""
import os
import sys
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv('../.env')

OPENAI_CHATAI_API_KEYS = os.getenv('OPENAI_CHATAI_API_KEYS')
OPENAI_MODEL = "gpt-4.1-mini"

client = OpenAI(api_key=OPENAI_CHATAI_API_KEYS)

input_text = "こんにちは。あなたは誰ですか？"

response = client.responses.create(
    model=OPENAI_MODEL,
    input=input_text,
)

print("Input:")
print(input_text)
print("Output:")
print(response.output_text)
