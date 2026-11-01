#!/usr/bin/env bash
# Both builder legs where every SoC-elaborating arm can run: round 1's interpreter and HOME. Adds to docs.yml's two legs.
set -u
H=$1; S=$VALIDATION_STORAGE/829-a725c; W=$S/gates/lane-wt; G=$S/gates/lane-logs
cd "$W" || exit 3
test "$(git rev-parse HEAD)" = "$H" || exit 4
export HOME=$WORKSPACE_HOME VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator TMPDIR=$S/tmp MAKEFLAGS="-j2 --no-print-directory" PYTHONHASHSEED=0 TSN_GEN_ROOT=$MANAGEMENT/tools/tsn-gen-deca300c
export PATH=$VALIDATION_STORAGE/sync-a723b/venv-docs/bin:$VALIDATION_STORAGE/scratch/a662/make43/bin:$VALIDATION_TOOLS/sv2v-v0.0.12:$VALIDATION_TOOLS/pinned-verilator-5.050:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin:$VALIDATION_TOOLS/clang-18/bin
for k in 0 1; do
  { echo "# head $H builder leg $k, round 1's environment"; python3 scripts/ci_builder_legs.py run $k --receipt $G/builder-leg$k-env1.json -- python3 sw/builder/test_builder.py --require-rv32; } > $G/builder_leg${k}_env1.log 2>&1
  echo $? > $G/builder_leg${k}_env1.rc
  echo "leg $k rc=$(cat $G/builder_leg${k}_env1.rc)"
done
git status --short > $G/tree-after-legs.txt
echo done > $G/LEGS_DONE
