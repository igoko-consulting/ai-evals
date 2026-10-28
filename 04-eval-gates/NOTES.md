# Module 4 notes: Ship Safely with Eval Gates

Drafted 28 Oct 2026, before class. Sources: Module 4 slides, pre-read, the [revised lab guide](https://product-school-platform.github.io/ps-content-library/certifications/aiec/2026.1/Modules/Module%204%20-%20Lab%20Guide.html) and the [CI practice](https://product-school-platform.github.io/ps-content-library/certifications/aiec/2026.1/Modules/M4%20-%20Post-Class%20Practice.html).

## The shift

- **Evaluators measure, gates enforce:** an evaluator produces a score and does nothing with it. A gate uses that score to decide whether a change can ship. In the course's airport analogy, the scanner is the evaluator and the rule that stops the belt is the gate. Missed: a gate is only as good as its evaluator. A Hard gate behind the course's Module 3 judge, at κ 0.27 against my labels, would have blocked on noise.
- **Architect to gardener:** traditional software is built and stays built. AI is grown, and needs tending: watch for drift, prune bad behaviour, feed it new data. Gates are the pruning shears.
- **Autonomy is earned:** the Tuned Trust Loop runs a precision cycle before launch and a trust cycle after, meeting at the gate. GitHub Copilot went from ghost text to chat to an agent that edits across files, each step justified by data from the last. A support bot drafts internal notes first, and earns auto-sending on low-risk tickets once people accept more than 95% of its drafts. Missed: the loop needs a signal like acceptance. A VP who quietly stops trusting Ascend IQ never rejects a draft.

## Why gates

- **The rationalisation trap:** under launch pressure, teams explain bad data away: "it's just one metric", "we'll fix it later". A gate removes that option. Shipping past it takes an explicit override, so the release becomes a conscious decision to accept the risk.
- **Missing gates make headlines:** a recurring pattern is an AI feature presenting a satirical or low-trust source as confident fact. The post-mortem always finds the same three missing gates: source reliability, safety and plausibility, and factuality.
- **Gates live in two places:** in CI before deployment, which is this module, and at runtime as an inline filter that refuses a critical failure before the user sees it. Missed: some failures only exist at runtime. Ascend IQ's stale price came from a cache, which no pull request would show.

## Three levels, three places

| Level | What happens | Use it for | Course example |
|---|---|---|---|
| Advisory | Warns, never blocks | Low risks you want to track | A minor tone slip in a consumer chatbot |
| Soft | Pauses the release until someone signs off a documented override | Medium risks; about 80% of gates | Latency up 1.5 s in a key productivity feature |
| Hard | Blocks the release until it's fixed; no override | Critical P0 risks | Unsafe medical advice in a health chatbot |

| Placement | What runs there | Gate levels |
|---|---|---|
| Pull Request | Quick code checks on every change, no model needed | Advisory, Hard |
| Staging | The full suite with an LLM judge, against the golden set | Soft, complex Hard |
| Release | The last line of defence | Hard only |

- **Rule of thumb:** if a keyword search can catch it, run it on the pull request. If not, staging. If shipping it creates legal or safety risk, release.
- **Hard gates follow the business objective, not the product category:** compliance products hard-gate hallucination, bias and unsafe content; engagement products hard-gate latency and tone; internal tools hard-gate whatever makes employees stop trusting the tool. Ascend IQ sells verified data to VPs, so it sits in the compliance column although it isn't regulated.
- Missed: the course calls Soft the sweet spot but says little about keeping the override honest. A Soft gate overridden every release is an Advisory gate with paperwork.

## Gates in CI

- **The suite runs on every pull request:** GitHub Actions runs the evals, compares each dimension with a stored baseline, and fails the build when one regresses past its limit, like a failing unit test. Engineering writes the YAML. The PM decides which dimensions are checked, what counts as a regression, and what blocks versus warns.
- **The regression golden set, at least 30 cases:** hand-reviewed cases the product must never get wrong again, each tagged with a severity from the taxonomy. Below about 30, one flaky result moves the pass rate by 3 points or more. Every production failure becomes a new case. A P0 or P1 regression fails the gate; a P2 warns.
- **Per dimension, never blended:** a change can lift factuality while sinking safety, and a blend hides the trade. In my CI policy, the one legal answer is worth 0.8 of a point across 130 cases.
- **Deterministic replay:** CI replays recorded fixtures instead of calling live models, so a red check means the change, not chance. Asana's Enzyme migration showed both sides: CI was the definition of done, and flaky infrastructure was where people had to step in. A gate nobody trusts gets ignored.
- **The stack:** GitHub Actions as the engine, a Python eval notebook as the ruler, and LangSmith, Braintrust or Phoenix as an optional dashboard and drift monitor. Keep the judge provider-neutral and from a different family from the system under test.
- Missed: confirm engineering can run it before promising it. Gating in CI needs infrastructure to run models, store baselines and compare per pull request.

## Thresholds in the PRD

- **Unwritten rules are the first to go:** if the gates live only in a meeting or a deck, they aren't real. In the PRD, done means the functional requirements are met and the release criteria are met.
- **Five parts:** metric, gate severity, threshold, dataset and evaluator. The dataset closes the "tested on easy data" loophole; the evaluator links to the Module 3 eval spec. The eval spec answered who owns it and why it matters; the PRD threshold answers whether we passed and can ship.
- **NeoBank example:** Hard on invented rates or fee waivers at 0%, Soft on p95 latency under 2.0 s, which the PM may approve over for accuracy, and Advisory on tone at 4.0 of 5 or above, all on one golden set.
- **The pipeline tax:** every eval adds time and cost to every CI run. Gate the P0s hard and keep the long tail cheap, sampled or run less often.
- **The PM legislates, engineering enforces:** the PM sets the number, owns the trade-off and chooses the path when a gate fails: delay, fix or mitigate. Engineering builds the test, runs the pipeline and fixes the cause.
- **Levers when a Soft gate fails:** staged rollout, feature flag, beta label or delay. Missed: none of them applies to a Hard gate.

## Labs

- **Lab 1, gate map:** six answers Engineering flagged, each given a gate, a placement and a business reason, then defended against a sceptical engineering lead. Output: [gate-map.md](gate-map.md).
- **Lab 2, release criteria:** a Hard, Soft and Advisory row for the PRD, a request for engineering, and a plan for a Soft-gate failure. Output: [launch-strategy.md](launch-strategy.md).
- **CI practice:** a gate policy for a pull request that rewrites the answer prompt, and the merge call. Output: [ci-gate-policy.md](ci-gate-policy.md).

## Discussion questions

- **The headline moment in my domain:** Ascend IQ passing off unverified data as verified. A VP repeats an inflated fact in a board pack, such as a "seamless" HubSpot integration that actually runs through Zapier, or a competitor's fees taken from a blog post, and the trail leads back to Ascend. For a company that sells verified data at $50k+ a year, that's the story. It's the course's missing-gate pattern, and my trajectory lab found a live case: a barred web search cited to a client.
- **The non-negotiable rule:** every claim comes from a sanctioned, verified source and says no more than that source does. Code fails any answer citing a source outside the sanctioned set, and the inflated-facts judge fails any claim stronger than its source. Threshold: zero confirmed in at least 100 held-out questions, with the judge at 95% recall or better. A Hard gate at release.
- **The hardest row to place:** row 8, the API comparison. It carries the same Hallucination label as rows 1 and 5, and it's the row GPT-6 would change first: it wanted a code check on the pull request. I kept the Hard gate on the judge in staging and added the code check as a warning, because my Module 3 word rule caught 4 of 13 fresh failures and raised 5 false alarms in 17.
- **The trade-off I debated:** three Hard gates against the course's guide that about 80% of gates should be Soft. Each of mine sits behind an exact check (pricing) or a calibrated judge (rows 5 and 8), so none blocks on noise, and the cost is a judge call per answer in staging. The pressure is real, though: the CPO wants the top 50 accounts next month, and a Hard gate is the one call no one can override.

## What this means for Ascend IQ

- **The launch strategy confirms HOLD:** the inflated-facts Hard gate fails today, at 6 of 20 answers, and no rollout lever ships around a Hard gate. The staged rollout only covers the latency Soft gate.
- **The gate map has no source gate:** the lab's six rows don't include the barred web source from my trajectory lab. A code check that answers cite only sanctioned sources is the first gate I'd add.
- **A Hard gate is only as good as its judge:** my rubric reached 12 of 12 in calibration, but on the same 12 answers it was written to fix. The Hard gates on rows 5 and 8 need that judge re-measured on new answers before they go live.
- **The golden set doesn't exist yet:** the gates assume at least 30 regression cases and 100 held-out questions. I have the 20 audited answers and 30 fresh ones. Building the set is the first ask of engineering.
