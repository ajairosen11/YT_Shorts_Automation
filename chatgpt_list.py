import openai
from dotenv import load_dotenv
import os
import re
import pandas as pd

load_dotenv()
API_KEY=os.environ.get('API_KEY')
openai.api_key=API_KEY

def chatresponse(input):
    output=openai.ChatCompletion.create(
    model='gpt-3.5-turbo',
    messages=[{"role":"user",
    "content":
              input }]
    )
    content = output['choices'][0]['message']['content']
    pattern = r'^\d{1,3}\.'
    cleaned_str = re.sub(pattern, '', content, flags=re.MULTILINE)
    output_list = cleaned_str.split('\n')
    output_list = [item.strip() for item in output_list if item.strip()]
    return output_list

Content=chatresponse('give 20 fact jokes')
pd.DataFrame(Content,columns=['Content']).to_excel('Content.xlsx',index=False)