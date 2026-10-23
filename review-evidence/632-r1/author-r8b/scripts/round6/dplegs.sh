#!/usr/bin/env bash
# milan_dp's legs one by one in a clean clone at the head (the timed notify leg
# fails its CRF-output steps 3 and 4 at the processor pin by ruling and its
# pool then starts no later leg, so each leg is built and run on its own), then
# the render controls (render_mutants.py, render-csr-controls) on the aclk
# build, then the notify leg at the pin. One Verilator build at a time.
# usage: dplegs.sh <clone> <case>...
set -u
here=$(cd "$(dirname "$0")" && pwd)
source "$here/env.sh"
export TSN_GEN_ROOT=$VALIDATION_STORAGE/scratch/632-a659/tsn-gen
L=$VALIDATION_STORAGE/scratch/632-a659/r6/camp/dplegs
mkdir -p "$L"
cd "$1/tb/verilator/milan_dp" || exit 2
shift
git rev-parse HEAD > "$L/HEAD.txt"
date -Is > "$L/start"
make --no-print-directory ci-prepare > "$L/ci_prepare.log" 2>&1; echo "ci-prepare rc=$?" >> "$L/summary.txt"
for c in "$@"; do
  s=$(date +%s)
  make --no-print-directory build-$c > "$L/build_$c.log" 2>&1; b=$?
  make --no-print-directory exec-$c > "$L/$c.log" 2>&1; r=$?
  t=$(grep -E 'checks: *[0-9]+ +failures: *[0-9]+|[0-9]+ checks, [0-9]+ failures' "$L/$c.log" | tail -1)
  echo "$c build=$b exec=$r $(( $(date +%s) - s ))s $t" >> "$L/summary.txt"
done
python3 render_mutants.py > "$L/render_mutants.log" 2>&1; echo "render_mutants rc=$?" >> "$L/summary.txt"
make --no-print-directory render-csr-controls > "$L/render_csr_controls.log" 2>&1; echo "render-csr-controls rc=$?" >> "$L/summary.txt"
make --no-print-directory run-notify > "$L/notify_pin.log" 2>&1; echo "run-notify rc=$?" >> "$L/summary.txt"
date -Is > "$L/end"
echo DONE >> "$L/summary.txt"
