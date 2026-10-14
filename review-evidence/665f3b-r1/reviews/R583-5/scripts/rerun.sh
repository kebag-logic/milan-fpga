#!/bin/sh
# R583-5: the exact focused checks this round relied on, in the form they finally ran.
# Usage: rerun.sh <clone at 7032bca5, submodules at their gitlinks> <output dir>
# Needs: pinned Verilator 5.050 at $VERILATOR, the RV32 SDK at ~/br-milan-rv32/host,
# GoogleTest, and a Python with the pinned Markdown renderer as $MDPY for the two doc gates.
set -u
CLONE=$1; OUT=$2
: "${VERILATOR:=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator}"
: "${MDPY:=python3}"
export VERILATOR PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
mkdir -p "$OUT/tmp"; export TMPDIR=$OUT/tmp
cd "$CLONE" || exit 2
run() { name=$1; shift; "$@" >"$OUT/$name.log" 2>&1; echo $? >"$OUT/$name.rc"; echo "$name rc=$(cat "$OUT/$name.rc")"; }
# Merge shape and tree equality.
run merge_tree git merge-tree --write-tree 6b4feeca5d2fab0ec35cf071322cc775a5b15cb5 fa7347fc59173f90e4feec2df207692e6e6e72ec
git rev-parse HEAD^{tree} >>"$OUT/merge_tree.log"
# Classifier, CI contract, documentation gates.
run ci_scope_selftest python3 scripts/ci_scope.py --selftest
run ci_events_check python3 scripts/ci_events.py --check
run doc_style python3 scripts/check_doc_style.py
run doc_map python3 docs/DOC_MAP.gen.py --check
run em_dash "$MDPY" scripts/check_em_dash.py --base 6b4feeca5d2fab0ec35cf071322cc775a5b15cb5
run docs_check "$MDPY" scripts/docs_check.py
run gen_mailbox python3 sw/mailbox/gen_mailbox.py --check --crosscheck
# Where #696's differential meets this lane's stack pin.
run maap_differential python3 sw/firmware/ctrl/test/maap_differential.py --self-test --keep "$OUT/maapdiff"
# firmware-unit's first phase, as the hosted job runs it (includes the service-bounds arm).
run fw_shard0 python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 0/4 --build-dir "$OUT/fw0"
