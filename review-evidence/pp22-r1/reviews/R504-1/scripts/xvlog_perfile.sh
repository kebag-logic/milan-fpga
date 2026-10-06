#!/usr/bin/env bash
# Per-file Vivado analysis (xvlog -sv) of the processor's derived source list.
# usage: xvlog_perfile.sh <tree> <list-file> <outdir> [define ...]
# One fresh work directory per run; the list is read in order (packages first),
# one xvlog invocation per file, as the parent's xvlog gate does. Writes
# <outdir>/<n>.log per file and <outdir>/table.tsv:
#   path  rc  count(VRFC 10-3380)  count(VRFC 10-8530)  identifiers(10-3380)
set -uo pipefail
tree=$(readlink -f "$1"); list=$(readlink -f "$2"); out=$(readlink -f -m "$3"); shift 3
XVLOG=${XVLOG:-$HOME/Xilinx/2026.1/Vivado/bin/xvlog}
defs=(); for d in "$@"; do defs+=(-d "$d"); done
rm -rf "$out"; mkdir -p "$out/work"
printf 'path\trc\tvrfc_10_3380\tvrfc_10_8530\tidentifiers\n' > "$out/table.tsv"
n=0
while IFS= read -r rel; do
  [ -n "$rel" ] || continue
  n=$((n + 1)); log="$out/$(printf '%02d' "$n").log"
  rc=0; (cd "$out/work" && "$XVLOG" -sv --work work "${defs[@]}" "$tree/$rel") >"$log" 2>&1 || rc=$?
  e1=$(grep -c 'VRFC 10-3380' "$log" || true)
  e2=$(grep -c 'VRFC 10-8530' "$log" || true)
  ids=$(grep 'VRFC 10-3380' "$log" | grep -oE "identifier '[^']+'" | sed "s/identifier //; s/'//g" | sort -u | paste -sd, -)
  printf '%s\t%s\t%s\t%s\t%s\n' "$rel" "$rc" "$e1" "$e2" "${ids:--}" >> "$out/table.tsv"
done < "$list"
awk -F'\t' 'NR>1 {f++; if ($2!=0) r++; a+=$3; b+=$4} END {printf "files=%d nonzero_rc=%d vrfc_10_3380=%d vrfc_10_8530=%d\n", f, r+0, a, b}' "$out/table.tsv" | tee "$out/summary.txt"
