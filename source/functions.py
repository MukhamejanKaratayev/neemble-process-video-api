import pandas as pd
from source import model
import openai 
from source import openai_api_key

def transcribe(videoLink):
    transcription_json = []
    segments, info = model.transcribe(videoLink, beam_size=5)
    for segment in segments:
        transcription_json.append({'start_time':segment.start, 'end_time':segment.end , 'text': segment.text.strip()})
    return {'language': info.language, 'transcription': transcription_json}

def summarize(transcription):
    openai.api_key = openai_api_key
    messages = [{"role": "system", "content": "An AI assistant that is an expert in video summarization."}]
    messages.append({"role": "user", "content": 'Summarize in a short but informative manner the following video based on its following script: ' + '\n'.join(transcription)})
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages, max_tokens=2048, temperature=1)
    return response.choices[0].message.content