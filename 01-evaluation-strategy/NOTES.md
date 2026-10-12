# Module 1 notes: Define Good, the Answer and the Path

Session 1 · 12 Oct 2026 · Sources: Module 1 slides, pre-read, [First Eval Lab walkthrough](https://product-school-platform.github.io/ps-content-library/certifications/aiec/2026.1/Modules/M1%20-%20First%20Eval%20Lab%20Walkthrough.html)

## The shift

- **PM owns "good":** a probabilistic system returns a range of valid outputs for the same input, so pass/fail QA no longer works. The PM defines the acceptable range and manages the risk of "not good enough". Engineering makes the model run; only product can say whether it should feel precise or empathetic.
- **What an eval is:** a systematic test of AI behaviour against a product-specific definition of good, across the dimensions that matter (accuracy, safety, latency and so on). It does three jobs: sets ship criteria on evidence, points iteration at where quality fails, and supplies the criteria that guardrails enforce. The eval scores; the guardrail intervenes.
- **Output and trajectory:** judge the final answer and the path an agent took (tool choice, order, arguments, recovery). Final-answer pass/fail is table stakes. Trajectory is taught in M3 and matters for Ascend IQ because it is an agent.

## When you need an eval

| Success is binary: standard QA | Success is ambiguous: eval |
|---|---|
| Payments, ledgers, inventory | Recommendations, feeds, ad targeting |
| Exact-match search, file retrieval | Generative tools (code, copy, images) |
| Form-based SaaS (CRM entry, HR, expenses) | Semantic search and RAG Q&A |
| Logic workflows (IFTTT rules) | AI agents (support, scheduling) |
| "Did it break?" | "What is good?" |

- **Rule of thumb:** you need an eval whenever good is a combination of dimensions that takes judgement and context.

## Framing to remember

- **Evals are the new analytics:** Amplitude and Mixpanel show what users did, not whether the answer deserved trust. A follow-up question can mean delight or failure. That blind spot is the trust gap.
- **Evals are the modern PRD** (Ankur Goyal, Braintrust): the PRD still owns problem, users and scope. The eval holds the quality spec in executable form, as two lists: the dimensions of good, and the "never" cases.
- **Trust, not tooling** (Elena Verna): the blocker to shipping AI is trust.
- **Single-metric trap:** a summariser at 95% accuracy with 5s latency still loses users. A narrow lens costs engineering (silent regressions), product (no line from metric to retention) and executives (trade-offs can't be weighed).

## Trust flywheel

- **Offline precision cycle (pre-ship):** curated datasets run in CI and gate releases.
- **Online trust cycle (post-ship):** evals on production traces, cluster the failures, fix, repeat. Real traffic surfaces failures the offline set missed. Covered in M4 and M5.

## Three jobs evals do in production

| Job | Where it runs | Example |
|---|---|---|
| Background monitoring | Passive, early warning | Spotify AI DJ watching for drift |
| Guardrails | Critical path, active intervention | Harvey blocking privileged client information |
| Improvement tools | Offline R&D loop | Grammarly typing errors to build training data |

## The eval toolkit

| Method | Quality | Speed | Cost and scale | Use for | Watch for |
|---|---|---|---|---|---|
| Code-based | Low fidelity | Instant | Cheap, unlimited | Format, schema, regex, exact match, CI guardrails | Blind to tone and reasoning |
| Human | Gold standard | Slow | Expensive, low scale | The golden set, highest-stakes calls | Does not scale |
| LLM-as-a-Judge | Tuned semantic | Fast | Moderate, high scale | Subjective scoring at volume | Must be validated against a human golden set; untuned judges rate everything highly; use a different model family from the generator to avoid self-preference bias |
| User and business | Noisy | Live | Free, ambient | Adoption, retention, thumbs up/down | Sentiment is not ground truth; triangulate, never use alone |

- **Triangulate:** direct methods tell you about quality, business metrics about adoption. When they disagree, that is a product problem worth chasing.

## Quick poll

- **Scenario A, creative co-pilot (creative and on-brand at scale):** hybrid. Editorial reviewers write the rubric and label a golden set; an LLM judge calibrated to that set scores volume; code checks catch banned terms, length and format. Creativity is subjective, so the human anchor is not optional.
- **Scenario B, "friendlier" chatbot, 10k conversations, one week:** LLM-as-a-Judge pairwise (old vs new) across all 10k, validated first against a human-labelled sample of a few hundred; code checks for length, refusal and safety regressions. Also check resolution rate: friendlier is not better if it solves fewer problems.

## Trust metrics: the five

- **Latency:** time to a complete first response, at P95 or P99.
- **Hallucination rate:** % of responses with provably false or fabricated information.
- **Fairness:** consistency of output quality across user groups, demographics or personas.
- **Robustness:** % of responses that stay coherent and accurate on messy, adversarial or out-of-scope input.
- **UX trust:** users' rating of predictability, clarity and consistency.
- Accuracy, precision, recall and F1 are necessary but not sufficient: they measure the model in the lab, not trust and safety in use.

## The four trade-offs

| Prioritise | Sacrifice |
|---|---|
| Lower hallucination (larger model, RAG) | Latency |
| Fairness (equitable performance across groups) | Top-end score on the majority group |
| Robustness (edge cases, adversarial input) | Early UX trust (slower rollout) |
| Safety (stricter filters, fewer false negatives) | UX trust (legitimate queries blocked, more false positives) |

## Evals across the product lifecycle

- **Discovery:** 20-prompt test for a baseline hallucination rate before pitching.
- **Development:** compare prompts to move factual accuracy from 70% to 85%.
- **Deployment:** CD gate, e.g. block if hallucination rate > 5% or latency > 1s.
- **Post-launch:** monitor drift, e.g. fairness on Spanish-language inputs.

## Labs

- **First eval:** same model, same email, two system prompts (A concise, B narrative). Optional 1/0 conciseness score from a different model family. Output: [eval-harness-proof.md](eval-harness-proof.md).
- **Cold start:** an LLM generates ~20 starter rows to beat the blank page. The asset is the human curation that follows: correcting labels, dropping weak rows, adding the edge cases you care about. That curated set is the golden dataset; calibrating the judge against it (κ) comes in M3.
- **Strategy canvas:** user promise, top three trust metrics, two pre-committed trade-offs. Output: [strategy-canvas.md](strategy-canvas.md), Slide 1 of the final deck.

## So what for Ascend IQ

- **It needs evals at both levels:** an agent doing retrieval over proprietary data is ambiguous-success by definition, and the brief asks for answer quality and the soundness of the path.
- **Verified data is the product:** clients pay $50k+ for verified data, so a fabricated figure attacks the core value proposition, not just one answer.
- **The rollout trade-off is already live:** the CPO wants the top 50 accounts next month and Sales is promoting it, which is Robustness against Early UX trust in practice.
