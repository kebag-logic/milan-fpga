#!/usr/bin/env bash
# Build adp.c with --coverage once per scenario and print, for each of the
# five adp.c exclusion statements, its arcs (gcov order) as taken counts and
# the stray line's count. Usage: adp_reentry_r3.sh <clone> <outdir>
set -eu
C=$1; O=$2; S=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$O"
src=$C/sw/firmware/ctrl/adp/adp.c
for sc in A1 A2 B1 B2 C1 C2; do
  d=$O/$sc; rm -rf "$d"; mkdir -p "$d"; cd "$d"
  inc="-I$C/sw/firmware/ctrl/adp -I$C/sw/firmware/ctrl/wire"
  gcc -std=c11 -O0 --coverage $inc -c "$src" -o adp.o
  gcc -std=c11 -O0 $inc -c "$S/adp_reentry_r3.c" -o probe_main.o
  gcc --coverage -o probe adp.o probe_main.o
  ./probe $sc
  gcov -b -c -o adp.o "$src" > gcov.out 2>&1
  g=$(ls *adp.c.gcov | head -1)
  python3 - "$g" "$sc" <<'PY'
import sys, re
lines = open(sys.argv[1]).read().splitlines()
frags = {"row1": "if (a->state == ADP_STATE_DOWN) {", "row2": "if (a->state != ADP_STATE_DOWN) {",
         "row3": "if (a->state == ADP_STATE_DELAY && kind == ADP_TIMER_DELAY) {",
         "row4": "} else if (a->state == ADP_STATE_WAITING && kind == ADP_TIMER_ADVERTISE) {",
         "row5": "if (a->enabled && a->state == ADP_STATE_DELAY) {"}
out = []
for row, frag in frags.items():
    for i, l in enumerate(lines):
        if l.rstrip().endswith(frag) and "    " in l:
            arcs = []
            j = i + 1
            while j < len(lines) and lines[j].startswith(("branch", "call", "unconditional")):
                m = re.match(r"branch\s+\d+ taken (\d+)", lines[j])
                if m: arcs.append(int(m.group(1)))
                elif lines[j].startswith("branch"): arcs.append(0)
                j += 1
            taken = [k + 1 for k, n in enumerate(arcs) if n]
            out.append(f"{row}@{l.split(':')[1].strip()}: arcs taken {taken} of {len(arcs)}")
for frag, name in (("a->stray_expiries++;", "stray"), ("a->available_owed = false;", "owed_clear")):
    for l in lines:
        if l.rstrip().endswith(frag):
            out.append(f"{name}@{l.split(':')[1].strip()}={l.split(':')[0].strip()}")
print(sys.argv[2], "|", "; ".join(out))
PY
done
