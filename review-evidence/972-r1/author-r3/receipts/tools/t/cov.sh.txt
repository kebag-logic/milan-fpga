#!/bin/bash
# cov.sh CLONE: fw_coverage.py --selftest, then --check --jobs 4 (rtl-fast.yml's two commands) on CLONE.
cd "$1" || exit 3
echo "HEAD $(git rev-parse --short=8 HEAD) dirty $(git status --porcelain --untracked-files=no | wc -l) start $(date +%T)"
python3 sw/firmware/gtest/fw_coverage.py --selftest; a=$?; echo "== selftest rc=$a $(date +%T)"
python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4; b=$?; echo "== check rc=$b $(date +%T)"
[ $a = 0 ] && [ $b = 0 ]; rc=$?; echo "END rc=$rc $(date +%T)"; exit $rc
