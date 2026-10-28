# AI Evals: Final Project

> My final project for Product School's **AI Evals** certification. One evaluation system for a real LLM feature, from strategy, through failure discovery and an automated eval suite, to the gates and governance that let it ship safely.

**How to read this repo:** start with the findings below, then the deliverables. Each module folder holds its deliverables, a `NOTES.md` with the module's ideas and my takeaways, and its evidence: inputs under `fixtures/`, judge runs under `results/`. [EVAL-PLAYBOOK.md](EVAL-PLAYBOOK.md) collects the lessons to reuse on other projects. The course runbooks (`LAB.md` in each folder, and `PROMPTS.md`) are kept as shipped.

---

## Deliverables at a glance

| Module | Artifact | Status | File |
|---|---|---|---|
| M1 | **Evaluation Strategy Canvas** | ✅ | `01-evaluation-strategy/strategy-canvas.md` |
| M1 | **Eval harness proof** (links + screenshots) | ✅ | `01-evaluation-strategy/eval-harness-proof.md` |
| M2 | **Failure audit log** | ✅ | `02-failure-discovery/audit-log.md` |
| M2 | **Failure Taxonomy** | ✅ | `02-failure-discovery/failure-taxonomy.md` |
| M3 | **Runnable eval suite** (results) | ✅ | `03-eval-suites/eval-suite.md` |
| M3 | **Trajectory eval** (scorecard) | ✅ | `03-eval-suites/trajectory.md` |
| M3 | **Judge calibration** (κ) | ✅ | `03-eval-suites/judge-calibration.md` |
| M3 | **Eval Spec** (5-part spec + audience messages) | ✅ | `03-eval-suites/eval-spec.md` |
| M4 | **Eval gate map** (severity × placement) | ✅ | `04-eval-gates/gate-map.md` |
| M4 | **CI gate policy** (prompt-rewrite PR) | ✅ | `04-eval-gates/ci-gate-policy.md` |
| M4 | **Launch strategy** (release criteria + CI policy + mitigation) | ✅ | `04-eval-gates/launch-strategy.md` |
| M5 | **Coverage matrix** | ☐ | `05-scale/coverage-matrix.md` |
| M5 | **Eval budget** | ☐ | `05-scale/budget.md` |
| M6 | **Ship / Hold memo** | ☐ | `06-culture/ship-hold-memo.md` |
| M6 | **Final pitch deck** (generated HTML) | ☐ | `final-pitch.html` |

## The feature in one sentence

Ascend IQ, an AI agent that answers plain-language market-intelligence questions for VP-level strategists at Ascend Analytics' top 50 enterprise accounts; a wrong answer puts $50k+ renewals and the company's most valuable relationships at risk.

## Findings so far

| Finding | Evidence |
|---|---|
| **15 of 20 audited answers fail** a strict source rule; 12 of them are hallucinations. | [Audit log](02-failure-discovery/audit-log.md) |
| **8 answers fail under every judge and rubric tried**, Claude and GPT-6, strict and lenient. Even the most lenient judge fails 9 of 20, so the failure rate doesn't depend on how strict the rule is. | [Judge runs](02-failure-discovery/fixtures/judge-runs.csv) |
| **Two P0 risks:** inflated facts (6 answers) and wrong numbers on the core use case (2). **One P1:** false refusals (2). | [Failure taxonomy](02-failure-discovery/failure-taxonomy.md) |
| **Two failures point to retrieval, not the model:** a stale cached price (row 1) and a missed page footer (row 8). | [Audit log](02-failure-discovery/audit-log.md) |
| **The top risk can be caught before launch, by a judge, not a word list.** On 30 fresh answers, the judge caught 13 of 13 inflated facts with 1 false alarm in 17, and gave the same 20 calls on two runs of the audit. A word-pair rule that caught 6 of 6 in-sample caught 4 of 13 fresh. | [Eval suite](03-eval-suites/eval-suite.md) |
| **An uncalibrated judge is noise.** The course's judge agreed with my labels at κ 0.27, passing answers with invented detail; a rubric that names unsupported claims reached 12 of 12. | [Judge calibration](03-eval-suites/judge-calibration.md) |
| **A fluent answer can hide a failed path.** Ascend IQ's Stripe and Adyen comparison read well, but its path failed 4 of 6 dimensions, ending with a barred web source cited to the client. | [Trajectory](03-eval-suites/trajectory.md) |
| **Today's build fails the ship bar.** The eval spec allows zero confirmed inflated answers; the audit found 6 of 20 (30%). | [Eval spec](03-eval-suites/eval-spec.md) |
| **No rollout plan ships around a failed Hard gate.** Three Hard gates guard the release, each behind an exact or calibrated check. The staged rollout covers only the Soft latency gate, and the inflated-facts gate already fails. | [Launch strategy](04-eval-gates/launch-strategy.md) |

The lessons behind these, written to reuse on other projects, are in [EVAL-PLAYBOOK.md](EVAL-PLAYBOOK.md).

## Repo structure

```
ai-evals/
├── README.md                         ← this dashboard
├── EVAL-PLAYBOOK.md                  ← lessons to reuse on other projects
├── final-pitch.html                  ← Module 6, the ship/hold pitch
├── 01-evaluation-strategy/           ← Module 1
│   ├── strategy-canvas.md            user promise, trust metrics, trade-offs
│   ├── eval-harness-proof.md         first LLM-as-a-Judge eval
│   ├── NOTES.md                      module notes and takeaways
│   └── fixtures/                     starter dataset
├── 02-failure-discovery/             ← Module 2
│   ├── audit-log.md                  scored audit of 20 answers
│   ├── failure-taxonomy.md           prioritised failure modes
│   ├── NOTES.md
│   └── fixtures/                     the 20 answers, every judge run
├── 03-eval-suites/                   ← Module 3
│   ├── eval-suite.md                 three checks on the P0, in-sample and fresh
│   ├── eval-spec.md                  5-part eval spec + audience messages
│   ├── trajectory.md                 trajectory scorecard
│   ├── judge-calibration.md          judge calibration (κ)
│   ├── ascend_suite.py               the runnable checks
│   ├── NOTES.md
│   ├── fixtures/                     fresh test set, labelling sheets
│   ├── results/                      every judge run, verbatim
│   └── cortex-eval/                  course notebook, not used: the suite targets Ascend IQ instead
├── 04-eval-gates/                    ← Module 4
│   ├── gate-map.md                   severity × pipeline-placement grid
│   ├── ci-gate-policy.md             CI gate policy and merge call
│   ├── launch-strategy.md            release criteria + CI policy + mitigation
│   └── NOTES.md
├── 05-scale/                         ← Module 5
│   ├── coverage-matrix.md            coverage across product lines
│   └── budget.md                     eval budget + trade-offs
└── 06-culture/                       ← Module 6
    └── ship-hold-memo.md             ship/hold recommendation
```

Each module folder also holds the course's `LAB.md` runbook. `03-eval-suites/trajectory-traces.csv` is course practice data, not used.
