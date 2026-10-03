#!/usr/bin/env python3
"""Line-citation drift check across a two-parent merge.

For every `path:N` or `path:N-M` citation in a tracked text file at HEAD whose
cited file changed on either side of the merge, find the revisions (base,
parent 1, parent 2) at which the identical citing line already existed, and
compare the cited text there with the cited text at HEAD. A citation whose
cited text differs from every revision it existed at, or that was moved at the
merge without its cited text matching, is printed for manual review.

usage: cite_drift.py REPO BASE P1 P2 HEAD
"""
import re
import subprocess
import sys

repo, base, p1, p2, head = sys.argv[1:6]


def git(*a):
    return subprocess.run(["git", "-C", repo, *a], capture_output=True,
                          text=True, errors="replace").stdout


def show(rev, path):
    r = subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"],
                       capture_output=True, text=True, errors="replace")
    return r.stdout.split("\n") if r.returncode == 0 else None


files = git("ls-files").split("\n")
files = [f for f in files if f]
changed = set()
for a, b in ((base, p1), (base, p2), (p1, head), (p2, head)):
    changed |= set(x for x in git("diff", "--name-only", a, b).split("\n") if x)

by_base = {}
for f in files:
    by_base.setdefault(f.rsplit("/", 1)[-1], []).append(f)

pat = re.compile(r"([A-Za-z0-9_./-]+\.(?:sv|svh|cpp|hpp|h|md|py|sh|tcl|v|yml|yaml|mk)|Makefile):(\d+)(?:-(\d+))?")
text_ext = (".sv", ".svh", ".cpp", ".hpp", ".h", ".md", ".py", ".sh", ".tcl", ".yml", ".yaml", ".mk", "Makefile", ".txt")
cache = {}


def lines(rev, path):
    k = (rev, path)
    if k not in cache:
        cache[k] = show(rev, path)
    return cache[k]


def resolve(cited, citing):
    if cited in files:
        return cited
    cands = [f for f in files if f.endswith("/" + cited) or f == cited]
    if len(cands) == 1:
        return cands[0]
    b = cited.rsplit("/", 1)[-1]
    c = by_base.get(b, [])
    if len(c) == 1:
        return c[0]
    # same-directory preference
    d = citing.rsplit("/", 1)[0]
    c2 = [x for x in c if x.startswith(d + "/")]
    return c2[0] if len(c2) == 1 else None


total = checked = flagged = 0
for f in files:
    if not f.endswith(text_ext):
        continue
    hl = lines(head, f)
    if hl is None:
        continue
    for ln, line in enumerate(hl, 1):
        for m in pat.finditer(line):
            total += 1
            tgt = resolve(m.group(1), f)
            if tgt is None or tgt not in changed:
                continue
            a = int(m.group(2))
            z = int(m.group(3) or a)
            if z < a or z - a > 400:
                continue
            th = lines(head, tgt)
            if th is None:
                continue
            cur = th[a - 1:z]
            checked += 1
            origin = []
            for rev, nm in ((base, "base"), (p1, "p1"), (p2, "p2")):
                fl = lines(rev, f)
                tl = lines(rev, tgt)
                if fl is None or tl is None:
                    continue
                if line in fl:
                    origin.append((nm, tl[a - 1:z] == cur))
            ok = any(same for _, same in origin)
            if not origin:
                status = "NEW-AT-MERGE"
            elif ok:
                continue
            else:
                status = "DRIFT(" + ",".join(n for n, _ in origin) + ")"
            flagged += 1
            print(f"{status}\t{f}:{ln}\t{m.group(0)}\t-> {tgt}")
print(f"# citations {total}, into changed files checked {checked}, flagged {flagged}",
      file=sys.stderr)
