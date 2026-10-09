"""Every file a LiteX export's TCL reads is the same at two commits.

Usage: check_tcl_reads.py <tree> <export-dir> <base> <head> <report.json>
A path inside a submodule is judged by the submodule's gitlink at both commits;
any other path inside the tree by its blob at both commits. Exit 1 on any
difference or on a path that is neither.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

tree, export, base, head, report = Path(sys.argv[1]).resolve(), Path(sys.argv[2]), sys.argv[3], sys.argv[4], Path(sys.argv[5])


def git(*args: str) -> str:
    """One git answer, refused when git fails."""
    return subprocess.run(["git", "-C", str(tree), *args], check=True, capture_output=True, text=True).stdout


subs = [ln.split()[1] for ln in git("config", "-f", ".gitmodules", "--get-regexp", r"submodule\..*\.path").splitlines()]
READ = re.compile(r"^(?:read_verilog|read_vhdl|read_xdc|read_mem|add_files|source)\b.*?\{([^}]+)\}", re.M)
paths = set()
for tcl in sorted(export.rglob("*.tcl")):
    for m in READ.finditer(tcl.read_text()):
        paths.add(m.group(1))
res = {"tcl_paths": len(paths), "tree_files": 0, "submodule_files": 0, "outside": [], "changed": [], "pins": {}}
for p in sorted(paths):
    pp = Path(p)
    if not pp.is_absolute():
        res["outside"].append(p)   # relative: inside the export directory, compared byte for byte there
        continue
    try:
        rel = pp.resolve().relative_to(tree).as_posix()
    except ValueError:
        res["outside"].append(p)
        continue
    sub = next((s for s in subs if rel == s or rel.startswith(s + "/")), None)
    if sub:
        res["submodule_files"] += 1
        if sub not in res["pins"]:
            pins = [git("ls-tree", c, sub).split()[2] if git("ls-tree", c, sub) else None for c in (base, head)]
            res["pins"][sub] = pins
            if pins[0] != pins[1]:
                res["changed"].append(sub)
        continue
    res["tree_files"] += 1
    blobs = [git("rev-parse", f"{c}:{rel}").strip() for c in (base, head)]
    if blobs[0] != blobs[1]:
        res["changed"].append(rel)
report.write_text(json.dumps(res, indent=1) + "\n")
print(json.dumps({k: (len(v) if isinstance(v, (list, dict)) else v) for k, v in res.items()}))
for c in res["changed"]:
    print("CHANGED", c)
for o in res["outside"]:
    print("OUTSIDE", o)
# A path outside the tree (the LiteX installation) is the same environment for both
# exports; the TCL bytes that name it are compared by compare_same.py.
sys.exit(1 if res["changed"] else 0)
