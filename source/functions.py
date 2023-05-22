import pandas as pd
from source import model
from source import openai 


def transcribe(videoLink):
    transcription_json = []
    segments, info = model.transcribe(videoLink, beam_size=5)
    for segment in segments:
        transcription_json.append({'start_time':segment.start, 'end_time':segment.end , 'text': segment.text.strip()})
    return {'language': info.language, 'transcription': transcription_json}

def summarize(transcription):
    # openai.api_key = "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"
    messages = [{"role": "system", "content": "An AI assistant that is an expert in YouTube video script summarization."}]
    messages.append({"role": "user", "content": 'Summarize the following video based on the given script: ' + '\n'.join(transcription)})
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages, max_tokens=2048, temperature=1)
    return response.choices[0].message.content