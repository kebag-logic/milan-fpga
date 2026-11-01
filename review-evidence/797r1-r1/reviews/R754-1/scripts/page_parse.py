#!/usr/bin/env python3
"""Parse the published page's register sections, independent of the generator's model."""
import re
def parse(path):
    regs, cur = [], None
    for ln in open(path, encoding="utf-8"):
        m = re.match(r"^### (\S+) register \(offset (0x[0-9A-Fa-f]+)(.*?)\)\s*\[reset = ([^\]]+)\]", ln)
        if m:
            cur = dict(name=m.group(1), off=int(m.group(2), 16), extra=m.group(3), reset=m.group(4), fields=[], text="")
            regs.append(cur); continue
        if ln.startswith("## ") or (ln.startswith("### ") and cur is not None and " register (offset" not in ln):
            cur = None; continue
        if cur is None: continue
        cur["text"] += ln
        m = re.match(r"^\| (\d+)(?::(\d+))? \| `([^`]+)` \| (\S+) \| (\S+) \| (.*)\|\s*$", ln)
        if m:
            hi = int(m.group(1)); lo = int(m.group(2)) if m.group(2) else hi
            cur["fields"].append(dict(hi=hi, lo=lo, name=m.group(3), access=m.group(4), reset=m.group(5), desc=m.group(6).strip()))
    return regs
if __name__ == "__main__":
    import sys
    regs = parse(sys.argv[1])
    print(len(regs), sum(len(r["fields"]) for r in regs))
    for r in regs:
        bits = sorted(b for f in r["fields"] for b in range(f["lo"], f["hi"]+1))
        if bits != list(range(32)):
            print("NOT32", r["name"], hex(r["off"]), len(bits))
        if r["extra"]: print("extra", r["name"], hex(r["off"]), r["extra"], r["reset"])
