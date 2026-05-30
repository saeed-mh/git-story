import os
import shutil
from git import Repo
from stat import S_IWRITE


def clone_repo(github_url: str) -> str:
    """Clone a GitHub repo and return the local path."""
    tmp_dir = "tmp"
    os.makedirs(tmp_dir, exist_ok=True)

    repo_name = github_url.rstrip("/").split("/")[-1].replace(".git", "")
    repo_path = os.path.join(tmp_dir, repo_name)

    if os.path.exists(repo_path):
        shutil.rmtree(repo_path)

    print(f"Cloning {github_url}...")
    Repo.clone_from(github_url, repo_path)
    print(f"Cloned into {repo_path}")

    return repo_path


def extract_commits(repo_path: str) -> list:
    """Extract all commits from a cloned repo."""
    repo = Repo(repo_path)
    commits = []

    for commit in repo.iter_commits():
        commits.append({
            # "hash": commit.hexsha[:7],
            "author": commit.author.name,
            "date": commit.committed_datetime.isoformat(),
            "message": commit.message.strip(),
            # "files_changed": len(commit.stats.files),
            "insertions": commit.stats.total["insertions"],
            "deletions": commit.stats.total["deletions"],
        })

    repo.close()  # ← close the repo object before cleanup
    return commits


def cleanup_repo(repo_path: str):
    """Delete the cloned repo from tmp/."""

    def force_remove(func, path, _):
        os.chmod(path, S_IWRITE)
        func(path)

    if os.path.exists(repo_path):
        shutil.rmtree(repo_path, onexc=force_remove)
        print(f"Cleaned up {repo_path}")