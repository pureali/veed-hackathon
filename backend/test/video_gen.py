import cv2
import os
import cv2
import os
import numpy as np
from natsort import natsorted
from moviepy.audio.fx.all import audio_loop 
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_audio
import tempfile
from natsort import natsorted  # For natural sorting of filenames
filePath = os.path.dirname(os.path.abspath(__file__))

houseImagesPath = filePath + "/images/house2"
import sieve_avatar_test
def create_video_from_images_with_pauses(image_folder, output_video, fps=30, image_size=None, pause_duration=1.0):
    """
    Create a video from a sequence of images with pauses between them.
    
    Args:
        image_folder (str): Path to folder containing images
        output_video (str): Path to output video file (e.g., 'output.mp4')
        fps (int): Frames per second of output video
        image_size (tuple): Desired (width, height) of output frames. If None, uses size of first image.
        pause_duration (float): Duration of pause between images in seconds
    """
    # Get all image files from the folder
    images = [img for img in os.listdir(image_folder) if img.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
    
    if not images:
        print("No images found in the specified folder!")
        return
    
    # Sort images naturally (so frame_1.jpg comes before frame_10.jpg)
    images = natsorted(images)
    
    # Determine frame size from first image if not specified
    if image_size is None:
        first_image = cv2.imread(os.path.join(image_folder, images[0]))
        image_size = (first_image.shape[1], first_image.shape[0])
    
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for MP4
    video_writer = cv2.VideoWriter(output_video, fourcc, fps, image_size)
    
    # Calculate how many frames to add for the pause duration
    pause_frames = int(fps * pause_duration)
    
    for image_name in images:
        image_path = os.path.join(image_folder, image_name)
        frame = cv2.imread(image_path)
        
        if frame is None:
            print(f"Warning: Could not read image {image_name}")
            continue
            
        # Resize frame if necessary
        if (frame.shape[1], frame.shape[0]) != image_size:
            frame = cv2.resize(frame, image_size)
        
        # Write the image frame
        video_writer.write(frame)
        print(f"Added frame: {image_name}")
        
        # Create pause by duplicating the frame
        for _ in range(pause_frames):
            video_writer.write(frame)
        print(f"Added {pause_frames} pause frames after {image_name}")
    
    video_writer.release()
    print(f"Video with pauses successfully created at: {output_video}")

# Example usage
def overlay_videos(base_video_path, overlay_path, output_path, position, alpha):
    """Overlay one video on top of another"""
    base_cap = cv2.VideoCapture(base_video_path)
    overlay_cap = cv2.VideoCapture(overlay_path)
    
    # Get video properties
    width = int(base_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(base_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = base_cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    while True:
        ret_base, base_frame = base_cap.read()
        ret_overlay, overlay_frame = overlay_cap.read()
        
        if not ret_base:
            break
        
        # If overlay video is shorter, restart it
        if not ret_overlay:
            overlay_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            _, overlay_frame = overlay_cap.read()
        
        # Resize overlay to maintain its aspect ratio if needed
        oh, ow = overlay_frame.shape[:2]
        if oh > height - position[1] or ow > width - position[0]:
            scale = min((height - position[1])/oh, (width - position[0])/ow)
            overlay_frame = cv2.resize(overlay_frame, None, fx=scale, fy=scale)
            oh, ow = overlay_frame.shape[:2]
        
        # Overlay processing
        overlay_frame = overlay_frame[:min(oh, height-position[1]), :min(ow, width-position[0])]
        oh, ow = overlay_frame.shape[:2]
        
        # Region of interest in base frame
        roi = base_frame[position[1]:position[1]+oh, position[0]:position[0]+ow]
        
        # Blend the overlay
        blended = cv2.addWeighted(overlay_frame, alpha, roi, 1 - alpha, 0)
        base_frame[position[1]:position[1]+oh, position[0]:position[0]+ow] = blended
        
        writer.write(base_frame)
    
    base_cap.release()
    overlay_cap.release()
    writer.release()
def create_video_with_overlay_and_audio(
        overlay_video_path, 
        output_video, 
        fps=30, 
        image_size=None, 
        pause_duration=1.0,
        overlay_position=(0, 0),
        overlay_alpha=0.7):
   
    
    # Create temporary files
    temp_dir = tempfile.mkdtemp()
    base_video_path = filePath+"/video.mp4"
    overlay_video_no_audio_path = os.path.join(temp_dir, "temp_overlay_no_audio.mp4")
    temp_audio_path = os.path.join(temp_dir, "temp_audio.mp3")
    
    try:
        # 1. Create base video from images
        #create_base_video(image_folder, base_video_path, fps, image_size, pause_duration)
        create_video_from_images_with_pauses(houseImagesPath,filePath+"/video.mp4")
        # 2. Extract audio from overlay video
        ffmpeg_extract_audio(overlay_video_path, temp_audio_path)
        
        # 3. Create overlay video without audio (for processing)
        overlay_clip = VideoFileClip(overlay_video_path)
        overlay_clip.without_audio().write_videofile(overlay_video_no_audio_path, codec='libx264')
        
        # 4. Combine videos with overlay
        combined_video_path = filePath+"/combined_video.mp4"
        overlay_videos(base_video_path, overlay_video_no_audio_path, combined_video_path, overlay_position, overlay_alpha)
        
        # 5. Add audio to final video
        final_clip = VideoFileClip(combined_video_path)
        audio_clip = AudioFileClip(temp_audio_path)
        
        # Make audio same duration as video (looping if necessary)
        if audio_clip.duration < final_clip.duration:
            # Loop audio if it's shorter than video
            audio_clip= audio_loop(audio_clip, duration=final_clip.duration)
            #audio_clip = audio_clip.loop(duration=final_clip.duration)
            
            
        else:
            # Trim audio if it's longer than video
            audio_clip = audio_clip.subclip(0, final_clip.duration)
        
        final_clip = final_clip.set_audio(audio_clip)
        final_clip.write_videofile(output_video, codec='libx264', audio_codec='aac')
        
        print(f"Final video with overlay and audio created at: {output_video}")
        
    finally:
        # Clean up temporary files
        for f in [base_video_path, overlay_video_no_audio_path, temp_audio_path, combined_video_path]:
            if os.path.exists(f):
                os.remove(f)
        os.rmdir(temp_dir)
def createAvatarVideo(text,image_path,houseNum):
    
    houseImagesPath = filePath + "/images/house{0}".format(houseNum)
    avatar_video_path=sieve_avatar_test.generate_avatar(text, image_path)
    output_video = houseImagesPath+"/output.mp4"
    create_video_with_overlay_and_audio(overlay_video_path=avatar_video_path,
                                        output_video=output_video,
                                        fps=30, 
                                        image_size=None, 
                                        pause_duration=1.0,
                                        overlay_position=(100, 200),  # Position of overlay video
                                        overlay_alpha=0.6)  # Transparency of overlay video
    print("Avatar video created successfully at:", output_video)
    return output_video
if __name__ == "__main__":
    #3
    result=createAvatarVideo("Hello, I will be presenting you more information about this property. This house has 4 rooms. I am the property agent. I am just kidding hehe. This content is AI generated", filePath+"/images/house1/avatar.jpeg", 1)
    print("result Avatar video path:", result)
    #2
    # image_folder = houseImagesPath  # Replace with your image folder path
    # output_video = houseImagesPath+"/output.mp4"  # Output video filename
    # overlay_video = houseImagesPath+"/avatar.mp4"  # Overlay video filename
    # create_video_with_overlay_and_audio(overlay_video_path=overlay_video,
    #                                     output_video=output_video,
    #                                     fps=30, 
    #                                     image_size=None, 
    #                                     pause_duration=1.0,
    #                                     overlay_position=(100, 200),  # Position of overlay video
    #                                     overlay_alpha=0.6)  # Transparency of overlay video
    #1
    #  Create video with 1-second pauses between images
    # create_video_from_images_with_pauses(
    #     image_folder, 
    #     output_video, 
    #     fps=30, 
    #     pause_duration=1.0  # 1 second pause
    # )
    # overlay_videos(output_video, overlay_video, houseImagesPath+"/final_output.mp4", position=(100, 200), alpha=0.6)
    print("Video creation and overlay completed successfully.")