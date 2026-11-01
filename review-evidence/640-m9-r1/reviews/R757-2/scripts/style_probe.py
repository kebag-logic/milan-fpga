#!/usr/bin/env python3
"""Style probe over the lines a change adds.

Usage: python3 -I style_probe.py <repo> <base> <page>...
1. scripts/check_doc_style.py analyze() over every prose block that overlaps
   an added line (the gate itself only covers its fixed page list).
2. Paragraph word counts of those blocks (min/max/mean).
3. Non-ASCII characters on added lines, by code point and count; dashes
   (U+2010..U+2015, U+2212) are listed with their lines.
"""
import collections, re, subprocess, sys, unicodedata
from pathlib import Path

repo = Path(sys.argv[1]).resolve(); base = sys.argv[2]; pages = sys.argv[3:]
sys.path.insert(0, str(repo / "scripts"))
import check_doc_style as cds  # noqa: E402

def added(page):
    out = subprocess.run(["git", "-C", str(repo), "diff", "-U0", base, "HEAD", "--", page],
                         capture_output=True, text=True, check=True).stdout
    s = set()
    for m in re.finditer(r"^@@ -\S+ \+(\d+)(?:,(\d+))? @@", out, re.M):
        a, c = int(m.group(1)), int(m.group(2) if m.group(2) is not None else 1)
        s.update(range(a, a + c))
    return s

rc = 0
for page in pages:
    text = (repo / page).read_text(encoding="utf-8"); lines = text.splitlines(); add = added(page)
    blocks = [b for b in cds.prose_blocks(text) if b.line in add]
    words = [sum(len(cds.WORD.findall(s)) for s in cds.sentences(cds.normalized_prose(b.text))) for b in blocks if b.paragraph]
    finds = [f for f in cds.analyze(text) if f.line in add]
    print(f"{page}: {len(add)} added lines, {len(blocks)} added prose blocks, analyze() findings {len(finds)}")
    for f in finds[:10]:
        print(f"  {page}:{f.line}: {f.reason}")
    if words:
        print(f"  paragraph words: min {min(words)} max {max(words)} mean {sum(words)/len(words):.1f}; "
              f"{sum(1 for w in words if w < 20)} below 20, {sum(1 for w in words if w > 30)} above 30")
    cnt = collections.Counter(); dash = []
    for n in sorted(add):
        if n - 1 < len(lines):
            for ch in lines[n - 1]:
                if ord(ch) > 127:
                    cnt[ch] += 1
                    if 0x2010 <= ord(ch) <= 0x2015 or ord(ch) == 0x2212:
                        dash.append((n, unicodedata.name(ch, hex(ord(ch)))))
    print("  non-ASCII on added lines: " + (", ".join(f"U+{ord(c):04X} {unicodedata.name(c, '?')} x{k}" for c, k in cnt.most_common()) or "none"))
    for n, nm in dash:
        print(f"  DASH {page}:{n}: {nm}"); rc = 1
    if finds: rc = 1
sys.exit(rc)
