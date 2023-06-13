# Imports
from fastapi import FastAPI
from faster_whisper import WhisperModel
from dotenv import load_dotenv
import os
# import openai
# Initialize FastAPI app
app = FastAPI(title="Neemble ML API", description="Transcribe and summarize video", version="1.0")

# Load model
model_size = "base"
model = WhisperModel(model_size, device="cpu", compute_type="int8")

# Load OpenAI API key
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

# openai.api_key = "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"