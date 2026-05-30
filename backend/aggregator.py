from collections import defaultdict
from datetime import datetime


def group_by_month(commits: list) -> list:
    """Group commits into monthly chapters with stats."""
    months = defaultdict(list)

    for commit in commits:
        date = datetime.fromisoformat(commit["date"])
        key = date.strftime("%Y-%m")  # e.g. "2023-06"
        months[key].append(commit)

    chapters = []

    for month_key in sorted(months.keys()):
        month_commits = months[month_key]

        # Top authors
        author_counts = defaultdict(int)
        for c in month_commits:
            author_counts[c["author"]] += 1
        top_authors = sorted(author_counts.items(), key=lambda x: x[1], reverse=True)[:3]

        # Most changed files keywords from messages
        keywords = extract_keywords([c["message"] for c in month_commits])

        # Total insertions/deletions
        total_insertions = sum(c["insertions"] for c in month_commits)
        total_deletions = sum(c["deletions"] for c in month_commits)

        chapters.append({
            "month": month_key,
            "total_commits": len(month_commits),
            "top_authors": [{"name": a, "commits": c} for a, c in top_authors],
            "keywords": keywords,
            "total_insertions": total_insertions,
            "total_deletions": total_deletions,
            "sample_messages": [c["message"] for c in month_commits[:5]],
        })

    return chapters


def extract_keywords(messages: list) -> list:
    """Extract most common meaningful words from commit messages."""
    stopwords = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to",
                 "for", "of", "with", "is", "it", "this", "that", "was", "be"}

    word_counts = defaultdict(int)
    for message in messages:
        for word in message.lower().split():
            word = word.strip(".,!?#():\"'")
            if word and word not in stopwords and len(word) > 2:
                word_counts[word] += 1

    top = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:8]
    return [w for w, _ in top]


if __name__ == "__main__":
    group_by_month([])