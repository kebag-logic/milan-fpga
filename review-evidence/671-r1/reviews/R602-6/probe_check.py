#!/usr/bin/env python3
"""R602-6: exercise read_fault_cases.comparison_findings beyond its own
self-test arms, and recount the documented case and control figures.
Usage: python3 probe_check.py <repo>"""
import sys
from pathlib import Path
repo = Path(sys.argv[1])
sys.path.insert(0, str(repo / "sw/firmware/nvm_hosttest"))
import read_fault_cases as R
fw = (repo / "sw/firmware/milan_baremetal/milan_baremetal.c").read_text()
bad = []
def say(ok, what):
    print(("OK   " if ok else "FAIL ") + what)
    if not ok: bad.append(what)
cases = R.fault_cases(1000)
say(R.comparison_findings(fw, cases) == [], "shipped firmware and campaign: no comparison finding")
# counts the docs state
cold = sum(not c.restart for c in cases); rst = sum(c.restart for c in cases)
terms = [c for c in cases if R.term_of(c)]
print(f"     cases={len(cases)} cold={cold} restart={rst} term-class={len(terms)}")
say((len(cases), cold, rst, len(terms)) == (3550, 1839, 1711, 128), "docs' 3,550 / 1,839 cold / 1,711 restart / 128 term cases")
say(len(R.READ_FAULT_MUTATIONS) == 18, f"eighteen #671 controls (have {len(R.READ_FAULT_MUTATIONS)})")
for term, _, _ in R.COMPARISON:
    n = [c for c in terms if R.term_of(c) == term]
    say(len(n) == 32 and {c.seq for c in n} >= set(R.FAULT_SEQS) and {c.valid for c in n} == {"a", "b"}
        and {c.restart for c in n} == {True, False} and all(c.count == 2 for c in n),
        f"{term}: 32 cases, every FAULT_SEQS sequence, both orientations, both entry paths, two faulty reads")
# one place removed must fail (the self-test removes only whole classes)
for term, _, _ in R.COMPARISON:
    victim = next(c for c in terms if R.term_of(c) == term and c.restart and c.seq == 0x8000_0000)
    f = R.comparison_findings(fw, [c for c in cases if c != victim])
    say(any(f"{term} has no fault class at 1 place" in x for x in f), f"{term}: one missing place is a finding: {f}")
# a class case whose window misses the judgement does not count
for term, _, _ in R.COMPARISON:
    victim = next(c for c in terms if R.term_of(c) == term and not c.restart and c.seq == 1)
    moved = R.FaultCase(victim.valid, victim.older, victim.seq,
                        (victim.fault[0], victim.fault[1].replace(f":{victim.skip}:2", f":{victim.skip + 5}:2")),
                        victim.skip + 5, 2, victim.restart)
    f = R.comparison_findings(fw, [moved if c == victim else c for c in cases])
    say(any(f"{term} has no fault class" in x for x in f), f"{term}: a window moved off the judgement is a finding")
# firmware comparison changes the check must see
plants = {
    "renamed function": fw.replace("static int nvm_reads_agree(", "static int nvm_reads_same("),
    "a term dropped": fw.replace("a.digest == b.digest &&\n", ""),
    "terms reordered": fw.replace("a.vd == b.vd && a.bytes == b.bytes", "a.bytes == b.bytes && a.vd == b.vd"),
    "or for and": fw.replace("a.digest == b.digest &&", "a.digest == b.digest ||"),
}
for name, text in plants.items():
    say(text != fw and R.comparison_findings(text, cases) != [], f"firmware plant '{name}' is a finding")
# a control with a different plant text is a finding
c2 = dict(R.READ_FAULT_MUTATIONS); k = R.control_of("trailer"); c2[k] = (((c2[k][0][0][0], "0 == 0"),), c2[k][1])
say(any("trailer has no control" in x for x in R.comparison_findings(fw, cases, c2)), "a control that is not the term removed is a finding")
print("probe_check:", "OK" if not bad else f"{len(bad)} failure(s)")
sys.exit(1 if bad else 0)
