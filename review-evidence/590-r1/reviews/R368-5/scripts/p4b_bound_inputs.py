#!/usr/bin/env python3
"""P4b: every source input whose recorded hash moved between the two merge-dev
packets must equal the exact bytes of this head (new) and of the previous merge
head 1f039cfe / processor 16be6768 (old). Run from the review clone.
Usage: p4b_bound_inputs.py <old receipt.json> <new receipt.json>"""
import hashlib, json, subprocess, sys
old = json.load(open(sys.argv[1])); new = json.load(open(sys.argv[2]))
def blob(rev, path):
    if path.startswith("protocol-processor/"):
        return subprocess.run(["git", "-C", "protocol-processor", "show", f"{rev[1]}:{path[19:]}"],
                              capture_output=True, check=True).stdout
    return subprocess.run(["git", "show", f"{rev[0]}:{path}"], capture_output=True, check=True).stdout
OLD = ("1f039cfe86d5337f5c9b7248696dba1c4bdda67e", "16be6768f710e79450aace277abacd6c2c3336e5")
NEW = ("4c2a30debb031595b81c5c4bfc53b601a0fec528", "c951a9ff0cb5851fb159d33e966e5a2a9a188fe3")
DEV = ("b5c0f69d5d11f0ec4bc847a2cfdd13e89e199a8a", "c951a9ff0cb5851fb159d33e966e5a2a9a188fe3")
for section in ("build_hashes", "input_hashes"):
    o, n = old.get(section, {}), new.get(section, {})
    print(f"[{section}] keys old={len(o)} new={len(n)} same-keyset={set(o)==set(n)}")
    for k in sorted(n):
        if o.get(k) == n[k]:
            continue
        if k.startswith("build/"):
            print(f"  GENERATED moved: {k}"); continue
        h = lambda rev: hashlib.sha256(blob(rev, k)).hexdigest()
        print(f"  SOURCE moved: {k}: new==head:{h(NEW)==n[k]} new==dev:{h(DEV)==n[k]} old==prev:{h(OLD)==o.get(k)}")
    for k in ("build/software/bios/bios.bin",):
        if k in n: print(f"  {k}: identical={o.get(k)==n.get(k)}")
