# Module 1 notes: Define Good, the Answer and the Path

Session 1, 12 Oct 2026. Sources: Module 1 slides, pre-read, [First Eval Lab walkthrough](https://product-school-platform.github.io/ps-content-library/certifications/aiec/2026.1/Modules/M1%20-%20First%20Eval%20Lab%20Walkthrough.html).

## The shift

- **The PM owns "good":** the same input to an LLM gives a range of valid outputs, so pass/fail QA stops working. The PM sets the acceptable range and manages the risk of "not good enough". Engineering makes the model run; only product can say whether it should feel precise or empathetic. Missed: in enterprise and regulated settings, legal, compliance and domain experts co-own the criteria. The PM owns the decision, not every rule.
- **An eval is an executable quality bar:** a systematic test of AI behaviour against a product-specific definition of good, across accuracy, safety, latency and whatever else matters. It sets ship criteria on evidence, shows where to iterate, and supplies the rules guardrails enforce. The eval scores; the guardrail intervenes. Missed: evals cost time and money, so depth should scale with risk.
- **Judge the answer and the path:** output evals check the final answer; trajectory evals check the agent's tool choice, order, arguments and recovery. Final-answer pass/fail is table stakes. Missed: trajectory evals need tool calls logged. If Ascend IQ's traces don't capture them, the path can't be judged.

## When you need an eval

| Binary success: standard QA | Ambiguous success: eval |
|---|---|
| Payments, ledgers, inventory | Recommendations, feeds, ad targeting |
| Exact-match search, file retrieval | Generative tools (code, copy, images) |
| Form-based SaaS (CRM, HR, expenses) | Semantic search and RAG Q&A |
| Rule-based workflows | AI agents (support, scheduling) |
| "Did it break?" | "What is good?" |

- **Rule of thumb:** you need an eval when good is a mix of dimensions that takes judgement and context. Missed: the line falls per component, not per product. A payments product with an AI fraud score needs evals for that score, and a "binary" extraction task still needs one at scale because error rates are probabilistic.

## Key frames

- **Evals are the new analytics:** Amplitude and Mixpanel show what users did, not whether the answer deserved trust. A follow-up question can mean delight or failure; that blind spot is the trust gap. Missed: behavioural data is still the outcome measure. Evals lead, analytics lag, and you need both.
- **Evals are the modern PRD** (Ankur Goyal, Braintrust): the PRD keeps problem, users and scope. The eval holds the quality spec as two lists, the dimensions of good and the "never" cases, and re-checks them on every change. Missed: an eval only tests what you thought of. It can encode the wrong definition very precisely.
- **Trust, not tooling** (Elena Verna): the blocker to shipping AI is trust, not tools.
- **The single-metric trap:** a summariser at 95% accuracy with 5s latency still loses users. A narrow lens leaves engineering with silent regressions, product with no line from metric to retention, and executives unable to weigh trade-offs.

## Trust flywheel

- **Offline precision cycle, pre-ship:** curated datasets run in CI and gate releases.
- **Online trust cycle, post-ship:** evals on production traces, cluster the failures, fix, repeat. Live traffic finds what the offline set missed. Covered in M4 and M5.

## Three jobs in production

| Job | Where it runs | Example |
|---|---|---|
| Background monitoring | Passive, early warning | Spotify AI DJ watching for drift |
| Guardrails | Critical path, blocks or falls back | Harvey blocking privileged client information |
| Improvement tools | Offline R&D loop | Grammarly typing errors to build training data |

## The eval toolkit

| Method | Quality | Speed | Cost and scale | Best for | Watch for |
|---|---|---|---|---|---|
| Code-based | Low fidelity | Instant | Cheap, unlimited | Format, schema, regex, exact match, CI checks | Blind to tone and reasoning |
| Human | Gold standard | Slow | Expensive, low scale | The golden set, highest-stakes calls | Doesn't scale |
| LLM-as-a-Judge | Tuned semantic | Fast | Moderate, high scale | Subjective scoring at volume | Validate against a human golden set; untuned judges rate everything highly; use a different model family from the generator |
| User and business | Noisy | Live | Free | Adoption, retention, thumbs up/down | Sentiment isn't ground truth; never use alone |

- **Triangulate:** direct methods measure quality, business metrics measure adoption. When they disagree, there's a product problem worth finding. Missed: judge calls at scale cost real money, which M5 picks up as the eval budget.

## Quick poll

- **Scenario A, creative co-pilot, creative and on-brand at scale:** hybrid. Editorial reviewers write the rubric and label a golden set; an LLM judge calibrated to that set scores volume; code catches banned terms, length and format. Creativity is subjective, so the human anchor isn't optional.
- **Scenario B, "friendlier" chatbot, 10k conversations, one week:** LLM-as-a-Judge, pairwise old vs new across all 10k, checked first against a few hundred human-labelled conversations; code checks for length, refusal and safety regressions. Also track resolution rate: friendlier isn't better if it solves fewer problems.

## The five trust metrics

- **Latency:** time to a complete first response, at P95 or P99.
- **Hallucination rate:** % of responses with provably false or fabricated information.
- **Fairness:** consistency of output quality across user groups or personas.
- **Robustness:** % of responses that stay coherent and accurate on messy, adversarial or out-of-scope input.
- **UX trust:** users' rating of predictability, clarity and consistency.
- **Accuracy, precision, recall and F1:** necessary, not sufficient. They measure the model in the lab, not trust in use.
- Missed: none of the five measures whether the answer was useful or complete. Treat them as a menu, and add product-specific metrics where they fall short.

## The four trade-offs

| Prioritise | Sacrifice |
|---|---|
| Lower hallucination (larger model, RAG) | Latency |
| Fairness, equitable performance across groups | Top-end score on the majority group |
| Robustness on edge cases and adversarial input | Early UX trust, through a slower rollout |
| Safety, stricter filters, fewer false negatives | UX trust, legitimate queries blocked |

- **Missed:** the frontier isn't fixed. Caching, streaming partial answers or a better retrieval index can improve both sides of a trade-off.

## Evals across the product lifecycle

- **Discovery:** a 20-prompt test for a baseline hallucination rate before pitching.
- **Development:** compare prompts to move factual accuracy from 70% to 85%.
- **Deployment:** a CD gate, e.g. block if hallucination rate exceeds 5% or latency exceeds 1s.
- **Post-launch:** monitor drift, e.g. fairness on Spanish-language inputs.

## Labs

- **First eval:** same model and email, two system prompts (A concise, B narrative), optional 1/0 conciseness score from a different model family. Output: [eval-harness-proof.md](eval-harness-proof.md).
- **Cold start:** an LLM generates about 20 starter rows to get past the blank page. The value is in the human curation after: correcting labels, dropping weak rows, adding the edge cases that matter. That curated set is the golden dataset; calibrating a judge against it (κ) comes in M3.
- **Strategy canvas:** user promise, top three trust metrics, two pre-committed trade-offs. Output: [strategy-canvas.md](strategy-canvas.md), Slide 1 of the final deck.

## What this means for Ascend IQ

- **It needs evals at both levels:** an agent retrieving from proprietary data has ambiguous success by definition, and the brief asks for answer quality and the soundness of the path.
- **Verified data is the product:** clients pay $50k+ a year for verified data, so a fabricated figure undermines what they are paying for, not just one answer.
- **The rollout trade-off is already live:** the CPO wants the top 50 accounts next month and Sales is already promoting it. That is robustness against early UX trust, in practice.
