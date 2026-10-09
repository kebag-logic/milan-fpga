#!/usr/bin/env python3
"""Count sentences over ten words on prose lines ADDED between two revisions,
using the repository's own check_doc_style normaliser and word pattern.
Usage: sentence_probe.py <repo> <base> <head> <page>...  (run with -I)"""
import subprocess, sys, re, importlib.util
repo, base, head, pages = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]
spec = importlib.util.spec_from_file_location("cds", f"{repo}/scripts/check_doc_style.py")
cds = importlib.util.module_from_spec(spec); sys.modules["cds"] = cds; spec.loader.exec_module(cds)
total = 0
for page in pages:
    diff = subprocess.run(["git", "-C", repo, "diff", "-U0", base, head, "--", page],
                          capture_output=True, text=True, check=True).stdout
    src = subprocess.run(["git", "-C", repo, "show", f"{head}:{page}"],
                         capture_output=True, text=True, check=True).stdout.splitlines()
    added = set()
    for m in re.finditer(r"^@@ -\S+ \+(\d+)(?:,(\d+))? @@", diff, re.M):
        start, n = int(m.group(1)), int(m.group(2) or 1)
        added.update(range(start, start + n))
    fenced = False; long_ = []; prose_lines = 0
    for i, raw in enumerate(src, 1):
        s = raw.strip()
        if s.startswith(("```", "~~~")):
            fenced = not fenced; continue
        if fenced or i not in added or not s or s.startswith(("#", "|", ">", "<!--")) or raw.startswith("    "):
            continue
        prose_lines += 1
        text = cds.LIST_ITEM.sub("", raw)
        for sent in cds.sentences(text):
            n = len(cds.WORD.findall(sent))
            if n > 10:
                long_.append((i, n, sent))
    total += len(long_)
    print(f"{page}: {prose_lines} added prose lines, {len(long_)} sentences over ten words")
    for i, n, sent in long_:
        print(f"  {page}:{i}: {n} words: {sent[:110]}")
print(f"TOTAL {total}")
