#!/usr/bin/env bash
# Mirror the hosted firmware-unit job's captured steps (.github/workflows/rtl-fast.yml at the head) on this
# host: every firmware command the job runs, each under ctrl_capture.py. The two mutation shards of the
# control-plane gate together run what its single --self-test run does; each command gets its own capture
# directory (ctrl_boundary.py --capture is repeatable) so concurrent runs never rewrite each other's wrappers.
# usage: hosted_capture.sh <checkout> <out dir>     (source env.sh first)
set -u
repo=$1 out=$2
mkdir -p "$out"
cap() {  # cap <name> <command...>
  local name=$1; shift
  (cd "$repo" && python3 sw/firmware/ctrl/test/ctrl_capture.py --out "$out/cap-$name" -- "$@") > "$out/$name.log" 2>&1
  echo $? > "$out/$name.rc"
}
cap rv32 python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32 &
for i in 0 1; do
  cap fw$i python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 \
      --mutation-shard $i 2 &
done
cap nvm python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 4 &
wait
cap covself python3 sw/firmware/gtest/fw_coverage.py --selftest &
cap covcheck python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4 &
wait
grep -H . "$out"/*.rc
