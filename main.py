from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import httpx

app = FastAPI()

class LLMRequest(BaseModel):
    prompt: str
    model: str
    temperature: float = 0.7
    streaming: bool = False

Model_links = {
    "llama3.2": "https://progressive-continues-boxed-expect.trycloudflare.com/llm"
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
        "streaming": data.streaming
    }

    url = Model_links[data.model]

    if data.streaming:
        async def stream():
            async with httpx.AsyncClient(timeout=None) as client:
                async with client.stream("POST", url, json=payload) as r:
                    async for line in r.aiter_lines():
                        if line:
                            yield line + "\n"

        return StreamingResponse(
            stream(),
            media_type="text/event-stream"
        )

    async with httpx.AsyncClient() as client:
        r = await client.post(url, json=payload)
        r.raise_for_status()
        return r.json()
