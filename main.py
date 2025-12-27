from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI()

class LLMRequest(BaseModel):
    prompt: str
    model: str
    temperature: float = 0.7

Model_links = {
    "llama3.2": "https://badge-charging-stylish-video.trycloudflare.com/llm"
}

@app.post("/llm")
async def handler(data: LLMRequest):
    if len(data.prompt) >= 4000:
        raise HTTPException(400, "Prompt too long")

    if data.model not in Model_links:
        raise HTTPException(400, "Model not supported")

    payload = {
        "prompt": data.prompt,
        "temperature": data.temperature,
    }

    url = Model_links[data.model]

    response=requests.post(url,json=payload)
    return response.json()["response"]
