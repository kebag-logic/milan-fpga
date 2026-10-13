#!/usr/bin/env python3
"""Independent gate-read inventory: every documentation-class page (per the
classifier) whose path or file name appears in a non-documentation tracked
file, including the kinds the classifier's scan does not read (C/C++, YAML,
workflow steps, scripts/). Restricts the report to files the branch changed
or added. Usage: gate_read_inventory.py <checkout> <base-sha> <head-sha>"""
import re, subprocess, sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
base, head = sys.argv[2], sys.argv[3]
sys.path.insert(0, str(root / "scripts"))
import ci_scope  # noqa: E402

files = subprocess.run(["git", "-C", str(root), "ls-files"], capture_output=True,
                       text=True, check=True).stdout.split()
subs = set(ci_scope.submodule_paths())
files = [f for f in files if f not in subs]
docs = [f for f in files if ci_scope.is_doc_only_path(f)]
changed = set(subprocess.run(["git", "-C", str(root), "diff", "--no-renames", "--name-only",
                              f"{base}..{head}"], capture_output=True, text=True,
                             check=True).stdout.split())
readers = [f for f in files if f in changed and not ci_scope.is_doc_only_path(f)]
print(f"tracked non-submodule files: {len(files)}; documentation-class: {len(docs)}; "
      f"branch-changed non-doc files scanned: {len(readers)}")
names = {}
for d in docs:
    names.setdefault(d.rsplit("/", 1)[-1], []).append(d)
hits = {}
for r in readers:
    try:
        text = (root / r).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        continue
    for n, line in enumerate(text.splitlines(), 1):
        for name, pages in names.items():
            if name in line:
                for p in pages:
                    if p in line or ("/" + name) not in line or name == line.strip():
                        hits.setdefault(p, []).append(f"{r}:{n}: {line.strip()[:140]}")
                    elif p.rsplit('/',1)[0].rsplit('/',1)[-1] in line:
                        hits.setdefault(p, []).append(f"{r}:{n}: {line.strip()[:140]}")
for p in sorted(hits):
    tag = "REGISTERED" if p in ci_scope.GATE_READ_DOCS else "doc-class"
    print(f"== {p} [{tag}] ({len(hits[p])} mentions)")
    for h in hits[p][:12]:
        print("   ", h)
    if len(hits[p]) > 12:
        print(f"    ... {len(hits[p]) - 12} more")
