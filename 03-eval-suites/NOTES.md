# Module 3 notes: Translate Failures Into Systematic Eval Suites

Sessions 3 and 4, from 26 Oct 2026. Sources: Module 3 slides, pre-read, and the [revised lab guide](https://product-school-platform.github.io/ps-content-library/certifications/aiec/2026.1/Modules/Module%203%20-%20Lab%20Guide.html). The slide PDF is missing Section 05 (calibration); that section is rebuilt here from the pre-read and the key takeaways.

## The shift

- **Every high-priority failure needs a guard:** the taxonomy is the map of risks, and each P0 or P1 on it needs an evaluator. "Fix hallucination" is too broad to act on; "check every suggested date against the live calendar API, fail on mismatch" is a requirement engineering can build. Missed: a guard per failure only covers the failures you've found. The audit sets the ceiling on what the suite can catch.
- **Evals are the modern PRD:** the eval spec is the executable definition of good, and it's what the Module 4 gates enforce.

## The evaluator spectrum

| Type | Role | Use when | Real example |
|---|---|---|---|
| Code-based | The guardrail, a kill switch | The rule is rigid and getting it wrong is costly: prices, refunds, banned terms | Stripe blocks a refund promise when the transaction isn't eligible |
| LLM-as-Judge | The scalable editor | Quality is subjective and the volume is too high for people: tone, helpfulness, factuality | Grammarly flags a defensive-sounding draft rather than replacing it |
| Human | The gold standard | The risk is catastrophic, and the other layers need ground truth to calibrate against | Intuit CPAs review 50 high-complexity tax answers a week and update the golden set |

- **The three paradoxes:** deterministic tests suit a probabilistic system because policy is absolute. An AI can grade an AI because nuance has to scale. You still pay for humans because a model can't grade its own safety.
- **Judge laziness:** a long rubric in one call skips criteria. Use one criterion per judge call, then combine the results.
- Missed: per-turn classifiers (jailbreak, looping, policy) sit between code and judge on cost. They're named in the deck but barely covered.

## Score the path, not just the answer

| Dimension | Failure it catches |
|---|---|
| Tool selection | A generic web search instead of the ingestion-status tool |
| Argument correctness | `tier="Pro"` when the user asked about Enterprise |
| No redundant or looping steps | The same lookup four times |
| Recovery | Giving up, or fabricating, after a failed tool call |
| Plan coherence | Drafting the reply before fetching the data |
| Task completion | Returning one price but never making the comparison |

| Matching mode | Rule | Use when |
|---|---|---|
| Strict | Same tool calls, same order | Regulated flows: KYC, payments, clinical |
| Unordered | Same set, any order | Independent steps. The default |
| Subset | Only sanctioned tools | Guarding against off-script or unsafe calls |
| Superset | At least every required tool | Guarding against doing the minimum |

- **The mode is a risk call:** strict matching on a creative task creates noise; loose matching on a regulated flow creates blind spots.
- Missed: trajectory evals need the tool calls logged. My Module 2 audit had no traces, so the path could only be inferred there.

## Building the suite

- **The pyramid:** code checks run on every answer at almost no cost, the judge triages what gets through, and humans calibrate. Never send a person a failure a script could have caught.
- **Coverage rule:** every P0 needs at least one strong evaluator. Partial coverage on a P0 is a risk you're choosing to accept.
- **The green dashboard trap:** evals pass while users leave. Business metrics are the backstop: thumbs down points to tone, churn to drift, drop-off to latency, ticket spikes to factuality.
- Missed: a suite only tests what you imagined. That's why the online loop in Module 5 matters.

## Validating the judge (Section 05, rebuilt from the pre-read)

- **Calibrate before you trust it:** label about 20 traces by hand, run the judge on the same traces, and compute Cohen's κ, which is agreement corrected for chance. Ship the judge at κ 0.6 or above.
- **TPR and TNR are a strategy choice:** safety-first maximises catching real failures (TPR); growth-first maximises passing good answers (TNR). The pre-read's three cases:
  - Telehealth triage at 99% TPR and 50% TNR: likely ship, because safety dominates.
  - Coding copilot at 99% TNR and 40% TPR: likely ship, because trust is the moat.
  - A cost-saving AI judge at 99% TNR and 80% TPR: likely hold, because an 80% ruler invalidates everything measured with it.
- **Biases to design against:** self-preference (use a different model family), position and verbosity bias.
- Missed: κ measures agreement on scores, not on reasons. Two judges can agree for different reasons, as in my Module 1 eval.

## The eval spec

| Part | Question |
|---|---|
| Target risk | What are you testing, and is it an output or trajectory risk? |
| Evaluator | How will you detect it? |
| Threshold | What exact number is required to ship? |
| Business stakes | Why does it matter? |
| Owner | Who monitors and enforces it? |

- **Three audiences:** engineering gets exact pass and fail rules, design gets the fallback the user sees, leadership gets the risk removed and why it's worth the cost.
- **Course example:** a fintech bot's interest rates, checked by code against the rates database, at 100% accuracy with zero tolerance.

## Labs

- **Lab 1, output suite:** three checks for inflated facts, run on all 20 answers. Output: [eval-suite.md](eval-suite.md).
- **Lab 2, eval spec:** the five parts and three messages. Output: `eval-spec.md` (next).
- **Trajectory and calibration labs:** the support-agent trace and the κ loop. Outputs: `trajectory.md`, `judge-calibration.md`.

## Discussion questions

- **An engineering lead wants Layer 1 only for launch. What evidence shows the blind spot?** The course's generic Layer 1 rules caught 1 of 16 audit failures, and that by coincidence. My own rule for inflated facts caught 6 of 6, but on the same rows its word lists came from, so new wording would get past it. Layer 1 alone is only as good as its word list; the judge stays until the rule survives fresh wording.
- **Which audience was hardest to write the spec for?** _After Lab 2._

## What this means for Ascend IQ

- **The P0 is catchable before launch:** a free rule and a judge each caught all 6 inflated-fact answers, with no false alarms.
- **A narrow check is a stable check:** the judge gave the same 20 calls on two runs, where Module 2's broad rubric flipped on two rows.
- **Counts belong in code:** GPT-6's row-level calls were sound, but its own summary was wrong on every line.
