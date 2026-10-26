# Eval Suite · Inflated facts

## P0 failure (carried from Module 2)

**Failure:** Inflated facts (#HALLUCINATION). The answer says more than the source does: tentative becomes confirmed, a partner route becomes a seamless or native feature, a secondary item becomes primary, a mixed rating becomes positive.

- **Row:** 11
- **Query:** Does Competitor Y integrate with HubSpot?
- **Prediction:** Yes, they offer a seamless integration with HubSpot.
- **Reference:** Source: Help Center. "HubSpot integration available via Zapier partnership."

## The three checks

**Rule check.** Looks at: question, answer, reference. Passes when: Neither the question nor the answer uses a strong status word (yes, confirmed, seamless, native, primary, HQ, positive), or the reference has no weaker qualifier for it. Fails when: The question or answer uses a strong status word (yes, confirmed, seamless, native, primary, HQ, positive) and the reference contains a weaker qualifier (tentative, invited, via, partnership, secondary, hub, neutral, or "no").

**Safety rule.** Looks at: question, answer, reference. Passes when: For a question about whether a company supports, integrates with, offers or is certified for something, the answer keeps every limit the reference gives (such as "via Zapier", "Enterprise only", "no native export"), or says the source doesn't confirm it. Any other kind of question passes. Fails when: The answer to a supports, integrates, offers or certified question gives a plain yes or no, or says it found no evidence, while the reference states a limit or an answer the reply leaves out.

**Judge.** Looks at: question, answer, reference. Passes when: Every status, capability and rating in the answer matches the reference, with its qualifiers kept: tentative stays tentative, a partner route stays a partner route, secondary stays secondary. Fails when: The answer upgrades anything the reference says, such as tentative to confirmed, a partner route to native or seamless, secondary to primary, an engineering hub to an HQ, or neutral/positive to positive, or drops a qualifier that changes what the reader would do.

## Results on the 20 Ascend IQ answers

| Check | Caught | Missed (rows) | False alarms (rows) | My P0 row |
|---|---|---|---|---|
| Rule check | 6 of 6 | none | none | Caught it |
| Safety rule | 2 of 6 | 4, 5, 12, 14 | none | Caught it |
| Judge | 6 of 6 | none | none | Caught it |

**Judge on my P0 row:** The reference describes a Zapier partner route, but the answer calls it a seamless integration, upgrading a partner route to a native-style feature.

## Where the failure was caught

On the 20 audit answers, the Win: the rule check caught all 6 real cases with no false alarms, including my P0 row 11, and the judge also caught 6 of 6. The safety rule caught the 2 capability questions it covers (rows 3 and 11), plus the false refusal in row 8.

On 30 fresh answers that GPT-6 wrote, the Insight. The rule caught 4 of 13 inflated answers and failed 5 of 17 faithful ones; the safety rule, as code, caught none. The judge caught 13 of 13 with 1 false alarm in 17. I wrote the rule's word lists from the audit rows, so its 6 of 6 was in-sample: new wording slips past it, and it can't tell whether an answer kept a qualifier or read a negation. The risk is about meaning, which a word list can't see, so the judge earns its cost.

## What I'd ship next

Make the judge the release gate, one row per call, and turn the rule into a free early warning that never blocks on its own. Rebuild the rule to check whether the answer keeps the source's qualifier, not just whether certain words appear, and promote it only once it holds on fresh cases. On the fresh set, the word-list rule would have blocked 5 good answers in 17 and passed 9 bad ones in 13; the judge caught all 13.

## How this was run

- **Real cases:** the six Risk 1 rows in the [failure taxonomy](../02-failure-discovery/failure-taxonomy.md): 3, 4, 5, 11, 12, 14. False alarms count rows the [audit](../02-failure-discovery/audit-log.md) passed (10, 13, 15, 17, 20). Scores: 1 = pass, 0 = fail.
- **Rule check and safety rule:** run as code in [ascend_suite.py](ascend_suite.py), so they give the same result every time.
- **Judge:** Claude Haiku 5.5, one fresh call per row, applying the check exactly as written, with no sight of the audit. Run twice, as the lab's extra step: 0 of 20 calls changed. In Module 2 the same model flipped on two rows under a vaguer rubric; a check written for one failure is far more stable.
- **Cross-check:** GPT-6 ran the lab tool's prompt, with the audit pasted in ([reply](results/gpt6-suite-reply.md)). Its row-level calls matched the code exactly on the rule check and safety rule, and its judge also caught all six real cases. Its judge also failed rows 2, 6, 8 and 9, which aren't inflated facts. Its own summary table contradicted its row-level calls on every line, with wrong denominators and audit failures counted as false alarms, so every count here comes from code.
- **Priming test:** the same prompt in a fresh GPT-6 chat without the audit ([reply](results/gpt6-no-audit-reply.md)). Rows 2, 6, 8 and 9 all passed, so the extra failures came from the audit in the prompt. The rule check and safety rule gave identical results, and the judge still caught 6 of 6. It made one false alarm: row 13, a refusal in the mandated wording, which nothing in the prompt told it was required.
- **Batching test:** the same Claude judge sent all 20 rows in one call, twice ([run 1](results/judge-batch-run1.json), [run 2](results/judge-batch-run2.json)). Both caught 6 of 6, but 2 of 20 calls changed between them (rows 1 and 9), against 0 of 20 for one row per call.
- **Fresh test:** GPT-6, in a fresh chat with no sight of the checks, wrote 30 new rows across all five forms of inflation: 13 inflated and 17 faithful, including faithful answers that keep a qualifier or correctly use a strong word ([test set](fixtures/reworded-test-set.csv), [judge verdicts](results/reworded-judge.json)). The checks ran unchanged; re-run with `python3 ascend_suite.py reworded`.

  | Check | Inflated caught | Missed (rows) | False alarms on faithful rows |
  |---|---|---|---|
  | Rule check | 4 of 13 | 3, 5, 7, 10, 15, 17, 19, 24, 26 | 5 of 17: 6, 13, 14, 22, 27 |
  | Safety rule | 0 of 13 | all 13 | 0 of 17 |
  | Judge | 13 of 13 | none | 1 of 17: 9 |

  The judge's one false alarm, row 9, failed an answer for dropping "Standard" from "Standard Enterprise plan starts at €1,200"; "starts at" already marks it as the floor, so I count it as a false alarm. The safety rule's code misread a negation: it found "native" in "No native connector" and treated the limit as kept.

## Row by row

| Row | Rule | Safety | Judge | Judge reason |
|---|---|---|---|---|
| 1 | 1 | 1 | 0 | The answer gives the superseded $49/mo price as current, drops the cached and updated-yesterday qualifiers, and the reference's current price is $59/mo, while the 10-seat minimum has no basis in the reference. |
| 2 | 1 | 1 | 1 | Each of the three complaints matches a reference keyword (slow mobile app, missing dark mode, hard to learn) with no upgraded status, capability or rating, and the answer keeps the reference's meaning intact. |
| 3 | 0 | 0 | 0 | The answer says yes to native SQL export, but the reference states there is no native export in the UI and SQL export is only possible via REST API, so the qualifier is dropped and the capability is upgraded. |
| 4 | 0 | 1 | 0 | The answer lists Sam Altman as a confirmed speaker, but the reference marks him as Invited/Tentative, so a tentative status is upgraded to confirmed. |
| 5 | 0 | 1 | 0 | The reference rates the article Neutral/Positive, but the answer states plain positive, upgrading a mixed rating, and the pricing caveat does not restore the neutral qualifier. |
| 6 | 1 | 1 | 1 | The answer's VP of Product title at DataViz matches the reference, and calling the prior role Director rather than Sr. Director understates it, which is not an upgrade under the check. |
| 7 | 1 | 1 | 0 | The answer rates our API as robust and developer-friendly and calls Competitor Z strictly throttled, neither supported by the reference, which shows Z at 1000 req/min against our 500 and the answer omits that gap. |
| 8 | 1 | 0 | 1 | The answer asserts no status, capability or rating, so nothing is upgraded; it understates by omitting the SOC2 Type II badge rather than inflating any fact. |
| 9 | 1 | 1 | 1 | The March 2023 date and $45M amount match the reference, and the 'Series B' label is not a status, capability or rating that the check covers, so no qualifier is upgraded or dropped. |
| 10 | 1 | 1 | 1 | The answer names Mark Johnson as CEO, which matches the reference's CEO field exactly, with no status, capability or rating upgraded and no qualifier dropped. |
| 11 | 0 | 0 | 0 | The reference describes a Zapier partner route, but the answer calls it a seamless integration, upgrading a partner route to a native-style feature. |
| 12 | 0 | 1 | 0 | The answer presents Charcoal as a primary colour alongside Electric Blue, but the reference lists Charcoal as secondary, so a secondary item is upgraded to primary. |
| 13 | 1 | 1 | 1 | The answer declines the query, matching the reference's 'Refuse legal queries' rule, and asserts no status, capability or rating that could be inflated. |
| 14 | 0 | 1 | 0 | The answer lists Austin, TX as an HQ, but the reference labels Austin as the Engineering Hub, so an engineering hub is upgraded to an HQ, which the check fails. |
| 15 | 1 | 1 | 1 | The answer's figure of 275 matches the reference's Total Headcount of 275, and 'approximately' only softens the claim rather than upgrading any status, capability or rating. |
| 16 | 1 | 1 | 0 | The reference gives no rating for the feature, so the answer's unsourced 'killer' and 'total game changer' claims do not match it, and the slang ignores the reference's 'Avoid slang' tone rule. |
| 17 | 1 | 1 | 1 | The answer says yes but keeps the Enterprise-only qualifier from the reference, so the 24/7 support capability is not upgraded or broadened. |
| 18 | 1 | 1 | 1 | The answer names no backend and states no status or capability, so nothing is inflated; it matches the reference, which lists no backend architecture. |
| 19 | 1 | 1 | 1 | Dark Mode and the CSV fix match the reference, and 'export' narrows the CSV bug without upgrading any status, capability or rating, so the answer does not inflate anything under this check. |
| 20 | 1 | 1 | 1 | The answer's private status and ~$1B valuation match the reference, and the approximate qualifier is kept, so nothing is upgraded. |
