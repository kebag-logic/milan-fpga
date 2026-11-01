#!/usr/bin/env python3
"""Measured input-port and output-port attribution against the page's field names."""
import json, re, sys
sys.path.insert(0, sys.argv[5])
page, rec, bitfile, portmap = sys.argv[1:5]
pm = json.load(open(portmap)); omap = pm["outputs"]
src = open(sys.argv[5] + "/compare_page.py").read()
regs, cur = [], None
for ln in open(page, encoding="utf-8"):
    m = re.match(r"^### (\S+) registers? \(offset (0x[0-9A-Fa-f]+)(?: to (0x[0-9A-Fa-f]+), stride (0x[0-9A-Fa-f]+))?\)\s*\[reset = ([^\]]+)\]", ln)
    if m:
        cur = dict(name=m.group(1), off=int(m.group(2),16), end=int(m.group(3),16) if m.group(3) else int(m.group(2),16), stride=int(m.group(4),16) if m.group(4) else 4, fields=[]); regs.append(cur); continue
    if ln.startswith("## ") or (ln.startswith("### ") and cur is not None): cur=None; continue
    if cur is None: continue
    m = re.match(r"^\| (\d+)(?::(\d+))? \| `([^`]+)` \| (\S+) \| ([^|]+?) \| (.*)\|\s*$", ln)
    if m and "`" not in m.group(4):
        hi=int(m.group(1)); lo=int(m.group(2)) if m.group(2) else hi
        cur["fields"].append(dict(hi=hi,lo=lo,name=m.group(3),access=m.group(4),reset=m.group(5),desc=m.group(6).strip()))
where={}
for r in regs:
    for a in range(r["off"], r["end"]+1, r["stride"]):
        for f in r["fields"]:
            for b in range(f["lo"],f["hi"]+1): where[(a,b)]=(r["name"],f)
def obit(i):
    for n,(p,w) in omap.items():
        if p<=i<p+w: return n,i-p
norm=lambda s: re.sub(r"[^a-z0-9]","",s.lower())
print("== input walk: port -> register bits it moves, page field name there")
seen={}
for ln in open(rec+"/sim_input.txt"):
    _,port,a,_,_,x=ln.split(); a=int(a,16); x=int(x.split("=")[1],16)
    for b in range(32):
        if x>>b&1:
            nm,f=where.get((a,b),("UNLISTED",dict(name="?",access="?",hi=b,lo=b)))
            seen.setdefault((port,a,nm,f["name"],f["access"],f["hi"],f["lo"]),[]).append(b)
for (port,a,nm,fn,ac,hi,lo),bs in seen.items():
    pn=norm(re.sub(r"^i_","",port)); ok=pn[:6] in norm(fn) or norm(fn)[:6] in pn
    print(("ok  " if ok else "DIFF"),port,f"0x{a:03X}",nm,fn,ac,f"[{hi}:{lo}]",f"bits {min(bs)}..{max(bs)} n={len(bs)}")
print("== write walk: register bit -> output ports it moves")
seen={}
for ln in open(bitfile):
    p=ln.split(); a=int(p[1],16); b=int(p[2]); o=[x for x in p[5].split("=")[1].split(",") if x]
    if not o: continue
    ports={}
    for x in o:
        n,i=obit(int(x)); ports.setdefault(n,[]).append(i)
    nm,f=where.get((a,b),("UNLISTED",dict(name="?",access="?",hi=b,lo=b,desc="")))
    seen.setdefault((a,nm,f["name"],f["access"],f["hi"],f["lo"]),[]).append((b,{k:(min(v),max(v)) for k,v in ports.items()}))
for (a,nm,fn,ac,hi,lo),rows in seen.items():
    allp=sorted({k for _,d in rows for k in d})
    print(f"0x{a:03X} {nm} {fn} {ac} [{hi}:{lo}] <- bits {rows[0][0]}..{rows[-1][0]} -> {allp}")
