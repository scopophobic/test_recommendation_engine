from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Any
from utils.recommender import recommend_tests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify like ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],  # OR ["GET", "POST", "OPTIONS"]
    allow_headers=["*"],
)
class PromptInput(BaseModel):
    prompt: str

class PromptRequest(BaseModel):
    prompt: str
    top_k: int = 5

@app.get("/")
def read_root():
    return {"message": "SHL Recommender API is up 🚀"}

@app.post("/recommend")
async def recommend(payload: PromptRequest):
    recommendations = recommend_tests(payload.prompt, payload.top_k)
    results = []
    for score, test in recommendations:
        results.append({
            "name": test.get("name", "Unnamed"),
            "link": test.get("link", "#"),
            "duration": test.get("assessment_length", "N/A"),
            "keys": test.get("keys", []),
            "score": score,
            "remote": test.get("is_remote", False),
            "adaptive": test.get("is_adaptive", False),
            "job_levels": test.get("job_levels", []),
            # "description": test.get("description", "No description available.")
        })
    return {"recommendations": results}
