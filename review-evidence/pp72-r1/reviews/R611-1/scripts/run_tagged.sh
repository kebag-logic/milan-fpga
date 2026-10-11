#!/usr/bin/env bash
# The CI suites step at a tree, unmodified: REQ_TAG_LOG=<fresh file>
# scripts/run_suites.sh | tee OUT, then the gate's executed half on that run.
# Usage: run_tagged.sh TREE OUTDIR
set -u -o pipefail
tree=$1; od=$2
mkdir -p "$od"; rm -f "$od/req-tags.txt"
export PATH="${PINNED_VERILATOR_DIR:-$VALIDATION_TOOLS/pinned-verilator-5.050}:$PATH"
verilator --version > "$od/verilator-version.txt"
(cd "$tree" && REQ_TAG_LOG="$od/req-tags.txt" ./scripts/run_suites.sh) > "$od/suites.txt" 2>&1
echo $? > "$od/suites.rc"
(cd "$tree" && python3 scripts/check-req-tags.py --suites "$od/suites.txt" --evidence "$od/req-tags.txt") \
  > "$od/executed.txt" 2>&1
echo $? > "$od/executed.rc"
