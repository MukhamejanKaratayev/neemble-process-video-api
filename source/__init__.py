# Imports
from fastapi import FastAPI
from faster_whisper import WhisperModel
import openai
# Initialize FastAPI app
app = FastAPI(title="Neemble ML API", description="Transcribe and summarize video", version="1.0")

# Load model
model_size = "base"
model = WhisperModel(model_size, device="cpu", compute_type="int8")

openai.api_key = "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"