#!/usr/bin/env bash
# Interrupt the candidate installer's whole process group at a chosen delay,
# then show that a rerun refuses the partial prefix without repairing it.
# Usage: probe_interrupt.sh <clone> <archive> <prefix-root> <delay-seconds>
set -uo pipefail
clone=$1 archive=$2 root=$3 delay=$4
dest="$root/host"
mkdir -p "$root"
[ ! -e "$dest" ] || { echo "refusing: $dest exists"; exit 2; }
cd "$clone" || exit 2
setsid python3 scripts/ci_rv32_sdk.py --destination "$dest" --archive "$archive" \
  > "$root/interrupted-run.log" 2>&1 &
pid=$!
sleep "$delay"
kill -KILL -- "-$pid" 2>/dev/null
wait "$pid"
echo "interrupted-exit=$? after ${delay}s (process group SIGKILL)"
sleep 1
echo "remaining processes in group: $(pgrep -g "$pid" | wc -l)"
echo "prefix exists: $([ -e "$dest" ] && echo yes || echo no)"
echo "receipt exists: $([ -e "$dest/.milan-rv32-sdk.json" ] && echo yes || echo no)"
echo "sdk-location: $(cat "$dest/share/buildroot/sdk-location" 2>/dev/null || echo absent)"
before=$(find "$dest" 2>/dev/null | wc -l)
echo "entries before rerun: $before"
python3 scripts/ci_rv32_sdk.py --destination "$dest" --archive "$archive" > "$root/rerun.log" 2>&1
echo "rerun-exit=$?"
tail -n 1 "$root/rerun.log"
grep -c '^SDK argv' "$root/rerun.log" | sed 's/^/rerun tool executions: /'
echo "entries after rerun: $(find "$dest" 2>/dev/null | wc -l)"
