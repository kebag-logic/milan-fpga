#!/usr/bin/env bash
# Run each gate command (one per line of CMDS) in LANE; one log per command and a TSV summary in OUT.
set -u
lane="$1"; out="$2"; cmds="$3"
mkdir -p "$out"
cd "$lane" || exit 2
export PATH="${GATE_VENV:?set GATE_VENV to the venv holding the pinned tools}/bin:$PATH"
summary="$out/summary.tsv"
: > "$summary"
n=0
while IFS= read -r cmd; do
  [ -z "$cmd" ] && continue
  n=$((n + 1))
  log="$out/$(printf '%03d' "$n").log"
  printf '$ %s\n' "$cmd" > "$log"
  start=$(date +%s)
  bash -c "$cmd" >> "$log" 2>&1 < /dev/null
  rc=$?
  end=$(date +%s)
  printf '%03d\t%s\t%ss\t%s\n' "$n" "$rc" "$((end - start))" "$cmd" >> "$summary"
done < "$cmds"
