# Module 5 · Eval Budget · Ascend IQ

**Quarterly budget cap:** $200,000
**Online eval spend:** $150,000 (2 of at most 3 online evals)

## Budget

| Failure | Trust metric | Risk | Level | Cost |
| --- | --- | :---: | :---: | ---: |
| Data Fabrication | Hallucination Rate | P0 | Online eval | $85,000 |
| Context Specificity | Robustness | P1 | Periodic audit | $7,000 |
| Overconfident Tone | UX Trust | P1 | Online eval | $65,000 |
| Data Bias | Fairness | P2 | Periodic audit | $5,500 |
| Slow Answers | Latency | P3 | Code-based check | $1,250 |

## Downgrades

### Periodic audit · Context Specificity (Robustness · P1)
- **Cheaper check:** Each week, an analyst checks 50 random live answers against the exact question, half drawn from questions that narrow the ask: negative reviews only, one tier, one region, one date range. Each confirmed miss is corrected with the client and joins the regression set. More than 2 misses in 50, two weeks running, reopens the online split with the CPO.
- **Why it’s enough:** A missed ask is usually visible: the client asked for the negative reviews, gets all of them, and asks again. Nobody can see a guess stated as fact, so that one gets the online eval instead; it was the most common failure in my audit, 6 of 20 answers, and missed asks weren't among its failure categories. Half the sample comes from narrowed questions, where a miss the client can't spot, such as the wrong pricing tier, is most likely.

### Periodic audit · Data Bias (Fairness · P2)
- **Cheaper check:** Every two weeks, an analyst scores 20 US and 20 APAC answers to matched questions from 1 to 5 for completeness and range of sources, against a reference answer.
- **Why it’s enough:** It's P2: a thinner APAC answer costs depth, not accuracy. Invented data is the online Data Fabrication eval's job, so this audit only has to catch thinner answers. Most questions are about US markets today, so a two-weekly comparison spots a gap before APAC clients do. If APAC averages more than half a point below US over a month, 40 answers a region, it moves up a level.

### Code-based check · Slow Answers (Latency · P3)
- **Cheaper check:** A timer on every answer that tracks live p95 against the 2.0-second target and alerts when a long, multi-step question takes more than 10 seconds, plus a timed run of the golden set's multi-step questions on every release.
- **Why it’s enough:** Time needs no judgement: a timer measures every answer exactly, so an online eval would add cost, not accuracy. It's P3. The staging gate in my launch strategy stops slow releases, and live p95 catches slowdowns under real load.

## Why these two are online

- **Data Fabrication (P0, $85,000):** a made-up price or review count breaks the verified-data promise behind $50k+ renewals. Wrong numbers on the core use case were a P0 in my [audit](../02-failure-discovery/failure-taxonomy.md) (rows 1 and 7). The judge is held to the bar in my [eval spec](../03-eval-suites/eval-spec.md): at least 95% recall, no more than 6% false alarms and κ 0.6 or above against human labels. A flagged answer goes to the account owner, who corrects it with the client the same day.
- **Overconfident Tone (P1, $65,000):** despite the label, this isn't about phrasing. "States guesses as facts" is the inflated-facts failure behind my HOLD call: 6 of the 20 audited answers, such as an invited speaker listed as confirmed. A client can't see it, and a cheap check misses it: on fresh answers my Module 3 word rule caught 4 of 13 and the judge 13 of 13 ([eval suite](../03-eval-suites/eval-suite.md)).
- **Why $50,000 of the online cap stays unspent:** no third online eval fits or pays its way. Context Specificity would take online spend to $220,000 and Data Bias to $205,000, and Slow Answers online ($25,000) buys nothing a timer doesn't. The cap is a limit, not a target.
- **One judge may cover both:** my [calibrated rubric](../03-eval-suites/judge-calibration.md) already names any claim its source doesn't support, so one judge call could score both online failures and the real cost come in under $150,000.

## After the CPO critique

GPT-6, playing the CPO, wanted Overconfident Tone ($65,000) moved to an audit and Context Specificity put online. I kept the split. It read "Tone" as phrasing, but the tool defines this failure as a guess stated as fact, Ascend IQ's most common P0, and the export gave no reason for the online picks; the section above now does. Its swap would also put online spend at $155,000 and leave $45,000 of the online cap spare, not the "$65K of budget headroom, less the cost of the new online Robustness eval" it described.

Its operational points did change the checks:

- **Context Specificity:** a random sample, half from narrowed questions; each miss corrected with the client; more than 2 in 50, two weeks running, reopens the online split.
- **Data Bias:** a 1-to-5 completeness score against a reference answer, and a trigger when APAC averages more than half a point below US over a month.
- **Slow Answers:** live p95 against the 2.0-second target as well as the 10-second alert, because the staging gate can't see slowdowns under real load.
- **Data Fabrication:** written thresholds and same-day escalation, which it said the P0 needs to hold up in a customer incident review.

Noted, not acted on: US against APAC alone can't show fairness across every market. True, but this failure is defined as US against APAC; another region would be a new failure mode for next quarter's budget.

## How this was written

- **Format.** Everything up to "Downgrades" is the lab tool's export format; the levels and reasons are mine. The export has no place for why the online evals were chosen or for the critique, so those sections follow it.
- **Sample sizes and thresholds are mine;** the tool fixes only the level costs. "Most questions are about US markets today" comes from the course's own Ascend IQ example in Lab 1.
- **Labels differ from my Module 1 canvas.** The course files Overconfident Tone under UX Trust, which my canvas left out as too subjective. In the canvas's terms it's hallucination rate: claims stronger than the source. The canvas's robustness metric, calibrated refusal, isn't among the lab's five failures; my [Module 5 notes](NOTES.md) carry it as an open gap.
- **Renamed from `budget.md`** to the current lab's file name.
- **The CPO critique came from GPT-6,** a different model family from Claude, which drafted the options with me, run on the lab's critique prompt with this budget pasted in.
