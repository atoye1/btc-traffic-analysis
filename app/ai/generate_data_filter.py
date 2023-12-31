import pandas as pd
import openai
import os
import json
from dotenv import load_dotenv, find_dotenv

from ai.prompts import generate_parse_filter_prompt

load_dotenv(find_dotenv())
openai.api_key = os.environ['OPENAI_API_KEY']


def get_completion_from_messages(messages,
                                 model="gpt-3.5-turbo",
                                 temperature=0,
                                 max_tokens=1500):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message["content"]


def generate_data_filter(df, user_message):
    delimiter = "#####"
    messages = [
        {'role': 'system',
         'content': generate_parse_filter_prompt(df)},
        {'role': 'user',
         'content': f"{delimiter}{user_message}{delimiter}"},
    ]
    final_response = get_completion_from_messages(messages)
    print(final_response)
    final_response = final_response.replace('\'', '"')
    json_result = json.loads(final_response)
    return json_result
