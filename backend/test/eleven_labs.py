import requests

ELEVENLABS_API_KEY = "sk_aa588e8b537bb5fe8afd96369d4a68da5c72036900432a74"
VOICE_ID = "YOUR_VOICE_ID"
#API_URL = f"https://api.elevenlabs.io/v1/speech-to-text/{VOICE_ID}"
API_URL = f"https://api.elevenlabs.io/v1/speech-to-text/"
def speech_to_text(audio_file_path):
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
    }
    files = {
        "audio": open(audio_file_path, "rb"),
    }
    response = requests.post(API_URL, headers=headers, files=files)
    response.raise_for_status()
    return response.json()["text"]

if __name__ == "__main__":
    audio_path = "./backend/test/harvard.wav"
    text = speech_to_text(audio_path)
    print("Transcribed text:", text)