from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import os
import sys

# Ensure Python can find your agents
sys.path.append(os.path.join(os.path.dirname(__file__), 'agents'))

from ross_agent import RossAgent
from rachel_agent import RachelVisionAgent
from utils.rachelUtility import get_all_categories
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="DreamDresser AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Initialize Agents
ross = RossAgent()
ross.wake_up()
rachel = RachelVisionAgent()

class SearchQuery(BaseModel):
    text: str
    category: Optional[str] = None

@app.get("/taxonomy")
def get_taxonomy():
    """Returns the Category -> Sub-category map for the UI menus."""
    return get_all_categories()

@app.post("/search")
def search_closet(query: SearchQuery):
    """Ross hunts for the items based on the UI's request."""
    # Convert text to vector using Rachel
    vector = rachel.model.encode(query.text).tolist()
    
    # Ross finds the match
    results = ross.find_match(vector, category_filter=query.category)
    
    if not results:
        return {"message": "Nothing found in the museum!", "matches": []}
    
    # Return clean JSON for the Angular frontend
    return {
        "matches": [
            {
                "id": m.id,
                "score": m.score,
                "name": m.metadata.get("item_name"),
                "vibe": m.metadata.get("vibe"),
                "category": m.metadata.get("category")
            } for m in results
        ]
    }