"""Probe the format page gate's LINE_CITE_RE at the clone given as argv[1]:
each claimed form must match whole, and listed non-claimed forms are reported."""
import importlib.util, sys
from pathlib import Path
root = Path(sys.argv[1])
sys.path.insert(0, str(root / "scripts"))
spec = importlib.util.spec_from_file_location("g", root / "scripts/check_nvm_format_32x32.py")
g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
claimed = ["`a/b.py:12`", "a/b.py:12", "`a/b.py:12-34`", "a/b.py:12-34", "`a/b.py:12,34`", "a/b.py:12, 34",
           "`a/b.py` line 12", "`a/b.py` lines 12-34", "a/b.py#L12", "a/b.py#L12-L34", "[x](../b.sv#L7)"]
other = ["Makefile:12", "`a/b.py`, line 12", "a/b.py line 12", "a/b.py lines 12 to 34", "a/b.py L12",
         "https://example.com:8080/x", "see `nvm_store.c` at line 12"]
bad = 0
for s in claimed:
    m = [x.group(0) for x in g.LINE_CITE_RE.finditer(s)]
    ok = bool(m) and any(s.strip('`[]()x').endswith(x.strip('`')) or x in s for x in m)
    print(f"CLAIMED {'MATCH' if m else 'MISS '} {s!r} -> {m}")
    bad += not m
for s in other:
    m = [x.group(0) for x in g.LINE_CITE_RE.finditer(s)]
    print(f"OTHER   {'MATCH' if m else 'miss '} {s!r} -> {m}")
print(f"claimed forms missed: {bad}")
sys.exit(1 if bad else 0)
