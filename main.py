from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from fastapi import FastAPI
import requests

app=FastAPI()

class LLMRequest(BaseModel):
  prompt:str
  model:str
  temperature:float=0.7
  streaming:bool=False
  
Model_links={
  "llama3.2":"url",
  "gemma:3b":"url",
  "llama3.1":"url",
  "phi-3":"url",
}

models_state=[]

@app.post("/llm")
def handler(data:LLMRequest):
  if len(data.prompt)> = 4000:
    raise HTTPException(400,"Prompt too long please shorten it")

  if not data.model in Model_links:
    raise HTTPException(400,"Please check the model name you entered if typo mistake so please correct that or if model name is correct then sorry we do not have the requested model")

  url=Model_links[data.model]

  payload={
    "prompt":data.prompt,
    "temperature":data.temperature,
    "streaming":data.streaming
  }
  if data.streaming:
    def stream():
      with requests.post(url,json=payload,stream=True) as r:
        for line in r.iter_lines():
          if line:
            yield line.decode() +"\n"
    return StreamingResponse(stream(), media_type="text/plain")
  r=requests.post(url,json=payload)
  r.raise_for_status()
  return r.json()
  
          
  
    
    
