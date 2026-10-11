#!/usr/bin/env bash
# Run a tree's own scripts/run_suites.sh, unchanged except that each suite's
# make log is copied to KEEP/<suite>.log before the script deletes it.
# Usage: run_keep_logs.sh TREE KEEPDIR OUT RCFILE [REQ_TAG_LOG]
# The stdout of the variant is the stdout run_suites.sh would print.
set -u
tree=$1; keep=$2; out=$3; rcf=$4; tag=${5:-}
mkdir -p "$keep"
runner="$tree/scripts/.run_keep_logs.sh"
sed "s|^  rm -f \"\$log\"\$|  cp \"\$log\" \"$keep/\$name.log\"; rm -f \"\$log\"|" \
  "$tree/scripts/run_suites.sh" > "$runner"
grep -q "cp \"\$log\"" "$runner" || { echo "runner patch did not apply"; echo 99 > "$rcf"; exit 99; }
chmod +x "$runner"
export PATH="${PINNED_VERILATOR_DIR:-$VALIDATION_TOOLS/pinned-verilator-5.050}:$PATH"
if [ -n "$tag" ]; then
  REQ_TAG_LOG="$tag" "$runner" > "$out" 2>&1; rc=$?
else
  env -u REQ_TAG_LOG "$runner" > "$out" 2>&1; rc=$?
fi
rm -f "$runner"
echo "$rc" > "$rcf"
exit "$rc"
