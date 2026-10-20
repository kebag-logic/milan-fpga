#!/bin/bash
# Run each milan_dp case in a clone; one log and rc per case.
export PATH=<tools>/pinned-verilator-5.050:<tools>/sv2v-v0.0.12:$PATH
export VERILATOR=<tools>/pinned-verilator-5.050/verilator VERILATOR_JOBS=2
export TMPDIR=<scratch>/round1c/tmp
CL=$1; OUT=$2; shift 2
mkdir -p "$OUT"
cd "$CL/tb/verilator/milan_dp"
make --no-print-directory ci-prepare > "$OUT/ci-prepare.log" 2>&1; echo "rc=$?" > "$OUT/ci-prepare.rc"
for c in "$@"; do
  date -Is > "$OUT/$c.start"
  make --no-print-directory run-$c > "$OUT/$c.log" 2>&1
  echo "rc=$?" > "$OUT/$c.rc"
done
echo done > "$OUT/ALL.done"
