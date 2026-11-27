# Question format

Each module has one file, `content/questions/<module>.json`:

```json
{
  "module": "lp7m1",
  "title": "Queue and process AI operations with Azure Service Bus",
  "questions": [ … ]
}
```

## Common fields

| Field | Type | Rule |
|---|---|---|
| `id` | string | `<module>-NNN`, positional. Never reorder or delete. Append new questions at the end |
| `unit` | string | Learn unit code from `course.json`, for example `U03`. Must be a content unit, not an exercise |
| `pool` | `practice` \| `mock` | Mock-pool questions are used only in the 3 mock exams |
| `type` | `single` \| `multi` \| `yesno` \| `match` \| `order` | |
| `scenario` | boolean | `true` when the question describes a situation and asks for a decision |
| `difficulty` | `easy` \| `medium` \| `hard` | |
| `q` | string | Markdown: `code`, **bold**, _italic_. No HTML |
| `code` | string | Optional code block shown under the question |
| `hint` | string | ≤ 200 characters. Points to the concept and never contains the answer |
| `explain` | string | One or two sentences that teach the fact |
| `origin` | string | Where the question came from (`lab500`, `site`, `ca1`, `ca3`, `ca4`, `new`) |

## By type

**single / multi**

```json
"options": [
  { "text": "Load leveling with a queue", "why": "Correct. The queue absorbs the burst…" },
  { "text": "Receive-and-delete mode", "why": "That's a receive mode, and it risks losing messages." }
],
"answer": 0            // multi: [0, 2]. Say "(Select two.)" in the question
```

The correct option's `why` starts with `Correct.`, and every other option explains why it's wrong.

**yesno**: `"rows": [{ "text": "…", "answer": true, "why": "…" }]`

**match**: `"choices": ["MAJOR", "MINOR", "PATCH"], "items": [{ "text": "…", "answer": 0, "why": "…" }]`

**order**: `"steps": ["first", "second", "third"]`, listed in the correct order. The site shuffles them.

## Writing a good question

- Start from a real situation: "An AI API…", "A team must…". At least 60% of each module's questions are scenarios.
- One defensible answer. If an expert could argue for two options, rewrite it.
- Distractors are things a learner might really believe, never jokes.
- Keep options similar in length and shape. The checker fails a module where the right answer is too often the longest or shortest.
- Avoid "always/never/only" in wrong options unless the right option uses one too.

---

Part of [AI-200 Prep](../README.md) · [aryantripathi.dev](https://aryantripathi.dev/ai-200)
