#!/usr/bin/env python3
"""Compare round-1 and round-2 reviewer receipts for behaviour, not text.

Usage: compare_rounds.py ROUND1_RECEIPTS ROUND2_RECEIPTS

- mutants.jsonl: equal once "Ran N tests in T s" timings are normalised.
- probes-{head,base}.jsonl: byte-identical.
- new-tests-vs-base-generator.log: the set of (test, subtest key, outcome)
  triples and the multiset of assertion messages are equal. Raw text differs
  because unittest -v prints each test's docstring (added in round 2) and the
  scratch path and line numbers differ.
Exit 0 when all are equal.
"""
import re
import sys
from collections import Counter
from pathlib import Path

r1, r2 = (Path(a) for a in sys.argv[1:3])
rc = 0


def timing(text):
    return re.sub(r"Ran (\d+) tests? in [0-9.]+s", r"Ran \1 tests in <t>", text)


def outcomes(text):
    # join a "name (...) (key=...)\nDocstring ... FAIL" pair back to one line
    text = re.sub(r"\)\n[^\n]*? \.\.\. ", ") ... ", text)
    return sorted(set(re.findall(
        r"^\s*(test_\w+) \([^)]*\)(?: \((key=[^)]*)\))? \.\.\. (ok|FAIL|ERROR)?$",
        text, re.M)))


def messages(text):
    return Counter(re.findall(r"^(AssertionError: .*)$", text, re.M))


same = timing((r1 / "mutants.jsonl").read_text()) == timing((r2 / "mutants.jsonl").read_text())
print(f"mutants.jsonl (timing-normalised): {'IDENTICAL' if same else 'DIFFERS'}")
rc |= not same
for name in ("probes-head.jsonl", "probes-base.jsonl"):
    same = (r1 / name).read_bytes() == (r2 / name).read_bytes()
    print(f"{name}: {'BYTE-IDENTICAL' if same else 'DIFFERS'}")
    rc |= not same
a = (r1 / "new-tests-vs-base-generator.log").read_text()
b = (r2 / "new-tests-vs-base-generator.log").read_text()
oa, ob = outcomes(a), outcomes(b)
print(f"new-tests-vs-base-generator.log: round1 {len(oa)} outcomes, "
      f"round2 {len(ob)} outcomes, {'EQUAL' if oa == ob else 'DIFFER'}; "
      f"FAIL count r1={sum(o[2] == 'FAIL' for o in oa)} "
      f"r2={sum(o[2] == 'FAIL' for o in ob)}")
rc |= oa != ob
ma, mb = messages(a), messages(b)
print(f"  assertion messages: {sum(ma.values())} vs {sum(mb.values())}, "
      f"{'EQUAL' if ma == mb else 'DIFFER'}")
rc |= ma != mb
print("  tails:", timing(a.strip().splitlines()[-1]), "|",
      [l for l in b.strip().splitlines() if l.startswith("FAILED")])
sys.exit(rc)
