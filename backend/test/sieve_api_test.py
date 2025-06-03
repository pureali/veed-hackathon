import requests

def transcribe_audio(file_path, api_key, api_url="https://api.sievedata.com/v1/transcribe"):
    """
    Sends an audio file to the SieveData Transcribe API and returns the transcription result.

    Args:
        file_path (str): Path to the audio file.
        api_key (str): Your SieveData API key.
        api_url (str): The SieveData Transcribe API endpoint.

    Returns:
        dict: The API response containing the transcription.
    """
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    files = {
        "file": open(file_path, "rb")
    }
    response = requests.post(api_url, headers=headers, files=files)
    response.raise_for_status()
    return response.json()

# Example usage (replace with your actual API key and file path)
if __name__ == "__main__":
    API_KEY = "yP6kSUHtIF1prsbBRpq-sCOBXo9ZfuJmrBOq_E49RwVk"
    AUDIO_FILE = "./backend/test/harvard.wav"  # Replace with your actual audio file path
    try:
        result = transcribe_audio(AUDIO_FILE, API_KEY)
        print("Transcription:", result.get("transcription", result))
    except Exception as e:
        print("Error:", e)