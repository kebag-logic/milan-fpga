"""Round 3 scratch: compare the reviewers' round-2 probe texts (parsed with
ast, never executed) with the shipped controls, and check that every anchor
their probes plant or patch at still occurs exactly once at the head.

usage: python3 -I compare_plants.py REPO R603_MUTANTS R603_REATTACH R602_PLANT
"""
import ast
import sys
from pathlib import Path

repo, mutants, reattach, plant = (Path(x) for x in sys.argv[1:5])
sys.path.insert(0, str(repo / "sw/firmware/nvm_hosttest"))
from read_fault_cases import READ_FAULT_MUTATIONS  # noqa: E402


def literal(path: Path, name: str):
    """The value of a module-level assignment, by ast.literal_eval."""
    for node in ast.parse(path.read_text()).body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", "") == name for t in node.targets):
            return ast.literal_eval(node.value)
    raise SystemExit(f"{name} not found in {path}")


fw = (repo / "sw/firmware/milan_baremetal/milan_baremetal.c").read_text()
host = (repo / "sw/firmware/nvm_hosttest/nvm_host.c").read_text()
r603 = literal(mutants, "PROBES")
r602 = literal(plant, "PROBES")
ok = True
for mine, theirs in (("r_reattach_goes_live", r603["p_reattach_goes_live"]),
                     ("r_judge_four_tries", r603["p_judge_four_tries"]),
                     ("r_reattach_goes_live", r602["p1_reattach_no_hold"][0])):
    pair = READ_FAULT_MUTATIONS[mine][0][0]
    same = tuple(pair) == tuple(theirs)
    contains = theirs[0] in pair[0] or pair[0] in theirs[0]
    print(f"{mine}: shipped pair {'IDENTICAL to' if same else 'differs from'} the reviewer's"
          f"{'' if same else (' (one old text contains the other)' if contains else '')}; "
          f"reviewer old text occurs {fw.count(theirs[0])} time(s) in the head firmware")
    ok &= fw.count(theirs[0]) == 1
for name in ("HARNESS_PATCH_ANCHOR", "MAIN_ANCHOR"):
    n = host.count(literal(reattach, name))
    print(f"probe_reattach {name} occurs {n} time(s) in the head harness")
    ok &= n == 1
n = fw.count(literal(reattach, "REATTACH_OLD"))
print(f"probe_reattach REATTACH_OLD occurs {n} time(s) in the head firmware")
ok &= n == 1
for label, (old, _new) in r603.items():
    print(f"R603-2 {label}: old text occurs {fw.count(old)} time(s)")
for label, pairs in r602.items():
    print(f"R602-2 {label}: old text(s) occur {[fw.count(o) for o, _ in pairs]} time(s)")
print("compare_plants: " + ("every shipped anchor matches" if ok else "A MISMATCH"))
sys.exit(0 if ok else 1)
