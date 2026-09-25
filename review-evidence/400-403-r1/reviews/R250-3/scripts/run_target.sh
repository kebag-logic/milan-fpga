#!/bin/sh
# Run one make target in a checkout and record exit status and wall clock.
# Usage: run_target.sh <checkout> <receipt-file> <make args...>
# Environment: TOOLBIN (optional) is prepended to PATH so `verilator` and
# `python3` resolve to the identified tools recorded in 00-tool-identity.txt.
set -u
repo=$1; out=$2; shift 2
[ -n "${TOOLBIN:-}" ] && PATH="$TOOLBIN:$PATH" && export PATH
{
  echo "# repo: $repo"
  echo "# head: $(git -C "$repo" rev-parse HEAD)"
  echo "# command: make $*"
  echo "# verilator: $(verilator --version)"
  echo "# start: $(date -Is)"
} > "$out"
t0=$(date +%s.%N)
make -C "$repo" "$@" >> "$out" 2>&1
rc=$?
t1=$(date +%s.%N)
{
  echo "# end: $(date -Is)"
  printf '# wall_seconds: %.3f\n' "$(echo "$t1 - $t0" | bc)"
  echo "# exit: $rc"
} >> "$out"
tail -n 3 "$out"
exit $rc
