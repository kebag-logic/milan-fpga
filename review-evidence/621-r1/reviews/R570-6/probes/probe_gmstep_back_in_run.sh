#!/usr/bin/env bash
# Disposable probe: re-add the GM-step leg as a prerequisite of milan_dp's
# `run`, require test_sim_pool.py to fail, then restore the exact head bytes.
set -u
repo=$1
mk=$repo/tb/verilator/milan_dp/Makefile
sed -i 's/^\(run: .* gptp gptp-lat\)$/\1 gmstep/' "$mk"
git -C "$repo" --no-pager diff --stat -- "$mk"
git -C "$repo" diff --quiet -- "$mk" && { echo "PROBE NOT PLANTED"; exit 3; }
timeout 580 python3 -I "$repo/tb/verilator/milan_dp/test_sim_pool.py" > /tmp/r570_6_probe.$$ 2>&1
rc=$?
grep -E '^\[FAIL\]|checks:' /tmp/r570_6_probe.$$; rm -f /tmp/r570_6_probe.$$
git -C "$repo" checkout -- "$mk"
git -C "$repo" diff --quiet -- "$mk" && echo "restored"
echo "test rc with plant: $rc (non-zero = caught)"
[ "$rc" -ne 0 ]
