"""Scratch: compare the reviewers' probe plant texts (parsed with ast, never
executed) with the shipped READ_FAULT_MUTATIONS pairs.

usage: python3 -I compare_plants.py REPO R603_PROBE R602_PROBE
"""
import ast
import sys
from pathlib import Path

repo, r603, r602 = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
sys.path.insert(0, str(repo / "sw/firmware/nvm_hosttest"))
from read_fault_cases import READ_FAULT_MUTATIONS  # noqa: E402


def literal(path: Path, name: str):
    for node in ast.parse(path.read_text()).body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", "") == name for t in node.targets):
            return ast.literal_eval(node.value)
    raise SystemExit(f"{name} not found in {path}")


theirs = {k: [tuple(p) for p in v] for k, v in literal(r603, "PLANTS").items()}
theirs.update({k: [tuple(v)] for k, v in literal(r602, "EXTRA_PLANTS").items()})
fw = (repo / "sw/firmware/milan_baremetal/milan_baremetal.c").read_text()
for label in ("r_digest_header_only", "r_fill_from_flash", "r_restage_fail_offers_none",
              "restage_fail_not_unread", "r_restage_any_seq"):
    mine = [tuple(p) for p in READ_FAULT_MUTATIONS[label][0]]
    same = mine == theirs[label]
    occurs = [fw.count(old) for old, _ in theirs[label]]
    print(f"{label}: shipped pairs {'IDENTICAL to' if same else 'DIFFER from'} the reviewer's; "
          f"reviewer text occurs {occurs} time(s) in the head firmware")
