from fastapi import FastAPI
import json
from pydantic import BaseModel
from typing import List, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from llm import genreate_reply, rewrite_query, decide_next_action, ask_clarification

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

with open("catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)

def make_text(item):
    return " ".join([
        item.get("name", ""),
        item.get("description", ""),
        " ".join(item.get("job_levels", [])),
        " ".join(item.get("keys", [])),
        item.get("duration", ""),
    ])

catalog_texts=[make_text(item) for item in catalog]

# model=SentenceTransformer("all-MiniLM-L6-v2")
# catalog_embeddings=model.encode(catalog_texts)

vectorizer = TfidfVectorizer(stop_words="english")
catalog_embeddings = vectorizer.fit_transform(catalog_texts)

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

def get_test_type(keys):
    text = " ".join(keys)
    if "Knowledge" in text:
        return "K"
    if "Personality" in text:
        return "P"
    if "Simulations" in text:
        return "S"
    if "Ability" in text:
        return "A"
    return "0"

def search_catalog(query, top_k=5):
    # query_embedding=model.encode([query])
    # scores=cosine_similarity(query_embedding, catalog_embeddings)[0]

    query_embedding = vectorizer.transform([query])
    scores = cosine_similarity(query_embedding, catalog_embeddings)[0]
    top_indices=scores.argsort()[::-1][:top_k]

    results = []
    for idx in top_indices:
        if scores[idx]<0.35:
            continue
        item=catalog[idx]
        results.append({
            "name": item.get("name", ""),
            "url": item.get("link", ""),
            "test_type": get_test_type(item.get("keys", [])),
            "description": item.get("description", ""),
            "duration": item.get("duration", ""),
            "job_level": item.get("job_levels", []),
        })
    return results


@app.post("/chat")
def chat(request: ChatRequest):
    # user_text = request.messages[-1].content
    full_context=" ".join([m.content for m in request.messages])
    latest_user_text=request.messages[-1].content.lower()

    final_words = [
    "confirmed",
    "confirm",
    "final",
    "lock it in",
    "that works",
    "looks good",
    "perfect",
    "covers it",
    "go ahead",
    "done"
]
    is_final = any(word in latest_user_text for word in final_words)

    off_topic_words=["weather", "movie", "food", "legal", "law", "salary", "resume", "interview tips"]
    if any(word in latest_user_text for word in off_topic_words):
        return {
            "reply" : "I can only help with SHL assessment recommendations and comparisons.",
        "recommendations" : [],
        "end_of_conversations" : False
        }
    
    legal_words = [
    "hipaa",
    "gdpr",
    "legal",
    "law",
    "regulation",
    "compliance",
    "legally",
    "mandatory",
    "required by law"
]
    if any(word in latest_user_text for word in legal_words):
        return {
            "reply": (
                "I can help recommend SHL assessments, "
                "but I can't advise whether an assessment satisfies legal "
                "or regulatory requirements. Please consult your legal or "
                "compliance team for that guidance."
            ),
            "recommendations": [],
            "end_of_conversation": False
        }

    vague_phrases=["assessment", "test", "i need an assessment", "need test"]
    if len(request.messages) == 1 and (len(latest_user_text.split()) < 5 or latest_user_text.strip() in vague_phrases):
        return {
            "reply" : "Sure. Which role or skills are you looking for?",
        "recommendations" : [],
        "end_of_conversations" : False
        }
    
    decision = decide_next_action(full_context)

    if decision == "ASK":
        reply = ask_clarification(full_context)
        return {
            "reply": reply,
            "recommendations": [],
            "end_of_conversation": False
        }

    search_query=rewrite_query(full_context)
    results=search_catalog(search_query, top_k=5)

    if not results:
        return {
            "reply": "I couldn't find a suitable SHL assessment for that requirement. Could you describe the role, skills, experience level, or competencies you're looking to assess?",
            "recommendations": [],
            "end_of_conversation": False
        }

    public_results=[
        {
            "name": r["name"],
            "url": r["url"],
            "test_type": r["test_type"]
        }
        for r in results
    ]

    reply=genreate_reply(full_context, results)

    return {
        "reply" : reply,
        "recommendations" : public_results,
        "end_of_conversations" : is_final
    }

