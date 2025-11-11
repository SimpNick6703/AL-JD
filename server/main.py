import os
import json
import uuid
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Literal
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("API_KEY")
base_url = os.getenv("BASE_URL")

if not api_key:
    raise RuntimeError("API_KEY not set in environment")

client = OpenAI(api_key=api_key, base_url=base_url) if base_url else OpenAI(api_key=api_key)

class Article(BaseModel):
    id: str
    title: str
    description: str
    content: str

class TopicRequest(BaseModel):
    topic: str

class EditRequest(BaseModel):
    content: str
    action: Literal["SUMMARIZE", "EXPAND", "REPHRASE", "FIX_GRAMMAR"]

class ContentResponse(BaseModel):
    content: str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def parse_json_text(text: str):
    t = text.strip()
    if t.startswith("```"):
        t = t.split("\n", 1)[1] if "\n" in t else t
        if t.endswith("```"):
            t = t.rsplit("```", 1)[0]
    try:
        return json.loads(t)
    except Exception:
        start = t.find("[")
        end = t.rfind("]")
        if start != -1 and end != -1 and end > start:
            return json.loads(t[start:end+1])
        start = t.find("{")
        end = t.rfind("}")
        if start != -1 and end != -1 and end > start:
            return json.loads(t[start:end+1])
        raise

def llm_text(prompt: str) -> str:
    try:
        r = client.responses.create(model="gpt-4o-mini", input=prompt)
        return r.output_text
    except Exception:
        cmpl = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return cmpl.choices[0].message.content or ""

@app.get("/api/health")
async def health():
    return {"status": "ok"}

@app.post("/api/articles/generate-tips", response_model=List[Article])
async def generate_tips():
    prompt = (
        "Generate 10 random, unique, and insightful programming tips. "
        "For each tip, provide: title, description (one sentence), content (a few paragraphs in Markdown). "
        "Return only a valid JSON array of objects with keys: title, description, content."
    )
    try:
        text = llm_text(prompt)
        data = parse_json_text(text)
        items = []
        for it in data:
            items.append(Article(
                id=str(uuid.uuid4()),
                title=str(it.get("title", "Untitled")),
                description=str(it.get("description", "")),
                content=str(it.get("content", "")),
            ))
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"generate-tips: {e}")

@app.post("/api/articles/from-topic", response_model=List[Article])
async def from_topic(req: TopicRequest):
    prompt = (
        f"Generate a programming blog post about \"{req.topic}\". "
        "Provide a creative title, a short description (2-3 sentences), and the full article content in Markdown. "
        "Return only a valid JSON object with keys: title, description, content."
    )
    try:
        text = llm_text(prompt)
        obj = parse_json_text(text)
        article = Article(
            id=str(uuid.uuid4()),
            title=str(obj.get("title", "Untitled")),
            description=str(obj.get("description", "")),
            content=str(obj.get("content", "")),
        )
        return [article]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"from-topic: {e}")

@app.post("/api/articles/edit", response_model=ContentResponse)
async def edit(req: EditRequest):
    if req.action == "SUMMARIZE":
        instruction = "Summarize the following article:"
    elif req.action == "EXPAND":
        instruction = "Expand on the following article, adding more detail, examples, and depth:"
    elif req.action == "REPHRASE":
        instruction = "Rephrase the following article to make it clearer and more engaging, while maintaining the core message:"
    else:
        instruction = "Correct any spelling and grammatical errors in the following text:"
    try:
        text = llm_text(f"{instruction}\n\n{req.content}")
        return ContentResponse(content=text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"edit: {e}")
