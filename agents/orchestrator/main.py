
from fastapi import FastAPI, Request
from pydantic import BaseModel
import requests

app = FastAPI()

class Question(BaseModel):
    query: str

@app.post("/ask")
def answer_question(payload: Question):
    try:
        query = payload.query
        alloc_resp = requests.get("http://api_agent:8001/asia_tech_allocation")
        earnings_resp = requests.get("http://api_agent:8001/earnings_surprises")
        alloc = alloc_resp.json()
        earnings = earnings_resp.json()
        asia_pct = alloc.get("asia_tech_percent", "N/A")
        tsmc_surprise = earnings.get("TSMC", {}).get("surprise_percent", "N/A")
        samsung_surprise = earnings.get("Samsung", {}).get("surprise_percent", "N/A")

        retrieval_resp = requests.get("http://retriever_agent:8003/retrieve", params={"query": query})
        chunks = retrieval_resp.json()
        context = "\n---\n".join([chunk["text"] for chunk in chunks])

        lang_resp = requests.post(
            "http://lang_agent:8005/generate_summary",
            json={"query": query, "context": context}
        )

        lang_json = lang_resp.json()
        summary = lang_json.get("summary", "")

        final_response = (
            f"Today, your Asia tech allocation is {asia_pct}% of AUM.\n"
            f"TSMC earnings surprise: {tsmc_surprise}%. Samsung: {samsung_surprise}%.\n"
            f"{summary}"
        )

        return {"text": final_response}

    except Exception as e:
        return {"error": str(e)}
