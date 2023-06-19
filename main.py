from pydantic import BaseModel, Field
from source import app
from source.functions import transcribe, summarize
from fastapi import HTTPException
from typing import List
from dotenv import load_dotenv
import requests
from fastapi import BackgroundTasks
import json

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

# Background task
def process_video(videoInput: VideoLink):
    summary = ""
    transcription = transcribe(videoInput.video)
    transcription_str = '\n'.join([segment['text'] for segment in transcription['transcription']])
    if transcription_str == "":
        # raise HTTPException(status_code=400, detail="Invalid video link. Transcription failed.")
        transcription_str = "No transcription available."
    else:
        summary = summarize(transcription_str)
    if summary == "":
        # raise HTTPException(status_code=400, detail="Invalid video link. Summarization failed.")
        summary = "No summary available."
    
    result = {
        "videoKey": videoInput.videoKey,
        "language": transcription['language'],
        "transcription": transcription_str,
        "segments": transcription['transcription'],
        "summary": summary
    }
    print(result)
    # send the result to another API http://127.0.0.1:8000/ru/api/video/fastapi/ using POST method
    res = requests.post('http://127.0.0.1:8000/ru/api/video/fastapi/', json=json.dumps(result))
    print(res)

# response_model=Response
@app.post('/process')
async def get_prediction(videoInput: VideoLink, background_tasks: BackgroundTasks):
    # try:
    background_tasks.add_task(process_video, videoInput)
    return {"message": "Video is being processed."}
    # except:
    #     raise HTTPException(status_code=400, detail="Invalid video link. Process failed.")


