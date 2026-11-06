"""resolution_check.py <repo> <merge> <file>...: for each file, rebuild the conflicted merge of the merge commit's two
parents (git merge-file over their merge base) and check the committed resolution against it: every line outside
the conflict hunks appears in the resolution in order, and how many lines of each side of each hunk it keeps."""
import subprocess, sys, tempfile
from pathlib import Path
repo, merge, files = sys.argv[1], sys.argv[2], sys.argv[3:]
git = lambda *a: subprocess.run(["git", "-C", repo, *a], check=True, capture_output=True, text=True).stdout
ours, theirs = git("rev-parse", f"{merge}^1", f"{merge}^2").split()
base = git("merge-base", ours, theirs).strip()
print(f"merge {git('rev-parse', merge).strip()} ours {ours} theirs {theirs} base {base}")
for f in files:
    with tempfile.TemporaryDirectory() as d:
        paths = []
        for name, rev in (("ours", ours), ("base", base), ("theirs", theirs)):
            p = Path(d) / name
            p.write_text(git("show", f"{rev}:{f}"))
            paths.append(str(p))
        conflicted = subprocess.run(["git", "merge-file", "-p", *paths], capture_output=True, text=True).stdout
    res = git("show", f"{merge}:{f}").split("\n")
    out, hunks, inside, side = [], [], False, None
    for line in conflicted.split("\n"):
        if line.startswith("<<<<<<< "):
            inside, side, h = True, "ours", {"ours": [], "theirs": []}
        elif inside and line.startswith("======="):
            side = "theirs"
        elif inside and line.startswith(">>>>>>> "):
            inside = False
            hunks.append(h)
        elif inside:
            h[side].append(line)
        else:
            out.append(line)
    j, ok = 0, True
    for line in out:
        while j < len(res) and res[j] != line:
            j += 1
        if j == len(res):
            ok = False
            break
        j += 1
    print(f"{f}: {len(out)} context lines in order in the resolution: {ok}; {len(hunks)} hunks")
    for k, h in enumerate(hunks):
        print(f"  hunk {k}: ours {len(h['ours'])} lines, {sum(l in res for l in h['ours'])} kept verbatim; "
              f"theirs {len(h['theirs'])} lines, {sum(l in res for l in h['theirs'])} kept verbatim")
        for side in ("ours", "theirs"):
            for l in h[side]:
                if l not in res:
                    print(f"    {side} line joined or re-measured: {l[:150]}")
