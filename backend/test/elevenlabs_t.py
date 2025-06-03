import requests

API_KEY = "sk_aa588e8b537bb5fe8afd96369d4a68da5c72036900432a74"
AUDIO_FILE_PATH = "./backend/test/harvard.wav"  # Supported formats: mp3, wav, m4a, etc.

def speech_to_text(audio_path):
    url = "https://api.elevenlabs.io/v1/speech-to-text"

    headers = {
            "xi-api-key": API_KEY,
            "Content-Type": "application/json",
            #"model_id": "scribe_v1"
            
        
    }
    data={

    'model_id': "scribe_v1",

  },
    files = {
       # 'model_id': (None, "scribe_v1"),
        'audio': open(audio_path, 'rb'),
        
    }

    response = requests.post(url, headers=headers,data=data,files=files)

    if response.status_code == 200:
        data = response.json()
        transcript = data.get("text", "")
        print("Transcript:", transcript)
    else:
        print("Error:", response.status_code, response.text)

# Example usage
speech_to_text(AUDIO_FILE_PATH)