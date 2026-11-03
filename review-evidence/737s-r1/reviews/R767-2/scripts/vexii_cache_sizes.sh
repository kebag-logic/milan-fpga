#!/usr/bin/env bash
# For each saved hosted job log given, print the CPU-metadata cache events
# (restore hit / miss / save / save refused) and the archive byte count the
# action logged within eight lines before each event. 200-202 bytes is an
# empty ~/vexii-netlist-args. Prints the sha256 of each log so a reader can
# re-fetch it (gh api --allow-escape-sequences repos/OWNER/REPO/actions/jobs/ID/logs).
set -euo pipefail
for f in "$@"; do
  printf '%s sha256=%s ' "$(basename "$f")" "$(sha256sum < "$f" | cut -d' ' -f1)"
  grep -nE 'elaborate-vexii' "$f" | grep -E 'restored from|not found|saved with|reserve' | while IFS=: read -r ln rest; do
    kind=$(printf '%s' "$rest" | grep -oE 'restored from|not found|saved with|reserve')
    size=$(sed -n "$(( ln > 8 ? ln - 8 : 1 )),${ln}p" "$f" | grep -oE '(Cache Size: ~[0-9]+ MB \([0-9]+ B\)|Sent [0-9]+ of [0-9]+)' | tail -1 || true)
    printf '[%s %s] ' "$kind" "$size"
  done
  echo
done
