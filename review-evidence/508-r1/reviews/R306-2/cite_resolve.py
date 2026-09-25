#!/usr/bin/env python3
"""List every processor file:line citation on lines a PR range ADDS, and print
the cited lines from the pinned processor tree so each can be judged against
the construct its text names.

usage: cite_resolve.py <repo> <base> <head> [<pp-rev>]
Reads only git objects (git show / git diff); writes nothing.
"""
import re, subprocess, sys

repo, base, head = sys.argv[1:4]
pp_rev = sys.argv[4] if len(sys.argv) > 4 else None


def git(*a, cwd=repo):
    return subprocess.run(["git", "-C", cwd, *a], check=True,
                          capture_output=True, text=True).stdout


pp_dir = repo + "/protocol-processor"
if pp_rev is None:
    pp_rev = git("rev-parse", f"{head}:protocol-processor").strip()
pp_files = git("ls-tree", "-r", "--name-only", pp_rev, cwd=pp_dir).split("\n")
by_base = {}
for p in pp_files:
    by_base.setdefault(p.rsplit("/", 1)[-1], []).append(p)

diff = git("diff", "-U0", "--no-color", f"{base}..{head}", "--", ".",
           ":(exclude)protocol-processor")
CITE = re.compile(r"((?:protocol-processor/)?[\w./-]*\.(?:sv|svh|v|md|cpp|py|h|yaml|tcl)):"
                  r"(\d+(?:-\d+)?(?:,\s*\d+(?:-\d+)?)*)")
cur = None
n = 0
for line in diff.split("\n"):
    if line.startswith("+++ "):
        cur = line[6:] if line.startswith("+++ b/") else None
        continue
    if not line.startswith("+") or cur is None:
        continue
    for m in CITE.finditer(line):
        path, spans = m.group(1), m.group(2)
        rel = path[len("protocol-processor/"):] if path.startswith("protocol-processor/") else path
        cands = [rel] if rel in pp_files else [p for p in pp_files if p.endswith("/" + rel)] \
            or by_base.get(rel.rsplit("/", 1)[-1], [])
        if not cands:
            continue          # not a processor file
        # a parent-repo file with the same name wins when the path is parent-rooted
        parent_hit = subprocess.run(["git", "-C", repo, "cat-file", "-e", f"{head}:{path}"],
                                    capture_output=True).returncode == 0
        if parent_hit and not path.startswith("protocol-processor/"):
            continue
        n += 1
        print(f"=== [{n}] {cur}: {path}:{spans}")
        print(f"    context: {line[1:].strip()[:160]}")
        for c in cands[:2]:
            body = git("show", f"{pp_rev}:{c}", cwd=pp_dir).split("\n")
            for sp in re.split(r",\s*", spans):
                a, _, b = sp.partition("-")
                lo, hi = int(a), int(b or a)
                for k in range(lo, min(hi, lo + 12) + 1):
                    txt = body[k - 1] if 0 < k <= len(body) else "<<PAST EOF>>"
                    print(f"    {c}:{k}: {txt.rstrip()[:150]}")
print(f"TOTAL {n} processor citations on added lines ({base[:10]}..{head[:10]}, pp {pp_rev[:10]})")
