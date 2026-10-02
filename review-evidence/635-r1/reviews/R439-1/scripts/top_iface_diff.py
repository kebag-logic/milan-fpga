#!/usr/bin/env python3
"""List protocol_processor_top's header parameters and ports at two processor
commits and print the difference. Usage: top_iface_diff.py <pp-repo> <old> <new>"""
import re, subprocess, sys

def header(repo, rev):
    src = subprocess.run(["git", "-C", repo, "show", f"{rev}:hdl/top/protocol_processor_top.sv"],
                         check=True, capture_output=True, text=True).stdout
    src = re.sub(r"//[^\n]*", "", src)
    src = re.sub(r"/\*.*?\*/", "", src, flags=re.S)
    m = re.search(r"\bmodule\s+protocol_processor_top\b(.*?)\)\s*;", src, re.S)
    hdr = src[m.start():]
    # header ends at the first ');' that closes the port list: find 'module ... #( ... ) ( ... );'
    depth = 0; end = None; started = False
    for i, ch in enumerate(hdr):
        if ch == '(':
            depth += 1; started = True
        elif ch == ')':
            depth -= 1
            if started and depth == 0 and hdr[i+1:].lstrip().startswith(';'):
                end = i; break
    hdr = hdr[:end]
    params = {}
    for pm in re.finditer(r"\b(parameter|localparam)\b([^=;,]*?)\b(\w+)\s*=", hdr):
        params[pm.group(3)] = (pm.group(1) + pm.group(2)).split()
    ports = {}
    for pt in re.finditer(r"\b(input|output|inout)\b([^,;()]*?)\b(\w+)\s*(?=,|$)", hdr, re.M):
        ports[pt.group(3)] = " ".join((pt.group(1) + " " + pt.group(2)).split())
    return params, ports

repo, old, new = sys.argv[1:4]
po, qo = header(repo, old)
pn, qn = header(repo, new)
print(f"old {old}: {len(po)} parameters, {len(qo)} ports")
print(f"new {new}: {len(pn)} parameters, {len(qn)} ports")
for k in sorted(set(po) | set(pn)):
    if k not in po: print(f"+param {k} {' '.join(pn[k])}")
    elif k not in pn: print(f"-param {k}")
    elif po[k] != pn[k]: print(f"~param {k} {po[k]} -> {pn[k]}")
for k in sorted(set(qo) | set(qn)):
    if k not in qo: print(f"+port {k}: {qn[k]}")
    elif k not in qn: print(f"-port {k}: {qo[k]}")
    elif qo[k] != qn[k]: print(f"~port {k}: {qo[k]} -> {qn[k]}")
