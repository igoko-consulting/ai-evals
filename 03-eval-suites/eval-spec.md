# Eval Spec · Inflated facts

| Part | Spec |
|---|---|
| Target risk | Inflated facts (#HALLUCINATION), an output risk and P0 in the [failure taxonomy](../02-failure-discovery/failure-taxonomy.md): the answer says more than its source does. Tentative becomes confirmed, a partner route becomes native or seamless, secondary becomes primary, mixed becomes positive, beta becomes generally available. Trust metric: hallucination rate. |
| Evaluator | The Lab 1 judge, one answer per call, from a different model family than Ascend IQ. It sees the question, the answer, the retrieved source and any mandated wording, never the expected labels. It fails an answer that upgrades a status, capability or rating, or drops a qualifier that changes what the reader would do. The word-pair rule runs first as a free early warning, never a gate. |
| Threshold | Safety-first. Ship only with zero confirmed inflated answers in a held-out set of at least 100 questions, with a person reviewing every judge flag; zero in 100 still allows up to about 3% at 95% confidence. The gate itself must catch at least 95% of inflated answers with at most 6% false alarms on fresh labelled cases, and agree with human labels at κ 0.6 or above. What supports it: the judge caught 6 of 6 audit cases and 13 of 13 fresh ones, with 1 false alarm in 17, and gave identical calls on two runs; human review of each flag absorbs its roughly 6% false-alarm rate. The word rule, at 4 of 13 fresh, can't carry a threshold. The current build fails the bar: 6 of 20 audited answers (30%) inflate facts. |
| Business stakes | A VP who repeats an inflated fact, such as a "seamless" integration that runs through Zapier, makes roadmap and competitive calls on something untrue. Ascend sells verified data, so one exposed error undermines the $50k+ renewals across the top 50 accounts, the revenue Ascend IQ exists to protect. |
| Owner | The Group PM for Ascend IQ owns the threshold and the ship/hold call. The engineering lead owns the gate in CI, and a data-quality reviewer clears flagged answers each week. |

## Messages

**Engineering · acceptance criteria:** GIVEN an answer, its question and its retrieved source, WHEN the judge reviews it one answer per call, THEN fail it if it states a status, capability, rating or availability stronger than the source, or drops a source qualifier, and pass it otherwise. Block the release unless the 100-question held-out set has zero confirmed failures and the gate scores at least 95% recall with at most 6% false alarms on the labelled fresh set.

**Design · what the user sees:** When the gate blocks an answer, show the source's own wording instead, for example "Our verified source says: 'HubSpot integration available via Zapier partnership'", with a link to the source and an option to ask a follow-up. Never a bare "I can't answer", which would add to the false refusals already ranked P1.

**Leadership · risk and return:** This gate stops Ascend IQ from overstating our verified data, the failure in 6 of 20 audited answers and the one most likely to cost top-50 renewals. It costs one judge call per answer plus review of flagged answers; we'll track the inflated-fact rate and the gate's false-alarm rate each release. Today's build doesn't meet the bar.

## How this was written

- **In the repo, not the lab tool.** The tool pre-fills the evaluator with whichever Lab 1 check scored best. The rule check and judge tied at 6 of 6 in-sample, so it would have chosen the rule check, which then caught 4 of 13 on fresh answers ([eval suite](eval-suite.md)).
- **Numbers trace to evidence:** the audit rate from the [audit log](../02-failure-discovery/audit-log.md), and the gate's recall and false alarms from the [fresh test](results/reworded-judge.json).
