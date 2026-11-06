#!/usr/bin/env python3
"""Compare every sha256-bearing command-table / exec-audit path against the exact-head bytes of the round's changed files."""
import hashlib, json, subprocess, sys
changed = subprocess.check_output(["git","diff","--name-only",sys.argv[1],sys.argv[2]],text=True).split()
def blob(rev,p):
    r = subprocess.run(["git","show",f"{rev}:{p}"],capture_output=True)
    return hashlib.sha256(r.stdout).hexdigest() if r.returncode==0 else None
def walk(o,path=()):
    if isinstance(o,dict):
        for k,v in o.items():
            yield from walk(v,path+(k,))
        if any(isinstance(v,str) and len(v)==64 for v in o.values()):
            yield ("row",path,o)
    elif isinstance(o,list):
        for i,v in enumerate(o):
            yield from walk(v,path+(i,))
for table in ("ci/image/command-table.json","ci/image/exec-audit-receipt.json","ci/image/tool-inventory.json"):
    data=json.load(open(table)); text=json.dumps(data)
    print("==",table,"bytes",len(text))
    for f in changed:
        print(" ",f,"mentions",text.count(f), "head",blob(sys.argv[2],f)[:12],"base",blob(sys.argv[1],f)[:12],
              "head_digest_present",blob(sys.argv[2],f) in text,"base_digest_present",blob(sys.argv[1],f) in text)
