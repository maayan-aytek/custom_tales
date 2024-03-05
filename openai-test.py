import openai
import json

with open('config.json', 'r') as file:
    config = json.load(file)

OPENAI_KEY = config['OPENAI_KEY']
openai.api_key = OPENAI_KEY
client = openai.OpenAI(api_key=OPENAI_KEY)


def get_response(prompt):
  completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
      {"role": "user", "content": prompt}
    ]
  )

  return completion.choices[0].message.content
