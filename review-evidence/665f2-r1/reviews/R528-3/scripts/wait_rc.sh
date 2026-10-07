#!/usr/bin/env bash
# Usage: wait_rc.sh SECONDS RCFILE...  - poll until every rc file exists or the time runs out.
deadline=$(( $(date +%s) + $1 )); shift
while :; do
    missing=0
    for f in "$@"; do [ -f "$f" ] || missing=1; done
    [ $missing = 0 ] && break
    [ "$(date +%s)" -ge $deadline ] && break
    read -r -t 15 < /dev/zero 2>/dev/null || true
    perl -e 'select(undef,undef,undef,15)'
done
for f in "$@"; do printf '%s: %s\n' "$f" "$(cat "$f" 2>/dev/null || echo PENDING)"; done
