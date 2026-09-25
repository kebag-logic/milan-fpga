#!/usr/bin/env python3
"""Compare comment-stripped KL_crf_rx.sv and list changed paths across commits.

Usage: rtl_identity.py <repo> <base> <mid> <head>
"""
import re
import subprocess
import sys

repo, base, mid, head = sys.argv[1:5]
PATH = "hdl/ieee1722/crf/KL_crf_rx.sv"


def blob(rev: str, path: str) -> str:
    return subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"],
                          check=True, capture_output=True, text=True).stdout


def strip(src: str) -> str:
    src = re.sub(r"/\*.*?\*/", "", src, flags=re.S)
    src = re.sub(r"//[^\n]*", "", src)
    return "\n".join(line.rstrip() for line in src.splitlines() if line.strip())


def changed(a: str, b: str) -> list[str]:
    out = subprocess.run(["git", "-C", repo, "diff", "--name-only", a, b],
                         check=True, capture_output=True, text=True).stdout
    return out.split()


rc = 0
for a, b in ((base, head), (mid, head), (base, mid)):
    same = strip(blob(a, PATH)) == strip(blob(b, PATH))
    raw = blob(a, PATH) == blob(b, PATH)
    print(f"{PATH} {a[:9]}..{b[:9]}: comment-stripped identical={same} raw identical={raw}")
    rc |= not same
for a, b in ((base, head), (mid, head)):
    files = changed(a, b)
    hdl = [f for f in files if f.startswith("hdl/")]
    print(f"changed {a[:9]}..{b[:9]}: {files}")
    print(f"  hdl paths changed: {hdl}")
print("RESULT:", "PASS" if rc == 0 else "FAIL")
sys.exit(rc)
