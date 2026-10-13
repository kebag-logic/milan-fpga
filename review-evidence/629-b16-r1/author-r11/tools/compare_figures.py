#!/usr/bin/env python3
"""Compare source and candidate receipts after normalizing only page line locators."""
import json
from pathlib import Path
import re
import sys
root=Path(sys.argv[1])
checks={}
for kind,col in [("rows",1),("coverage",0)]:
    text=(root/("cand-"+kind+".tsv")).read_text()
    out=[]
    for line in text.splitlines(True):
        if line.startswith("#") or not line.strip(): out.append(line); continue
        fields=line.split("\t")
        m=re.fullmatch(r"((?:629_MEDIA_CLOCK_FOLLOWING_BENCH\.md:)?)(\d+)",fields[col])
        if m:fields[col]=m[1]+str(int(m[2])-7)
        out.append("\t".join(fields))
    normalized="".join(out)
    checks[kind]=normalized==(root/("src-"+kind+".tsv")).read_text()
checks["stdout"]=(root/"src.stdout").read_bytes()==(root/"cand.stdout").read_bytes()
(root/"normalized-comparison.json").write_text(json.dumps(checks,indent=1)+"\n")
print(json.dumps(checks))
assert all(checks.values())
