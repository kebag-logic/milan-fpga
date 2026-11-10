#!/usr/bin/env bash
# run_probes.sh <clean-checkout-at-7c97e99f> <work-dir>
# Re-runs the reviewer's three disposable probes on a COPY of the tree:
#   probe_copy_misread         - one silent misread of the old slot's log during the compaction's copy
#   probe_powercut_first_base  - the store's own --powercut-compaction sweep, started from blank media
#   probe_powercut_torn_old    - the same sweep, started from a slot whose last delta is torn (torn_pad)
# The source checkout is never modified. Needs the submodules gptp-processor and
# protocol-processor checked out in the source, gtest/gmock and the host compiler.
set -euo pipefail
SRC=$(cd "$1" && pwd); WORK=$(mkdir -p "$2" && cd "$2" && pwd)
HERE=$(cd "$(dirname "$0")" && pwd)
TREE=$WORK/tree
rm -rf "$TREE"; mkdir -p "$TREE"
git -C "$SRC" archive HEAD | tar -x -C "$TREE"
for sm in gptp-processor protocol-processor; do
  git -C "$SRC/$sm" archive HEAD | tar -x -C "$TREE/$sm"
done
(cd "$TREE" && patch -p0 < "$HERE/../receipts/probes/probe_tests.diff")
(cd "$TREE" && git init -q . && git add -A)   # the suite lists files with git ls-files
for shape in endstation_arty_current endstation_ax7101_8x8; do
  (cd "$TREE" && python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --config "configs/$shape.yaml" \
     --jobs 4 --coverage "$WORK/cov-$shape" > "$WORK/build-$shape.log" 2>&1) || true
  D=$WORK/cov-$shape/shapes/$shape
  (cd "$D/suite" && NVM_FIXTURE="$D/fixture" ./nvm_suite --gtest_filter='*probe*' > "$WORK/probe-$shape.log" 2>&1) || true
  grep -E "POWERCUT|PROBE (first_base|torn_old):|differs|FAILED|PASSED" "$WORK/probe-$shape.log" || true
done
