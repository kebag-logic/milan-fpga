#!/usr/bin/env bash
# Usage: run_step.sh <receipt-name> <workdir> <command...>
# Runs one command in the foreground from <workdir>, with the scoped pinned
# Verilator first on PATH, and writes receipts/<receipt-name>.log carrying the
# exact head, tool identity, command, full output, exit status and wall clock.
set -u
PKT=${PKT:-$REVIEWS/545-r301-3-packet}
TOOLBIN=${TOOLBIN:?set TOOLBIN to the directory holding the pinned Verilator 5.050}
name=$1; wd=$2; shift 2
log="$PKT/receipts/$name.log"
export PATH="$TOOLBIN:$PATH"
export VERILATOR="$TOOLBIN/verilator"
{
  echo "# receipt: $name"
  echo "# date: $(date -u +%FT%TZ)"
  echo "# head: $(git -C "$wd" rev-parse HEAD 2>/dev/null)"
  echo "# workdir: $wd"
  echo "# verilator: $(verilator --version 2>&1)"
  echo "# command: $*"
  echo "# ----"
} > "$log"
start=$(date +%s.%N)
( cd "$wd" && "$@" ) >> "$log" 2>&1
rc=$?
end=$(date +%s.%N)
printf '# ----\n# rc: %s\n# wall_s: %.3f\n' "$rc" "$(echo "$end - $start" | bc)" >> "$log"
tail -n 3 "$log"
exit $rc
