from fastapi import FastAPI
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import requests

app = FastAPI()

model = SentenceTransformer('all-MiniLM-L6-v2')
index = faiss.IndexFlatL2(384)
docs = []
metadata = []

@app.on_event("startup")
def load_embeddings():
    global docs, metadata
    articles = requests.get("http://scraper_agent:8002/scrape_filings").json()
    # articles = requests.get("http://localhost:8002/scrape_filings").json()

    texts = [article["text"] for article in articles if "text" in article]

    if not texts:
        raise ValueError("No texts retrieved from scraper_agent. Cannot build embeddings.")

    embeddings = model.encode(texts)

    if embeddings is None or len(embeddings) == 0:
        raise ValueError("Embeddings are empty or invalid.")

    embedding_array = np.array(embeddings).astype("float32")
    if embedding_array.ndim != 2 or embedding_array.shape[0] == 0:
        raise ValueError("Embeddings must be a non-empty 2D array.")

    index.add(embedding_array)
    docs = texts
    metadata = [article.get("title", "No Title") for article in articles]


@app.get("/retrieve")
def retrieve(query: str):
    embedding = model.encode([query])
    D, I = index.search(np.array(embedding).astype("float32"), k=3)
    results = [{"title": metadata[i], "text": docs[i]} for i in I[0]]
    return results
