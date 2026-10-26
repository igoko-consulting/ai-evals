# Eval playbook

What I'd do again on any AI eval project, and the evidence from the Ascend IQ audit behind each rule. Each entry gives the rule, what happened here, and how to apply it next time. Updated as each module adds evidence.

## Defining good

### 1. Define good per audience before measuring

- **What happened:** the same email summary was the right answer for a comms team and the wrong one for a CEO. The rubric decided which reader the eval served. ([Module 1 eval](01-evaluation-strategy/eval-harness-proof.md))
- **Apply it:** name the reader in every rubric. If two audiences need different things, write two rubrics, not one compromise.

### 2. Commit to the trade-offs before the pressure arrives

- **What happened:** I wrote "we prioritise grounding over latency" and "robustness over latency" before any results, so later calls are judged against a bar set in advance. ([Strategy canvas](01-evaluation-strategy/strategy-canvas.md))
- **Apply it:** write each trade-off as "we prioritise X over Y because..." at the start, and keep them between the metrics you actually chose.

## Auditing outputs

### 3. Label strictly, and decide materiality through severity

- **What happened:** strict labelling found 15 failures in 20 answers; the course's narrower rubric found 10 to 11. The ranking of risks was the same either way. ([Audit log](02-failure-discovery/audit-log.md))
- **Apply it:** keep "is it wrong?" and "does it matter?" as separate steps. Label every departure from the source, then let the P0 to P3 severity carry the judgement.

### 4. Report the range, and the core that fails everywhere

- **What happened:** different judges and rubrics gave anywhere from 9 to 15 failures on the same 20 rows, but 8 rows failed under every one. The rubric moved the count more than the model did. ([Judge runs](02-failure-discovery/fixtures/judge-runs.csv))
- **Apply it:** never quote a single failure rate. Give the range across rubrics and the rows that fail under all of them; that core is the number leadership can rely on.

### 5. Check your labels are reproducible

- **What happened:** GPT-6, in a fresh chat with only my written rule and the 20 answers shuffled and unlabelled, matched 19 of 20 of my audit labels (κ 0.88), and a second run prompted as a strict, sceptical human gave the same 20 labels. The one miss, row 2, was the same row every earlier judge had split on. ([Audit log](02-failure-discovery/audit-log.md), [judge runs](02-failure-discovery/fixtures/judge-runs.csv))
- **Apply it:** shuffle the rows, strip the labels, and have a fresh labeller apply the written rule. Flag any row that splits as contested rather than forcing a verdict, and keep a person's blind labels as the real ground-truth check.

### 6. Find the root cause before swapping models

- **What happened:** row 1 quoted a price from a stale cached page and row 8 missed a badge in a page footer. Both are retrieval problems that a newer model wouldn't fix. ([Failure taxonomy](02-failure-discovery/failure-taxonomy.md))
- **Apply it:** tag each failure with its likely cause (prompt, retrieval, data or model) before proposing a fix.

### 7. Separate agent failures from policy failures

- **What happened:** I first failed row 13 for calling a lawsuit "ongoing", then found that sentence is the mandated refusal wording, and reversed it. The agent followed policy; any fault is in the policy. ([Audit log](02-failure-discovery/audit-log.md))
- **Apply it:** check the spec and guidelines before blaming the agent. Log policy problems separately, because the fix belongs to a different owner.

## Judges

### 8. Judge with a different model family from the generator

- **What happened:** where Claude scored its own summaries, GPT-6 agreed, but that was only knowable after the cross-family check. A judge marking its own family's work proves nothing on its own. ([Module 1 eval](01-evaluation-strategy/eval-harness-proof.md))
- **Apply it:** keep the generator and judge in different families. If the generator's family is unknown, use judges from two families.

### 9. Write one check per failure

- **What happened:** a broad rubric ("contradicts, or leaves out a fact that changes the meaning") flipped its call on rows 5 and 6 between runs. A judge written for one named failure gave the same 20 calls twice. ([Audit log](02-failure-discovery/audit-log.md), [eval suite](03-eval-suites/eval-suite.md))
- **Apply it:** one named failure per judge prompt, with the pass and fail patterns spelled out.

