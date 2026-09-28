#!/usr/bin/env bash
# Declaration-before-use check of KL_acmp_talker at a revision: a static scan
# (every logic declared at module scope vs its first textual use). Usage:
#   forward_ref_check.sh SRC_CLONE REV SCRATCH
set -uo pipefail
src=$1; rev=$2; scratch=$3; t="$scratch/fwd-${rev:0:8}"; rm -rf "$t"; mkdir -p "$t"
git -C "$src" archive "$rev" hdl/acmp/KL_acmp_talker.sv | tar -x -C "$t"
echo "rev $(git -C "$src" rev-parse "$rev")"
python3 - "$t/hdl/acmp/KL_acmp_talker.sv" <<'PY'
import re, sys
lines = open(sys.argv[1]).read().split("\n")
code = [re.sub(r"//.*", "", l) for l in lines]
decl = {}
for i, l in enumerate(code, 1):
    m = re.match(r"\s*logic\b(?:\s*\[[^\]]*\])*\s*(.*?);", l)
    if m and "(" not in m.group(1):
        for name in re.findall(r"\b([A-Za-z_]\w*)\b(?:\s*\[[^\]]*\])*\s*(?:,|$)", m.group(1)):
            decl.setdefault(name, i)
found = 0
for name, d in sorted(decl.items(), key=lambda x: x[1]):
    for i, l in enumerate(code[:d - 1], 1):
        if re.search(rf"\b{name}\b", l):
            print(f"USED BEFORE DECLARATION: {name} used at line {i}, declared at line {d}")
            found += 1
            break
print(f"forward references: {found}")
PY
rm -rf "$t"
