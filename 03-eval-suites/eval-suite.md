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

The Win. The rule check caught all 6 real cases with no false alarms, including my P0 row 11, and the judge also caught 6 of 6. The safety rule caught the 2 capability questions it covers (rows 3 and 11), plus the false refusal in row 8. Each catch is the real problem, a dropped qualifier or an upgraded status, not a formatting issue. The caveat: I wrote the rule's word lists from these same 20 rows, so its 6 of 6 is in-sample. New wording such as "fully integrated" would get past it, which is why the judge stays.

## What I'd ship next

Put the rule check in front of every answer as a release gate, with the judge running on whatever the rule passes, and test the rule's word lists on a fresh set of reworded upgrades before it is allowed to block a release. The rule costs nothing per answer and caught every real case here, so it takes most of the load off the judge. The fresh test is what turns an in-sample 6 of 6 into a number I'd stake a launch on.

## How this was run

- **Real cases:** the six Risk 1 rows in the [failure taxonomy](../02-failure-discovery/failure-taxonomy.md): 3, 4, 5, 11, 12, 14. False alarms count rows the [audit](../02-failure-discovery/audit-log.md) passed (10, 15, 17, 20). Scores: 1 = pass, 0 = fail.
- **Rule check and safety rule:** run as code in [ascend_suite.py](ascend_suite.py), so they give the same result every time.
- **Judge:** Claude Haiku 5.5, one fresh call per row, applying the check exactly as written, with no sight of the audit. Run twice, as the lab's extra step: 0 of 20 calls changed. In Module 2 the same model flipped on two rows under a vaguer rubric; a check written for one failure is far more stable.
- **Cross-check:** GPT-6 ran the lab tool's prompt, with the audit pasted in ([reply](results/gpt6-suite-reply.md)). Its row-level calls matched the code exactly on the rule check and safety rule, and its judge also caught all six real cases. Its judge also failed rows 2, 6, 8 and 9, which aren't inflated facts, so it judged beyond the check as written, most likely primed by the audit in the same prompt. Its own summary table contradicted its row-level calls on every line, with wrong denominators and audit failures counted as false alarms, so every count here comes from code.
- **Limit:** the rule's word lists come from these 20 rows. Its score on fresh answers is unknown until Module 5.

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
