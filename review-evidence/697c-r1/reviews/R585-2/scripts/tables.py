#!/usr/bin/env python3
"""Print the mutation tables of a checkout: name, file, arm, test and needle of every AECP plant, and the
size and names of the control, SRP and AECP tables. Usage: tables.py <checkout>"""
import hashlib, json, sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "sw/firmware/ctrl/test")); sys.path.insert(0, str(root / "sw/firmware/gtest"))
import aecp_mutants, ctrl_mutants, srp_mutants  # noqa
def norm(d):
    return {k: (str(v) if not isinstance(v, (int, str, tuple, list, type(None))) else v) for k, v in vars(d).items()} if hasattr(d, "__dict__") else repr(d)
a = [repr(d) for d in aecp_mutants.DEFECTS]
print("aecp", len(a), hashlib.sha256("\n".join(a).encode()).hexdigest())
for n in ("DEFECTS", "TABLE", "MUTANTS", "PLANTS"):
    for mod in (ctrl_mutants, srp_mutants):
        if hasattr(mod, n):
            v = getattr(mod, n)
            try: print(mod.__name__, n, len(v))
            except TypeError: pass
for name in sorted(x for x in dir(ctrl_mutants) if x.isupper()):
    v = getattr(ctrl_mutants, name)
    if isinstance(v, (list, tuple)) and v and not isinstance(v[0], str):
        print("ctrl_mutants", name, len(v))
for name in sorted(x for x in dir(srp_mutants) if x.isupper()):
    v = getattr(srp_mutants, name)
    if isinstance(v, (list, tuple)) and v and not isinstance(v[0], str):
        print("srp_mutants", name, len(v))
