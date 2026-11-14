#!/usr/bin/env python3
"""resolve_hunks.py FILE SPEC.json: replace each merge-conflict hunk (default merge style) of FILE by the
resolution SPEC names for it, by index from 1: "ours", "theirs", or {"text": "..."} (verbatim lines). Every hunk must
be named; a leftover marker refuses. Prints one line a hunk: its index, its choice, the lines written."""
import json
import re
import sys

path, spec = sys.argv[1], json.load(open(sys.argv[2]))
text = open(path).read()
pat = re.compile(r"^<<<<<<< [^\n]*\n(.*?)^=======\n(.*?)^>>>>>>> [^\n]*\n", re.S | re.M)
hunks = list(pat.finditer(text))
if len(hunks) != len(spec):
    sys.exit(f"REFUSED: {len(hunks)} hunks in {path}, {len(spec)} resolutions")
out, last = [], 0
for n, (m, choice) in enumerate(zip(hunks, spec), 1):
    out.append(text[last:m.start()])
    if choice == "ours":
        body = m.group(1)
    elif choice == "theirs":
        body = m.group(2)
    else:
        body = choice["text"]
        if not body.endswith("\n"):
            body += "\n"
    out.append(body)
    last = m.end()
    print(f"{path} hunk {n}: {choice if isinstance(choice, str) else 'composed'}, {body.count(chr(10))} lines")
out.append(text[last:])
res = "".join(out)
if re.search(r"^(<<<<<<<|=======$|>>>>>>>|\|\|\|\|\|\|\| )", res, re.M):
    sys.exit("REFUSED: markers remain")
open(path, "w").write(res)
