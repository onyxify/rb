import requests
import os
import re

COMMENT_API_URL = "https://api-inference.huggingface.co/models/KunalK2/Redditcommentbot"
API_TOKEN = os.environ['HF_API_KEY']
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def comment_generator(topic):
  payload = {
        "inputs": f"Create a rude comment about: {topic}. Comment: ",
        "parameters": {
          "max_length": 300,
          "top_k": 10,
          "temperature": 0.5,
          "repetition_penalty": 1.5
        }
      }
  response = requests.post(COMMENT_API_URL, headers=headers, json=payload)
  return response.json()
  
try:
  output = comment_generator('News')[0]['generated_text']
except:
  output='The reddit bot is waking up, please refresh the page in 10 seconds'
print(output)

#########################################

def process_comment(comment):
  index = comment.find("Comment:")
  try:
      comment = comment[index + len("Comment:"):].strip()
      return comment
  except:
      return comment

processed_output = process_comment(output)

#########################################

CONVO_API_URL = "https://api-inference.huggingface.co/models/BlueandOrangeBoi/argument_bot"

def convo_generator(output):
  payload = {
    "inputs": f"$$$Bot_1: {output} \n$$$Bot_2: ",
    "parameters": {
      "max_length": 500,
      "top_k": 20,
      "temperature": 0.5,
      #"repetition_penalty": 1.5
    }
  }
  response = requests.post(CONVO_API_URL, headers=headers, json=payload)
  return response.json()

try:
  convo = convo_generator(processed_output)[0]['generated_text']
except:
  convo = "loading"
print(convo)

#########################################

def extract_comments(input_string):
    comments = re.split(r'\$\$\$Bot_\d+:', input_string)
    return [comment.strip() for comment in comments if comment.strip()]

convo = extract_comments(convo)
print(convo)