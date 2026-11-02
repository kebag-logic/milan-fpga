#!/usr/bin/env bash
# behave and both builder legs, one log and one rc each, never piped, in the clean clone with real dependency origins.
set -u
H=d4d8cff92658e57b11090c97daf7b44edb31b3b6; W=$VALIDATION_STORAGE/833-a726/gates/wt-final; O=$MANAGEMENT/2026-09-23/833-a726/receipts/gates/lane
cd "$W" || exit 3
test "$(git rev-parse HEAD)" = "$H" || exit 4
export HOME=$WORKSPACE_HOME VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator TMPDIR=$VALIDATION_STORAGE/833-a726/gates/tmp MAKEFLAGS="-j4 --no-print-directory" PYTHONHASHSEED=0 TSN_GEN_ROOT=$MANAGEMENT/tools/tsn-gen-deca300c
export PATH=$VALIDATION_STORAGE/sync-a723b/venv-docs/bin:$VALIDATION_STORAGE/scratch/a662/make43/bin:$VALIDATION_TOOLS/sv2v-v0.0.12:$VALIDATION_TOOLS/pinned-verilator-5.050:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin:$VALIDATION_TOOLS/clang-18/bin
run() { id=$1; shift; { echo "# head $H gate $id: $*"; bash -c "$*"; } > "$O/$id.log" 2>&1; rc=$?; echo $rc > "$O/$id.rc"; echo "$id rc=$rc"; }
run diffcheck "git diff --check 1f29f189279f9fc0132f4918e47342b87d22f33a HEAD"
run behave "cd tests && behave --no-capture -f plain"
run builder_leg0 "python3 scripts/ci_builder_legs.py run 0 --receipt $O/builder-leg0.json -- python3 sw/builder/test_builder.py --require-rv32"
run builder_leg1 "python3 scripts/ci_builder_legs.py run 1 --receipt $O/builder-leg1.json -- python3 sw/builder/test_builder.py --require-rv32"
git status --short > "$O/tree-after.txt"
echo done > "$O/DONE"
