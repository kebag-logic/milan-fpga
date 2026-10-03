#!/usr/bin/env bash
# Summarize <dir>/<case>/{rc,gate.log} as R449-1's SUMMARY.md table.
# Usage: summarize_faults.sh <dir> <case>...
d=$1; shift
echo "| case | rc | YOSYS OK | parses | FAIL lines (first 4) |"
echo "|---|---:|---:|---|---|"
for c in "$@"; do
  g="$d/$c/gate.log"
  ok=$(grep -c '^YOSYS OK ' "$g")
  ps=$(grep -oE 'parsed [0-9]+' "$g" | head -1)
  fl=$(grep -E '^YOSYS FAIL|^modules declared|^tops array|^  [A-Za-z_]|^sv2v:|^  error' "$g" | head -4 | cut -c1-140 | tr '\n' ';')
  echo "| $c | $(cat "$d/$c/rc") | $ok | $ps | $fl |"
done
