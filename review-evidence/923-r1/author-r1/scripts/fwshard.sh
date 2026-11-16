#!/usr/bin/env bash
# fwshard.sh <clone> <k>: rtl-fast's firmware job for shard k/4 on a clone, as the workflow runs it (shard 0 adds the
# selftests, the saved-state store suites and the coverage ratchet); one rc per step at the end.
set -u
C=$1; K=$2; T=/data-2/milan/tmp/923-a789
. $T/env.sh
export HOME=$T/home-fw$K TMPDIR=$T/tmp/fw$K MAKEFLAGS="-j1 --no-print-directory"
mkdir -p "$HOME" "$TMPDIR"; [ -e "$HOME/br-milan-rv32" ] || ln -s $WORKSPACE_HOME/br-milan-rv32 "$HOME/br-milan-rv32"
cd "$C" || exit 3
echo "HEAD $(git rev-parse HEAD) shard $K start $(date +%T)"
rcs=""
step() { echo "== $* $(date +%T)"; "$@"; r=$?; echo "== rc=$r $(date +%T)"; rcs="$rcs $r"; }
if [ "$K" = 0 ]; then
  step python3 sw/firmware/gtest/tally_selftest.py
  step python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32
fi
step python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard "$K/4"
if [ "$K" = 0 ]; then
  step python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 4
  step python3 sw/firmware/gtest/fw_coverage.py --selftest
  step python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4
fi
echo "RCS$rcs DIRTY-after $(git status --porcelain --untracked-files=all | wc -l) end $(date +%T)"
for r in $rcs; do [ "$r" = 0 ] || exit 1; done
