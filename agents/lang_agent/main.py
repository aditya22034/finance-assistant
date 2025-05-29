from fastapi import FastAPI
from pydantic import BaseModel
import requests
from langchain_community.chat_models import ChatOllama  

app = FastAPI()

llm = ChatOllama(base_url="http://host.docker.internal:11434", model="mistral", temperature=4)

class SummaryRequest(BaseModel):
    query: str
    context: str

@app.post("/generate_summary")
def generate_summary(req: SummaryRequest):
    prompt = f"""You are a financial analyst. Based on the following documents, answer this question:

{req.query}

Documents:
{req.context}
"""
    try:
        response = llm.predict(prompt)
    except Exception as e:
        return {"summary": f"LLM failed to generate a summary: {str(e)}"}

    return {"summary": response}
