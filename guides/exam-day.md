# Exam-day guide

> Read this the day before. Check the official pages for anything that may have changed:
> [AI-200 study guide](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/ai-200) ·
> [Exam duration and question types](https://learn.microsoft.com/en-us/credentials/support/exam-duration-exam-experience) ·
> [Exam sandbox](https://aka.ms/examdemo).

## The day before

- [ ] Re-read the [Which service?](../content/cheatsheets/which-service.md) sheet and your weakest learning path's cheat sheet.
- [ ] Redo the questions you've marked wrong more than once. Don't start new material.
- [ ] Try the official **exam sandbox** so the question types and navigation aren't a surprise.
- [ ] Online exam: run the system test on the same computer, network and room you'll use. Clear the desk.
- [ ] Test centre: check the address, travel time and the ID rules in your confirmation email.
- [ ] Sleep. A rested brain beats one more hour of cramming.

## During the exam

- **Budget your time.** You have 120 minutes. Check the clock about once every quarter of the questions.
- **Read the last sentence first.** It tells you what's asked ("Which tier…", "What should you do first…").
- **Underline the constraints in your head:** "without code changes", "least privilege", "lowest cost", "no downtime", "first". They decide between two plausible answers.
- **Eliminate.** On most questions two options are clearly wrong. Decide between the remaining two by the constraint.
- **Watch for absolute words in the requirement, not in the options.** "Must never", "only" and "exactly" in the scenario usually point to one feature.
- **Yes/No series:** judge each statement on its own. Don't look for a pattern.
- **Flag and move on.** Don't spend more than about 3 minutes on one question on the first pass.
- **Case studies, if you get them:** read the requirements section first, then the questions, then look things up in the case text.

## Common traps across AI-200

| If the question says… | Think about… |
|---|---|
| "exact same image on every node" | Digest, not tag |
| "without storing credentials" | Managed identity plus the narrowest data role |
| "secret rotates" | Versionless Key Vault references; refetch on auth failure |
| "only one worker should process it" | Queue or Stream consumer group, not pub/sub or topics |
| "every service must react" | Topic + subscriptions, Event Grid, or pub/sub broadcast |
| "takes longer than 230 seconds over HTTP" | Async request-reply (return 202, queue the work) |
| "wait days for a human" | Durable Functions external event + durable timer |
| "find where the time went across services" | Distributed tracing (OpenTelemetry) |

## After the exam

- You see a provisional pass/fail at the end. The score report shows performance by skill area, so note your weakest areas either way.
- Passed? Share it, and consider [contributing](../CONTRIBUTING.md) a fix or a question to help the next person.

---

Part of **AI-200 Prep**, a free course by Aryan Tripathi · [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200)
