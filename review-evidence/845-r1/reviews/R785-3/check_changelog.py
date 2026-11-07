#!/usr/bin/env python3
"""Check a merged CHANGELOG keeps both sides' sections whole and its contents list matches."""
import re, subprocess, sys
repo, head, ours, theirs = sys.argv[1:5]
def show(rev): return subprocess.run(["git","-C",repo,"show",f"{rev}:CHANGELOG.md"],capture_output=True,text=True,check=True).stdout
def sections(t):
    out, cur = {}, None
    for ln in t.splitlines():
        if ln.startswith("## "): cur = ln[3:]; out[cur] = []
        elif cur: out[cur].append(ln)
    return {k:"\n".join(v).strip("\n") for k,v in out.items()}
def slug(h): return re.sub(r"[^a-z0-9 _-]","",h.lower()).replace(" ","-")
H, O, T = show(head), show(ours), show(theirs)
sh, so, st = sections(H), sections(O), sections(T)
ok = True
for name, src in (("847 side",so),("849 side",st)):
    for k,v in src.items():
        if k == "Contents": continue
        if k not in sh: print(f"MISSING {name}: {k}"); ok=False
        elif sh[k] != v: print(f"ALTERED {name}: {k}"); ok=False
extra = [k for k in sh if k not in so and k not in st]
print("extra sections:", extra)
heads = [k for k in sh if k != "Contents"]
order = list(sh.keys())
i847 = order.index("Unreleased - processor pin 92100657"); i849 = order.index("Unreleased - station MAC from reset")
print("847 before 849:", i847 < i849, "adjacent:", i849 == i847+1)
toc = re.findall(r"^- \*\*\[(.+?)\]\(#(.+?)\)\*\*", H.split("## Contents",1)[1].split("\n## ",1)[0], re.M)
print("toc entries:", len(toc), "sections:", len(heads))
if [t for t,_ in toc] != heads: print("TOC TITLE/ORDER MISMATCH"); ok=False
for t,a in toc:
    if slug(t) != a: print("ANCHOR MISMATCH", t, a); ok=False
print("RESULT", "PASS" if ok else "FAIL")
