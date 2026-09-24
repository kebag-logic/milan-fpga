#!/bin/sh
# Build the engine harness at two commits with an identical, disposable
# instrumentation of expect() that logs every check (ordinal, name, got, exp),
# run the three shipping passes (plain, request seed, Sync seed) and diff.
# Usage: probe_checklist.sh <repo> <scratch> <verilator> <old-rev> <new-rev>
set -eu
REPO=$1; SCR=$2; VERILATOR=$3; OLD=$4; NEW=$5
GENARGS="--clk-hz 2000000 --cease-ms 3000"
for tag in old new; do
  rev=$OLD; [ "$tag" = new ] && rev=$NEW
  d=$SCR/checklist-$tag; rm -rf "$d"; mkdir -p "$d"
  git -C "$REPO" archive "$rev" | tar -x -C "$d"
  e=$d/tb/verilator/engine
  # probe: print every check; the original FAIL/tally output is untouched
  python3 - "$e/sim_main.cpp" <<'PY'
import sys, pathlib
p = pathlib.Path(sys.argv[1]); s = p.read_text()
old = "  void expect(const char *what, uint64_t got, uint64_t exp) {\n    checks++;\n"
assert s.count(old) == 1, "expect() anchor moved"
s = s.replace(old, old + '    printf("CHECK %d %s got %016llx exp %016llx\\n", checks, what,'
              ' static_cast<unsigned long long>(got), static_cast<unsigned long long>(exp));\n')
p.write_text(s)
PY
  ( cd "$e"
    python3 ../../../hdl/ucode/gen_gptp_ucode.py $GENARGS -o regen.hex >/dev/null
    cmp regen.hex gptp_ucode.hex && echo "committed image matches generator" > run.log
    rc=0; make -s VERILATOR="$VERILATOR" run >> run.log 2>&1 || rc=$?
    echo "make rc=$rc" >> run.log )
done
