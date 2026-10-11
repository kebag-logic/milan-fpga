#!/usr/bin/env python3
"""Census of check 13's comparison-term classes at a tree (#671 round 6).

Usage: term_census.py TREE

Prints the generated campaign's size, the term-class cases per term, group,
orientation, sequence and entry path, where each term first appears in the
interleaved order, and the comparison check's findings at the tree's own
firmware (none expected). Exit 1 if a class is missing, a case repeats, or
the check reports anything.
"""
import sys
from collections import Counter
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tree / "sw/firmware/nvm_hosttest"))
import read_fault_cases as c  # noqa: E402

firmware = (tree / "sw/firmware/milan_baremetal/milan_baremetal.c").read_text()
rc = 0
for img_len in (1504, 9984):            # any even record area; the classes do not depend on it
    body = 40 + (img_len - 44) // 2
    cases = c.fault_cases(body)
    terms = [x for x in cases if c.term_of(x)]
    print(f"body {body}: {len(cases)} cases ({sum(x.restart for x in cases)} restarts), "
          f"{len(set(cases))} distinct, {len(terms)} term-class cases")
    rc |= len(set(cases)) != len(cases)
    per = Counter((c.term_of(x), x.older, x.fault[1][0] == x.valid) for x in terms)
    for key, n in sorted(per.items()):
        print(f"  term {key[0]:<10} other {'older' if key[1] else 'blank'}, faulted "
              f"{'valid/newer' if key[2] else 'older'}: {n} cases")
    first = {}
    for i, x in enumerate(cases):
        first.setdefault(c.term_of(x), i)
    print("  first index per term:", {k: v for k, v in first.items() if k})
    for term, _, _ in c.COMPARISON:
        sample = next(x for x in terms if c.term_of(x) == term)
        print(f"  e.g. {term}: {sample.name}; judgement {c.expect(sample).judgement}")
    got = c.comparison_findings(firmware, cases)
    print("  comparison_findings:", got or "none")
    rc |= bool(got)
print("controls:", [k for k in c.READ_FAULT_MUTATIONS if k.startswith("r_omit_")])
sys.exit(rc)
