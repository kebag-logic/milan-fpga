#!/usr/bin/env python3
"""anchors_probe.py <repo> <old-rev> <new-rev>: for each Markdown link to a source
file with #L<n>, compare the anchored line at new-rev against the line the same
link (by order of occurrence per document and target) named at old-rev."""
import re, subprocess, sys
repo, old, new = sys.argv[1:4]
def show(rev, path):
    r = subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None
def docs(rev):
    out = subprocess.run(["git", "-C", repo, "ls-tree", "-r", "--name-only", rev], capture_output=True, text=True).stdout.split()
    return [p for p in out if p.endswith(".md")]
link = re.compile(r"\]\(([^)#\s]+)#L(\d+)\)")
import posixpath
bad = total = 0
for d in docs(new):
    nt, ot = show(new, d), show(old, d)
    if nt is None:
        continue
    nl = [(m.group(1), int(m.group(2))) for m in link.finditer(nt)]
    ol = [(m.group(1), int(m.group(2))) for m in link.finditer(ot)] if ot else []
    for i, (target, n) in enumerate(nl):
        path = posixpath.normpath(posixpath.join(posixpath.dirname(d), target))
        src_new = show(new, path)
        if src_new is None:
            print(f"MISSING-TARGET {d} {target}"); bad += 1; continue
        lines = src_new.split("\n")
        total += 1
        text_new = lines[n - 1].strip() if n <= len(lines) else "<past end>"
        if i < len(ol) and ol[i][0] == target:
            src_old = show(old, path).split("\n")
            text_old = src_old[ol[i][1] - 1].strip() if ol[i][1] <= len(src_old) else "<past end>"
            status = "SAME" if text_old == text_new else "MOVED"
        else:
            text_old, status = "<no counterpart>", "NEW"
        if status != "SAME":
            bad += status == "MOVED"
        print(f"{status} {d} {target}#L{n}: {text_new[:90]}" + ("" if status == "SAME" else f"  || old: {text_old[:90]}"))
print(f"anchors {total}; moved {bad}")
