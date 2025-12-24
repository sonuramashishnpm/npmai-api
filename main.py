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
  

models_state=[]

@app.post("/llm")
def handler(data:LLMRequest):
  if len(data.prompt)<=4000:
    if data.model:
      if not data.model in models_state:
        if data.model=="llama3.2":
          models_state.append(data.model)
          url="https://herein-faculty-flickr-outline.trycloudflare.com/llm"
        elif data.model=="gemma:3b":
          models_state.append(data.model)
          url=""
        else:
          return "Sorry your requested model is not available here use another model like and also check wheather the model name is correct or not."
      else:
        model="llama3.1"
        if not model in models_state:
          url="url"
          models_state.append(model)
        else:
          model="phi-3"
          if not model in models_state:
            url="url"
            models_state.append(model)



    else:
      return "Please when you are calling the class then specify model name also you want to use."
  else:
    return "Sorry your prompt should be less than 4000 but length of prompt that you sent us is not satisfying condition"
  
  
  
  
  
  
  if data.streaming==True:
    def _stream_response():
      with requests.post(url, json={"prompt": data.prompt, "temperature": data.temperature}, stream=True) as response:
        if response:
          try:
            models_state.remove(data.model)
          except:
            models_state.remove(model)
        for line in response.iter_lines():
          if line:
            yield line.decode("utf-8") + "\n"
    return StreamingResponse(_stream_response(),media_type="text/plain")
            
  else:
    response=requests.post(url,json={"prompt":data.prompt,"temperature":data.temperature})
    if response:
      try:
        models_state.remove(data.model)
      except:
        model_state.remove(model)
    return response.json()
