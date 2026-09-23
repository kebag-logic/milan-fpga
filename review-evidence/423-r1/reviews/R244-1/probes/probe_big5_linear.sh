#!/bin/sh
# Linear stranded work on a Big5-lossy filename: pr edits b"\xa1\xfe.txt";
# main never receives it and gains unrelated work. Correct verdict: STRANDED/1.
# Usage: probe_big5_linear.sh <workdir>   (builds fixture with raw plumbing)
set -eu
W=$1; rm -rf "$W"; mkdir -p "$W"; cd "$W"
export GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null
g() { git -c user.name=F -c user.email=f@example.invalid "$@"; }
g init -q -b main
old=$(printf 'old\n' | g hash-object -w --stdin); new=$(printf 'new\n' | g hash-object -w --stdin)
t0=$(printf '100644 blob %s\t\241\376.txt\0' "$old" | g mktree -z)
t1=$(printf '100644 blob %s\t\241\376.txt\0' "$new" | g mktree -z)
t2=$(printf '100644 blob %s\t\241\376.txt\000100644 blob %s\tother\0' "$old" "$new" | g mktree -z)
o=$(g commit-tree "$t0" -m O); p=$(g commit-tree "$t1" -p "$o" -m 'pr edits lossy name')
m=$(g commit-tree "$t2" -p "$o" -m 'unrelated main work')
g update-ref refs/heads/pr "$p"; g update-ref refs/heads/main "$m"
