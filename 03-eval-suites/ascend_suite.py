"""Output eval suite for Ascend IQ's P0 failure, inflated facts.

Scores follow the course convention: 1 = pass, 0 = fail. The rule check and safety rule
run here as code. The judge needs a model, so its verdicts are read from
results/judge-run*.json (one JSON object per row: row, judge, reason).

Usage: python3 ascend_suite.py           the 20 audited answers
       python3 ascend_suite.py reworded  the fresh test set GPT-6 wrote, to test the checks out of sample
"""
import csv
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
ROWS = HERE.parent / "02-failure-discovery" / "fixtures" / "ascend-iq-sample-data.csv"
AUDIT = HERE.parent / "02-failure-discovery" / "fixtures" / "judge-runs.csv"
RESULTS = HERE / "results"

P0_ROW = 11
REAL_CASES = (3, 4, 5, 11, 12, 14)  # Risk 1 rows in failure-taxonomy.md

STRONG = ("yes", "confirmed", "seamless", "native", "primary", "hq", "positive")
QUALIFIERS = ("tentative", "invited", "via", "partnership", "secondary", "hub", "neutral", "no")
CAPABILITY_QUESTION = re.compile(r"^(does|do|is|are)\b.*\b(support|integrate|offer|certified|compliant)", re.I)
NO_EVIDENCE = re.compile(r"cannot find|can't find|do not have access|no information", re.I)


def words(text, vocab):
    return [w for w in vocab if re.search(rf"\b{w}\b", text, re.I)]


def rule_check(question, answer, reference):
    strong, weak = words(f"{question} {answer}", STRONG), words(reference, QUALIFIERS)
    if strong and weak:
        return 0, f"{', '.join(strong)} against {', '.join(weak)} in the reference"
    return 1, ""


def reference_limits(reference):
    limits = re.findall(r"\bvia\s+\W*(\w+)", reference, re.I)
    limits += re.findall(r"\bno\s+\W*(\w+)", reference, re.I)
    limits += [m.split()[0] for m in re.findall(r"(\w+\s+\w+)\s+only\b", reference, re.I)]
    return limits


def safety_rule(question, answer, reference):
    if not CAPABILITY_QUESTION.search(question):
        return 1, ""
    if NO_EVIDENCE.search(answer):
        return 0, "claims no evidence when the reference answers it"
    dropped = [w for w in reference_limits(reference) if not re.search(rf"\b{w}\b", answer, re.I)]
    if dropped:
        return 0, f"drops the reference's limit: {', '.join(dropped)}"
    return 1, ""


def load_judge(path):
    return {v["row"]: v for v in json.loads(path.read_text())}


def summarise(name, scores, audit_pass):
    caught = [n for n in REAL_CASES if scores[n] == 0]
    missed = [n for n in REAL_CASES if scores[n] == 1]
    false_alarms = [n for n, s in scores.items() if s == 0 and n in audit_pass]
    p0 = "Caught it" if scores[P0_ROW] == 0 else "Missed it"
    fmt = lambda rows: ", ".join(map(str, rows)) or "none"
    return f"| {name} | {len(caught)} of {len(REAL_CASES)} | {fmt(missed)} | {fmt(false_alarms)} | {p0} |"


def main():
    rows = list(csv.DictReader(ROWS.open()))
    audit_pass = {int(r["row"]) for r in csv.DictReader(AUDIT.open()) if r["final_label"] == "1"}
    runs = [load_judge(p) for p in sorted(RESULTS.glob("judge-run*.json"))]
    judge = runs[0]

    rule, safety, out = {}, {}, []
    for n, r in enumerate(rows, 1):
        rule[n], rule_why = rule_check(r["query"], r["prediction"], r["reference"])
        safety[n], safety_why = safety_rule(r["query"], r["prediction"], r["reference"])
        out.append({"row": n, "rule": rule[n], "safety": safety[n], "judge": judge[n]["judge"],
                    "rule_reason": rule_why, "safety_reason": safety_why, "judge_reason": judge[n]["reason"]})

    with (RESULTS / "suite-run.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)

    print("| Check | Caught | Missed (rows) | False alarms (rows) | My P0 row |")
    print("|---|---|---|---|---|")
    print(summarise("Rule check", rule, audit_pass))
    print(summarise("Safety rule", safety, audit_pass))
    print(summarise("Judge", {n: v["judge"] for n, v in judge.items()}, audit_pass))

    print("\n| Row | Rule | Safety | Judge | Judge reason |")
    print("|---|---|---|---|---|")
    for o in out:
        print(f"| {o['row']} | {o['rule']} | {o['safety']} | {o['judge']} | {o['judge_reason']} |")

    if len(runs) > 1:
        changed = [n for n in judge if judge[n]["judge"] != runs[1][n]["judge"]]
        print(f"\nJudge calls that changed between runs: {len(changed)} of {len(judge)} {changed or ''}")


def reworded():
    rows = list(csv.DictReader((HERE / "fixtures" / "reworded-test-set.csv").open()))
    judge = load_judge(RESULTS / "reworded-judge.json")
    inflated = [int(r["id"]) for r in rows if r["label"] == "INFLATED"]
    faithful = [int(r["id"]) for r in rows if r["label"] == "FAITHFUL"]
    scores = {
        "Rule check": {int(r["id"]): rule_check(r["question"], r["answer"], r["source"])[0] for r in rows},
        "Safety rule": {int(r["id"]): safety_rule(r["question"], r["answer"], r["source"])[0] for r in rows},
        "Judge": {n: v["judge"] for n, v in judge.items()},
    }
    fmt = lambda rows: ", ".join(map(str, rows)) or "none"
    print("| Check | Inflated caught | Missed (rows) | False alarms on faithful rows |")
    print("|---|---|---|---|")
    for name, s in scores.items():
        caught = [n for n in inflated if s[n] == 0]
        missed = [n for n in inflated if s[n] == 1]
        alarms = [n for n in faithful if s[n] == 0]
        print(f"| {name} | {len(caught)} of {len(inflated)} | {fmt(missed)} | {len(alarms)} of {len(faithful)}: {fmt(alarms)} |")


if __name__ == "__main__":
    reworded() if sys.argv[1:] == ["reworded"] else main()
