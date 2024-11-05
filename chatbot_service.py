# AIzaSyA-HQh0RjFUSupgVyezUdKNmAOWGoClw1c
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai

# Define request model
class UserInput(BaseModel):
    user_input: str

app = FastAPI()


os.environ["GOOGLE_API_KEY"] = "AIzaSyA-HQh0RjFUSupgVyezUdKNmAOWGoClw1c"  
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel("models/gemini-1.5-pro")

@app.post("/chat")
async def chat(user_input: UserInput):
    prompt = f"You are Professional in solving problems, debugging codes, and in content writing and generation. Respond to the following conversation:\nUser: {user_input.user_input}\nAssistant:"
    
    try:
      
        response = model.generate_content(prompt).text.strip()
        return {"response": response}
    
    except Exception as e:
       
        print(f"Error generating response: {e}")  

       
        raise HTTPException(status_code=500, detail="Internal Server Error: Unable to generate response.")

