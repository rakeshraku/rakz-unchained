
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import json

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_input = data.get("message", "")
    if not user_input:
        return {"response": "No message provided."}

    try:
        response = subprocess.check_output(
            ["ollama", "run", "llama3", user_input],
            stderr=subprocess.STDOUT,
            timeout=30
        )
        return {"response": response.decode()}
    except subprocess.CalledProcessError as e:
        return {"response": f"Error: {e.output.decode()}"}
