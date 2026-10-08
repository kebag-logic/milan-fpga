"""Find line citations of the both-sides files whose cited text moved in the merge.

Usage: python3 -I cite_shift.py <repo> <dev> <pr> <candidate> <path> [<path> ...]
For each cited path P (by basename) and each tracked text file of the
candidate that cites `basename(P):N` or `basename(P):N-M`, the cited line N
(and M) is read at the side that introduced the citation and at the
candidate. A citation whose line text differs is listed as MOVED. A citation
present on neither side alone (it predates the merge base) is still checked
against both sides and reported with its origin.
"""
import re
import subprocess
import sys

repo, dev, pr, cand = sys.argv[1:5]
paths = sys.argv[5:]


def git(*args):
    return subprocess.run(["git", "-C", repo, "-c", "core.commitGraph=false", *args],
                          check=True, capture_output=True, text=True, errors="replace").stdout


def lines(rev, path):
    try:
        return git("show", f"{rev}:{path}").splitlines()
    except subprocess.CalledProcessError:
        return None


files = [f for f in git("ls-tree", "-r", "--name-only", cand).splitlines()
         if not f.startswith(("external/", "third_party/"))]
moved = 0
for target in paths:
    base = target.rsplit("/", 1)[-1]
    pat = re.compile(re.escape(base) + r":(\d+)(?:-(\d+))?")
    side_text = {rev: lines(rev, target) for rev in (dev, pr, cand)}
    for f in files:
        text = lines(cand, f)
        if text is None:
            continue
        for ln, line in enumerate(text, 1):
            for m in pat.finditer(line):
                # which side carries this exact citation line?
                origin = []
                for rev, name in ((dev, "dev"), (pr, "pr")):
                    other = lines(rev, f) or []
                    if line in other:
                        origin.append(name)
                origin = "+".join(origin) or "merge-only"
                refs = [int(m.group(1))] + ([int(m.group(2))] if m.group(2) else [])
                sides = [r for r, n in ((dev, "dev"), (pr, "pr")) if n in origin] or [dev, pr]
                for n in refs:
                    now = side_text[cand][n - 1].strip() if n <= len(side_text[cand]) else "<past end>"
                    for rev in sides:
                        was = side_text[rev][n - 1].strip() if n <= len(side_text[rev]) else "<past end>"
                        if was != now:
                            moved += 1
                            print(f"MOVED {f}:{ln} cites {base}:{n} origin={origin} side={rev[:8]}\n"
                                  f"    side text: {was[:110]}\n    candidate: {now[:110]}")
print(f"moved citations: {moved}")
