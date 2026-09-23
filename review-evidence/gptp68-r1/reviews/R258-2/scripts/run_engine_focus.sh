#!/bin/bash
# Focused engine-suite run on a pristine export of one revision.
# Usage: run_engine_focus.sh <clone> <rev> <workdir> <receipt> [run|mutants|both]
# Needs the pinned simulator first on PATH. Writes only under <workdir> and
# the receipt path; the clone is read through `git archive` alone.
set -euo pipefail
clone=$1; rev=$2; work=$3; receipt=$4; what=${5:-run}
rm -rf "$work"
mkdir -p "$work"
git -C "$clone" archive "$rev" | tar -x -C "$work"
cd "$work/tb/verilator/engine"
{
  echo "# engine suite, rev $(git -C "$clone" rev-parse "$rev"), $(date -u +%FT%TZ)"
  echo "# simulator: $(verilator --version) at $(command -v verilator)"
  echo "# image: $(sha256sum gptp_ucode.hex)"
} > "$receipt"
rc_run=skipped; rc_mut=skipped
if [ "$what" = run ] || [ "$what" = both ]; then
  set +e; make run >> "$receipt" 2>&1; rc_run=$?; set -e
fi
if [ "$what" = mutants ] || [ "$what" = both ]; then
  set +e; make mutants >> "$receipt" 2>&1; rc_mut=$?; set -e
fi
echo "# exit: run=$rc_run mutants=$rc_mut" >> "$receipt"
grep -E 'checks:|^# exit' "$receipt"
