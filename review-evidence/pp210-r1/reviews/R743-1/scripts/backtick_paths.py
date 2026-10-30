#!/usr/bin/env python3
"""List backticked tokens in a checkout's tracked Markdown that look like
repository paths (a known top-level directory, or a root file name) and do not
exist from the repository root. usage: backtick_paths.py <checkout>"""
import re, subprocess, sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
files = subprocess.run(["git", "-C", str(root), "ls-files", "*.md"], capture_output=True, text=True).stdout.split()
tops = ("hdl/", "tb/", "docs/", "scripts/", "syn/", ".github/")
miss = []
for f in files:
    body = re.sub(r"^```.*?^```", "", (root / f).read_text(encoding="utf-8"), flags=re.M | re.S)
    for tok in re.findall(r"`([^`\s]+)`", body):
        t = tok.rstrip(".,:;)")
        if not t.startswith(tops) or any(c in t for c in "*<>{}$|"): continue
        t = t.split(":")[0]
        if not (root / t).exists(): miss.append(f"{f}: {tok}")
print(f"tracked Markdown files: {len(files)}; missing backticked paths: {len(miss)}")
for m in miss: print("  " + m)
