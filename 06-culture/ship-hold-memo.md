# Ship-or-Hold Memo · Ascend IQ

> **Decision:** HOLD

## The Answer

I recommend we hold Ascend IQ's enterprise launch until it passes its release gate, because it overstates its sources in 6 of 20 audited answers, and one overstated fact repeated by a VP puts a $50k+ renewal at risk.

## The Arguments

### 1. Ascend IQ would break the verified-data promise our clients pay for

Evidence: 6 of 20 audited answers (30%) state facts their sources don't support, such as an invited speaker listed as confirmed. The release bar is 0 in 100 held-out questions. 2 other answers quote a wrong price or reverse a comparison, and even the most lenient judge tried fails 9 of 20.

### 2. A staged rollout wouldn't contain the risk

Evidence: The rollout's first 5 accounts are top-50 clients at $50k+ a year each, so the rollout alone would expose at least $250k a year of renewals to a build that fails its release gate. The staged rollout was planned for the latency gate, not for facts.

### 3. The hold has a clear exit: the check catches the failure, and the test set and a human-label check are still missing

Evidence: On 30 fresh answers the judge caught 13 of 13 overstatements with 1 false alarm in 17 (5.9%), inside the spec's bar of 95% caught and 6% false alarms. The sample is small, so the judge has to hold that bar again on the golden set and agree with human labels there, and none of its 100 held-out questions or 30 regression cases exist yet.

## Next Step · Decision Needed

Please approve two things by Friday 6 November: the hold, and engineering time to build the golden set and fix the overstatements. I'll bring you the Release gate result by Friday 4 December, and if it passes, the staged rollout to 5 of the top 50 accounts follows.

## After the Pressure Test

The call stands; four changes. GPT-6, as a sceptical CPO, called HOLD defensible but found that arguments 1 and 2 both leaned on the 30% rate, and read $250k as a predicted loss. Argument 2 now counts only the renewals exposed, and argument 1 says the 2 wrong numbers are separate answers. Argument 3 drops "proven quickly", which nothing backed, and says the judge's 30-answer test is small and must hold again on the golden set. The ask names engineering time as a second approval. I didn't add an engineering estimate: my evals don't contain one, so the 4 December date is my commitment, and engineering sizes the work.

## Evidence · Trust Metrics

| Metric | Result | Gate | Status | Source |
|---|---|---|---|---|
| Inflated facts | 6 of 20 (30%) | 0 in ≥100 held-out questions | FAIL | [Eval spec](../03-eval-suites/eval-spec.md) |
| Wrong numbers on the core use case | 2 of 20 | Hard: 100% of prices match; 0% contradicted specs | FAIL | [Gate map](../04-eval-gates/gate-map.md) |
| Judge recall | 13 of 13 | ≥95% | PASS, small sample | [Eval suite](../03-eval-suites/eval-suite.md) |
| Judge false alarms | 1 of 17 (5.9%) | ≤6% | PASS, small sample | [Eval suite](../03-eval-suites/eval-suite.md) |
| Judge agreement with human labels | Not measured yet for this judge | κ ≥ 0.6 | Not measured | [Eval spec](../03-eval-suites/eval-spec.md) |
| False refusals | 2 of 20 | No gate yet | Open | [Failure taxonomy](../02-failure-discovery/failure-taxonomy.md) |
| Latency p95 | Not measured yet; one answer in the gate-map lab took 4.2 s | Soft: ≤ 2.0 s | Not measured | [Launch strategy](../04-eval-gates/launch-strategy.md) |
| Off-brand tone | 1 of 20 | Advisory: 0% slang | Warning only | [Gate map](../04-eval-gates/gate-map.md) |
| Fairness | Not measured yet | None set | Not measured | [Module 5 notes](../05-scale/NOTES.md) |
| Golden set | 0 of 100 held-out questions; 0 of 30 regression cases | ≥100 held-out, ≥30 regression | Not built | [Module 4 notes](../04-eval-gates/NOTES.md) |

## Business Risk

- **Ship now:** the staged rollout exposes at least $250k a year of renewals, and a full launch exposes the top 50, at least $2.5m a year, to a build that fails its gate. An overstated fact looks like a correct one, so the first sign is a VP repeating it.
- **Hold:** the launch slips past 4 December, and the slow digging Ascend IQ exists to remove stays in place. The cost of that delay in renewals isn't measured yet.

## Reflection

Defining "good enough" meant admitting what a bar can't prove. Zero inflated answers in 100 sounds like perfection, but it only keeps the true rate under about 3%, so a pass is a bound, not a guarantee. And the evaluator had to earn its place: the word rule met the bar in-sample, then caught 4 of 13 fresh answers. Good enough has to be a number, measured on the right sample.

## How this was written

- **Format.** Everything up to "Next Step" is the lab tool's export format; the call, arguments and ask are mine. The sections after it cover what the course's older runbook asks for.
- **Overstates means inflated facts.** The memo uses the plainer word for the CPO; it's the inflated-facts P0 everywhere else in the repo.
- **Written 4 Nov 2026.** The dates in the ask are my commitments, not engineering estimates.
- **Derived numbers.** $250k is 5 × $50k, $2.5m is 50 × $50k, and 5.9% is 1 of 17.
- **Argument 3 was tightened on 5 Nov,** after a final review found its title claimed more than the evidence table: the judge's agreement with human labels isn't measured yet.
- **The pressure test came from GPT-6,** a different model family from Claude, which drafted the options with me, run on the lab's prompt.
