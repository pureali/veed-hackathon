import requests
# Create transcript (POST /v1/speech-to-text)
# response = requests.post(
#   "https://api.elevenlabs.io//v1/speech-to-text",
#   headers={
#     "Xi-Api-Key": "sk_aa588e8b537bb5fe8afd96369d4a68da5c72036900432a74"
import requests

# Create transcript (POST /v1/speech-to-text)

response = requests.post(

  "https://api.elevenlabs.io//v1/speech-to-text",

  headers={"Xi-Api-Key": ""},

  data={

    'model_id': "foo",

  },

  files={

    'file', ('harvard.wav', open('./backend/test/harvard.wav', 'rb')),

  },

)

print(response.json())