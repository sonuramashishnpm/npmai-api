from pydantic import BaseModel
from fastapi import FastAPI
import requests

app=FastAPI()

class LLMRequest(BaseModel):
  prompt:str
  model:str

models_state=[]

@app.post("/llm")
def handler(data:LLMRequest):
  if len(data.prompt)<=4000:
    if data.model:
      if not data.model in models_state:
        if data.model=="llama3.2":
          models_state.append(data.model)
          url="https://mountains-searched-texas-components.trycloudflare.com/llm"
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
    
  response=requests.post(url,json={"prompt":data.prompt})
  try:
    models_state.remove(data.model)
  except:
    models_state.remove(model)
  return response.json()
  
  
