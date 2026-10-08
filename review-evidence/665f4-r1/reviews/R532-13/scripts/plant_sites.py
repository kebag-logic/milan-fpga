"""R532-13: static check that every SRP plant has exactly one planting site at the candidate,
that names are unique, and that the IF=1 selection includes the round-13 plants. Usage: <repo> <lwsrp> <out>"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import REPO, LWSRP, OUT
from collections import Counter
import srp_mutants
from ctrl_build import CTRL
bad = [d.name for d in srp_mutants.DEFECTS if (CTRL / d.path).read_text().count(d.old) != 1]
dup = [n for n, c in Counter(d.name for d in srp_mutants.DEFECTS).items() if c > 1]
pref = ("four-way-", "binding-", "feedback-", "r10-", "p11-", "srp-bound-", "srp-term-", "srp-poll-extra", "srp-send-extra")
if1 = [d.name for d in srp_mutants.DEFECTS if d.name.startswith(pref)]
new = {"feedback-leave-clears-advertise-only", "feedback-failed-indication-as-advertise", "feedback-change-clears-both-kinds"}
print(f"plants={len(srp_mutants.DEFECTS)} if1_selected={len(if1)} bad_sites={bad} duplicates={dup} new_in_if1={sorted(new & set(if1))}")
sys.exit(1 if bad or dup or not new <= set(if1) else 0)
