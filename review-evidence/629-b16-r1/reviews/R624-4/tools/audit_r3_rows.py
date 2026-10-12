#!/usr/bin/env python3
"""R624-4: the packet-file hash rows of lane B16's section on the page at round 3 against author-r3 and the pinned manifest.

usage: audit_r3_rows.py <page-at-0782c55f.md> <evidence-repo> <pinned-commit> <out.json>
"""
import hashlib, json, re, subprocess, sys
DOC, EV, PIN, OUT = sys.argv[1:5]
BASE = "review-evidence/629-b16-r1"
show = lambda p: subprocess.run(["git", "-C", EV, "show", f"{PIN}:{p}"], check=True, capture_output=True).stdout
man = {e["file"]: e for e in json.loads(show(f"{BASE}/MANIFEST.json"))}
text = open(DOC, encoding="utf-8").read().split("\n")
s = next(i for i, l in enumerate(text) if l.startswith("## Dev 5603c353, 2026-10-12: lane B16"))
e = next((i for i in range(s + 1, len(text)) if text[i].startswith("## ")), len(text))
out = []
for i in range(s, e):
    c = [x.strip() for x in text[i].strip().strip("|").split("|")]
    if len(c) == 3 and re.fullmatch(r"`[0-9a-f]{64}`", c[-1]) and c[1].replace(",", "").isdigit():
        path = re.match(r"`([^`]+)`", c[0]).group(1)
        sha = c[2].strip("`"); size = int(c[1].replace(",", ""))
        m = man.get(f"author-r3/{path}")
        data = show(f"{BASE}/author-r3/{path}")
        ok = (m is not None and m["original_sha256"] == sha and m["published_sha256"] == sha and not m["path_redacted"]
              and hashlib.sha256(data).hexdigest() == sha and len(data) == size)
        out.append({"line": i + 1, "path": path, "ok": ok})
json.dump(out, open(OUT, "w"), indent=1)
print(json.dumps({"rows": len(out), "ok": sum(r["ok"] for r in out)}))
sys.exit(0 if all(r["ok"] for r in out) else 1)
