#!/usr/bin/env bash
# Run the resource gate's self-test, its shipped mutant campaign and a 20,000-case fixture --fuzz at seed 234 on
# each round-6 commit and on round 5's head, each from a git-archive export (never inside the checkout), in parallel.
# Usage: per_commit.sh <repo checkout> <scratch dir> <output dir>
set -u
repo=$1 scratch=$2 out=$3
mkdir -p "$out" "$scratch"
commits="ec7eb2d8ff81700842f4e3a35b79879c8c3838e5 c7cde33137093e4192654ee44af57b2bad4044e1 80ba13d70ed960162623ac77ed751fff73be5da8 d5f56313dc5a5c2716211356f99796664dc843dd"
for c in $commits; do
  rm -rf "$scratch/$c"; mkdir -p "$scratch/$c"
  git -C "$repo" archive "$c" | tar -x -C "$scratch/$c"
done
for c in $commits; do
  s=${c:0:8}
  ( cd "$scratch/$c" && python3 -B syn/ooc/pp_resource_gate.py --selftest > "$out/$s.selftest.log" 2>&1; echo $? > "$out/$s.selftest.rc" ) &
  ( cd "$scratch/$c" && python3 -B syn/ooc/pp_resource_gate_mutants.py > "$out/$s.mutants.log" 2>&1; echo $? > "$out/$s.mutants.rc" ) &
  ( cd "$scratch/$c" && python3 -B syn/ooc/pp_resource_gate.py --fuzz 20000 --seed 234 > "$out/$s.fuzz20k.log" 2>&1; echo $? > "$out/$s.fuzz20k.rc" ) &
done
wait
for c in $commits; do
  s=${c:0:8}
  printf '%s selftest rc=%s :: %s | %s\n' "$s" "$(cat $out/$s.selftest.rc)" "$(grep 'selftest:' $out/$s.selftest.log)" "$(grep 'case digest' $out/$s.selftest.log)"
  printf '%s mutants  rc=%s :: %s\n' "$s" "$(cat $out/$s.mutants.rc)" "$(tail -1 $out/$s.mutants.log)"
  printf '%s fuzz20k  rc=%s :: %s\n' "$s" "$(cat $out/$s.fuzz20k.rc)" "$(grep 'case digest' $out/$s.fuzz20k.log)"
done
