import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai

# Set up Google Generative AI
os.environ["GOOGLE_API_KEY"] = "AIzaSyA-HQh0RjFUSupgVyezUdKNmAOWGoClw1c"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel("models/gemini-1.5-pro")

# Define request and response models
class MCQRequest(BaseModel):
    text: str
    num_questions: int

class MCQResponse(BaseModel):
    mcqs: str

app = FastAPI()

def Question_mcqs_generator(input_text: str, num_questions: int) -> str:
    prompt = f"""
    You are an AI assistant helping the user generate multiple-choice questions (MCQs) based on the following text:
    '{input_text}'
    Please generate {num_questions} MCQs from the text. Each question should have:
    - A clear question
    - Four answer options (labeled A, B, C, D)
    - The correct answer clearly indicated
    Format:
    ## MCQ
    Question: [question]
    A) [option A]
    B) [option B]
    C) [option C]
    D) [option D]
    Correct Answer: [correct option]
    """
    response = model.generate_content(prompt).text.strip()
    return response

@app.post("/generate-mcqs", response_model=MCQResponse)
async def generate_mcqs(request: MCQRequest):
    try:
        mcqs = Question_mcqs_generator(request.text, request.num_questions)
        return MCQResponse(mcqs=mcqs)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
