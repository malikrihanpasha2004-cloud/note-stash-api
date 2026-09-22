# 📝 NoteStash - Lightweight Notes & Search API

A fast, RESTful personal note-taking API with full-text keyword filtering and tag indexing built using FastAPI.

## 🚀 Features

- **CRUD Support:** Create, read, and delete notes instantly.
- **Tag-Based Filtering:** Organize notes using flexible, lowercased tags.
- **Keyword Search:** Case-insensitive search across note titles and content.
- **Automated Docs:** Interactive Swagger UI available out of the box.

## 📦 Getting Started

```bash
git clone https://github.com/malikrihanpasha2004-cloud/note-stash-api.git
cd note-stash-api
pip install -r requirements.txt
uvicorn main:app --reload
