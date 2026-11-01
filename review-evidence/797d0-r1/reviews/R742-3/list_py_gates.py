#!/usr/bin/env python3
"""Print each pure-Python gate command a workflow template runs, one per line, for a local replay."""
import re, sys
seen = []
for name in sys.argv[1:]:
    text = open(name, encoding="utf-8").read().split("\n")
    i = 0
    while i < len(text):
        m = re.match(r"\s*(?:- )?run: (.*)$", text[i])
        if m:
            indent = len(text[i]) - len(text[i].lstrip())
            body = []
            if m.group(1).strip() in ("|", ">"):
                i += 1
                while i < len(text) and (not text[i].strip() or len(text[i]) - len(text[i].lstrip()) > indent):
                    body.append(text[i].strip()); i += 1
            else:
                body = [m.group(1).strip()]; i += 1
            for line in body:
                if re.match(r"python3 (scripts|sw|docs|tests|avdecc|tools)/\S+\.py(\s+--[\w-]+)*\s*$", line) and line not in seen:
                    seen.append(line)
            continue
        i += 1
print("\n".join(seen))
