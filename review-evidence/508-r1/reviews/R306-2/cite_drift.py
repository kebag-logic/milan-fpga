#!/usr/bin/env python3
"""Pin-move citation drift: for every `<processor file>:<line spans>` citation
in the parent's tracked text at <head> (submodules excluded), compare the cited
lines at the OLD processor pin with the same line numbers at the NEW pin. A
citation whose text differs was valid at the old pin and has drifted unless
the citing text was updated with the move. Lines that continue a citation on
the next source line ("...sv:\\n  //! 451") are listed separately for hand review.

usage: cite_drift.py <repo> <head> <old-pp> <new-pp>
"""
import re, subprocess, sys

repo, head, old_pp, new_pp = sys.argv[1:5]
pp = repo + "/protocol-processor"


def git(*a, cwd=repo):
    return subprocess.run(["git", "-C", cwd, *a], check=True,
                          capture_output=True, text=True, errors="replace").stdout


new_files = set(git("ls-tree", "-r", "--name-only", new_pp, cwd=pp).split("\n"))
old_files = set(git("ls-tree", "-r", "--name-only", old_pp, cwd=pp).split("\n"))
changed = set(git("diff", "--name-only", old_pp, new_pp, cwd=pp).split("\n")) - {""}
parent_files = set(git("ls-tree", "-r", "--name-only", head).split("\n"))
cache = {}


def body(rev, path):
    k = (rev, path)
    if k not in cache:
        try:
            cache[k] = git("show", f"{rev}:{path}", cwd=pp).split("\n")
        except subprocess.CalledProcessError:
            cache[k] = None
    return cache[k]


CITE = re.compile(r"((?:protocol-processor/)?[\w./-]*\.(?:sv|svh|v|md|cpp|py|h|yaml|tcl)):"
                  r"(\d+(?:-\d+)?(?:,\s*\d+(?:-\d+)?)*)")
DANGLING = re.compile(r"((?:protocol-processor/)?[\w./-]*\.(?:sv|svh|v|md|cpp|py)):\s*$")
tracked = [p for p in git("ls-files", "--", ".", ":(exclude)protocol-processor",
                          ":(exclude)external", ":(exclude)gptp-processor",
                          ":(exclude)third_party").split("\n")
           if re.search(r"\.(sv|svh|v|md|cpp|py|h|sh|tsv|txt|yml|yaml|mk)$|Makefile$", p)]
drift = total = 0
for f in tracked:
    try:
        text = git("show", f"{head}:{f}").split("\n")
    except subprocess.CalledProcessError:
        continue
    for ln, line in enumerate(text, 1):
        for m in CITE.finditer(line):
            path, spans = m.group(1), m.group(2)
            rel = path[len("protocol-processor/"):] if path.startswith("protocol-processor/") else path
            if not path.startswith("protocol-processor/") and path in parent_files:
                continue
            cands = [rel] if rel in new_files else sorted(
                p for p in new_files if p.endswith("/" + rel) or p == rel)
            if not cands:
                continue
            total += 1
            c = cands[0]
            o, n = body(old_pp, c), body(new_pp, c)
            if c not in changed:
                continue
            diffs = []
            for sp in re.split(r",\s*", spans):
                a, _, b = sp.partition("-")
                for k in range(int(a), int(b or a) + 1):
                    ot = o[k - 1] if o and 0 < k <= len(o) else "<absent>"
                    nt = n[k - 1] if n and 0 < k <= len(n) else "<absent>"
                    if ot != nt:
                        diffs.append((k, ot.strip()[:110], nt.strip()[:110]))
            if diffs:
                drift += 1
                print(f"DRIFT {f}:{ln}: {path}:{spans}  (ambiguous: {len(cands)})")
                print(f"   cite: {line.strip()[:150]}")
                for k, ot, nt in diffs[:4]:
                    print(f"   L{k} old: {ot}")
                    print(f"   L{k} new: {nt}")
        if DANGLING.search(line):
            print(f"CONTINUED {f}:{ln}: {line.strip()[:120]} || {text[ln].strip()[:120] if ln < len(text) else ''}")
print(f"TOTAL processor citations {total}; drifted across {old_pp[:10]}->{new_pp[:10]}: {drift}")
