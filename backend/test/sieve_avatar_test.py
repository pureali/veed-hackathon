import sieve
import os
filePath = os.path.dirname(os.path.abspath(__file__))
os.environ["SIEVE_API_KEY"] = "P6kSUHtIF1prsbBRpq-sCOBXo9ZfuJmrBOq_E49RwVk"
import eleven_working
import fal_client
import os
 

os.environ["FAL_KEY"] = "e47ab552-d96c-4eda-a0fa-90952150a569:bf07ce225bd857883cf67ea0f978f841"


def generate_avatar(text, image_path):
    
    #local_file = sieve.File("path/to/file.txt")
    #source_image = sieve.File(url="https://storage.googleapis.com/sieve-prod-us-central1-public-file-upload-bucket/8fc8d3b1-1f24-4f31-b052-cc980b60e713/6e393753-4e5b-41e6-8b14-b8a322b7a267-input-source_image.jpg")
    print("image_path:", image_path)
    file_result = fal_client.upload_file(image_path)
    source_image = sieve.File(url=file_result)
    print("file_result:", image_path)
    soundPath=filePath+"/sound.mp3"
    eleven_working.convertTextToSound(text)
    print("sound_path:", soundPath)
    
    sound_result = fal_client.upload_file(soundPath)
    driving_audio = sieve.File(sound_result)

    #driving_audio = sieve.File(url="https://storage.googleapis.com/sieve-prod-us-central1-public-file-upload-bucket/8fc8d3b1-1f24-4f31-b052-cc980b60e713/6e393753-4e5b-41e6-8b14-b8a322b7a267-input-driving_audio.wav")
    backend = "hedra-character-2"
    aspect_ratio = "-1"
    enhancement = "none"
    resolution = "512"
    whole_body_mode = False
    crop_head = False
    expressiveness = 1

    portrait_avatar = sieve.function.get("sieve/portrait-avatar")
    output = portrait_avatar.run(
        source_image = source_image,
        driving_audio = driving_audio,
        backend = backend,
        aspect_ratio = aspect_ratio,
        enhancement = enhancement,
        resolution = resolution,
        whole_body_mode = whole_body_mode,
        crop_head = crop_head,
        expressiveness = expressiveness
    )
    print("Avatar generation completed successfully.")
    print("Output URL:{0}".format(output.url))
    videoPath=output.path
    return videoPath
if __name__ == "__main__":
    # Example usage
    text = "Hello, this is a test avatar video."
    image_path = filePath + "/images/house1/avatar.jpeg"  # Replace with your actual image path
    avatar_video_path = generate_avatar(text, image_path)
    print("Avatar video created successfully at:", avatar_video_path)