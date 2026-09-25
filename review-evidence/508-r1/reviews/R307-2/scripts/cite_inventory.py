#!/usr/bin/env python3
"""List every line added by BASE..HEAD (outside the gitlink) that names a
file existing in the pinned processor tree together with a line number, and
print the cited processor lines at the pinned revision for manual grading.
Usage: cite_inventory.py <repo> <base> <head>"""
import re, subprocess, sys
repo, base, head = sys.argv[1:4]
def git(*a, cwd=repo):
    return subprocess.run(["git", *a], cwd=cwd, check=True, capture_output=True, text=True).stdout
pin = git("ls-tree", head, "protocol-processor").split()[2]
files = git("ls-tree", "-r", "--name-only", pin, cwd=repo + "/protocol-processor").splitlines()
base_names = {}
for f in files:
    base_names.setdefault(f.rsplit("/", 1)[-1], []).append(f)
diff = git("diff", "-U0", base, head, "--", ".", ":!protocol-processor")
cur = None; lineno = 0; added = []
for ln in diff.splitlines():
    if ln.startswith("+++ "):
        cur = ln[6:]; continue
    m = re.match(r"@@ -\S+ \+(\d+)", ln)
    if m:
        lineno = int(m.group(1)); continue
    if ln.startswith("+") and cur:
        added.append((cur, lineno, ln[1:])); lineno += 1
# join each added line with the next added line of the same file (wrapped cites)
pat = re.compile(r"([A-Za-z0-9_./-]+\.(?:sv|svh|cpp|h|py|md|c|v))\s*:\s*((?:[A-Za-z_]+\s+(?:at\s+)?)?\d+(?:\s*-\s*\d+)?(?:\s*,\s*\d+(?:\s*-\s*\d+)?)*)")
n = 0
for i, (f, l, t) in enumerate(added):
    joined = t + (" " + added[i+1][2] if i + 1 < len(added) and added[i+1][0] == f and added[i+1][1] == l + 1 else "")
    for m in pat.finditer(joined):
        if m.start() >= len(t):
            continue
        name = m.group(1).rsplit("/", 1)[-1]
        cands = [p for p in base_names.get(name, []) if p.endswith(m.group(1).lstrip("./")) or m.group(1).endswith(p) or "/" not in m.group(1)]
        if not cands:
            continue
        n += 1
        print(f"=== {f}:{l}: {m.group(0)!r}")
        print(f"    context: {joined.strip()[:200]}")
        for p in cands:
            src = git("show", f"{pin}:{p}", cwd=repo + "/protocol-processor").splitlines()
            for rng in re.findall(r"\d+(?:\s*-\s*\d+)?", m.group(2)):
                a, _, b = rng.partition("-")
                a = int(a); b = int(b) if b else a
                for k in range(a, min(b, a + 12) + 1):
                    if 1 <= k <= len(src):
                        print(f"    {p}:{k}: {src[k-1]}")
print(f"TOTAL processor line citations added: {n}")
