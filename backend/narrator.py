import os
from groq import Groq
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed

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


def narrate_chapter(chapter: dict) -> dict:
    """Generate a narrative for a single chapter."""
    prompt = build_prompt(chapter)

    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    narrative = response.choices[0].message.content.strip()
    print(f"✓ {chapter['month']}")

    return {
        "month": chapter["month"],
        "total_commits": chapter["total_commits"],
        "top_authors": chapter["top_authors"],
        "narrative": narrative,
    }


def generate_story(chapters: list, max_workers: int = 5) -> list:
    """Generate narratives for all chapters in parallel."""
    results = {}

    print(f"Narrating {len(chapters)} chapters with {max_workers} parallel workers...")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(narrate_chapter, chapter): chapter["month"] for chapter in chapters}

        for future in as_completed(futures):
            month = futures[future]
            try:
                result = future.result()
                results[month] = result
            except Exception as e:
                print(f"✗ {month} failed: {e}")

    # Return sorted by month
    return [results[month] for month in sorted(results.keys())]

if __name__ == "__main__":
    from git_extractor import extract_commits
    from aggregator import group_by_month

    commits = extract_commits("tmp/WACVR")
    chapters = group_by_month(commits)
    print(f"Total chapters: {len(chapters)}")

    story = generate_story(chapters)
    for chapter in story:
        print(f"\n## {chapter['month']}")
        print(chapter["narrative"])