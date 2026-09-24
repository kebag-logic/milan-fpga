#!/usr/bin/env python3
"""Every tracked page's heading anchors vs GitHub's file-view ids.

Usage: tree_anchor_check.py <repo> <out.json> [mode]
Renders every `git ls-files '*.md'` page at the checkout through GitHub
(`gh api POST markdown`, mode default `markdown` = the file view) and
compares GitHub's `user-content-` heading ids, in order, with the anchors
gen_toc.headings() gives. Keeps the SHA-256 of every request and response.
"""
import hashlib, json, re, subprocess, sys
from pathlib import Path
repo, out = Path(sys.argv[1]), Path(sys.argv[2])
mode = sys.argv[3] if len(sys.argv) > 3 else "markdown"
sys.path.insert(0, str(repo / "scripts"))
import gen_toc
files = sorted(f for f in subprocess.run(["git", "-C", str(repo), "ls-files", "-z", "*.md"],
               capture_output=True, text=True, check=True).stdout.split("\0") if f)
rows, diff = [], 0
for rel in files:
    text = (repo / rel).read_text()
    req = json.dumps({"context": "kebag-logic/milan-fpga", "mode": mode, "text": text}, separators=(",", ":"))
    r = subprocess.run(["gh", "api", "--method", "POST", "markdown", "--input", "-"],
                       input=req.encode(), capture_output=True, timeout=120)
    if r.returncode:
        rows.append({"page": rel, "error": r.stderr.decode()[:300]}); print("ERR", rel); continue
    resp = r.stdout.decode()
    gh = re.findall(r'<a id="user-content-([^"]*)" class="anchor"', resp)
    local = [a for _, _, a in gen_toc.headings(text)] if not gen_toc.refusals(text) else None
    same = gh == local
    diff += not same
    rows.append({"page": rel, "request_sha256": hashlib.sha256(req.encode()).hexdigest(),
                 "response_sha256": hashlib.sha256(resp.encode()).hexdigest(),
                 "github_ids": gh, "local_anchors": local, "equal": same})
    if not same:
        print("DIFF", rel, len(gh), None if local is None else len(local))
        if local is not None:
            import difflib
            for l in difflib.unified_diff(gh, local, "github", "local", lineterm="", n=0):
                print("   ", l)
out.write_text(json.dumps({"mode": mode, "pages": len(files), "differing": diff, "rows": rows}, indent=1))
print(f"pages {len(files)}, differing {diff}")
