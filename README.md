# 📖 Git Storyteller
 
> Turn any GitHub repository into a human-readable story using its commit history and AI.
 
Git Storyteller analyzes a repository's full git history — commits, authors, insertions, deletions, and patterns — and generates a narrative that reads like a story of how the project was built.

## Demo
https://github.com/user-attachments/assets/bbe89a29-8530-411c-9b3e-7b517a4fe966

## How It Works
 
```
GitHub URL
    ↓
Clone repo locally (temp folder)
    ↓
Extract all commits via git log --numstat (single subprocess call)
    ↓
Aggregate commits into monthly chapters with stats
    ↓
Send each chapter to LLaMA 4 via Groq API (parallel workers)
    ↓
Return structured JSON story
    ↓
Display in Vue 3 frontend
```
 
---
## Tech Stack
 
| Layer | Technology |
|---|---|
| Backend | Python 3, FastAPI |
| Git Parsing | GitPython + subprocess |
| AI Narration | LLaMA 4 Scout via Groq API |
| Frontend | Vue 3, Vite |

---

## Architecture
GitHub URL → Clone → Extract Commits → Aggregate by Month → LLM Narration → API → Vue UI

## Project Structure
 
```
git-storyteller/
├── backend/
│   ├── main.py            # FastAPI app and /story endpoint
│   ├── git_extractor.py   # Clone repo + extract commits
│   ├── aggregator.py      # Group commits into monthly chapters
│   ├── narrator.py        # LLM narration with parallel processing
│   └── requirements.txt
├── frontend/
│   └── src/
│       └── App.vue        # Vue 3 single-page app
└── README.md
```
 
---

## Run Locally
 
### Backend
 
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```
 
Create a `.env` file:
```
GROQ_API_KEY=your_key_here
```
 
Get a free API key at [console.groq.com](https://console.groq.com).
 
```bash
uvicorn main:app --reload
```
 
Backend runs at `http://localhost:8000`. API docs at `http://localhost:8000/docs`.

### Frontend
 
```bash
cd frontend
npm install
npm run dev
```
 
Frontend runs at `http://localhost:5173`.
 
---

## API
 
### `POST /story`
 
**Request:**
```json
{
  "github_url": "https://github.com/username/repo"
}
```
 
**Response:**
```json
{
  "repo": "https://github.com/username/repo",
  "total_commits": 1042,
  "total_chapters": 28,
  "story": [
    {
      "month": "2023-06",
      "total_commits": 47,
      "top_authors": [
        { "name": "Alice", "commits": 28 }
      ],
      "narrative": "June was a pivotal month..."
    }
  ]
}
```
 
---

 ## License
 
MIT
 
