from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.chat_model import get_response


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatInput(BaseModel):
    message: str

@app.post("/chat")
async def chat_endpoint(chat_input: ChatInput):
    response = get_response(chat_input.message)
    return {"response": response}
