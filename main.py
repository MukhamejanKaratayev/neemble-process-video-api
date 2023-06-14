from pydantic import BaseModel, Field
from source import app
from source.functions import transcribe, summarize
from fastapi import HTTPException
from typing import List
from dotenv import load_dotenv
import requests

# Input for data validation
class VideoLink(BaseModel):
    videoKey: str = Field(..., example="9bZkp7q19f0")
    video: str = Field(..., example="https://www.youtube.com/watch?v=9bZkp7q19f0")

# Ouput for data validation
class VideoSegment(BaseModel):
    start_time: float
    end_time: float
    text: str

class Response(BaseModel):
    videoKey: str
    language: str
    transcription: str
    segments: List[VideoSegment]
    summary: str

# class Response(BaseModel):
#     key: str

# response_model=Response
@app.post('/process')
def get_prediction(videoInput: VideoLink):
    # try:
    transcription = transcribe(videoInput.video)
    transcription_str = '\n'.join([segment['text'] for segment in transcription['transcription']])
    if transcription_str == "":
        raise HTTPException(status_code=400, detail="Invalid video link. Transcription failed.")
    summary = summarize(transcription_str)
    if summary == "":
        raise HTTPException(status_code=400, detail="Invalid video link. Summarization failed.")
    
    result = {
        "videoKey": videoInput.videoKey,
        "language": transcription['language'],
        "transcription": transcription_str,
        "segments": transcription['transcription'],
        "summary": summary
    }
    
    # send the result to another API http://127.0.0.1:8000/ru/api/video/fastapi/ using POST method
    res = requests.post('http://127.0.0.1:8000/ru/api/video/fastapi/', json=result)
    return True
    # except:
    #     raise HTTPException(status_code=400, detail="Invalid video link. Process failed.")


