ali_api_key="e47ab552-d96c-4eda-a0fa-90952150a569:bf07ce225bd857883cf67ea0f978f841"
api_key="5c585f14-c80a-4a4a-8a27-0609c74e498f:1e0fc1bc9a2ee306a908be5fb3f41fa2"
import fal_client
import os
def createFallVideoFromImage(prompt="paint the house walls with pink color and add a dragon on the wall",imagePath="/images/house1/outside.webp"):  
    os.environ["FAL_KEY"] = api_key
    filePath=os.path.dirname(os.path.abspath(__file__))
    imagePath=filePath+imagePath
    def on_queue_update(update):
        if isinstance(update, fal_client.InProgress):
            for log in update.logs:
             print(log["message"])


    file_result = fal_client.upload_file(imagePath)


    result = fal_client.subscribe(
        "fal-ai/kling-video/v1/pro/image-to-video",
        arguments={
            "prompt": prompt,
            "image_url": file_result,
        },
        with_logs=True,
        on_queue_update=on_queue_update,
    )
    print(result)

if __name__ == "__main__":
    createFallVideoFromImage(prompt="Please empty the room.",imagePath="/images/house2/bedroom1.jpeg")
    #createFallVideoFromImage(prompt="paint the house walls with pink color and add a dragon on the wall",imagePath="/images/house2/outside.webp")
    #createFallVideoFromImage(prompt="paint the house walls with pink color and add a dragon on the wall",imagePath="/images/house3/outside.webp")