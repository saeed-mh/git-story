# 📖 Git Storyteller

Turn any GitHub repository into a human-readable story using its commit history and AI.

## How it works
1. Paste any public GitHub URL
2. The backend clones the repo and extracts all commits
3. Commits are grouped into monthly chapters
4. Each chapter is narrated by an LLM (Groq / LLaMA 4)
5. The full story is displayed in the UI

## Tech Stack
- **Backend**: Python, FastAPI, GitPython, Groq API
- **Frontend**: Vue 3, Vite
- **AI**: LLaMA 4 Scout via Groq

## Architecture
GitHub URL → Clone → Extract Commits → Aggregate by Month → LLM Narration → API → Vue UI
