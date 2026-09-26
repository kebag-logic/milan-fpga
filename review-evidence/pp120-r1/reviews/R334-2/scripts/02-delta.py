#!/usr/bin/env python3
"""Delta a9b7874d..83c84b19: files touched, subtrees untouched, the wrapper's port
set (module, name, direction/kind, width) before/after via the parent's shared
header parser, and a comment/whitespace-stripped token comparison of both files
(the wrapper also compared as a multiset of port declarations, since only order
changed)."""
import re, subprocess, sys
from pathlib import Path
PK = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(PK / "scratch/parent-scripts"))
from sv_ports import declarations  # noqa: E402
import os
C = os.environ.get("CLONE", "$REVIEWS/r334-2-pp120")
BASE, R2, HEAD = ("0922e43408f891fc0b84a84691df86b4fd0f1c0d", "a9b7874d415d935949becd7ccfd58799927efb08",
                  "83c84b19e09d397ed2eb6f5ace337686ce0ef86b")
git = lambda *a: subprocess.run(["git", "-C", C, *a], capture_output=True, text=True, check=True).stdout
print("== commits a9b7874d..83c84b19:"); print(git("log", "--format=%H %P %s", f"{R2}..{HEAD}"), end="")
print("== files changed a9b7874d..83c84b19 (numstat):"); print(git("diff", "--numstat", R2, HEAD), end="")
print("== files changed base..head (numstat):"); print(git("diff", "--numstat", BASE, HEAD), end="")
for sub in ("hdl", "docs", "syn", "scripts", ".github", "tb/pp_top/Makefile", "tb/pp_top/README.md", "tb/pp_top/name_wr_mutant.py"):
    a, b = git("rev-parse", f"{R2}:{sub}").strip(), git("rev-parse", f"{HEAD}:{sub}").strip()
    print(f"  {sub}: {'IDENTICAL' if a == b else 'CHANGED'} {a[:12]}")
strip_sv = lambda t: re.sub(r"\s+", " ", re.sub(r"//[^\n]*|/\*.*?\*/", "", t, flags=re.S)).strip()
def ports(rev):
    t = git("show", f"{rev}:tb/pp_top/pp_top_wrap.sv")
    return t, [(m, n, k) for m, n, _d, _mb, k in declarations(t) if k != "param"]
t2, p2 = ports(R2); th, ph = ports(HEAD)
print(f"== pp_top_wrap.sv port declarations: r2 {len(p2)}, head {len(ph)}; same multiset: {sorted(p2) == sorted(ph)}; same order: {p2 == ph}")
print("   order-changed names:", [x[1] for i, x in enumerate(ph) if i >= len(p2) or p2[i] != x][:12])
hdr = lambda t: t[t.index("module pp_top_wrap"):t.index(");", t.index("module pp_top_wrap"))]
decl = lambda t: sorted(re.sub(r"\s+", " ", l.strip().rstrip(",")) for l in strip_sv(hdr(t)).replace(",", ",\n").split("\n") if "put " in l)
print(f"   header declarations (type, width, name; comment/space-stripped) identical as a multiset: {decl(t2) == decl(th)} ({len(decl(th))})")
body = lambda t: strip_sv(t[t.index(");", t.index("module pp_top_wrap")):])
print(f"   module body after the header token-identical: {body(t2) == body(th)}")
c2, ch = (git("show", f"{r}:tb/pp_top/sim_main.cpp") for r in (R2, HEAD))
s2, sh = strip_sv(c2), strip_sv(ch)
print(f"== sim_main.cpp stripped tokens identical: {s2 == sh}; identical after removing '[[maybe_unused]] ' once: {s2 == sh.replace('[[maybe_unused]] ', '', 1)}; "
      f"'[[maybe_unused]]' occurrences r2/head: {c2.count('[[maybe_unused]]')}/{ch.count('[[maybe_unused]]')}")
