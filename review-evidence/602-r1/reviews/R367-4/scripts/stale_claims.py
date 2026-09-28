#!/usr/bin/env python3
"""List every line of the tracked tree (docs/history excluded) that puts a PHC
step / re-base / adjtime / settime within 160 characters of an mr toggle or
MEDIA_RESET count, for manual classification. Usage: stale_claims.py <repo>"""
import re
import subprocess
import sys

repo = sys.argv[1]
files = subprocess.run(["git", "-C", repo, "ls-files", "-z"], check=True,
                       capture_output=True).stdout.decode().split("\0")
step = r"(PHC[- ]?(only )?(step|re-?base)|media[_ ]re-?base|re-?base on a PHC|adjtime|settime|GM step|grandmaster step|step-only)"
effect = r"(toggl\w*|`?mr`?\b|MEDIA_RESET|mcr_restart)"
pat = re.compile(rf"{step}.{{0,160}}{effect}|{effect}.{{0,160}}{step}", re.I)
hits = 0
for path in files:
    if not path or path.startswith("docs/history/"):
        continue
    if not re.search(r"\.(md|sv|v|svh|py|cpp|hpp|h|c|txt|yml|yaml|sh|tcl|json)$|Makefile$", path):
        continue
    try:
        text = open(f"{repo}/{path}", encoding="utf-8").read()
    except (UnicodeDecodeError, IsADirectoryError, FileNotFoundError):
        continue
    for n, line in enumerate(text.splitlines(), 1):
        if pat.search(line):
            hits += 1
            print(f"{path}:{n}: {line.strip()[:260]}")
print(f"TOTAL {hits}", file=sys.stderr)
