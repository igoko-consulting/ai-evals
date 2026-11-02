# Module 5 · Coverage Matrix · AI Report Summaries

## Coverage Row

| Product | Hallucination Rate | Fairness | Latency | UX Trust | Robustness |
|---|---|---|---|---|---|
| AI Report Summaries | ✅ Covered | ❌ Gap | ⚠️ Partial | ❌ Gap | ❌ Gap |

## What Runs Today

- An LLM judge compares each summary with its source report before every release.
- Response time is logged, but nobody has set a target.

## Accepted Gap

**Fairness.** We haven't shown this risk is low, only that a dedicated check isn't worth it yet: an audit across every sector and region would take more analyst time than the risk justifies today. The completeness judge in our Robustness plan will report its failure rate by sector and region, so uneven quality will show up there first.

We’ll look again: if the completeness judge fails any sector or region at twice the overall rate over a month, if a client says their sector's summaries are thinner, or when next quarter's eval budget is set, whichever comes first.

## Critical Gap

We’ve flagged Robustness as the most critical gap for AI Report Summaries because the release judge only sees the test reports, while live reports get longer, denser and more varied. A summary that drops the key finding reads as well as a good one and goes straight to the client. The client notices first, often after acting on it, and one miss with a top-50 account puts a $50k+ renewal at risk. To close it, we'll add a completeness judge, from a different model family, that checks every summary against its source's key findings before it's sent. A drift monitor also flags reports unlike the release test set (length, tables, report type, sector, region, language). Any summary the judge fails, or of a flagged report, waits for an analyst's check. Each miss the analyst confirms joins the release test set. Before it can block summaries, the judge must catch 95% of known misses with no more than 6% false alarms. Owner: the Report Summaries PM. Judge and drift monitor live by 30 Nov 2026.

## After the Pressure Test

Two changes; the marks stand. GPT-6 asked how a drift monitor would catch a summary that drops the key finding of a normal-looking report. It wouldn't: it flags unusual inputs, not bad outputs. So every summary now goes through a completeness judge before it's sent, and the drift monitor is a second trigger for the analyst check. GPT-6 also called my Fairness reasoning too confident, because an accurate summary can still leave out more for some sectors than others. I still accept the gap, but the judge now reports failures by sector and region, so uneven quality shows up without a separate audit. UX Trust stays open as the next gap to close.

## Method and ground truth

The two cells with a check today.

**Hallucination Rate (✅)**
- **Method:** an LLM judge compares each summary with its source report before every release.
- **Ground truth:** the source report.
- **What it misses:** it runs on the release test set, not on live summaries, so a live summary that invents a claim goes out unchecked. The new completeness judge runs on live summaries, but it looks for missing findings, not false ones.

**Latency (⚠️)**
- **Method:** response time is logged.
- **Ground truth:** none yet. With no target, nothing can fail, which is why it's Partial. A p95 target would make it a check, as the 2.0-second target does for Ascend IQ in my [launch strategy](../04-eval-gates/launch-strategy.md).

## What else GPT-6 raised

- **UX Trust is a real risk for an external product:** agreed. Nothing checks tone, and summaries reach clients with no one reviewing them. It stays open as the next gap to close, not one I accept.
- **Its spec for the plan is now met:** the check is a completeness judge plus a drift monitor; the data is the source's key findings and each report's length, tables, type, sector, region and language; it runs on every summary; an analyst holds anything flagged; and confirmed misses feed the release test set.

## How this was written

- **Format.** Everything up to "After the Pressure Test" is the lab tool's export format; the marks, gaps and plan are mine. The sections after it add what the course's older runbook asks for: a method and ground truth for each covered cell.
- **Why this product, not Ascend IQ.** The lab maps one of Ascend Analytics' four live AI products. Ascend IQ hasn't launched, so nothing runs on it yet to mark. AI Report Summaries is the closest: the same clients, the same promise of verified data, and summarising was my [Module 1 eval](../01-evaluation-strategy/eval-harness-proof.md).
- **What carries over to Ascend IQ.** The completeness judge has to meet the bar in my [eval spec](../03-eval-suites/eval-spec.md) before it can block anything. Confirmed misses joining the release test set is the golden set that [Module 4](../04-eval-gates/NOTES.md) found Ascend IQ doesn't have yet. And the manager's question is the Module 3 lesson again: a check on a cheap proxy misses what a judge on the output catches.
- **The tool's worked examples use the same two metrics for Ascend IQ:** Fairness accepted, Robustness closed. The reasons and checks here are specific to summaries.
- **Assumptions:** reports carry sector and region tags, which the judge's breakdown needs; report volume is low enough for a judge call on every summary; the owner and date are placeholders.
- **The pressure test came from GPT-6,** a different model family from Claude, which drafted the options with me, run on the prompt the lab tool builds from these answers.
