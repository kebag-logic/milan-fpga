#!/usr/bin/env bash
# Reviewer control for the campaign count contract: in a disposable clone at the head, make the generator
# emit COUNT+DELTA in every campaign command, regenerate the workflows, and require the contract and the
# generator self-test to refuse it by name; then restore and require both to pass.
# Usage: probe_count.sh PROBE_CLONE DELTA
set -u
cd "$1" || exit 2
export PYTHONDONTWRITEBYTECODE=1
delta=$2
sed -i "s/+ str(count) + \"\\\\n\")/+ str(count + ($delta)) + \"\\\\n\")/" scripts/ci_fast_legs.py
git diff --stat
python3 scripts/ci_gate_workflows.py >/dev/null 2>&1; echo "regenerate rc=$?"
grep -n -- '--campaign-shard' .github/workflows/rtl-fast.yml | sed 's/.*--shard/--shard/'
python3 scripts/ci_events.py --check > ev.out 2>&1; echo "planted ci_events --check rc=$?"
grep -c 'must run its campaign once' ev.out; grep 'must run its campaign once' ev.out | cut -c1-220
python3 scripts/ci_fast_legs_selftest.py > fl.out 2>&1; echo "planted ci_fast_legs_selftest rc=$?"; tail -2 fl.out | cut -c1-220
git checkout -q -- scripts/ci_fast_legs.py .github/workflows; rm -f ev.out fl.out
python3 scripts/ci_events.py --check >/dev/null 2>&1; echo "restored ci_events --check rc=$?"
git status --porcelain | wc -l
