from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
from pydantic import BaseModel

# Define request models
class UserInput(BaseModel):
    user_input: str

class MCQRequest(BaseModel):
    text: str
    num_questions: int

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CHATBOT_SERVICE_URL = "http://localhost:8001/chat"  # URL for the Chatbot Service
MCQ_SERVICE_URL = "http://localhost:8002/generate-mcqs"  # URL for the MCQ Service

@app.post("/chat")
async def chat(user_input: UserInput): 
    async with httpx.AsyncClient(timeout=30.0) as client:  # Increase timeout to 30 seconds
        response = await client.post(CHATBOT_SERVICE_URL, json={"user_input": user_input.user_input})
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error in Chatbot Service")
        return response.json()

@app.post("/generate-mcqs")
async def generate_mcqs(mcq_request: MCQRequest):
    async with httpx.AsyncClient(timeout=30.0) as client:  # Increase timeout to 30 seconds
        response = await client.post(MCQ_SERVICE_URL, json=mcq_request.model_dump())
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error in MCQ Service")
        return response.json()

