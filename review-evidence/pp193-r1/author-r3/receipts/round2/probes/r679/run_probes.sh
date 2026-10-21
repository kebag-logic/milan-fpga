#!/bin/sh
# Re-run the R679-1 parked-Leave probes (issue #193) against a processor clone.
# Usage: run_probes.sh <clone> <revision> <outdir>
# Needs a simulator 5.050 as `verilator` on PATH (the CI pin). Exports the
# revision with `git archive` into <outdir>/tree-*, never touching <clone>.
# Each probe's build/run status is written to <outdir>/<name>.rc; the probes
# are EXPECTED to fail (rc 2) while the defect is present.
set -eu
clone=$1; rev=$2; out=$3
here=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$out"
for name in fsm wire; do
  t="$out/tree-$name"; rm -rf "$t"; mkdir -p "$t"
  git -C "$clone" archive "$rev" hdl tb | tar -x -C "$t"
done
python3 -I "$here/probe_parked_leave.py" "$out/tree-fsm"
python3 -I "$here/probe_parked_leave_wire.py" "$out/tree-wire"
set +e
(cd "$out/tree-fsm/tb/srp_stream_fsms" && make RUN_ARGS=suite) > "$out/fsm.log" 2>&1
echo $? > "$out/fsm.rc"
(cd "$out/tree-wire/tb/srp_top" && make RUN_ARGS=share) > "$out/wire.log" 2>&1
echo $? > "$out/wire.rc"
grep -E "^PROBE|^FAIL: P|checks:" "$out/fsm.log" "$out/wire.log"
