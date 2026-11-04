# Module 6 notes: Make Evals the Way the Org Ships

Drafted 4 Nov 2026. Sources: Module 6 slides, the [revised lab guide](https://product-school-platform.github.io/ps-content-library/certifications/aiec/2026.1/Modules/Module%206%20-%20Lab%20Guide.html) and the [Final Project Deliverables Builder](https://product-school-platform.github.io/ps-content-library/certifications/aiec/2026.1/Modules/Final%20Project%20Deliverables%20Builder.html).

## Who owns evals

- **The maturity curve has four stages:** ad hoc, where each team spot-checks on its own; standardised, with shared metrics and specs; shared infrastructure, where a central platform runs every team's gates; and org-wide trust, where trust is a C-suite KPI reviewed next to revenue. Each stage needs one PM move from the course: a taxonomy, an eval spec, gates in the pipeline, an eval playbook. Missed: no stage maps to Module 5, yet the coverage matrix is how you'd tell which stage each product has reached. One company can have gates on one product and nothing on the next.
- **Governance follows stage and regulation:** decentralised (stages 1 and 2) buys speed and gives up consistency between products. Hybrid (stage 3) has a central team owning tools and standards while product teams own their risks. Centralised (stage 4, high regulation) buys compliance and gives up release speed.
- **Product teams always own the decision:** in every model, they own the failure modes that matter to their users and the ship-or-hold call. My eval spec already splits it this way: the Group PM owns the threshold and the call, and the engineering lead owns the gate in CI.

## Making evals part of how the org decides

- **An eval playbook answers five questions:** what we test, who builds and who decides, how hard we enforce, how often we run, and who makes the final call when a soft gate fails under launch pressure. Missed: my [EVAL-PLAYBOOK.md](../EVAL-PLAYBOOK.md) is a different thing, lessons for my next project rather than rules for a team. Ascend IQ's team playbook already exists in pieces: the taxonomy, gate map, CI policy and eval budget answer the first four questions, and my launch strategy answers the fifth, with the PM signing off a latency override.
- **Report quality and what the evals saved:** a trust dashboard gives each metric a target, an owner and its business meaning. Next to it go incidents prevented, time to detection, clean releases and catch rate. Leave out evals run, token spend and tool seats, which show activity, not value. Missed: the slide's example target, a hallucination rate under 5%, is looser than my bar of zero in 100, which keeps the true rate under about 3%. A dashboard target has to match the gate, or leadership reviews a number nobody ships against.
- **Bring the numbers to meetings leadership already holds:** the trust dashboard as a standing item at the QBR, a gate that caught a serious risk at every all-hands, and a trust OKR such as halving the hallucination rate. Missed: a catch is easy to celebrate. The all-hands story that matters more is a hold, because a delayed launch reads as a failure unless someone explains what it prevented.

## Communicating the call

- **Answer first, then arguments, then evidence:** executives read the first line and decide whether to keep going, so the recommendation goes there. Two or three arguments follow without overlapping, each with the number that proves it. Missed: the slide's own example breaks the rule it teaches. Its third argument, "Competitors are winning on dependability", has no number, which is the vague claim the lab's review prompt asks the reviewer to find.
- **Three outcomes, not two:** the slide allows ship, hold or ship with conditions, while the lab tool offers only ship or hold. My HOLD carries its conditions in the ask: approval by 6 November, and the release gate result by 4 December. A hold with no exit date reads as a no.

## Labs

- **Ship-or-hold memo:** HOLD. 6 of 20 audited answers overstate their sources against a bar of zero, a staged rollout would expose at least $250k a year of renewals, and the hold ends when the golden set exists to run the judge on. GPT-6, as a sceptical CPO, found that two arguments leaned on the same 30% rate and read $250k as a predicted loss; four changes followed. Output: [ship-hold-memo.md](ship-hold-memo.md).
- **Final project:** built with the builder's own code from the repo. I replaced nine of its cards: seven shortened to a sentence or three, and two the builder misreads, my canvas's metrics and my taxonomy's impact statement, filled by hand. GPT-6's CPO review caught my pitch claiming the judge "already meets the spec": it meets the catch and false-alarm bar on 30 fresh answers, but its agreement with human labels isn't measured. I declined three requests that needed numbers the repo doesn't have: proof that a fabricated figure costs renewals, the link between the 10 failures and the 6, and ROI for the eval budget. Output: [final-presentation.html](../final-presentation.html).

## Discussion questions

- **Where Ascend Analytics sits on the maturity curve:** between stages 1 and 2. AI Report Summaries runs a release judge but nothing on live summaries, and three of its five trust metrics have no check ([coverage matrix](../05-scale/coverage-matrix.md)). Ascend IQ now has an eval spec, but no golden set to run it on.
- **Whether its governance fits:** decentralised fits the stage but not the risk. Clients hold the whole brand to its weakest product, so I'd move to hybrid: a central team owns the judge, the golden set format and the coverage matrix, and product teams own their failure modes and ship calls.
- **My call in one line, and the number that decided it:** HOLD, because 6 of 20 audited answers overstate their sources, against a bar of zero.

## What this means for Ascend IQ

- **The hold has two builds behind it:** the golden set, with at least 100 held-out questions and 30 regression cases, and a fix for the overstatements. Neither exists yet.
- **The judge needs one more test before it can block:** the eval spec requires κ 0.6 or above against human labels, and that's unmeasured for the inflated-facts judge. The memo's evidence table is where this surfaced.
- **What stays open after the course:** a gate on false refusals (P1, audit rows 8 and 18), the runtime check on stale prices, and the source check from Module 4. None blocks the release gate, but each is a known failure with no check on it.
