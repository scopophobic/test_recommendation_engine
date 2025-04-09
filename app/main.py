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
    prompt: str = "We need a data analyst with good numerical reasoning and Excel knowledge, mid-level experience with test durations less than 60."
    top_k: int = 10

@app.get("/")
def read_root():
    return {"message": "SHL Recommender API is up 🚀"}


@app.get("/health")
def health_status():
    return {
        "status": "healthy",
        "message": "API is healthy and running ✅"
    }
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
            "description": test.get("description", "No description available.")
        })
    return {"recommendations": results}


@app.get("/recommend")
async def recommend_docs():
    return {
       
        "IMP_MESSAGE ": "THIS IS AN EXAMPLE, TO TRY OUT THE API GO TO https://shl-recommendation-engine-hnys.onrender.com/docs#/default/recommend_recommend_post ",
        "message": "Send a POST request with a hiring prompt and top_k value.",
        "example_input": {
            "prompt": "I am hiring for Java developers who can also collaborate effectively with my business teams. Looking for an assessment(s) that can be completed in 40 minutes.",
            "top_k": 2
        },
        "example_output": {
            "recommendations": [
                 {
            "link": "https://www.shl.com/solutions/products/product-catalog/view/core-java-advanced-level-new/",
            "name": "Core Java (Advanced Level) (New)",
            "duration": 13,
            "keys": [
              "K"
            ],
            "remote": True,
            "adaptive": False,
            "job_levels": [
              "Job levelsMid-Professional",
              "Professional Individual Contributor"
            ],
            "description": "DescriptionMulti-choice test that measures the knowledge of basic Java constructs, OOP concepts, files and exception handling, and advanced Java concepts like generics, collections, threads, strings and concurrency."
            },
            {
        "name": "Core Java (Entry Level) (New)",
        "link": "https://www.shl.com/solutions/products/product-catalog/view/core-java-entry-level-new/",
        "duration": 13,
        "keys": [
          "K"
        ],
        "remote": True,
        "adaptive": False,
        "job_levels": [
        "Job levelsMid-Professional",
        "Professional Individual Contributor"
        ],
      "description": "DescriptionMulti-choice test that measures the knowledge of basic Java constructs, OOP concepts, file handling, exception handling, threads, generic class and inner class."
        }
            ]
        }
    }