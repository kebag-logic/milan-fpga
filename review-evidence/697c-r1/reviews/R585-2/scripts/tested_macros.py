#!/usr/bin/env python3
"""List every macro a conditional directive tests in the boundary's units (firmware side and stack side),
with whether a directive region guarded by it contains an #include. Usage: tested_macros.py <checkout>"""
import re, sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
ctrl = root / "sw/firmware/ctrl"
stack = root / "third_party/tsn-c-stack"
units = [p for d in sorted(ctrl.iterdir()) if d.is_dir() and d.name not in ("host", "test") and not d.name.startswith((".", "__"))
         for p in sorted(d.glob("*.[ch]"))] + sorted((ctrl / "test").rglob("*.c"))
units += sorted((stack / "src").glob("*.c")) + sorted((stack / "include").glob("*.h"))
units += sorted((stack / "tests").glob("*.[ch]pp"))
cond = re.compile(r"^\s*#\s*(if|ifdef|ifndef|elif|elifdef|elifndef)\b(.*)$")
ident = re.compile(r"\b([A-Za-z_]\w*)\b")
skip = {"defined", "__has_include", "__has_include_next"}
seen = {}
for u in units:
    lines = u.read_text(errors="replace").splitlines()
    stackd = []
    for i, ln in enumerate(lines):
        m = cond.match(ln)
        if m:
            names = [n for n in ident.findall(re.sub(r'"[^"]*"|<[^>]*>', "", m.group(2))) if n not in skip]
            if m.group(1).startswith("if"):
                stackd.append(names)
            else:
                stackd[-1:] = [names]
            for n in names:
                seen.setdefault(n, set()).add(u.relative_to(root).as_posix())
        elif re.match(r"^\s*#\s*endif", ln) and stackd:
            stackd.pop()
        elif re.match(r"^\s*#\s*include", ln) and stackd:
            for names in stackd:
                for n in names:
                    seen.setdefault(n + "  [guards an #include]", set()).add(f"{u.relative_to(root).as_posix()}:{i+1}")
for n in sorted(seen):
    print(n, " ".join(sorted(seen[n])[:6]))
