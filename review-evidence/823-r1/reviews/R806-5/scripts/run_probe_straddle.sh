#!/usr/bin/env bash
# run_probe_straddle.sh <clean clone at 7c97e99f with submodules> <scratch dir>
# Applies the reviewer probe (two disposable GoogleTest cases) to a COPY's
# test_nvm_journal.cpp and runs the store's suite at 1x1 and 8x8. Expected at
# 7c97e99f: P1 and P2 report class=1 (a mix of the work set) on both ports;
# the P1-uncut line is a control that reports class=2 (the store recovers).
set -u
SRC=$1; WORK=$2; HERE=$(cd "$(dirname "$0")" && pwd)
git clone -q --no-checkout "$SRC" "$WORK/probe" && cd "$WORK/probe" && git checkout -q 7c97e99f53ab0efc3e05e4617ee652dbab6e1b14 || exit 2
for d in gptp-processor protocol-processor third_party/tsn-c-stack third_party/lwSRP third_party/verilog-axis; do
  sha=$(git ls-tree HEAD "$d" | awk '{print $3}'); rmdir "$d" 2>/dev/null
  git clone -q --no-checkout "$SRC/$d" "$d" && git -C "$d" checkout -q "$sha" || exit 2
done
git apply "$HERE/probe_straddle.patch" || exit 2
TMPDIR=$WORK python3 -I sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --config configs/endstation_ax7101_1x1_tdm8.yaml \
  --config configs/endstation_ax7101_8x8.yaml --require-rv32 --jobs 8
# Cadence probe: instead apply probe_cadence.patch (it includes the straddle
# probes, two cadence probes and the rig's loop at PROBE_LOOP_US = 10,000 us,
# the shipped composition's one store step per fabric centisecond) and run the
# 1x1 config: P3/P4 report the figures; the bound binary's save_bound and
# commit_deadline fail. Other tests fail too because their timings assume 100 us.
