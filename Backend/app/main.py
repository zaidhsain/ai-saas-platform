from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


class Query(BaseModel):
    message: str


@app.post("/chat")
def chat(query: Query):

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are a helpful AI assistant for a SaaS product."},
            {"role": "user", "content": query.message}
        ]
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=data
    )

    result = response.json()

    return {
        "answer": result["choices"][0]["message"]["content"]
    }