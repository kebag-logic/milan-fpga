#!/usr/bin/env bash
# Poll a run_gates.sh output directory for at most <seconds>, then print every rc.
OUT=$1 LIMIT=${2:-540}
end=$((SECONDS + LIMIT))
while [ ! -e "$OUT/ALL.done" ] && [ $SECONDS -lt $end ]; do sleep 10; done
[ -e "$OUT/ALL.done" ] && echo "ALL done" || echo "still running"
for f in "$OUT"/*.rc; do [ -e "$f" ] && printf '%s %s\n' "$(basename "$f" .rc)" "$(cat "$f")"; done
