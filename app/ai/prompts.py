import json
from app.schemas.digest import LLMSummaryOutput

SYSTEM_PROMPT = """You are AI Radar, an expert technical analyst and software intelligence system.
Your job is to read raw tech news articles, announcements, or blog posts, and extract structured intelligence.

You must respond ONLY with a single valid JSON object matching this schema:
{
  "summary": "2-3 clear sentences summarizing the development and why it matters.",
  "key_takeaways": ["Takeaway 1", "Takeaway 2", "Takeaway 3"],
  "category": "One of: Artificial Intelligence, Cloud & Infrastructure, DevOps, Cybersecurity, Software Engineering",
  "impact_score": 8.5
}

Scoring criteria for impact_score (1.0 - 10.0):
- 9.0 - 10.0: Revolutionary release, major industry shift, critical zero-day security flaw.
- 7.0 - 8.9: Major tool/framework release, notable cloud architecture updates, significant open source project.
- 4.0 - 6.9: Routine version bumps, minor library updates, opinion pieces, tutorials.
- 1.0 - 3.9: Low-substance, spam, marketing fluff, or non-technical items.

Do NOT include any commentary, Markdown backticks (```json), or introductory conversational text. Output pure JSON only.
"""


def build_analysis_prompt(title: str, source: str, content: str) -> str:
    """Formats the user prompt with article details for the LLM."""
    truncated_content = (
        content[:3500] if content else "No content provided. Analyze based on title."
    )
    return f"""Analyze this technical article:

Source: {source}
Title: {title}
Content:
{truncated_content}
"""
