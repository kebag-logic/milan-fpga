#!/usr/bin/env bash
# usage: devsuites.sh <dev-root> <suite...>   run each suite's default make in a scratch copy
D="$1"; shift
export PATH=<scratch>/bin:$PATH TMPDIR=<scratch>/tmpdir
for s in "$@"; do st=$(date +%s); (cd "$D/tb/$s" && make) > "$D/$s.log" 2>&1; echo "$s rc=$? secs=$(( $(date +%s) - st ))" >> "$D/suites.rc"; done
echo done >> "$D/suites.rc"
