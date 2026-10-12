# First LLM-as-a-Judge Eval, Module 1

> Repo file `ai-evals/01-evaluation-strategy/eval-harness-proof.md`. The eval evidence behind the **Eval Results** slide of the final pitch deck (Module 6).
>
> Fill this with the **First Eval Lab** builder, then **Copy markdown** and paste it over this file. The headings below mirror the tool's output exactly.

## Version A, Concise, system prompt used

```
You are an executive briefing assistant.
Summarize in exactly 3 bullet points under 60 words. No preamble, no extra text.
```

**Output** (Claude Opus 5.5; user message: the Q4 Marketing Campaign Update email from the lab walkthrough):

> - Social media engagement up 25% month on month, driven by the new content calendar and paid ad tests.
> - Newsletter open rate fell from 42% to 35%; new subject lines will be tested next week.
> - Product video campaign delayed until November pending legal approval (assets ready); all campaign tracking links due by Friday.

## Version B, Narrative, system prompt used

```
You are a PR communications assistant.
Write a 100-word narrative summary highlighting wins first, then risks and next steps.
Keep a positive tone. No bullets.
```

**Output** (same model, same email, fresh turn):

> Q4 marketing is building momentum. Social media engagement rose 25% month over month, driven by the new content calendar and paid ad experiments. Newsletter open rates dipped from 42% to 35%, so the team will test new subject lines next week. The product video campaign has moved to November while it awaits legal approval; the creative assets are already complete and ready to launch as soon as it clears. The immediate next step is for everyone to add all campaign tracking links by Friday, so the team can measure what is working and keep this progress going.

**Comparison:** Version A is more concise and sticks to the facts. Version B takes longer to read. For a CEO who needs speed, A wins. B suits a comms team: its softer framing of the delay and the open-rate drop is acceptable polish for that audience.

**Same prompts on ChatGPT, for comparison** (GPT-6):

Version A, 3 bullets, 53 words:

> - Social media engagement rose 25% month-on-month, driven by the new content calendar and paid advertising experiments.
> - Newsletter open rates fell from 42% to 35%; new subject lines will be tested next week.
> - Product video campaign delayed until November, pending legal approval; creative assets are ready. Campaign tracking links must be added by Friday.

Version B, 100 words:

> Q4 marketing is showing positive momentum, with social media engagement increasing 25% month-on-month following the introduction of a new content calendar and paid advertising experiments. Two areas require attention: newsletter open rates have declined from 42% to 35%, and the product video campaign has been delayed until November while awaiting legal approval. The team will test new newsletter subject lines next week to improve engagement, while creative assets for the video campaign are already prepared. The immediate priority is to ensure all campaign tracking links are implemented by Friday, maintaining measurement readiness and supporting informed decisions across upcoming marketing activity.

## Eval setup, dataset name + judge model/family

- **Dataset:** `Module1Output`, four rows: Version A and Version B from two generators, all on the Q4 Marketing Campaign Update email.
- **Generators:** Claude Opus 5.5 (Anthropic) and GPT-6 (OpenAI). Same system prompts, same user message, a fresh turn for each version.
- **Judge:** Conciseness LLM-as-a-Judge. 1 = concise and faithful (every fact matches the email, nothing invented, no padding), 0 = not. Summaries labelled 1 to 4 so the judge can't see which model wrote them.
- **Judge rule:** the judge comes from a different model family from the generator, to avoid self-preference bias. Claude's scores on the GPT-6 rows are valid. Claude's scores on its own rows are self-scores, kept as a bias check until GPT-6 or Gemini scores them.

| # | Generator | Version | Words | Judge | Score | Reason |
|---|---|---|---|---|---|---|
| 1 | Claude Opus 5.5 | A, concise | 52 | Claude Opus 5.5 (self-score) | 1 | All four facts kept, nothing added, no padding. |
| 2 | Claude Opus 5.5 | B, narrative | 97 | Claude Opus 5.5 (self-score) | 0 | Says the campaign "moved" rather than was delayed; adds "ready to launch as soon as it clears" and "keep this progress going", neither in the email. |
| 3 | GPT-6 | A, concise | 53 | Claude Opus 5.5 | 1 | All four facts kept, nothing added, no padding. |
| 4 | GPT-6 | B, narrative | 100 | Claude Opus 5.5 | 0 | Facts intact, but pads the close with a purpose the email never states ("measurement readiness", "informed decisions"). |

- **Limit:** rows 1 and 2 were generated in a session that already held notes on the likely failure modes, which may have made them more faithful than a clean run.

## Cold-start, the prompt you used to seed a starter dataset

Generator: Claude Opus 5.5. Output: 20 rows, 10 first-pass good and 10 bad, in [`fixtures/module1-starter.csv`](fixtures/module1-starter.csv).

```
Generate 20 example rows for evaluating email-summary quality.
Each row: an input email + a candidate summary + a first-pass label ("good" or "bad") + a one-line reason.
Make roughly half concise/faithful ("good") and half verbose or inaccurate ("bad").
Return it as a markdown table.
```

## Your definition of good vs bad (golden-set criteria) — the graded part, write your own

Good summaries:

- **Stick to the facts.**
- **No padding.**
- **Quick to read.**
- **Keeps every fact the reader needs to act or decide; other detail can go.**

Curation so far: row 15 of the starter set relabelled from bad to good. Dropping the cutover dates is acceptable for a CEO.

## Screenshots, links or repo paths (optional if you followed the demo)

_2 shots: (1) eval setup (dataset + judge), (2) starter rows. Image links, or paths under `01-evaluation-strategy/screenshots/`._
