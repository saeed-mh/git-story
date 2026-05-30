import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def build_prompt(chapter: dict) -> str:
    """Build a prompt for a single monthly chapter."""
    authors = ", ".join([f"{a['name']} ({a['commits']} commits)" for a in chapter["top_authors"]])
    keywords = ", ".join(chapter["keywords"])
    messages = "\n".join([f"- {m}" for m in chapter["sample_messages"]])

    return f"""
You are narrating the story of a software project based on its git history.
Write ONE short paragraph (4-6 sentences) describing what happened this month.
Be specific, engaging, and use the data to tell a human story.
Do not invent facts. Only use what is given.

Month: {chapter["month"]}
Total commits: {chapter["total_commits"]}
Top contributors: {authors}
Lines added: {chapter["total_insertions"]}
Lines deleted: {chapter["total_deletions"]}
Common keywords in commit messages: {keywords}
Sample commit messages:
{messages}

Write the paragraph now:
"""


def generate_story(chapters: list) -> list:
    """Generate a narrative paragraph for each chapter."""
    story = []

    for chapter in chapters:
        print(f"Narrating {chapter['month']}...")
        prompt = build_prompt(chapter)

        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )

        narrative = response.choices[0].message.content.strip()
        story.append({
            "month": chapter["month"],
            "total_commits": chapter["total_commits"],
            "top_authors": chapter["top_authors"],
            "narrative": narrative,
        })

    return story


if __name__ == "__main__":
    from git_extractor import clone_repo, extract_commits, cleanup_repo
    from aggregator import group_by_month

    path = "tmp/json-server"  # already cloned before, but re-clone if needed
    commits = extract_commits(path)
    chapters = group_by_month(commits)

    # Test with first 2 months only to save API calls
    story = generate_story(chapters[:2])
    for chapter in story:
        print(f"\n## {chapter['month']}")
        print(chapter["narrative"])

        