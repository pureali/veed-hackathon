#works great
import sieve
import os
os.environ["SIEVE_API_KEY"] = ""
file = sieve.File(url="https://storage.googleapis.com/sieve-prod-us-central1-public-file-upload-bucket/851601dc-e4d7-436c-b37d-67003ca2ef50/dd67fad4-2e96-475f-bda5-c16fa6ef71c6-input-file.mp3")
backend = "stable-ts-whisper-large-v3-turbo"
word_level_timestamps = True
source_language = "auto"
diarization_backend = "None"
min_speakers = -1
max_speakers = -1
#custom_vocabulary = ["object Object"]
custom_vocabulary = {"Object": object}
translation_backend = "None"
target_language = ""
segmentation_backend = "ffmpeg-silence"
min_segment_length = -1
min_silence_length = 0.4
vad_threshold = 0.2
pyannote_segmentation_threshold = 0.8
chunks = []
denoise_backend = "None"
initial_prompt = ""

transcribe = sieve.function.get("sieve/transcribe")
output = transcribe.run(
    file = file,
    backend = backend,
    word_level_timestamps = word_level_timestamps,
    source_language = source_language,
    diarization_backend = diarization_backend,
    min_speakers = min_speakers,
    max_speakers = max_speakers,
    custom_vocabulary = custom_vocabulary,
    translation_backend = translation_backend,
    target_language = target_language,
    segmentation_backend = segmentation_backend,
    min_segment_length = min_segment_length,
    min_silence_length = min_silence_length,
    vad_threshold = vad_threshold,
    pyannote_segmentation_threshold = pyannote_segmentation_threshold,
    chunks = chunks,
    denoise_backend = denoise_backend,
    initial_prompt = initial_prompt
)
for output_object in output:
    print(output_object)