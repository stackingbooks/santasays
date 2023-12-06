import os
TEXT = "YOUR TEXT HERE"
TOKEN = os.environ['TOKEN']

# Do not change anything starting from here
# made by StackingBooks

import requests
import subprocess

def get_duration(file):
    """Get the duration of a video using ffprobe."""
    cmd = 'ffprobe -i {} -show_entries format=duration -v quiet -of csv="p=0"'.format(file)
    output = subprocess.check_output(
        cmd,
        shell=True, # Let this run in the shell
        stderr=subprocess.STDOUT
    )
    # return round(float(output))  # ugly, but rounds your seconds up or down
    return float(output)


CHUNK_SIZE = 1024
url = "https://api.elevenlabs.io/v1/text-to-speech/knrPHWnBmmDHMoiMeP3l"

headers = {
  "Accept": "audio/mpeg",
  "Content-Type": "application/json",
  "xi-api-key": TOKEN
}

data = {
  "text": TEXT,
  "model_id": "eleven_monolingual_v1",
  "voice_settings": {
    "stability": 0.5,
    "similarity_boost": 0.5
  }
}

response = requests.post(url, json=data, headers=headers)
with open('output.mp3', 'wb') as f:
    for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
        if chunk:
            f.write(chunk)

talk = str(os.getcwd()) + "/resources/talk.mp4"
start = str(os.getcwd()) + "/resources/start.mp4"
end = str(os.getcwd()) + "/resources/end.mp4"
audio = str(os.getcwd()) + "/output.mp3"
output = str(os.getcwd()) + "/speak.mp4"
final = str(os.getcwd()) + "/final.mp4"
length = get_duration(audio)

os.system(f'./ffmpeg-4.3-amd64-static/ffmpeg -stream_loop 1 -t {length} -i {talk} -i {audio} -c copy -y {output}')
os.system(f'./ffmpeg-4.3-amd64-static/ffmpeg -i {start} -i {output} -i {end} -filter_complex "[0:v] [0:a] [1:v] [1:a] [2:v] [2:a] concat=n=3:v=1:a=1 [v] [a]" -map "[v]" -map "[a]" -y {final}')
