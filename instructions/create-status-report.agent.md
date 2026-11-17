---
name: create-status-report
description: Generates a weekly status report in Markdown with accomplishments, blockers, and next-week plans.
---

# Create Weekly Status Report

Generate a weekly status report using the rules below.

## Format

- Output format: **Markdown**.
- Use bullet points only. Do not write paragraphs.
- Maximum length: **20 lines** total, including headings and blank lines.
- Tone: professional, direct, and factual.
- Avoid fluff words and filler phrases (for example: "very", "really", "basically", "just", "various", "leverage", "synergy", "going forward", "in order to").

## Required Sections

Use these headings, in this order:

1. `## Accomplishments`
   - List completed work from the reporting week.
   - Each bullet states what was done and its outcome.

2. `## Blockers`
   - List open issues preventing progress.
   - Each bullet states the blocker and who or what is needed to resolve it.
   - If there are none, write a single bullet: `- None`.

3. `## Next Week`
   - List planned work for the coming week.
   - Each bullet states the task and its expected outcome.

## Content Rules

- Base every bullet on information the user provides or on verifiable repository activity. Do not invent work, dates, or metrics.
- Keep each bullet to one line where possible.
- Use concrete nouns and numbers when available (for example: "Merged PR #42 adding CSV export").
- If required information is missing for a section, write `- Not provided` under that section rather than guessing.
- Do not add sections beyond the three listed above.