### 10. Keep the answer key out of the judge's prompt, but give it the policy

- **What happened:** with my audit pasted into the prompt, GPT-6's judge failed four rows that weren't the failure being tested (2, 6, 8, 9). In a fresh chat without the audit, all four passed. Without the audit it also failed row 13, a refusal in the mandated wording, because nothing told it that wording was required. One controlled run each way, so supported rather than proven. ([With audit](03-eval-suites/results/gpt6-suite-reply.md), [without](03-eval-suites/results/gpt6-no-audit-reply.md))
- **Apply it:** give the judge the question, the answer, the reference, and any policy that defines legitimate behaviour, such as mandated wording or refusal rules. Never give it the expected labels.

### 11. Agreeing on a score isn't agreeing on the reason

- **What happened:** Claude and GPT-6 both failed the same summary, but only Claude noticed it had softened a delay; GPT-6 flagged only the added claims. Cohen's κ would count that as full agreement. ([Module 1 eval](01-evaluation-strategy/eval-harness-proof.md))
- **Apply it:** read the judge's reasons on a sample, not just its scores.

### 12. Run the judge one row and one check per call, more than once

- **What happened:** the same judge prompt on the same model changed 0 of 20 calls between two runs when sent one row per call, and 2 of 20 when sent as a 20-row batch. The batched runs drifted on the check's scope in both directions: one failed an added detail the check doesn't cover (row 9), the other passed a stale price as out of scope (row 1). Both still caught all six real cases. When GPT-6 ran three checks in one prompt, its judge borrowed the rule check's word lists on rows 1, 6 and 7. ([Results](03-eval-suites/results/))
- **Apply it:** one row and one check per call, run twice, and report how many calls changed.

## Checks and suites

### 13. Write checks for your failure; generic rules don't transfer

- **What happened:** the course's generic price and legal rules caught 1 of 16 failures, and that one only because a disclaimer was missing, not because the price was stale. Checks written for inflated facts caught all 6 cases. ([Eval suite](03-eval-suites/eval-suite.md))
- **Apply it:** derive every rule from your own failure taxonomy, then check that each catch is the real problem and not a formatting coincidence.

### 14. A rule written from your audit is in-sample

- **What happened:** the word-pair rule caught 6 of 6 on the 20 rows its word lists came from. On 30 fresh answers written by a different model, it caught 4 of 13 and failed 5 of 17 faithful ones, because new wording slipped past it and it couldn't tell a kept qualifier from a dropped one. Part of its 6 of 6 came from words in the questions, not the answers. ([Eval suite](03-eval-suites/eval-suite.md), [test set](03-eval-suites/fixtures/reworded-test-set.csv))
- **Apply it:** before a rule can block a release, test it on fresh cases written by someone, or something, that never saw the rule. Include faithful answers that keep the qualifier, so false alarms show up.

### 15. Count in code, never in the model

- **What happened:** GPT-6's row-by-row calls were sound, but its own summary table contradicted them on every line. ([GPT-6 reply](03-eval-suites/results/gpt6-suite-reply.md))
- **Apply it:** models make the row-level calls; code computes catches, misses and false alarms.

### 16. Code for rigid rules, the judge for meaning

- **What happened:** a word-list rule for inflated facts matched the judge in-sample, then failed out of sample, while the judge caught 13 of 13 fresh cases. The safety rule written as code misread "No native connector" as keeping the limit. Inflation is a question of meaning, and code can't read meaning. ([Eval suite](03-eval-suites/eval-suite.md))
- **Apply it:** build the pyramid by the kind of check, not by cost alone. Code checks the rigid things (format, required wording, numbers against a source of truth), the judge decides meaning, and humans calibrate the judge. A cheap rule that can't read meaning is an early warning, never a gate.

## Working habits

- **Keep every run as evidence.** Saving each judge run is what made the range in rule 4 measurable after the fact.
- **State the limits next to the result.** Each deliverable here has a method note saying what was run, by which model, and what it can't show.
- **Label hypotheses as hypotheses, then test them.** Rules 10 and 12 started as guesses. Small controlled tests now support both, and each says how small.
