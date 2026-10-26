# Check Your Judge

**You and the judge agree on 8 of 12 answers** (12 of 12 labeled).

**Cohen's κ:** 0.27, fair agreement, so the judge FAILS the κ ≥ 0.60 gate. Raw agreement 67%; agreement expected by chance 54%.

| | Me: PASS | Me: FAIL |
|---|---|---|
| **Judge: PASS** | 6 | 3 |
| **Judge: FAIL** | 1 | 2 |

## Disagreements

| Answer | Question | My call | Judge's call |
|---|---|---|---|
| 03 | Summarize Competitor Z's latest product launch. | FAIL | PASS |
| 05 | Which CRMs does Competitor Y integrate with? | FAIL | PASS |
| 08 | Has Competitor X announced layoffs this year? | PASS | FAIL |
| 10 | Summarize InsightFlow's G2 reviews. | FAIL | PASS |

## What the judge keeps getting wrong

It rewards fluent, detailed answers even when the detail is invented. It passed all three answers that added unsupported content: Competitor Z's launch (03), with an invented price, plans and analyst view; an extra CRM (05); and an invented reviewer quote with the wrong complaint (10). It also failed an honest "none found" answer (08), treating the absence of information as a failure to answer. It checks for contradictions, not for claims the source doesn't contain, the same blind spot my Module 2 audit found.

## My rewritten rubric

PASS only if every claim in the answer appears in the source and the answer responds to the question. FAIL any answer that adds a fact, feature, number, quote, name or comparison the source doesn't contain, however fluent or detailed. A "no information found" answer passes when the source shows none was found, and fails when the source holds the answer.

- **Example of a FAIL.** Question: Which video tools does Company Q integrate with? Source: Integrations page: Slack and Microsoft Teams. Answer: Company Q integrates with Slack, Microsoft Teams and Zoom. Why: Zoom is not in the source.
- **Example of a PASS.** Question: Does Company R hold any patents? Source: Patent search: no patents found for Company R. Answer: I found no patents for Company R in the sources I checked. Why: the answer reports exactly what the source shows.

## Re-measure

A fresh judge using the rewritten rubric, one answer per call, agreed with me on 12 of 12 answers: **κ 1.00**, which passes the gate ([verdicts](results/calibration-rerun.json)).

| | Me: PASS | Me: FAIL |
|---|---|---|
| **Judge: PASS** | 7 | 0 |
| **Judge: FAIL** | 0 | 5 |

## How this was run

- **My labels:** all 12 answers labelled before seeing the judge's calls ([sheet](fixtures/calibration-label-sheet.md)). I changed answer 12 from FAIL to PASS on review: the source says "about 140" and the answer says "About 140", which is grounded and direct.
- **The judge's calls:** the course tool's fixed calls for the original rubric, and Claude Haiku 5.5 in a fresh context per answer for the rewritten one.
- **Examples written fresh:** the rubric's two examples are new, not taken from the 12 answers, so the re-measure doesn't hand the judge the answers it is scored on.
- **Limit:** the rubric was written after reading these 12 disagreements, so κ 1.00 on the same 12 is optimistic. The out-of-sample evidence for this style of rubric is the [fresh test](eval-suite.md) in Lab 1, where a judge with an explicit unsupported-claim rule caught 13 of 13. Twelve answers is a small sample; κ swings a long way on one disagreement.
