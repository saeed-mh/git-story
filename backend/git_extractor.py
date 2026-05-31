import os
import shutil
import subprocess
from stat import S_IWRITE
from git import Repo


def force_remove(func, path, _):
    """Handle read-only files on Windows during deletion."""
    os.chmod(path, S_IWRITE)
    func(path)


def clone_repo(github_url: str) -> str:
    """Clone a GitHub repo and return the local path."""
    tmp_dir = "tmp"
    os.makedirs(tmp_dir, exist_ok=True)

    repo_name = github_url.rstrip("/").split("/")[-1].replace(".git", "")
    repo_path = os.path.join(tmp_dir, repo_name)

    if os.path.exists(repo_path):
        shutil.rmtree(repo_path, onerror=force_remove)  # ← fixed

    print(f"Cloning {github_url}...")
    Repo.clone_from(github_url, repo_path)
    print(f"Cloned into {repo_path}")

    return repo_path


def extract_commits(repo_path: str) -> list:
    """Extract commits using a single git log call — much faster than GitPython iteration."""
    result = subprocess.run(
        ["git", "log", "--format=COMMIT|%H|%an|%ai|%s", "--numstat"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace"
    )

    commits = []
    current_commit = None

    for line in result.stdout.splitlines():
        if line.startswith("COMMIT|"):
            if current_commit:
                commits.append(current_commit)
            parts = line.split("|", 4)
            current_commit = {
                "hash": parts[1][:7],
                "author": parts[2],
                "date": parts[3],
                "message": parts[4] if len(parts) > 4 else "",
                "files_changed": 0,
                "insertions": 0,
                "deletions": 0,
            }
        elif line.strip() and current_commit:
            parts = line.split("\t")
            if len(parts) >= 2:
                try:
                    ins = int(parts[0]) if parts[0] != "-" else 0
                    dels = int(parts[1]) if parts[1] != "-" else 0
                    current_commit["insertions"] += ins
                    current_commit["deletions"] += dels
                    current_commit["files_changed"] += 1
                except ValueError:
                    pass

    if current_commit:
        commits.append(current_commit)

    return commits


def cleanup_repo(repo_path: str):
    """Delete the cloned repo from tmp/."""
    if os.path.exists(repo_path):
        shutil.rmtree(repo_path, onerror=force_remove)
        print(f"Cleaned up {repo_path}")