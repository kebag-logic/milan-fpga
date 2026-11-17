#!/bin/sh
# Disposable probe of finding R861-F1: apply probe_record_across_sleep.patch to a clean clone at
# 7cfb8a0499941e56682f0c2f63326d120f5b7d9e, build the firmware suites, and run the App probe on both interface shapes.
# usage: run_probe.sh <clean clone> <build dir>
set -eu
CLONE=$1; BUILD=$2; HERE=$(cd "$(dirname "$0")" && pwd)
git -C "$CLONE" apply "$HERE/probe_record_across_sleep.patch"
(cd "$CLONE" && python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --build-only --build-dir "$BUILD" --jobs 4)
for v in if1 if2; do
  "$BUILD/checkout/aecp-mailbox-endstation_ax7101_1x1_tdm8-$v/suite" \
    --gtest_filter='App.ReviewProbe*:App.SrpDeclarationChange*'
done
