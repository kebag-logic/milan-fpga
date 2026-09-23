#!/usr/bin/env bash
# Run a list of focused commands against a clone, at most JOBS in parallel,
# keeping each command's combined output and exit status as a receipt.
# usage: run_bank.sh <clone> <commands-file> <receipt-dir> [jobs<=8]
# commands-file: one "<id>|<shell command>" per line; '#' lines ignored.
set -euo pipefail
clone="$(cd "$1" && pwd)"; list="$(cd "$(dirname "$2")" && pwd)/$(basename "$2")"
out="$3"; jobs="${4:-8}"
[ "$jobs" -le 8 ] || { echo "at most 8 jobs" >&2; exit 2; }
mkdir -p "$out"; out="$(cd "$out" && pwd)"
one() {
  local id="${1%%|*}" cmd="${1#*|}" start rc
  start="$(date +%s)"
  rc=0
  ( cd "$CLONE" && bash -c "$cmd" ) > "$OUT/$id.out" 2>&1 || rc=$?
  printf 'id=%s\nexit=%s\nseconds=%s\ncwd=%s\ncommand=%s\n' \
    "$id" "$rc" "$(( $(date +%s) - start ))" "$CLONE" "$cmd" > "$OUT/$id.rc"
}
export -f one
export CLONE="$clone" OUT="$out"
grep -v '^\s*#' "$list" | grep -v '^\s*$' | tr '\n' '\0' | xargs -0 -P "$jobs" -I{} bash -c 'one "$@"' _ {}
{
  printf '%-34s %5s %6s  %s\n' id exit secs command
  for rc in "$out"/*.rc; do
    # shellcheck disable=SC1090
    id="$(sed -n 's/^id=//p' "$rc")"; ex="$(sed -n 's/^exit=//p' "$rc")"
    s="$(sed -n 's/^seconds=//p' "$rc")"; c="$(sed -n 's/^command=//p' "$rc")"
    printf '%-34s %5s %6s  %s\n' "$id" "$ex" "$s" "$c"
  done
} | tee "$out/SUMMARY.txt"
