api_key="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"
from openai import OpenAI

client = OpenAI(
  api_key="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"
)

completion = client.chat.completions.create(
  model="gpt-4o-mini",
  store=True,
  messages=[
    {"role": "user", "content": "write a haiku about ai"}
  ]
)

print(completion.choices[0].message);