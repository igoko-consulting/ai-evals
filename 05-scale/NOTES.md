# Module 5 notes: Run Evals on Live Traffic Across Product Lines

Drafted 2 Nov 2026. Sources: Module 5 slides, pre-read and the [revised lab guide](https://product-school-platform.github.io/ps-content-library/certifications/aiec/2026.1/Modules/Module%205%20-%20Lab%20Guide.html).

## The shift

- **Passing every gate isn't the end:** gates decide whether a change can ship, but quality still slips once real people use the product. Drift: the world changes while the model stays the same. Bias: skew creeps back in after pre-launch de-biasing. Missed: Ascend IQ's stale price is drift at its simplest. The pricing page changed and the cached answer didn't, and no pull request would have shown it.
- **Offline decides whether a change ships; online decides whether the product is still good:** offline evals run fixed cases in CI, so the same change always gets the same result, but they only prove the cases someone thought of. Online evals run the same checks on a sample of real traffic every day, which is where new kinds of questions show up.

## Scoring live traffic

- **Traces make live traffic scorable:** a trace records one request end to end: the question, each step the agent took, the sources it pulled and the answer. The Module 3 checks run on the trace, and a failed request opens at the step where it went wrong. My [trajectory lab](../03-eval-suites/trajectory.md) scored one path by hand; traces are how that runs in production.
- **Sample, don't score everything:** score a random sample, more of the high-risk questions such as pricing, and every request a cheap check flags. Engineering builds it; the PM requires that live traffic is recorded, scored and sampled. Missed: the sampling rule is where the budget is really set. The lab prices an online eval as continuous, while the slide says to score a sample.
- **Match the monitor to the risk:** code-based checks keep running after launch, and two more kinds of monitoring catch what they miss.

| Monitor | What it does | What it catches | Ascend IQ example |
|---|---|---|---|
| Drift monitor | Compares the questions live users ask with the ones the product was built and tested on | New kinds of questions, users or topics the tests don't cover | Alerts when the mix of industries, company sizes or question types moves away from the golden set |
| Periodic audit | People review a sample of high-risk answers on a set schedule | Bias and fairness gaps only a person can judge | A quarterly sample of US and APAC briefs, compared for uneven coverage |

- **The closed loop:** golden set, eval gate, live traffic, error feed, and back. The worst live failures become new golden set cases, and the fix ships through the gate. Missed: the loop needs an owner for the error feed and a golden set to grow. Ascend IQ has neither yet.

## Across product lines

- **The scaling tax:** when each team builds its own evals, every team pays for the same judge prompts and labelling, "helpfulness" means something different in each product, one product has fairness checks and the next doesn't, and leadership has no single view of risk. Clients and regulators hold the whole brand to its weakest product.
- **The coverage matrix:** every product against the same five Module 1 trust metrics, each cell naming the check that covers it. ✅ means a check runs regularly, ⚠️ that someone spot-checks it by hand or the check covers only part of the risk, and ❌ that nothing checks it.
- **Internal and external:** external products fail in public, so Hallucination Rate, UX Trust and Latency hurt most. Internal products fail quietly into everything downstream, so Robustness and Fairness hurt most. Missed: the real test is whether anyone can see the failure, not who the user is. A summary that drops its key finding is external but fails as quietly as an internal pipeline, which is why I closed Robustness first in Lab 1.

## Spending a finite budget

- **Three budgets:** annotation (experts labelling gold data and running audits), compute (running evaluators in the pipeline) and velocity (slower releases). Coverage, cost and velocity pull against each other.
- **Three levers:** the coverage matrix says where to spend; the 80/20 rule says how, with most team time on targeted evals and error analysis rather than rebuilt infrastructure; the sampling cadence says when, with light checks daily and exhaustive tests at release.
- **Fund what nobody can see:** in Lab 2 I put Overconfident Tone online and audited Context Specificity, both P1. A client spots a missed ask and asks again; nobody spots a guess stated as fact. Missed: the lab prices each failure separately, but one judge call can score several failures, so the real unit of cost is the judge call. Sharing judges across products also cuts the scaling tax.

## Labs

- **Lab 1, coverage matrix:** AI Report Summaries, one of the four live products. Fairness accepted, but measured through a new judge; Robustness closed with a completeness judge on every summary, after GPT-6 showed a drift monitor alone flags unusual inputs, not bad outputs. Output: [coverage-matrix.md](coverage-matrix.md).
- **Lab 2, eval budget:** Data Fabrication and Overconfident Tone online, $150,000 of the $200,000 cap, and the rest downgraded with samples, thresholds and triggers. GPT-6, as CPO, read "Tone" as phrasing and wanted it swapped out; the split held. Output: [eval-budget.md](eval-budget.md).

## Discussion questions

- **Where quality slips after launch:** Ascend IQ's stale price. The vendor changes its pricing page, the cache doesn't refresh, and Ascend IQ keeps quoting $49 when the price is now $59. The VP notices first, when the vendor quotes the new price in a negotiation, and from then on doubts every other number.
- **The gap I accepted:** Fairness on AI Report Summaries. A dedicated audit across every sector and region would cost more analyst time than the risk justifies today, and the new completeness judge reports its failures by sector and region anyway. I'd change my mind if the judge fails any sector or region at twice the overall rate over a month, if a client says their sector's summaries are thinner, or at next quarter's budget.
- **Whether internal or external changed the call:** yes, but not the way the course's guide suggests. For an external product the guide points to Hallucination, UX Trust and Latency, because users see them. I closed Robustness first because a summary that drops its key finding is the failure a client can't see.
- **The P1 I moved below online, and the defence to the CPO:** Context Specificity, to a weekly audit of 50 answers. A missed ask is visible: the client asked for the negative reviews, got all of them, and asks again. A guess stated as fact isn't visible, and it was 6 of my 20 audited answers, so that's where the online money goes. If the audit finds more than 2 misses in 50 two weeks running, I reopen the split.
- **What the cheaper check misses:** a rare miss the client can't spot, such as the wrong pricing tier, that falls between weekly samples. I can live with it because half the sample targets the narrowed questions where those misses happen, each one found is corrected with the client and joins the golden set, and the trigger moves it online if it turns out to be common.

## What this means for Ascend IQ

- **The course's Ascend IQ row matches my gate map:** Hallucination and Latency gated, tone advisory, Fairness and Robustness open. My P1 false refusals (audit rows 8 and 18) sit in that Robustness gap, with no gate or monitor on them yet.
- **The budget only starts once the HOLD lifts:** online evals score live traffic, and Ascend IQ has none until the inflated-facts Hard gate passes. The first live traffic to score would be the staged rollout to 5 of the top 50 accounts.
- **The stale price still needs a runtime check:** Module 4 left it for this module. A code check that fails any price quoted from a page older than its refresh window is cheap and runs on every answer.
- **The loop needs a golden set to grow:** both labs feed confirmed misses into a golden set, and Ascend IQ's isn't built yet: at least 30 regression cases and 100 held-out questions. That stays the first ask of engineering.
