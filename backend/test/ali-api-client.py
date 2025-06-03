
import requests

def testGetConvert():
    # Replace with your actual server URL
    url = "http://localhost:8000/convert/harvard.wav"
    # File path to send
    params = {"file_path": "./backend/test/harvard.wav"}  # Adjust the file path as needed
    params={}
    response = requests.get(url, params=params)
    # Output result
    print(response.json())
def testPostConvert():
    # Replace with your actual server URL
    url = "http://localhost:8000/convertpost"
    # File path to send
    #files = {"file": open("./backend/test/harvard.wav", "rb")}  # Adjust the file path as needed
    params = {"file_path": "harvard.wav"}  # Adjust the file path as needed
    
    response = requests.post(url,params=params)
    # Output result
    print(response.json())

if __name__ == "__main__":
    testPostConvert()