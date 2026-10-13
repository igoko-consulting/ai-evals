# Failure Taxonomy Canvas · Ascend IQ

> Repo file `ai-evals/02-failure-discovery/failure-taxonomy.md`. Becomes the **Failure Taxonomy** slide of the final pitch deck (Module 6) and feeds the Module 3 eval suite.

## How to complete this file

1. First complete `audit-log.md` (the failure audit) — this canvas prioritizes the failures you found there.
2. Open the **M2 · Failure Taxonomy Canvas** tool from the Module 2 deck. Fill the three risk cards (click **↺ Load Ascend IQ defaults** to see a worked example first), then click **📋 Copy markdown** and paste it over the template below.
3. Anchor severity to the **user promise / trust metrics you chose in the Module 1 Strategy Canvas** (`ai-evals/01-evaluation-strategy/strategy-canvas.md`) — severity is a strategic judgment, not just a frequency count.

**Definition of done —** you're finished when the Top 3 table is fully filled (no `_…_` left), the #1 risk has a one-sentence Business Impact Statement in leadership language, and the prioritization is defended in 2–3 bullets.

### Scoring guides

**Frequency** = how many of the 20 audited rows carry this Trust Metric tag. **≥ 3 of 20 = HIGH** frequency; ≤ 2 = LOW.

**Severity (P0–P3)** — a strategic call about business cost, independent of how often it happens:

| Level | Meaning | Rough test |
|---|---|---|
| **P0** | Crisis Zone | Blocks the core promise; legal, compliance, or contract-breaking. |
| **P1** | Hidden Risk | Real damage to trust or revenue, but survivable short-term. |
| **P2** | Annoyance | Degrades experience; a workaround exists. |
| **P3** | Low Priority | Cosmetic or rare. |

**Agentic mode** (optional) — if the failure lives in the *trajectory* (the path of tool calls), tag it: `TOOL_MISUSE`, `REASONING_LOOP`, `SCOPE_ESCALATION`, or `RECOVERY_FAILURE`. Leave blank for output-only failures.

## Top 3 Prioritized Failures

| Rank | Failure Type | Trust Tag | Agentic Mode | Frequency | Severity | Business Impact |
|---|---|---|---|---|---|---|
| 1 | **Inflated facts:** answers say more than the source does. Tentative becomes confirmed, a Zapier route becomes a "seamless integration", an engineering hub becomes an HQ, API-only becomes "yes" to native export. Audit rows 3, 4, 5, 11, 12, 14. | #HALLUCINATION | Output-level | 13/20, HIGH (this pattern 6/20) | P0 | VPs make roadmap and competitive calls on capabilities and facts that aren't true. Breaks the verified-data promise and puts top-50 renewals at risk. |
| 2 | **Wrong numbers on the core use case:** a stale price from a cached page, and a rate-limit comparison that gets the facts backwards in the client's favour. Audit rows 1, 7. | #HALLUCINATION | Output-level; row 1 points to stale data in retrieval | 13/20, HIGH (this pattern 2/20) | P0 | Pricing and competitor comparisons are the headline use case. A wrong number in a board pack is the error a client won't forgive. |
| 3 | **False refusals:** the answer is in the source, but the agent says it can't find or access it. Audit rows 8, 18. | #ROBUSTNESS | Output-level; row 8 points to a retrieval gap | 2/20, LOW | P1 | Sends users back to digging by hand, the friction Ascend IQ exists to remove. A missed SOC2 badge can mislead a competitive or vendor assessment. |

## #1 Risk · Business Impact Statement

> This failure matters because Ascend IQ overstates what its sources say in 6 of 20 audited answers, which results in Fortune 500 strategists acting on facts that aren't true and puts our top-50 renewals at risk.

## Defending the Prioritization

- **Anchored to the Module 1 promise** that every figure traces back to Ascend's verified data. Risks 1 and 2 break it directly. Risk 3 breaks the speed half, because users go back to digging by hand.
- **Frequency and scale:** #HALLUCINATION at 13 of 20 is HIGH; #ROBUSTNESS at 2 of 20 is LOW. P-levels follow the pre-read's severity × frequency quadrants; the template's severity-only scale gives the same ranking.
- **Risk accepted for now (P2):** minor invented details (audit rows 2, 6, 9, 13, 19) and off-brand tone (row 16). Tone sits outside the core Q&A use case, and a person reviews drafts before sending.
