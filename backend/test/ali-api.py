#/home/ali/git/veed-hackathon/.venv/bin/python -m uvicorn ali-api:app --reload --host=0.0.0.0


from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import eleven_working
import openrouter
import objectdetector
import video_gen
import fall
app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#1 voice recorder from user
@app.get("/show_fal_video/{prompt}")
def show_fal_video(prompt:str):
    result=fall.createFallVideoFromImage(prompt="paint the house walls with pink color and add a dragon on the wall", imagePath="/images/house1/outside.webp")
    print("result Avatar video path:", result)
    return {"video_path": result}


# showing the avatar video overaly
@app.get("/show_video/{housenum}")
def show_video(housenum: int):
    result=video_gen.createAvatarVideo("Hello, I will be presenting you more information about this property. I am the property agent, just kidding.", filePath+"/images/house1/avatar.jpeg", housenum)
    print("result Avatar video path:", result)
    return {"video_path": result}

#2 showwing the house text
@app.get("/detect/{housenum}")
def send(housenum: str):
    text=objectdetector.getHouseObjects(housenum)
    print("Received text:", text)
    return {"text": text}



@app.get("/ask/{housenum}/{text}")
def ask_house_info(housenum:int,text: str):
    text=openrouter.askHouseInfo(1, text)
    print("Received text:", text)
    return {"text": text}

@app.get("/")
def read_hello():
    return {"message": "Root method is working"}
@app.get("/hello")

def read_hello():
    return {"message": "Hello, World!"}

@app.get("/send/{text}")
def send(text: str):
    #file_path = request.query_params.get("file_path")
    #text=eleven_working.convertSoundToText(soundFile=file_path)
    #text="This is a placeholder for the transcribed text."
    print("Received text:", text)
    return {"text": text}

@app.get("/convert/{file_path}")
def convert(file_path: str):
    #file_path = request.query_params.get("file_path")
    if not file_path:
        return {"error": "file_path parameter is required"}
    text=eleven_working.convertSoundToText(soundFile=file_path)
    #text="This is a placeholder for the transcribed text."
    return {"text": text}
@app.post("/convertpost/")
def convert(data: bytes):
    #file_path = request.query_params.get("file_path")
    if not data:
        return {"error": "data parameter is required"}
    text=eleven_working.convertSoundToText(sound=data)
    #text="This is a placeholder for the transcribed text."
    return {"text": text}


# Test the API method
client = TestClient(app)

def test_read_hello():
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)