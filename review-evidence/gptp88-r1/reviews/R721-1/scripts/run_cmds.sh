#!/bin/bash
# usage: run_cmds.sh <outdir> <cwd> <cmdfile>; each line of cmdfile is one command,
# run with bash -c in <cwd>; NN.log per command, results.tsv "NN<TAB>rc<TAB>seconds<TAB>command"
out="$1"; cwd="$2"; cmds="$3"; mkdir -p "$out"; : > "$out/results.tsv"
n=0
while IFS= read -r c; do
  [ -z "$c" ] && continue; case "$c" in \#*) continue;; esac
  n=$((n+1)); nn=$(printf %02d $n); t0=$(date +%s.%N)
  ( cd "$cwd" && bash -c "$c" ) > "$out/$nn.log" 2>&1; rc=$?
  t1=$(date +%s.%N); printf '%s\t%s\t%.1f\t%s\n' "$nn" "$rc" "$(echo "$t1 - $t0" | bc)" "$c" >> "$out/results.tsv"
done < "$cmds"
echo done > "$out/complete"
