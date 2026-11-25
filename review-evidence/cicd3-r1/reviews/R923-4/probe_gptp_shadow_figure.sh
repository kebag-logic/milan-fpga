#!/bin/sh
# Disposable probe: set gptp_shadow's SUITE_SECONDS figure to a measured hosted window
# and run the dealer's own self-test, then restore the exact tracked bytes.
# Usage: probe_gptp_shadow_figure.sh CHECKOUT SECONDS
set -u
cd "$1" || exit 2
f=scripts/suite_shards.py
grep -q '^    "gptp_shadow": 393,$' "$f" || { echo "anchor missing"; exit 2; }
sed -i "s/^    \"gptp_shadow\": 393,\$/    \"gptp_shadow\": $2,/" "$f"
python3 "$f" --selftest > /tmp/probe_selftest.$$ 2>&1; rc=$?
echo "figure=$2 selftest rc=$rc"; grep -i "exceeds\|budget\|FAIL\|problem" /tmp/probe_selftest.$$ | head -8
for i in $(seq 0 25); do printf '%s: ' "$i"; python3 "$f" --suite-root tb/verilator --ci-pieces --shard "$i/26" | tr '\n' ' '; echo; done | grep -n gptp_shadow
git checkout -- "$f"; rm -f /tmp/probe_selftest.$$
git diff --quiet -- "$f" && echo "restored $f"
