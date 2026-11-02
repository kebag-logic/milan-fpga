#!/usr/bin/env python3
"""Compare the page's field tables with measured reset, write-readback and output activity."""
import json, re, sys
page, rec, bitfile, portmap = sys.argv[1:5]
omap = json.load(open(portmap))["outputs"]
imap = json.load(open(portmap))["inputs"]
def obit(i):
    for n, (p, w) in omap.items():
        if p <= i < p + w: return f"{n}[{i-p}]"
regs, cur = [], None
for ln in open(page, encoding="utf-8"):
    m = re.match(r"^### (\S+) registers? \(offset (0x[0-9A-Fa-f]+)(?: to (0x[0-9A-Fa-f]+), stride (0x[0-9A-Fa-f]+))?\)\s*\[reset = ([^\]]+)\]", ln)
    if m:
        cur = dict(name=m.group(1), off=int(m.group(2),16), end=int(m.group(3),16) if m.group(3) else int(m.group(2),16),
                   stride=int(m.group(4),16) if m.group(4) else 4, reset=m.group(5), fields=[], table={})
        regs.append(cur); continue
    if ln.startswith("## ") or (ln.startswith("### ") and cur is not None): cur=None; continue
    if cur is None: continue
    m = re.match(r"^\| (\d+)(?::(\d+))? \| `([^`]+)` \| (\S+) \| ([^|]+?) \| (.*)\|\s*$", ln)
    if m:
        hi=int(m.group(1)); lo=int(m.group(2)) if m.group(2) else hi
        cur["fields"].append(dict(hi=hi,lo=lo,name=m.group(3),access=m.group(4),reset=m.group(5),desc=m.group(6).strip()))
    m = re.match(r"^\| (\d+) \| `(0x[0-9A-F]+)` \| `(0x[0-9A-F]+)` \|", ln)
    if m: cur["table"][int(m.group(2),16)] = int(m.group(3),16)
rst0, rst1, word, bits = {}, {}, {}, {}
for ln in open(rec + "/sim_reset.txt"):
    _, pat, a, v, ok = ln.split(); (rst1 if pat=="1" else rst0)[int(a,16)] = int(v,16)
for ln in open(rec + "/sim_word.txt"):
    p = ln.split(); a=int(p[1],16); word[a] = {k:int(x.split("=")[1],0) for k,x in zip("rst w1 w0 wp ok".split(), p[2:])}
for ln in open(bitfile):
    p = ln.split(); a=int(p[1],16); b=int(p[2]); o=p[5].split("=")[1]
    bits.setdefault(a,{})[b] = dict(r0=int(p[3].split("=")[1],0), rb=int(p[4].split("=")[1],0), out=[obit(int(x)) for x in o.split(",") if x])
out=[]; covered=set(); nfield=nchk=0
def mask(f): return ((1<<(f["hi"]-f["lo"]+1))-1)<<f["lo"]
for r in regs:
    for a in range(r["off"], r["end"]+1, r["stride"]):
        covered.add(a)
        for f in r["fields"]:
            nfield+=1; m=mask(f); acc=f["access"]; lo=f["lo"]; name=f"{r['name']}@{a:03X}[{f['hi']}:{lo}] {f['name']} {acc} rst={f['reset']}"
            hw0=(rst0[a]&m)>>lo; hw1=(rst1[a]&m)>>lo
            # reset
            if f["reset"]=="X" or "X" in f["reset"]:
                if hw0==hw1 and "X" in f["reset"]: out.append(("X-NOT-INPUT",name,f"hw0={hw0:#x} hw1={hw1:#x}"))
            elif f["reset"]=="see table":
                if a in r["table"]:
                    if rst0[a]!=r["table"][a]: out.append(("RESET-TABLE",name,f"hw={rst0[a]:#x} page={r['table'][a]:#x}"))
            else:
                
                if "`" in f["reset"]: continue
                v=int(f["reset"].rstrip("h") or "0",16)
                if hw0!=v: out.append(("RESET",name,f"hw={hw0:#x} page={v:#x}"))
                if hw1!=v: out.append(("RESET-INPUT-DEP",name,f"hw_in1={hw1:#x} page={v:#x}"))
            # writes: stored bits observable by readback; per-bit write to a fresh reset
            for b in range(lo,f["hi"]+1):
                nchk+=1
                bit=bits[a][b]; rb=(bit["rb"]>>b)&1; r0=(bit["r0"]>>b)&1
                others=(bit["rb"]^bit["r0"])&~(1<<b)
                moved=bit["out"]
                w1=(word[a]["w1"]>>b)&1; w0=(word[a]["w0"]>>b)&1
                tag=f"{name} bit{b}"
                if acc=="R":
                    if rb!=r0 or w1!=w0: out.append(("R-BUT-WRITABLE",tag,f"r0={r0} rb={rb} w1={w1} w0={w0}"))
                    if moved: out.append(("R-BUT-OUTPUT",tag,str(moved[:6])))
                elif acc=="R/W":
                    if not (w1==1 and w0==0) : out.append(("RW-NOT-STORED",tag,f"w1={w1} w0={w0} rb={rb}"))
                elif acc=="W":
                    if w1 or w0: out.append(("W-BUT-READS",tag,f"w1={w1} w0={w0}"))
                    if not moved: out.append(("W-NO-EFFECT",tag,""))
                elif acc=="W1S":
                    if w1 or w0: out.append(("W1S-BUT-READS",tag,f"w1={w1} w0={w0}"))
                    if not moved: out.append(("W1S-NO-EFFECT",tag,""))
                elif acc in("R/W1S","R/W1C","W1C"):
                    pass
                else:
                    out.append(("UNKNOWN-ACCESS",tag,""))
        # undocumented side effects: a field listed R whose write moves other bits handled above
# addresses not on the page
un=[]
for a in sorted(word):
    if a in covered: continue
    w=word[a]
    moved=[(b,bits[a][b]["out"][:3]) for b in range(32) if bits[a][b]["out"]]
    if any(w[k] for k in("rst","w1","w0","wp")) or moved or rst1[a]:
        un.append((f"{a:03X}",{k:hex(w[k]) for k in("rst","w1","w0","wp")},hex(rst1[a]),moved[:2]))
print("registers",len(regs),"words",len(covered),"field-instances",nfield,"bit-checks",nchk)
from collections import Counter
print(Counter(k for k,_,_ in out))
for k,n,d in out: print(k,"|",n,"|",d)
print("UNLISTED ADDRESSES WITH ACTIVITY",len(un))
for u in un: print(u)
