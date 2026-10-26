# Module 2 notes: Build a Failure Taxonomy by Business Impact

Session 2, 14 Oct 2026. Drafted from the slides, pre-read and [Failure Audit walkthrough](https://product-school-platform.github.io/ps-content-library/certifications/aiec/2026.1/Modules/M2%20-%20Failure%20Audit%20Walkthrough.html) before class; discussion answers added after.

## The shift

- **Failure discovery comes first:** in traditional software, bug hunting happens late and belongs to QA. In AI products, mapping failures happens at the start of discovery and belongs to the PM. Missed: before launch, discovery runs on beta or synthetic traffic, which under-represents the strange inputs real users bring.
- **Cartographer, then doctor:** the cartographer maps and names every failure mode; the doctor diagnoses the cause behind each one (prompt, retrieval data or a real model limit). A rising hallucination rate is a symptom, not a diagnosis.
- **The PM translates:** engineering sees technical issues, executives see business risk, the PM sees the user and connects the three.

## Two traps

| Trap | Looks like | Why it fails | Example |
|---|---|---|---|
| Vanity metric | "We're at 95% accuracy" | The average hides the catastrophic 5% | Air Canada's chatbot invented a bereavement-fare policy; the tribunal held the airline liable (Moffatt v. Air Canada, 2024 BCCRT 149) |
| Model swap | "Let's try a newer model" | Skips the diagnosis; the cause is usually data, prompt, retrieval or tool routing | McDonald's pulled its drive-thru AI; the failure was in speech-to-text, not the LLM |

- Missed: sometimes the model really is the limit. Diagnose first, and swap only if the evidence points there.

## Four-step error analysis

| Step | What you do | Output |
|---|---|---|
| Capture | Gather a representative sample of outputs, good and bad | Raw log dataset |
| Label | Tag each row against the quality dimensions; name new failure modes as they appear | Searchable data |
| Cluster | Group labelled failures into patterns | Statistical signal |
| Map | Document the patterns in a failure taxonomy | The executive risk artefact |

- **Top-down and bottom-up evals:** top-down rules come from the Module 1 definition of good, and an LLM can write them from a spec. Bottom-up failures come from traces and human edits, and models miss them until a human names them. Confirm a bottom-up failure on 10 to 20 examples before it becomes an eval row.
- Missed: 20 rows is enough to name failure modes, not to estimate their rates. "4 of 20" is a signal, not a 20% hallucination rate.

## Agent failures live in the trajectory

| Mode | What it looks like | Where it shows in the trace |
|---|---|---|
| Tool misuse | Wrong tool, or the right tool with wrong arguments | Tool name or arguments don't match the user's intent |
| Reasoning loop | Repeats a step and never finishes | Near-identical steps, rising step count, no new information |
| Scope escalation | Reaches beyond its permissions | A tool call outside the allowed set |
| Recovery failure | Gives up, fabricates or retries blindly after a failed call | The step after a failed tool result |

- **Capture rule:** read the trace in order and ask: right tool and arguments, looped, in scope, recovered? Each "no" is a new taxonomy row. When an agent loops or misroutes, fix the path, not the model.
- Missed: the Module 2 dataset has question, answer and source only, no traces, so trajectory failures can only be inferred here. Module 3 scores the path directly.

## Prioritisation

- **Severity over frequency:** a minor annoyance that happens 1,000 times a day can wait; a reputation-destroying failure that has happened once can't. Prioritise by business risk, not frequency or ease of fix.

| | Low frequency | High frequency |
|---|---|---|
| **High severity** | P1 Hidden risk: guardrails now, fix before the next incident | P0 Crisis zone: hotfix, block the launch |
| **Low severity** | P3 Low priority: watchlist | P2 Annoyance: acceptable debt, backlog |

- **Grammarly example:** P0 hallucinated citations in essays; P1 tone rewrites that create HR or legal risk; P2 robotic rewrites; P3 missed typos in niche multilingual text.
- **Cost curve:** found in discovery, 1× (fix the prompt spec); in development, 10× (sprint delay, rerun the suite); at deployment, 50× (a gate blocks release an hour before launch); post-launch, 100× (public reports, hotfix, apology, fines).
- **Two definitions in the course:** the pre-read and slides set P0 to P3 by severity and frequency together. The repo template sets them by severity alone, so a rare contract-breaking failure is P0 there and P1 here.
- Missed: P-levels should be agreed with stakeholders, not assigned alone, and a threshold of 3 in 20 is arbitrary at this sample size.

## The PM's role

- **For users, trust architect:** catch the technically correct but functionally disastrous answer, such as a chatbot agreeing to sell a car for $100.
- **For legal, governance lead:** engineering builds the filter; the PM sets where "helpful" ends and liability begins.
- **For executives, decision maker:** turn "95% accuracy" into "ready to ship", and own the go/no-go.
- **Checklist:** own the definition of good; prioritise subtle risks like tone and latency; block P0 and P1 failures with guardrails; write down which P2 and P3 failures you accept; frame findings as adoption, compliance and retention; keep the checks running across the lifecycle.

## Labs

- **Failure audit:** an LLM judge scores 20 Ascend IQ beta logs with the course's QA Analyst prompt; human overrides for correct refusals; each confirmed failure tagged. Data: [fixtures/ascend-iq-sample-data.csv](fixtures/ascend-iq-sample-data.csv). Output: [audit-log.md](audit-log.md).
- **Failure taxonomy:** top 3 with frequency, severity and impact; a business impact statement for #1; the ranking defended. Output: [failure-taxonomy.md](failure-taxonomy.md).

## Discussion questions

My answers, from the calls I made in the audit and taxonomy.

- **Refusals:** the judge never failed the legal refusal (row 13); it passed it on its own, so the override the lab expected didn't come up. It did fail row 8, which refused a question the source answered, and I agreed: that's a false refusal, not a guardrail. Row 18 was the close call: right to flag the gap, wrong to blame a lack of access. I later reversed my own strict fail on row 13, because "ongoing" is the course's mandated refusal wording.
- **Tone and vague answers:** a VP pastes our answer into a board pack or an email to their own CEO. A slangy draft or a vague "robust and developer-friendly" comparison embarrasses them in front of their leadership, so the damage lands on their credibility and they stop trusting the tool. I still rated tone P3 for Ascend IQ, because drafting isn't the core use case and a person reviews drafts before sending. The vague comparison in row 7 is P0, because it gets the facts backwards.
- **Hardest severity call:** whether small added details (rows 2, 9, 19) count as failures at all. I labelled them failures under the strict source rule and made them P2, so the audit stays consistent and severity carries the judgement. I anchored on the Module 1 promise that every figure traces back to verified data.

## What this means for Ascend IQ

- **Latency can't be audited here:** the logs have no timings, so one of my three trust metrics is untested by this module.
- **The source column hints at causes:** a cached pricing page points to data freshness, not the model, which is the doctor lens in practice.
- **The count depends on the rubric, the core doesn't:** judges and rubrics gave 9 to 15 failures, but 8 rows failed under every one. Those 8 carry the ship/hold argument.
- **Check the policy before blaming the agent:** row 13 looked like a hallucination until the mandated refusal wording turned up in Module 3.
