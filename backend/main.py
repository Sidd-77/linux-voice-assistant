import os
import base64
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv
import speech_recognition as sr
from fastapi.middleware.cors import CORSMiddleware
import json

# Load environment variables
load_dotenv()

# Configure the Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to the URL of your frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Query(BaseModel):
    query: str


# Sample prompt template
PROMPT_TEMPLATE = """
You are given a task where you need to provide a Bash command that can be directly executed in a Bash script. The command should resolve the issue described below, and your response should follow these rules:

1. Provide the commands in the form of bash script to solve the problem.
2. Include a small description explaining what each command does.
3. Return the result in JSON format so that it can be parsed easily.
4. Each JSON object should have the following structure:
   - "bash script": The actual Bash script to be executed.
   - "description": Just small explanation of what the script does. Don't mention the word script itself in the description.

Here is the issue you need to resolve:
{query}

Please return only the JSON object in your response.
Don't include any additional text like ``` or comments in your response.
return in stringfyed json format
"""

@app.post("/query")
async def process_query(query: Query):
    print(f"Received query: {query.query}")
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")  
        prompt = PROMPT_TEMPLATE.format(query=query.query)
        response = model.generate_content(prompt)
        jsondata = json.loads(response.text)
        with open('script.sh', 'w') as f:
            f.write(jsondata.get('bash script'))
        os.system('chmod +x script.sh')
        os.system('bash script.sh')


        # Return the generated content
        return {response.text}
    except Exception as e:
        print(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

def listen_and_transcribe():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    
    try:
        print("Transcribing...")
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Speech recognition could not understand audio"
    except sr.RequestError as e:
        return f"Could not request results from speech recognition service; {e}"

@app.get("/record_and_process")
async def record_and_process():
    try:
        # Listen and transcribe audio
        transcribed_text = listen_and_transcribe()

        # Process the transcribed text using Gemini
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(f"Analyze the following transcribed speech: {transcribed_text}")

        # Return the generated content
        return {"transcription": transcribed_text, "analysis": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)