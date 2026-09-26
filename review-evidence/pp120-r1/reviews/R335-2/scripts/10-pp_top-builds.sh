#!/bin/sh
# Build and run both pp_top builds (default + PP_TOP_SRP_DOM_DEF_VID fixture)
# and the name-write-only scenario at one revision, from a pristine
# `git archive` export. Usage: 10-pp_top-builds.sh <donor-clone> <rev> <outdir>
# Environment: VERILATOR (pinned 5.050 shim), JOBS (default 8).
# The only deviation from the committed gate command is the Verilator build
# parallelism (-j $JOBS instead of -j 0), to respect the review job budget.
set -u
CLONE=$1; REV=$2; mkdir -p "$3"; OUT=$(cd "$3" && pwd)
JOBS=${JOBS:-8}
PKT=$(cd "$(dirname "$0")/.." && pwd)
TREE=$PKT/scratch/trees/$REV
rm -rf "$TREE"; mkdir -p "$TREE" "$OUT"
git -C "$CLONE" archive "$REV" | tar -x -C "$TREE"
cd "$TREE/tb/pp_top" || exit 2
VF="--cc --exe --build -j $JOBS --top-module pp_top_wrap -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM"
# committed VFLAGS minus -CFLAGS, which the Makefile appends identically
grep -q 'CFLAGS "-std=c++17 -O2 -I$(CURDIR) -Wall -Wextra"' Makefile || { echo "Makefile VFLAGS drifted"; exit 2; }
make run VERILATOR="$VERILATOR" VFLAGS="$VF -CFLAGS \"-std=c++17 -O2 -I$TREE/tb/pp_top -Wall -Wextra\"" \
  > "$OUT/run.log" 2>&1
echo "make run rc=$?" >> "$OUT/run.log"
make name-writes VERILATOR="$VERILATOR" VFLAGS="$VF -CFLAGS \"-std=c++17 -O2 -I$TREE/tb/pp_top -Wall -Wextra\"" \
  > "$OUT/name-writes.log" 2>&1
echo "make name-writes rc=$?" >> "$OUT/name-writes.log"
{
  echo "rev $REV"
  echo "C++ compiler warnings (run.log):   $(grep -c 'warning:' "$OUT/run.log")"
  echo "Verilator %Warning (run.log):      $(grep -c '%Warning' "$OUT/run.log")"
  echo "unused-function mentions:          $(grep -c 'Wunused-function' "$OUT/run.log")"
  grep -n 'warning:' "$OUT/run.log" | sed "s#$PKT#<packet>#g"
  grep -E '^\[build |checks: .* PASS|NW: |rc=' "$OUT/run.log" "$OUT/name-writes.log" | sed "s#$OUT/##"
} > "$OUT/summary.txt"
sed -i "s#$PKT#<packet>#g; s#$HOME#~#g" "$OUT/run.log" "$OUT/name-writes.log"
cat "$OUT/summary.txt"
