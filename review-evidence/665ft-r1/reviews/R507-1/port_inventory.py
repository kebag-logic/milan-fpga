#!/usr/bin/env python3
"""Audit carried check labels and named NVM checks from base to head."""
import ast
from pathlib import Path
import re
import subprocess
import sys

repo = Path(sys.argv[1]).resolve()
base = "423ac5d910d09ab189b3acc39ae3ae1d10d50b19"
def old(path):
    return subprocess.check_output(["git", "-C", str(repo), "show", f"{base}:{path}"], text=True)
def literals(text):
    return [ast.literal_eval(x) for x in re.findall(r'"(?:\\.|[^"\\\n])*"', text)]
missing = []
for stem in ("test_port_loop", "test_adp", "lwsrp_port"):
    before = old(f"sw/firmware/ctrl/test/{stem}.c")
    after = (repo / f"sw/firmware/ctrl/test/{stem}.cpp").read_text()
    names = [ast.literal_eval(m.group(1)) for m in re.finditer(r'\b(?:check|check_eq|bound)\(\s*("(?:\\.|[^"\\])*")', before)]
    joined = "\n".join(literals(after))
    gone = [name for name in names if name not in joined]
    print(f"{stem}: {len(names)} literal check call sites, {len(gone)} missing labels")
    for name in names:
        print("  PRESENT" if name not in gone else "  MISSING", name)
    missing += gone
before = old("tb/verilator/mbx/suite.hpp")
after = (repo / "tb/verilator/mbx/suite.hpp").read_text()
old_words = [s for s in literals(before) if s and re.match(r"[A-Z]\d |no bus", s)]
gone = [s for s in old_words if s not in literals(after)]
print(f"mailbox shared suite: {len(old_words)} labelled assertions, {len(gone)} missing")
missing += gone
tests = "\n".join(p.read_text() for p in (repo / "sw/firmware/ctrl_nvm/test").glob("test_nvm_*.cpp"))
registered = set(re.findall(r"TEST_[FP]\(\w+,\s*(\w+)\)", tests))
driver = ast.parse(old("sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py"))
names = set()
for node in ast.walk(driver):
    if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) and node.value.id in ("checks", "write"):
        names.add(node.attr)
# Base aliases are also captured by the public per-module CHECKS tables.
for module in ("nvm_checks.py", "nvm_checks_write.py"):
    tree = ast.parse(old("sw/firmware/ctrl_nvm/test/" + module))
    for node in tree.body:
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.target.id in ("BOOT_CHECKS", "WRITE_CHECKS"):
            assert isinstance(node.value, ast.Dict)
            names.update(ast.literal_eval(k) for k in node.value.keys)
assert len(names) == 42, len(names)
gone = sorted(names - registered)
print("NVM base driver/table references:", sorted(names))
print("NVM missing registrations:", gone)
missing += gone
assert not missing, missing
print("PASS: inventoried old labels and NVM registrations retained; expression and setup semantics require review.")
