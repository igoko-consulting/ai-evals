# Trajectory Scorecard · Stripe vs Adyen pricing

**Task:** "Compare the pricing models of Stripe and Adyen."

**Matching mode:** unordered, as set by the lab tool · **Score:** 1 of 6 dimensions passed · **Verdict:** HOLD

## Reference path

1. get_pricing(company="Stripe")
2. get_pricing(company="Adyen")
3. compare(a="Stripe pricing", b="Adyen pricing")  [added by me]
4. write_answer(text, sources)

`compare` is the step the draft path was missing. Without it, the comparison is whatever the model writes freehand.

## The recorded run

| Step | Call | Result |
|---|---|---|
| 1 | get_pricing(company="Stripe") | Verified Stripe pricing: 2.9% + 30¢ per online card charge in the US, custom at volume |
| 2 | get_pricing(company="Ayden") | Error: no company named "Ayden" in the library |
| 3 | web_search(query="Adyen pricing") | An unverified blog post on Adyen's fees. Web results are barred from client answers |
| 4 | write_answer(sources=["Stripe pricing page", "paymentsblog.example/adyen-fees"]) | Sent to the client |

The client received a fluent comparison that mixes a verified source with an unverified blog, both cited as sources.

## The six dimensions

Judge's scores are given as Claude run 1 · Claude run 2 · GPT-6.

| Dimension | Judge's score | The step that decided it | My call | Why |
|---|---|---|---|---|
| Tool selection | Fail · Fail · Fail | Step 3: web_search, barred from client answers | Fail | It called a barred tool and never called compare. |
| Argument correctness | Fail · Fail · Fail | Step 2: "Ayden" for "Adyen" | Fail | The typo broke the Adyen lookup; everything after follows from it. |
| Redundant or looping | Pass · Pass · Pass | No step repeats | Pass | No repeated or looping calls. |
| Recovery | Partial · Fail · Fail | Step 3: fell back to the open web after the error | Fail | A sound recovery retries with the correct name or tells the client the verified data wasn't found. This one switched to a barred source and hid the error, which is what turned a typo into unverified data. |
| Plan coherence | Partial · Partial · Fail | Steps 3 and 4: web_search in, compare dropped | Partial | The two lookups were sound; switching to the web and dropping compare weren't. |
| Task completion | Partial · Partial · Partial | Step 4: the Adyen half rests on an unverified blog | Fail | The client pays for verified data, and half this comparison rests on a blog cited as if it were a source. A plausible answer doesn't excuse a failed path on a P0. |

**Failed worst:** Recovery. The typo was recoverable; the harm came from the recovery, which delivered a confident comparison mixing a verified source with an unverified blog, both cited.

**The check I'd add:** a trace check in code. Every source cited in write_answer must come from a verified tool result in the same run, and web_search must never appear in a run that answers a client. It's a rigid rule, so code can enforce it as a hard gate, and it's subset matching on sanctioned tools, which catches what the tool's unordered matching misses.

## Verdict

HOLD. Four of six dimensions fail, including the one that breaks the verified-data promise. The answer reads well, which is exactly why an output-only eval would have shipped it. In the Module 2 taxonomy's terms this run is a recovery failure, and calling a tool outside the allowed set is scope escalation.

## How this was run

- **Judges:** the lab tool's judge prompt, with my completed reference path, run on Claude Haiku 5.5 twice in fresh contexts and on GPT-6 once in a fresh chat. Replies are saved verbatim in [results/trajectory-judges.md](results/trajectory-judges.md).
- **Agreement:** all three agreed on four of six dimensions. They split on Recovery (Partial, Fail, Fail) and Plan coherence (Partial, Partial, Fail). The tool's prompt scores all six dimensions in one call; scoring one dimension per call is the more stable design ([playbook rule 12](../EVAL-PLAYBOOK.md)).
- **My calls:** I agreed with the majority on five dimensions and overrode Task completion from Partial to Fail, because the task is a verified comparison and half of it isn't verified.
- **Limit:** one recorded run of one task. It shows how a trajectory eval reads a path, not how often Ascend IQ's paths fail.
