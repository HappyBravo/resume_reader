import pymupdf
import json, ast, os
import openai 
from dotenv import dotenv_values

resume_file = "./Resume_June_2024.pdf" # <--- ENTER YOUR RESUME PATH HERE
output_file = "./output.json"

doc = pymupdf.open(resume_file)
doc_textt = ""
for page in doc:
  text = page.get_text()  
  # print(text)
  doc_textt += text

config = dotenv_values(".env")
openai.api_key = config["OPENAI_API"]

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0, 
    )
    return response

prompt = "this is a resume in text format. Identify the sections and return the {section : data_in_section} as json format - \n <<< "\
         + doc_textt + "\n>>>"

response = get_completion(prompt=prompt)
response_str = response.choices[0].message.content
dict_obj = ast.literal_eval(response_str)
with open("output.json", "w", encoding="utf-8") as json_f:
    json.dump(dict_obj, json_f, indent=3)
