from fastapi import FastAPI, HTTPException 
from pydantic import BaseModel, create_model, ValidationError 
from typing import Optional, Dict, Any 
import requests, json 

app = FastAPI() 

class LLMRequest(BaseModel): 
    prompt: str 
    model: str 
    temperature: float = 0.7 
    validated_schema: Optional[Dict[str, Any]] = None 

Model_links = {
    "llama3.2": "https://modified-ram-periodic-addressed.trycloudflare.com/llm" 
} 

@app.post("/llm") 
async def handler(data: LLMRequest): 
    if len(data.prompt) >= 4000: 
        raise HTTPException(400, "Prompt too long") 
    
    if data.model not in Model_links: 
        raise HTTPException(400, "Model not supported") 
        
    payload = { "prompt": data.prompt, "temperature": data.temperature, } 
    url = Model_links[data.model] 

    response = requests.post(url, json=payload) 
    try:
        raw_output = response.json()["response"]
    except:
        raw_output = response.text
    
    if not data.validated_schema: 
        return {"response":raw_output}
    try:
        DynamicSchema = create_model("DynamicSchema", **data.validated_schema) 
        parsed = json.loads(raw_output) 
        validated = DynamicSchema(**parsed) 
        return validated.dict() 
    except (json.JSONDecodeError, ValidationError) as e: 
        raise HTTPException(500, f"LLM output invalid: {raw_output}") # No schema, return raw  
    
    return {"response": raw_output}
