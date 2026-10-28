# CI Eval Gate Policy · Ascend IQ

**Pull request:** "Rewrite Ascend IQ's answer prompt". GitHub Actions runs the eval suite on the golden set and compares each check with the current version.

## Gate policy and CI result

| Check | Method | Current version | This pull request | Gate | Fails when | Result |
|---|---|---|---|---|---|---|
| Factuality | LLM judge, 50 answers | 96% (48 of 50) | 88% (44 of 50) | Hard | it drops more than 2 points | Down 8 points · blocks the merge |
| Pricing accuracy | Rule check against the pricing page, 20 answers | 100% (20 of 20) | 100% (20 of 20) | Hard | it drops more than 0 points | No change · passes |
| Refuses legal questions | Safety rule, 10 questions | 100% (10 of 10) | 90% (9 of 10) | Hard | it drops more than 0 points | Down 10 points · blocks the merge |
| Tone | LLM judge, 50 answers | 92% (46 of 50) | 90% (45 of 50) | Advisory | it drops more than 0 points | Down 2 points · warning only |
| Latency (p95) | Timer | 1.8 s | 2.3 s | Advisory | it goes above 2.0 s | 0.3 s over · warning only |

**Gate result:** merge blocked by Factuality and Refuses legal questions. Warnings on Tone and Latency (p95).

## Merge decision

**BLOCK.** The change answers 1 of the 10 legal questions instead of refusing it, and 4 more of the 50 answers are now factually wrong, an 8-point drop against a 2-point limit. Either alone blocks the merge. Tone slipped by one answer and latency rose 0.5 seconds; both warn, and neither holds the merge.

## Which checks I made Hard, and why

- **Factuality, with a 2-point limit:** a wrong answer under our name is the risk Ascend IQ can't carry. Two points is one answer in 50, which allows for judge noise: the Module 3 judge raised 1 false alarm in 17 fresh answers. That tolerance can't ship an inflated fact, because the [Release gate](launch-strategy.md) still holds those to zero.
- **Pricing accuracy, with no drop allowed:** a code check has no noise, so any drop is a wrong price reaching a client, the Hard gate on [gate-map](gate-map.md) row 1.
- **Refuses legal questions, with no drop allowed:** a legal answer reaching a client is legal exposure the safety guidelines exist to prevent. This is the reverse of gate-map row 14: there the refusal was right and needed no gate; here the check catches the mandated refusal going missing.

## Which I left as warnings, and why that's safe

- **Tone:** a person reviews every draft before it's sent, so a one-answer slip costs polish, not a client. It warns on any drop so the trend stays visible, as gate-map row 17 does.
- **Latency:** the Soft gate in staging still pauses the release above 2.0 seconds at p95 ([launch strategy](launch-strategy.md)). The warning here is an early signal on the pull request, as in the gate map.

## Debrief

**The blocking dimension:** factuality. **The regression that flips my merge call:** a drop of more than 2 points, which is two newly wrong answers in 50.

## How this was run

- **In the repo, not the practice page.** The course's CI practice simulates the pipeline and has no markdown export, so this file mirrors its table. The results apply the page's own rule (a check fails when its drop exceeds the limit, or latency exceeds the cap), reproduced in code.
- **Per check, never one blended score.** Blended across the 130 scored cases, this change falls from 95.4% to 90.8%, and the legal answer is worth 0.8 of a point. A blended gate would bury the one regression that most needs to block.
- **The revised course's data.** The template's older PR #218 table, with floors on six dimensions, is replaced by the practice page's five checks and drop limits.
