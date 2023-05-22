from pydantic import BaseModel, Field
from source import app
from source.functions import transcribe, summarize
from fastapi import HTTPException
from typing import List

# Input for data validation
class VideoLink(BaseModel):
    link: str = Field(..., example="https://www.youtube.com/watch?v=9bZkp7q19f0")

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

# @app.on_event('startup')
# def load_model():
#     model_size= "base"
#     model = WhisperModel(model_size, device="cpu", compute_type="int8")


@app.post('/process', response_model=Response)
async def get_prediction(videoInput: VideoLink):
    videoKey = videoInput.link.split("/")[-1].replace(".mp4", "")
    try:
        transcription = transcribe(videoInput.link)
        transcription_str = '\n'.join([segment['text'] for segment in transcription['transcription']])
        if transcription_str == "":
            raise HTTPException(status_code=400, detail="Invalid video link. Transcription failed.")
        summary = summarize(transcription_str)
        if summary == "":
            raise HTTPException(status_code=400, detail="Invalid video link. Summarization failed.")
        return {
            "videoKey": videoKey,
            "language": transcription['language'],
            "transcription": transcription_str,
            "segments": transcription['transcription'],
            "summary": summary
        }
         
    except:
        raise HTTPException(status_code=400, detail="Invalid video link. Process failed.")


