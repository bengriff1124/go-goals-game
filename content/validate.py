#!/usr/bin/env python3
"""Validate and balance the SDG question banks.

Checks every goal file for structural integrity, then shuffles answer positions
so no single slot holds a disproportionate share of correct answers (otherwise
students learn "just pick the first one").

Usage:  python3 content/validate.py [--fix]
"""
import json, sys, random, collections, pathlib

HERE = pathlib.Path(__file__).parent
FIX = "--fix" in sys.argv
random.seed(20300101)  # deterministic: reruns don't reshuffle differently

total = 0
all_ok = True

for path in sorted(HERE.glob("goal-*.json")):
    data = json.loads(path.read_text())
    qs = data["questions"]
    errs = []
    ids = set()

    for q in qs:
        qid = q.get("id", "<no id>")
        if qid in ids:
            errs.append(f"{qid}: duplicate id")
        ids.add(qid)
        if q.get("src") not in data.get("sources", {}):
            errs.append(f"{qid}: src '{q.get('src')}' not in sources")
        opts, wrong = q.get("options", []), q.get("whyWrong", [])
        if len(opts) != len(wrong):
            errs.append(f"{qid}: {len(opts)} options but {len(wrong)} whyWrong")
        ci = q.get("correctIndex")
        if not isinstance(ci, int) or not (0 <= ci < len(opts)):
            errs.append(f"{qid}: bad correctIndex {ci}")
            continue
        if wrong[ci] is not None:
            errs.append(f"{qid}: whyWrong[{ci}] should be null (it's the correct answer)")
        for i, w in enumerate(wrong):
            if i != ci and not w:
                errs.append(f"{qid}: missing whyWrong for option {i}")
        for field in ("prompt", "whyCorrect", "action"):
            if not q.get(field):
                errs.append(f"{qid}: empty {field}")
        if len(set(opts)) != len(opts):
            errs.append(f"{qid}: duplicate option text")

    if FIX and not errs:
        # even spread of correct-answer positions
        n = len(qs)
        slots = [i % 3 for i in range(n)]
        random.shuffle(slots)
        for q, want in zip(qs, slots):
            k = len(q["options"])
            want %= k
            ci = q["correctIndex"]
            if ci == want:
                continue
            for arr in ("options", "whyWrong"):
                a = q[arr]
                a[ci], a[want] = a[want], a[ci]
            q["correctIndex"] = want
        q.pop("tier", None)
        for q in qs:
            q.pop("tier", None)   # single difficulty level; field is vestigial
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")

    spread = collections.Counter(q["correctIndex"] for q in qs)
    total += len(qs)
    status = "OK " if not errs else "FAIL"
    if errs:
        all_ok = False
    print(f"{status} {path.name}: {len(qs):>3} questions  "
          f"sources={len(data.get('sources', {}))}  "
          f"answer slots={dict(sorted(spread.items()))}")
    for e in errs[:10]:
        print(f"       - {e}")

print(f"\n{total} questions across {len(list(HERE.glob('goal-*.json')))} goals"
      f"  ({17 * 50} target)")
sys.exit(0 if all_ok else 1)
