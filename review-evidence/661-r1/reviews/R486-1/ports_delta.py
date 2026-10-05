#!/usr/bin/env python3
"""Compare protocol_processor_top's parameter and port headers between two processor commits.

Run from the protocol-processor checkout: ports_delta.py <old-rev> <new-rev>.
"""
import re, subprocess, sys

def header(rev):
    src = subprocess.run(["git", "show", f"{rev}:hdl/top/protocol_processor_top.sv"],
                         capture_output=True, text=True, check=True).stdout
    src = re.sub(r"//[^\n]*", "", src)
    start = src.index("module protocol_processor_top")
    split = src.index(") (", start)
    end = src.index(");", split)
    params = re.findall(r"\bparameter\b[^=;]*?(\w+)\s*=", src[start:split])
    ports = re.findall(r"\b(input|output|inout)\b\s+(?:wire|logic|reg)?\s*(?:signed\s*)?((?:\[[^\]]*\]\s*)*)(\w+)",
                       src[split:end])
    return params, {p[2]: (p[0], re.sub(r"\s", "", p[1])) for p in ports}

a, b = sys.argv[1], sys.argv[2]
pa, qa = header(a)
pb, qb = header(b)
print(f"params {a[:8]}: {len(pa)}  {b[:8]}: {len(pb)}")
print("params added:", sorted(set(pb) - set(pa)), "removed:", sorted(set(pa) - set(pb)))
print(f"ports {a[:8]}: {len(qa)}  {b[:8]}: {len(qb)}")
print("ports added:", sorted(set(qb) - set(qa)), "removed:", sorted(set(qa) - set(qb)))
print("ports changed:", sorted(k for k in qa if k in qb and qa[k] != qb[k]))
