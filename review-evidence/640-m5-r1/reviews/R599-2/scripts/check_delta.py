#!/usr/bin/env python3
"""Usage: check_delta.py REPO. Check the R599-2 delta and patch-anchor exposure."""
import ast
import difflib
import hashlib
from pathlib import Path
import re
import subprocess
import sys

repo = Path(sys.argv[1]).resolve()
old = "988ec7f653d0a21e0f7b40b03b8c74155d8962cf"
head = "c0cba330fd485e52fcb90d5ccc69169edf9f0c2b"
rtl = "hdl/common/csr/milan_csr.sv"


def git(*args):
    return subprocess.check_output(["git", "-C", str(repo), *args])


a = git("show", f"{old}:{rtl}")
b = git("show", f"{head}:{rtl}")
changed = git("diff", "--name-only", old, head).decode().splitlines()
assert changed == ["docs/design/MARK_II_AREA_PLAN.md", rtl], changed
print("Delta paths:", ", ".join(changed))
delta = list(difflib.unified_diff(a.decode().splitlines(), b.decode().splitlines()))
edits = [x[1:] for x in delta if x[:1] in ("+", "-") and x[:3] not in ("+++", "---")]
assert len(edits) == 12 and all(x.lstrip().startswith("//!") for x in edits)
strip = lambda data: re.sub(rb"//[^\n]*", b"", data)
assert strip(a) == strip(b)
print("Exactly six deleted and six added banner-comment lines; comment-stripped bytes identical")
print("Line counts:", len(a.splitlines()), len(b.splitlines()))
for label, data in (("old", a), ("head", b)):
    print(label, "RTL sha256", hashlib.sha256(data).hexdigest())
for name in ("tb/verilator/csr/lock_mutants.py", "tb/verilator/csr/gen_lockstep.py"):
    assert git("show", f"{old}:{name}") == git("show", f"{head}:{name}")
    tree = ast.parse(git("show", f"{head}:{name}").decode())
    strings = {x.value for x in ast.walk(tree) if isinstance(x, ast.Constant)
               and isinstance(x.value, str) and len(x.value) >= 12}
    hits = [s for s in strings if s in a.decode() or s in b.decode()]
    assert all(a.decode().count(s) == b.decode().count(s) for s in hits)
    print(f"{name}: unchanged; all {len(hits)} RTL-matching strings of at least 12 characters preserve counts")
    if name.endswith("lock_mutants.py"):
        assignment = next(x for x in tree.body if isinstance(x, ast.Assign)
                          and any(isinstance(t, ast.Name) and t.id == "MUTATIONS" for t in x.targets))
        mutations = ast.literal_eval(assignment.value)
        for title, pattern, replacement, check, leg in mutations:
            assert a.decode().count(pattern) == b.decode().count(pattern) == 1
            print(f"mutation anchor exact once: {check} ({leg}): {title}")
patches = git("ls-files", "-z", "--", "tb/**/*.patch").split(b"\0")
patches = [x.decode() for x in patches if x]
for name in patches:
    data = git("show", f"{head}:{name}").decode()
    assert git("show", f"{old}:{name}").decode() == data
    assert not any(line.strip() in data for line in edits)
    print("patch unaffected:", name)
print(f"All {len(patches)} tracked tb/**/*.patch files unchanged; none contains a changed banner line")
ref = git("show", f"{head}:tb/verilator/csr/milan_csr_ref.sv").replace(
    b"module milan_csr_ref #(", b"module milan_csr #(")
assert ref == git("show", "e8454e2751d05b02ee8e5a571857589ab358ab86:" + rtl)
print("Frozen reference matches e8454e27 byte for byte after module-name normalization")
print("PASS")
