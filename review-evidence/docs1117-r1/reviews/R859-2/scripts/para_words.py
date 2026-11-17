#!/usr/bin/env python3
"""Word count of every paragraph or bullet that contains a line added in BASE..HEAD.
Usage: para_words.py <repo> <base> <head> <file>..."""
import subprocess, sys, re
repo, base, head, *files = sys.argv[1:]
for f in files:
    diff = subprocess.run(["git","-C",repo,"diff","-U0",base,head,"--",f],capture_output=True,text=True).stdout
    added=set()
    for m in re.finditer(r"^@@ -\S+ \+(\d+)(?:,(\d+))? @@",diff,re.M):
        s=int(m.group(1)); n=int(m.group(2) or 1)
        added.update(range(s,s+n))
    lines=subprocess.run(["git","-C",repo,"show",f"{head}:{f}"],capture_output=True,text=True).stdout.split("\n")
    blocks=[];cur=[];fence=False
    for i,l in enumerate(lines,1):
        if l.startswith("```"): fence=not fence; 
        if fence or l.startswith("```"):
            if cur: blocks.append(cur);cur=[]
            continue
        if not l.strip():
            if cur: blocks.append(cur);cur=[]
            continue
        if re.match(r"\s*([-*]|\d+\.)\s",l) and cur:
            blocks.append(cur);cur=[]
        cur.append((i,l))
    if cur: blocks.append(cur)
    for b in blocks:
        if any(i in added for i,_ in b):
            text=" ".join(l for _,l in b)
            text=re.sub(r"\]\([^)]*\)","]",text)
            w=len(re.findall(r"[^\s]+",re.sub(r"^\s*([-*]|\d+\.)\s","",text)))
            kind="bullet" if re.match(r"\s*([-*]|\d+\.)\s",b[0][1]) else "para"
            print(f"{f}:{b[0][0]}-{b[-1][0]} {kind} {w}")
