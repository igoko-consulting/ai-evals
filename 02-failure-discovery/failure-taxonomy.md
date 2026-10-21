# Failure Taxonomy Canvas · Ascend IQ

> Repo file `ai-evals/02-failure-discovery/failure-taxonomy.md`. Becomes the **Failure Taxonomy** slide of the final pitch deck (Module 6) and feeds the Module 3 eval suite.

## Top 3 Prioritized Failures

| Rank | Failure | Audit rows | Trust tag | Frequency | Severity | Business impact |
|---|---|---|---|---|---|---|
| 1 | Inflated facts | 3, 4, 5, 11, 12, 14 | #HALLUCINATION | 13/20, HIGH | P0 | VPs make roadmap and competitive calls on facts that aren't true, which puts top-50 renewals at risk. |
| 2 | Wrong numbers on the core use case | 1, 7 | #HALLUCINATION | 13/20, HIGH | P0 | Pricing and competitor comparisons are the headline use case. A wrong number in a board pack is the error a client won't forgive. |
| 3 | False refusals | 8, 18 | #ROBUSTNESS | 2/20, LOW | P1 | Sends users back to digging by hand, the friction Ascend IQ exists to remove. A missed SOC2 badge can mislead a vendor assessment. |

- **Frequency** counts every audited answer with that tag (3 or more of 20 is HIGH). Risks 1 and 2 share the #HALLUCINATION count; on their own they cover 6 and 2 answers.
- **Severity** follows the course's severity × frequency matrix: P0 is high severity and high frequency, P1 high severity and low frequency, P2 low severity and high frequency, P3 low severity and low frequency.
- **Agentic mode:** all three are output-level failures, because the logs hold no tool traces. Rows 1 and 8 point to retrieval causes: a stale cached page and a missed page footer.

## What each failure looks like

| Risk | Examples from the audit |
|---|---|
| 1 · Inflated facts | A tentative speaker listed as confirmed (row 4). A Zapier route called a "seamless integration" (11). An engineering hub listed as an HQ (14). "Yes" to native export when only the API supports it (3). "Neutral/positive" reported as positive (5). A secondary colour listed as primary (12). |
| 2 · Wrong numbers | The old $49 price from a cached page, when it rose to $59 yesterday (1). A rate-limit comparison reversed in the client's favour, when Competitor Z allows twice the requests (7). |
| 3 · False refusals | "Cannot find compliance documents" when a SOC2 badge is on the page (8). "No access to internal architecture" when the public docs simply list no backend (18). |

## #1 Risk · Business Impact Statement

> This failure matters because Ascend IQ overstates what its sources say in 6 of 20 audited answers, which results in Fortune 500 strategists acting on facts that aren't true and puts our top-50 renewals at risk.

## Defending the Prioritization

- **Anchored to the Module 1 promise** that every figure traces back to Ascend's verified data. Risks 1 and 2 break it directly. Risk 3 breaks the speed half, because users go back to digging by hand.
- **Holds under any rubric:** rows 1, 3, 4, 7, 8, 11 and 14 fail under every judge and rubric tested (audit log, judge sensitivity check), and a severity-only scale gives the same P-levels. The ranking doesn't rest on the strict labelling rule.
- **Risk accepted for now:** minor added or altered details (rows 2, 6, 9, 13, 19) are P2: low severity on a high-frequency tag. Off-brand tone (row 16) is P3: low severity and low frequency, outside the core Q&A use case, and a person reviews drafts before sending.
