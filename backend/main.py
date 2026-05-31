from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from git_extractor import clone_repo, extract_commits, cleanup_repo
from aggregator import group_by_month
from narrator import generate_story

app = FastAPI(title="Git Storyteller")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class RepoRequest(BaseModel):
    github_url: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/story")
def get_story(request: RepoRequest):
    repo_path = None
    try:
        # 1. Clone
        repo_path = clone_repo(request.github_url)

        # 2. Extract commits
        commits = extract_commits(repo_path)
        if not commits:
            raise HTTPException(status_code=400, detail="No commits found in this repository")

        # 3. Aggregate into chapters
        chapters = group_by_month(commits)

        # 4. Generate story
        story = generate_story(chapters)

        return {
            "repo": request.github_url,
            "total_commits": len(commits),
            "total_chapters": len(chapters),
            "story": story,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # Always clean up even if something fails
        if repo_path:
            cleanup_repo(repo_path)