# Module 4 · Launch Strategy · Ascend IQ Copilot

## 4.0 Release Criteria

| Gate | Failure | Metric | Threshold | Dataset | Method | Runs at |
|---|---|---|---|---|---|---|
| Hard | Inflated facts (#HALLUCINATION) | Share of answers that state a status, capability, rating or availability stronger than the source, or drop a source qualifier | 0 confirmed in ≥100 held-out questions; the judge must keep ≥95% recall, ≤6% false alarms and κ ≥ 0.6 | Ascend IQ golden set | LLM judge | Release |
| Soft | Row 3 · Latency: exceeded the maximum response time | p95 time to a complete answer | ≤ 2.0 s | Ascend IQ golden set | Code-based check | Staging |
| Advisory | Row 17 · Tone: slang detected | Share of drafts that use a term from the brand voice's banned-slang list | 0% | Ascend IQ golden set | Code-based check | Pull Request |

## CI Gate Request for Engineering

- **Hard gate · Inflated facts (#HALLUCINATION).** Check: the LLM judge, run on the Ascend IQ golden set at Release. Measures: Share of answers that state a status, capability, rating or availability stronger than the source, or drop a source qualifier. Passes when: 0 confirmed in ≥100 held-out questions; the judge must keep ≥95% recall, ≤6% false alarms and κ ≥ 0.6. On a fail: block the release.
- **Soft gate · Row 3 · Latency: exceeded the maximum response time.** Check: the code-based check, run on the Ascend IQ golden set at Staging. Measures: p95 time to a complete answer. Passes when: ≤ 2.0 s. On a fail: pause the release until the PM signs off on an override.
- **Advisory gate · Row 17 · Tone: slang detected.** Check: the code-based check, run on the Ascend IQ golden set at Pull Request. Measures: Share of drafts that use a term from the brand voice's banned-slang list. Passes when: 0%. On a fail: post a warning, and don't block.

## Mitigation Plan · Soft Gate

If our Soft gate fails (latency is 4.2 seconds against a 2.0-second target), I recommend a staged rollout because it will allow us to release Ascend IQ to 5 of the top 50 accounts first, measure whether slow answers cut repeat use, and roll back before the delay reaches every renewal conversation.

## Other gates for engineering

The tool's export has one row per gate level, so it leaves out two Hard gates and the early warnings in the [gate map](gate-map.md). Engineering needs all of them.

- **Hard gate · Row 1 · Hallucination: the answer quotes the old price as current.** Check: the code-based check, run on the Ascend IQ golden set at Pull Request. Measures: share of pricing answers that match the saved copy of the pricing page. Passes when: 100%. On a fail: block the merge.
- **Hard gate · Row 8 · Hallucination: contradicts the specs and criticizes a named competitor.** Check: the LLM judge, with the rubric from my [judge calibration](../03-eval-suites/judge-calibration.md), run on the Ascend IQ golden set at Staging. Measures: share of comparison answers that contradict the spec's figures or disparage a named competitor without support. Passes when: 0%. On a fail: block the merge.
- **Early warnings, never blocking:** a code-based check on the PR that warns when a comparison leaves out or contradicts the spec's figures (row 8); a timer on the PR that warns above 2.0 s (row 3); the inflated-facts judge on every staging build, and the word-pair rule from the eval spec on every PR (row 5). The Release gate above is what blocks.

## How this was written

- **In the repo, not the lab tool.** The release criteria, the request for engineering and the mitigation plan follow the tool's export format. The extra section adds the gates its three rows leave out.
- **The Hard row is copied from the [eval spec](../03-eval-suites/eval-spec.md),** as the lab instructs, so the two can't drift apart.
- **2.0 s is the lab's target, kept as the Soft threshold.** Trust comes before speed in my [strategy canvas](../01-evaluation-strategy/strategy-canvas.md), and that trade-off lives in the PM's override, not in a looser number. A gate set to fit today's build stops being a gate.
- **No lever ships around a Hard gate.** Today's build fails it: 6 of 20 audited answers (30%) inflate facts, against a bar of zero. The staged rollout applies only once that gate passes.
