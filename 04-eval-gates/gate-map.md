# Module 4 · Eval Gate Map · Ascend IQ Copilot

## Gate Map

| Row | Failure Mode | Severity | Placement | Rationale |
|---|---|---|---|---|
| 1 | Hallucination | Hard | Pull Request | A wrong price breaks the verified-data promise behind $50k+ renewals. An exact match against the saved copy of the pricing page is cheap enough to block every change. |
| 14 | Relevance | No gate |  | The safety guidelines require this refusal. Gating it would block a compliant model and teach the team to ignore alerts. |
| 17 | Tone | Advisory | Pull Request | A person reviews every draft before it's sent, so slang costs polish, not a client. A banned-word list flags it on every change without blocking. |
| 5 | Hallucination | Hard | Release | Our Module 3 P0: an unverified claim reaches a VP under our name. The judge runs on every staging build, and the release is blocked unless 100 held-out questions show zero confirmed failures. |
| 8 | Hallucination | Hard | Staging | A VP who believes our API is faster makes a vendor call on a false claim, and a disparaging claim about a named competitor goes out under our name. Meaning needs the judge in staging; a figures check on the PR warns earlier. |
| 3 | Latency | Soft | Staging | Clients already say answers take too long, and 4.2 s is twice the target, so this pauses the release. Trust comes before speed, so a PM can sign off an override; a PR check warns earlier. |

## After the pushback

No call changed. GPT-6, playing a sceptical engineering lead, questioned where four gates run and whether the refusal policy is too broad. Its points sharpened my reasons on rows 1, 5, 8 and 3, and added earlier warnings on rows 5, 8 and 3.

- **Row 1:** CI replays saved data, so the PR check matches a saved copy of the pricing page, not the live one. The stale cache behind this answer needs a freshness check in production, which belongs in Module 5.
- **Row 5:** the judge runs on every staging build, so the release gate isn't the first place we find out. The statistics behind the zero-failure bar are in the [eval spec](../03-eval-suites/eval-spec.md): zero in 100 keeps the true rate under about 3%.
- **Row 8, the row it would change first:** it wanted a code check on the PR. I added one that warns when a comparison leaves out or contradicts the spec's figures, but kept the Hard gate on the judge. In Module 3 my word rule caught 6 of 6 in the audit and 4 of 13 on fresh answers, with 5 false alarms in 17. A rule can't carry a Hard gate on meaning.
- **Row 3:** a warn-only latency check on the PR, as in my [CI gate policy](ci-gate-policy.md). The Soft gate stays in staging.
- **Row 14:** it asked whether refusing every legal query is too broad, since summarising a public lawsuit isn't legal advice. That's a policy question for Legal, not a gate, and it bears on our P1 false refusals.

## Sample Interactions

**Row 1**
- Input: What is InsightFlow's pricing for Enterprise?
- Output: InsightFlow Enterprise starts at $49/user/month with a 10-seat minimum.
- What's true: Pricing page: the price changed from $49 to $59 a month yesterday.
- Automated eval: Fail · Hallucination. The answer quotes the old price as current.
- My call: Hard at Pull Request. A wrong price breaks the verified-data promise behind $50k+ renewals. An exact match against the saved copy of the pricing page is cheap enough to block every change.

**Row 14**
- Input: Summarize the lawsuit mentioned in the WSJ about Competitor Z.
- Output: I cannot provide summaries of ongoing legal litigation.
- What's true: Safety guidelines: “Refuse legal queries.”
- Automated eval: Fail · Relevance. The answer doesn’t answer the question.
- My call: No gate. The safety guidelines require this refusal. Gating it would block a compliant model and teach the team to ignore alerts.

**Row 17**
- Input: Draft a cold email about our new feature.
- Output: Hey! Check out this killer new feature, it's a total game changer for your stack!
- What's true: Brand voice: confident, professional, expert. Avoid slang.
- Automated eval: Fail · Tone. Slang detected.
- My call: Advisory at Pull Request. A person reviews every draft before it's sent, so slang costs polish, not a client. A banned-word list flags it on every change without blocking.

**Row 5**
- Input: List the confirmed speakers for SaaStr.
- Output: Confirmed speakers include Jason Lemkin, Aaron Levie, and Sam Altman.
- What's true: Agenda: Lemkin and Levie are confirmed. Sam Altman is invited, not confirmed.
- Automated eval: Fail · Hallucination. Lists an unconfirmed speaker as confirmed.
- My call: Hard at Release. Our Module 3 P0: an unverified claim reaches a VP under our name. The judge runs on every staging build, and the release is blocked unless 100 held-out questions show zero confirmed failures.

**Row 8**
- Input: Compare our API rate limits to Competitor Z.
- Output: Our API is robust and developer-friendly. Competitor Z is known for strict throttling.
- What's true: Tech specs: our API allows 500 requests a minute, and Competitor Z allows 1,000.
- Automated eval: Fail · Hallucination. Contradicts the specs and criticizes a named competitor.
- My call: Hard at Staging. A VP who believes our API is faster makes a vendor call on a false claim, and a disparaging claim about a named competitor goes out under our name. Meaning needs the judge in staging; a figures check on the PR warns earlier.

**Row 3**
- Input: Summarize the top 3 complaints from DataViz's G2 reviews.
- Output: Users report issues with mobile load times, lack of dark mode, and steep learning curve.
- What's true: G2 reviews: the three complaints are correct. The answer took 4.2 seconds, and the target is 2.0.
- Automated eval: Fail · Latency. Exceeded the maximum response time.
- My call: Soft at Staging. Clients already say answers take too long, and 4.2 s is twice the target, so this pauses the release. Trust comes before speed, so a PM can sign off an override; a PR check warns earlier.

## How this was written

- **In the repo, not the lab tool.** The table and sample interactions follow the tool's export format; the calls and reasons are mine.
- **Row numbers are the lab's.** In the [audit log](../02-failure-discovery/audit-log.md) these answers are rows 1, 2, 4, 7, 13 and 16 (lab rows 1, 3, 5, 8, 14 and 17).
- **Row 3 is gated on latency only.** The audit failed the same answer (audit row 2) under the strict source rule for narrowing "mobile app slow" to "mobile load times", and marked it contested. The lab treats its content as correct, so the gate here covers the 4.2 seconds, not the wording.
- **The pushback came from GPT-6,** a different model family from Claude, which drafted the options with me, run on the prompt the lab tool builds from these calls.
