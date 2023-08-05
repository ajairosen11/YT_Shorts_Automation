import openai
from dotenv import load_dotenv
import os
import re
import pandas as pd
import requests
import speech_recognition as sr
from pydub import AudioSegment
from moviepy.editor import VideoFileClip, TextClip, concatenate_videoclips, AudioFileClip
load_dotenv()

API_KEY=os.environ.get('API_KEY')
openai.api_key=API_KEY

def chatresponse(input):
    output=openai.ChatCompletion.create(
    model='gpt-3.5-turbo',
    messages=[{"role":"user",
    "content":
              input }]
    )
    content = output['choices'][0]['message']['content']
    pattern = r'^\d{1,3}\.'
    cleaned_str = re.sub(pattern, '', content, flags=re.MULTILINE)
    output_list = cleaned_str.split('\n')
    output_list = [item.strip() for item in output_list if item.strip()]
    return output_list

api_key_el=os.environ.get('API_eleven_labs')

def text_to_audio(text):
    #https://api.elevenlabs.io/v1/voices Use this URL for different voices
    url = "https://api.elevenlabs.io/v1/text-to-speech/Zlb1dXrM653N07WRdFW3"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key":api_key_el,
    }
    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.5},
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        with open('C:\\Users\\ajai\sh\\text_to_audio.mp3', 'wb') as f:
            f.write(response.content)
    else:
        print(f"Error: {response.status_code} - {response.text}")

def convert_mp3_to_wav(mp3_file):
    audio = AudioSegment.from_mp3(mp3_file)
    audio.export(mp3_file.split(".")[0]+".wav", format='wav')
text_to_audio_file='text_to_audio.mp3'

def add_audio_and_subtitles(video_file, audio_file):
    video_clip = VideoFileClip(video_file)
    audio_clip = AudioFileClip(audio_file)
    video_clip = video_clip.set_audio(audio_clip)
    audio_duration = audio_clip.duration
    trimmed_video_clip = video_clip.subclip(0, audio_duration)
    trimmed_video_path = "video_with_audio.mp4"
    trimmed_video_clip.write_videofile(trimmed_video_path)