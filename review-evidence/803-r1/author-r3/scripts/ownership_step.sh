#!/usr/bin/env bash
# #803 round 3, item 3: the verilator-shards job's "Prove specialized suite ownership" step body, literally, for
# every worker of the matrix (SHARD 0..18 of 19), at the lane's merge head, then each worker's owned list kept.
# usage: ownership_step.sh
set -u
R=$MANAGEMENT/2026-09-23/803-a693c/receipts/shards/ownership
RUNNER_TEMP=$VALIDATION_STORAGE/scratch/803-a693c/runner-temp
mkdir -p "$R" "$RUNNER_TEMP"
# The driver's process-ownership preflight needs os.pidfd_open, which the standalone CPython 3.12.3 build here
# lacks (the hosted image's system python3 has it), so the step runs on the host's system python3, as the sweep
# units do; the planner self-test is also run under CPython 3.12.3 first.
export PATH=$VALIDATION_STORAGE/scratch/a662/make43/bin:$PATH
export RUNNER_TEMP
cd $LANES/803-adopt-gptp || exit 2
git rev-parse HEAD > "$R/head.txt"
python3 --version > "$R/python.txt"
: > "$R/summary.txt"
$VALIDATION_STORAGE/scratch/a662/ci312/bin/python3 scripts/suite_shards.py --selftest > "$R/selftest-cpython-3.12.3.log" 2>&1
echo "suite_shards.py --selftest under CPython 3.12.3 rc=$?" >> "$R/summary.txt"
SHARDS=19
fails=0
for SHARD in $(seq 0 $((SHARDS - 1))); do
  export SHARD SHARDS
  bash -c '
          set -euo pipefail
          python3 scripts/suite_shards.py --selftest
          scripts/run_all_suites.sh --ci-pieces --shard "$SHARD/$SHARDS" --list \
            > "$RUNNER_TEMP/owned-suites"
          echo "Shard $SHARD owns:"
          sed "s/^/  /" "$RUNNER_TEMP/owned-suites"
          case "$SHARD" in
            1) grep -Fx tsn_fuzz "$RUNNER_TEMP/owned-suites" ;;
            3) grep -Fx chmap_capture "$RUNNER_TEMP/owned-suites" ;;
          esac
  ' > "$R/shard-$SHARD.log" 2>&1
  rc=$?
  [ "$rc" -eq 0 ] || fails=$((fails + 1))
  echo "shard $SHARD/$SHARDS rc=$rc owned=$(grep -c '^  ' "$R/shard-$SHARD.log")" >> "$R/summary.txt"
done
echo "failed shards: $fails" >> "$R/summary.txt"
cat "$R/summary.txt"
[ "$fails" -eq 0 ]
