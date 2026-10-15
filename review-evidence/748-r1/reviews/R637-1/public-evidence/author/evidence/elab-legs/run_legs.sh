#!/bin/bash
# Run both elaboration legs' driver concurrently, natively, each in the private
# venv the isolation control set up for it, from a clone at the head.
# Usage: run_legs.sh <control work dir> <rev> <out dir>
set -euo pipefail
WORK=$1; REV=$2; OUT=$3
LANE=$LANES/748-elab-race
mkdir -p "$OUT"
for sm in third_party/verilog-axis protocol-processor gptp-processor; do
  top=$(git -C "$LANE/$sm" rev-parse --show-toplevel)
  [ "$top" = "$LANE/$sm" ] || { echo "toplevel mismatch for $sm: $top" >&2; exit 2; }
done
TC_BIN=$(echo "$WORK"/toolcache/Python/*/x64/bin)
for leg in 0 1; do
  L="$WORK/elaborate-gates-$leg"; ws="$L/ws"
  if [ ! -d "$ws/.git" ]; then
    git clone -q --no-checkout "$LANE" "$ws"
    git -C "$ws" checkout -q --detach "$REV"
    for sm in third_party/verilog-axis protocol-processor gptp-processor; do
      git -C "$ws" submodule init "$sm" >/dev/null
      git -C "$ws" config "submodule.$sm.url" "$LANE/$sm"
      git -C "$ws" -c protocol.file.allow=always submodule update -q "$sm"
    done
  fi
  ln -sfn "$HOME/br-milan-rv32" "$L<home-path>"
  mkdir -p "$L/temp/gate-results"
done
run_leg() {
  leg=$1; L="$WORK/elaborate-gates-$leg"
  cpus=$(nproc)
  env -i HOME="$L/home" RUNNER_TEMP="$L/temp" LANG=C.UTF-8 TMPDIR="$L/temp" \
    PATH="$L/temp/litex-venv/bin:$TC_BIN:$VALIDATION_TOOLS/sv2v-v0.0.12:/usr/local/bin:/usr/bin:/bin" \
    PIP_CONSTRAINT="$L/ws/ci/constraints-ci.txt" \
    CI_BUILD_JOBS=$cpus CI_TOOL_BUILD_JOBS=$(( cpus < 8 ? cpus : 8 )) CI_CAMPAIGN_JOBS=$(( cpus < 4 ? cpus : 4 )) \
    VERILATOR_JOBS=$cpus SIM_JOBS=$(( cpus < 4 ? cpus : 4 )) MAKEFLAGS="-j1 --no-print-directory" \
    bash -c "cd '$L/ws' && command -v python3 && /usr/bin/time -f 'wall %e s maxrss %M KB' python3 scripts/ci_builder_legs.py run $leg --receipt \"\$RUNNER_TEMP/gate-results/builder-leg-$leg.json\" -- python3 sw/builder/test_builder.py --require-elaboration --require-rv32" \
    > "$OUT/leg-$leg.log" 2>&1
  echo $? > "$OUT/leg-$leg.rc"
}
date +%s > "$OUT/start"
run_leg 0 & p0=$!
run_leg 1 & p1=$!
wait $p0 $p1 || true
date +%s > "$OUT/end"
echo done > "$OUT/done"
