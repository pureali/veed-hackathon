import requests
from elevenlabs import ElevenLabs
import os
filePath=os.path.dirname(os.path.abspath(__file__))
def convertTextToSound(text):
    stability=0.5
    similarity_boost=0.75
    api_key=""
    #text=TEXT,
    #voice_id="9BWtsMINqrJLrRacOk9x"#female
    voice_id="CYw3kZ02Hs0563khs1Fj"
    output_file=filePath+"/sound.mp3"
    
    # ElevenLabs API endpoint
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    
    # Headers
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }
    
    # Request body
    data = {
        "text": text,
        "voice_settings": {
            "stability": stability,
            "similarity_boost": similarity_boost
        }
    }
    
    try:
        # Make the API request
        response = requests.post(url, headers=headers, json=data)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Save the audio content to a file
            with open(output_file, "wb") as f:
                f.write(response.content)
            print(f"Audio file saved successfully to: {output_file}")
            return True
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False
   
def convertSoundToText(soundbytes):
  
  with open("./sound.wav", "wb") as binary_file:
  
    binary_file.write(soundbytes)
    binary_file.close()
  soundFile = "./sound.wav"
  headers = {
      'Xi-Api-Key': 'sk_aa588e8b537bb5fe8afd96369d4a68da5c72036900432a74',
      # requests won't add a boundary if this header is set when you pass files=
      # 'Content-Type': 'multipart/form-data',
  }

  files = {
      'model_id': (None, 'scribe_v1'),
      'file': ('harvard.wav', open(soundFile, 'rb'), 'audio/wav'),
  }

  response = requests.post('https://api.elevenlabs.io//v1/speech-to-text', headers=headers, files=files)
  result=response.json()["text"]
  print(response.json()["text"])
  return result
if __name__ == "__main__":
    
    convertTextToSound(text="The first move is what sets everything in motion.")