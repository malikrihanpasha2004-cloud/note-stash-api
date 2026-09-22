from datetime import datetime
from typing import Dict, List, Optional
import uuid
from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="NoteStash API",
    description="A minimalist Markdown note-taking and search API.",
    version="1.0.0",
)

notes_db: Dict[str, dict] = {}


class NoteCreate(BaseModel):
    title: str = Field(..., example="FastAPI Architecture Tips")
    content: str = Field(
        ..., example="Use dependency injection for database sessions."
    )
    tags: List[str] = Field(default=[], example=["python", "fastapi", "backend"])


class NoteResponse(BaseModel):
    id: str
    title: str
    content: str
    tags: List[str]
    created_at: str
    updated_at: str


@app.post("/notes", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def create_note(payload: NoteCreate):
    note_id = str(uuid.uuid4())[:8]
    timestamp = datetime.utcnow().isoformat()

    note = {
        "id": note_id,
        "title": payload.title,
        "content": payload.content,
        "tags": [tag.strip().lower() for tag in payload.tags],
        "created_at": timestamp,
        "updated_at": timestamp,
    }
    notes_db[note_id] = note
    return note


@app.get("/notes", response_model=List[NoteResponse])
def list_or_search_notes(
    tag: Optional[str] = Query(None, description="Filter notes by tag"),
    q: Optional[str] = Query(
        None, description="Keyword search in title or content"
    ),
):
    results = list(notes_db.values())

    if tag:
        tag_lower = tag.strip().lower()
        results = [n for n in results if tag_lower in n["tags"]]

    if q:
        query_lower = q.strip().lower()
        results = [
            n
            for n in results
            if query_lower in n["title"].lower()
            or query_lower in n["content"].lower()
        ]

    return results


@app.get("/notes/{note_id}", response_model=NoteResponse)
def get_note(note_id: str):
    if note_id not in notes_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )
    return notes_db[note_id]


@app.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: str):
    if note_id not in notes_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )
    del notes_db[note_id]
    return None
