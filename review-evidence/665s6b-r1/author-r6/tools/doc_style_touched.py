#!/usr/bin/env python3
"""doc_style_touched.py REPO BASE PAGE...: check_doc_style.py's analyze() on each page at BASE and at HEAD, and on
the paragraphs of HEAD's page that BASE's does not carry (the text this round adds), as kind counts."""
import collections, subprocess, sys
repo, base, pages = sys.argv[1], sys.argv[2], sys.argv[3:]
sys.path.insert(0, f"{repo}/scripts")
import check_doc_style as cds
show = lambda rev, p: subprocess.run(["git", "-C", repo, "show", f"{rev}:{p}"], capture_output=True, text=True, check=True).stdout
print("in list:", [p for p in pages if p in cds.DOCUMENTS])
for p in pages:
    old, new = show(base, p), show("HEAD", p)
    paras = set(old.split("\n\n"))
    added = "\n\n".join(x for x in new.split("\n\n") if x not in paras)
    kinds = collections.Counter(f.reason.split()[0] for f in cds.analyze(added))
    print(f"{p}: {len(cds.analyze(old))} findings at {base}, {len(cds.analyze(new))} at HEAD; "
          f"in paragraphs new since {base}: {sum(kinds.values())} {dict(kinds)}")
