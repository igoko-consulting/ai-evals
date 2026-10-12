# AI Evaluation Strategy Canvas

> Repo file `ai-evals/01-evaluation-strategy/strategy-canvas.md` (the repo is your submission).
> Becomes the **Strategy Canvas** slide of the final pitch deck you assemble in Module 6.
>
> Fill this with the **AI Evaluation Strategy Canvas** tool, then **Copy markdown** and paste it over this file. The headings below mirror the tool's output exactly.

## 1. Product Strategy, The Context

- **Target user:** VP-level strategists and product leaders at Ascend Analytics' top 50 enterprise accounts (Fortune 500, $50k+ a year each), who use Ascend's verified market data to set roadmaps.
- **Key use case:** asking plain-language market questions, such as "Compare the pricing models of Stripe and Adyen" or "Summarise the negative G2 reviews for Salesforce", and getting an answer in seconds instead of digging through a dense platform by hand.
- **Value proposition:** Ascend IQ turns Ascend's verified data into fast answers, removing the time-to-insight friction that is driving disengagement and putting Q4 retention at risk.

## 2. Measurements, The Execution

- **User promise.** For VP-level strategists at our top 50 accounts, Ascend IQ promises answers in seconds where every figure traces back to Ascend's verified data, so that they make roadmap calls on Ascend and renew their $50k+ contracts.
- **Top 3 trust metrics:**
  - **Hallucination rate (groundedness)**, % of factual claims (figures, prices, review themes) not traceable to a retrieved Ascend source.
  - **Robustness (calibrated refusal)**, % of out-of-coverage, ambiguous or leading questions where Ascend IQ flags the gap or declines rather than answers.
  - **Latency**, P95 time to a complete answer.
- **Why these three:** they cover what clients pay for (verified data), the most likely failure (answering beyond the data) and the reason the product exists (slow answers). Each has an objective signal. UX trust and completeness are more subjective, and trajectory correctness gets its own eval in Module 3.

## 3. Strategic Trade-Offs, The Cost

### Trade-off 1 · Hallucination rate ↔ Latency

We prioritise grounded answers over response time because one fabricated competitor price in a VP's board pack costs more than a few seconds' wait, and a grounded answer is still far faster than digging through the platform by hand.

### Trade-off 2 · Robustness ↔ Early UX trust

We prioritise resilience on edge cases over shipping to all 50 accounts next month because a bad answer to the wrong client can permanently damage a $50k+ relationship. A staged rollout protects the quarter without betting the book.

---
_Generated from the AI Evaluation Strategy Canvas, M1 lab tool, AI Evals Certification._
