# Quality gates

A pull request can merge only when **every gate below passes** in CI **and** a maintainer approves it.
Hints are also scanned for words that appear only in the correct option (a warning; reviewed ids live in `tools/hint-reviewed.json`). The gates run with `npm run check` (no install needed: Node 20+). Thresholds live at the top of
[tools/check.mjs](tools/check.mjs). Changing a threshold needs a reason in the pull request.

## Questions

| Gate | Rule | Why |
|---|---|---|
| Schema | Every question has id, unit, pool, type, scenario, difficulty, text, hint, explanation, and a reason for every option | A learner always finds out *why* |
| Source | `unit` is a content unit of that module (not an exercise), and the fact is in that Microsoft Learn page | No invented facts |
| Stable ids | Ids are positional (`lp1m1-001`…). New questions go at the end. Published ids are in `tools/ids-lock.json` and can never be removed | Saved progress in learners' browsers |
| Answer tells | The correct option is the single longest in ≤ 30% of single-choice questions (≤ 45% within one module), and the single shortest in ≤ 35% | You can't pass by picking the longest |
| Position balance | Correct answers spread across A–D (15–35% each) | No "always C" pattern |
| Absolute words | ≤ 10% of questions have "always / never / only…" only in the wrong options | No "absolute word = wrong" shortcut |
| Formatting tell | The correct option is never the only one shown as `code` | Formatting must not give the answer away |
| No bare URLs | URLs in question text sit in code spans (real references use `[text](url)`) | Example and wrong-answer URLs must not become clickable links |
| Diagrams | Every Mermaid block has a `title:` and a known diagram type; 2+ diagrams per lesson (warning); a site widget marker is always followed by a diagram | Readers on GitHub and the site see the same picture |
| Hint | ≤ 200 characters, never contains the correct option's text, never says "the answer is" | A hint points you somewhere; it doesn't hand you the answer |
| Scenario floor | ≥ 60% scenario questions in every module, every mock, and overall | The exam tests decisions, not recall |
| Coverage | Every Learn content unit has at least one question | Nothing in the syllabus is skipped |
| Near-duplicates | No two questions above 0.8 word overlap (exceptions in `tools/allow-dupes.json`) | Variety |

## Mock exams

3 mocks, 60 questions, 120 minutes each. Questions come only from the `mock` pool, and no question appears in two mocks.
Each skill area is within ±2 questions of its target (14 / 19 / 14 / 13).

## Lessons and cheat sheets

Every module has a lesson. Its `##` headings equal the Learn unit titles, in Learn order, and each section links to its Learn page.
Every learning path has a cheat sheet.

## Labs

Each lab has a README with a **cost** section and a **clean up** section. `cmd/bash.sh` and `cmd/ps.ps1` have the same
`# @@ <step>` names, and one of them is a clean-up step. CI runs ShellCheck and PSScriptAnalyzer.

## Every file

- Every `.md` and `.html` carries the **aryantripathi.dev** credit line.
- No personal data (emails, roll numbers, phone numbers) and no secrets. CI also runs gitleaks.
- Markdown lint, spell check (codespell), and a link check (lychee, also weekly).

## Review checklist (human)

The maintainer checks what a script can't:

1. The answer is right per the cited Learn page, and only one option is defensible.
2. Distractors are plausible: things a learner might really pick.
3. The wording is plain, with no trick negatives.

---
Part of [AI-200 Prep](README.md) · [aryantripathi.dev](https://aryantripathi.dev/ai-200)
