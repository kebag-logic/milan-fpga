#!/usr/bin/env bash
# Usage: run_gate.sh <clone> <receipt-name> <command...>
# Runs one gate in the clone with the pinned Verilator first on PATH and
# records the command, the tool identity, the full output and the exit code.
set -u
clone=$1; name=$2; shift 2
out="$(dirname "$0")/receipts/$name.log"
PIN=${PIN_BIN:?set PIN_BIN to the directory holding the pinned verilator}
export PATH="$PIN:$PATH"
{
  echo "# gate: $name"
  echo "# head: $(git -C "$clone" rev-parse HEAD)"
  echo "# verilator: $(verilator --version)"
  echo "# cmd: $*"
  echo "# start: $(date -u +%FT%TZ)"
} > "$out"
( cd "$clone" && "$@" ) >> "$out" 2>&1
rc=$?
{ echo "# end: $(date -u +%FT%TZ)"; echo "# rc=$rc"; } >> "$out"
echo "$name rc=$rc"
exit $rc
