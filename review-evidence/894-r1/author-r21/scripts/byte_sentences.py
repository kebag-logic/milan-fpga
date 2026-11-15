# Copied unchanged but for this one-line provenance comment from the R837-15 review's packet (review-evidence/894-r1/reviews/R837-15/scripts/byte_sentences.py), by its reviewer; run here by the author (R837-15-S3).
#!/usr/bin/env python3
"""List every sentence of a line range of a Markdown file that states a byte count, an image size,
RAMB36/tiles, a granule or a spare, and mark whether it carries a present-tense verb and no history
marker. Usage: byte_sentences.py FILE FIRST LAST > out.tsv  (read-only; prints line.sentence, flag, text)."""
import re
import sys

path, first, last = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
lines = open(path, encoding="utf-8").read().split("\n")
FIG = re.compile(r"\b\d{1,3}(?:,\d{3})+ ?(?:B\b|bytes)|\b\d+ ?(?:B|bytes)\b|RAMB36|\btiles?\b|granule|spare|KiB|\bledger")
PRESENT = re.compile(r"\b(is|are|holds|hold|takes|take|needs|need|plans|fits|fit|grows|adds|add|leaves|stays|"
                     r"puts|gives|costs|keeps|carries|moves|links|reaches|remains|uses|has|have)\b")
HIST = re.compile(r"\b(was|were|then|before|had|added|took|grew|rose|fell|became|held|moved|cost|left|kept|"
                  r"at the merge of|at round|round \d+'s|at `[0-9a-f]{7,8}`)\b")
SPLIT = re.compile(r"(?<=[.;])\s+(?=[A-Z`(*\[])")
for n in range(first, min(last, len(lines)) + 1):
    text = lines[n - 1]
    for i, s in enumerate(SPLIT.split(text)):
        if not FIG.search(s):
            continue
        flag = "PRESENT-NOHIST" if PRESENT.search(s) and not HIST.search(s) else (
            "PRESENT+HIST" if PRESENT.search(s) else "OTHER")
        print(f"{n}.{i}\t{flag}\t{s}")
