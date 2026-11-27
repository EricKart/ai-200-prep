# Contributing

Thanks for helping other people pass AI-200. Small fixes are just as welcome as new questions.

## Report a problem (no code)

Use **[Wrong answer or unclear question](../../issues/new?template=wrong-answer.yml)**. Include the question id
(for example `lp7m1-012`, shown under each question on the site) and the Microsoft Learn link that proves your point.

## Fix it yourself

```bash
git clone https://github.com/EricKart/ai-200-prep && cd ai-200-prep
npm run check          # all quality gates (Node 20+, no install)
npm run check -- --only lp7m1   # just one module while you work
npm run report         # per-module stats
```

### Where things live

| Path | What |
|---|---|
| `course.json` | Learning paths, modules, Learn units and links, skill areas, mock targets |
| `content/questions/lpXmY.json` | Question bank for one module (format: [docs/question-format.md](docs/question-format.md)) |
| `content/lessons/lpXmY.md` | Lesson. One `##` per Learn unit, using the exact unit title |
| `content/cheatsheets/` | One page per learning path, plus the global sheets |
| `mocks/mock-N.json` | The 3 mock exams (lists of question ids) |
| `labs/lpN-*/` | Hands-on labs: `README.md`, `cmd/bash.sh`, `cmd/ps.ps1`, `app/` |
| `tools/` | Quality gates and generators |

### Rules that matter most

- **Facts come only from Microsoft Learn.** Set `unit` to the Learn unit the fact is on.
- **Never reorder or delete questions.** Ids are positional, and learners' progress is saved against them. Fix a question in
  place, or add new ones at the end of the file.
- **Every option needs a reason.** The correct one starts with "Correct.".
- **Hints point; they don't tell.** Name the concept to think about, never the answer.
- Keep the credit line at the bottom of every Markdown/HTML file.

## Pull requests

1. Fork the repo, create a branch, and make your change.
2. Run `npm run check` until it says `0 errors`.
3. Open the PR and fill in the checklist. CI runs the same gates plus lint, spelling, links, secrets and lab script checks.
4. A maintainer reviews the facts against Learn. Merges need green CI **and** an approval.

By contributing, you agree that your contribution is licensed under this repository's licences (MIT for code,
CC BY-NC-SA 4.0 for content).

---
Part of [AI-200 Prep](README.md) · [aryantripathi.dev](https://aryantripathi.dev/ai-200)
