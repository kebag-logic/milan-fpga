#!/usr/bin/env python3
"""Check the rx_mac_filter.sv change is comment-only and no anchor depends on it.

Usage (from the reviewed tree): rtl_comment_only.py <old-rev> <new-rev>
1. Strip // and /* */ comments from both revisions and compare the code bytes,
   and compare line counts (line-number anchors stay valid only if equal).
2. Search every tracked file for each removed and added comment line's text
   (exact-text anchors: tb patches, mutant tables, planting scripts) and for
   references to the file with a line number inside the edited span.
"""
import re
import subprocess
import sys

OLD, NEW = sys.argv[1], sys.argv[2]
PATH = "hdl/ieee8021q/filtering/rx_mac_filter.sv"


def show(rev):
    return subprocess.run(["git", "show", f"{rev}:{PATH}"], capture_output=True,
                          text=True, check=True).stdout


def strip(src):
    src = re.sub(r"/\*.*?\*/", "", src, flags=re.S)
    return "\n".join(re.sub(r"//.*", "", l).rstrip() for l in src.splitlines())


old, new = show(OLD), show(NEW)
print(f"lines: {OLD[:8]}={len(old.splitlines())} {NEW[:8]}={len(new.splitlines())}")
print(f"code bytes identical after comment strip: {strip(old) == strip(new)}")
ol, nl = old.splitlines(), new.splitlines()
changed = [i for i in range(max(len(ol), len(nl)))
           if i >= len(ol) or i >= len(nl) or ol[i] != nl[i]]
print(f"changed line numbers (1-based): {[i + 1 for i in changed]}")
files = subprocess.run(["git", "ls-files"], capture_output=True, text=True,
                       check=True).stdout.split()
texts = {}
for f in files:
    if f == PATH:
        continue
    try:
        with open(f, encoding="utf-8") as h:
            texts[f] = h.read()
    except (UnicodeDecodeError, IsADirectoryError, FileNotFoundError):
        pass
hits = 0
for i in changed:
    for side, lines in (("removed", ol), ("added", nl)):
        if i < len(lines):
            frag = lines[i].strip().lstrip("/").strip()
            if len(frag) < 12:
                continue
            for f, t in texts.items():
                if frag in t:
                    hits += 1
                    print(f"  TEXT HIT ({side} line {i + 1}) in {f}: {frag[:80]}")
span = {i + 1 for i in changed}
ref = re.compile(r"rx_mac_filter\.sv:(\d+)")
for f, t in texts.items():
    for m in ref.finditer(t):
        if int(m.group(1)) in span:
            hits += 1
            print(f"  LINE-NUMBER HIT in {f}: {m.group(0)}")
patches = [f for f in files if f.endswith(".patch")]
print(f"patch files scanned: {len(patches)}; "
      f"patches naming rx_mac_filter: {[p for p in patches if 'rx_mac_filter' in texts.get(p, '')]}")
print(f"anchor hits on the edited span: {hits}")
