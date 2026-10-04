#!/usr/bin/env bash
# Prove the three hdl/tb edits are comment-only: comment-stripped preprocessed
# sources at base and head must be byte-identical.
# usage: comment_only.sh <repo> <verilator> <outdir>
set -euo pipefail
repo=$1; vl=$2; out=$3
base=c050d97153dd0480ae741102c1647eeda9b7f273
head=91cef52b3c56cc69f66966b004782a69d2940a46
mkdir -p "$out"
rc=0
# every hdl/ tb/ file the PR touches, so nothing is skipped
mapfile -t files < <(git -C "$repo" diff --name-only "$base" "$head" -- hdl tb)
echo "touched hdl/tb files: ${files[*]}"
for f in "${files[@]}"; do
  for rev in base head; do
    sha=$base; [ $rev = head ] && sha=$head
    git -C "$repo" show "$sha:$f" > "$out/$rev.$(basename "$f")"
  done
  b="$out/base.$(basename "$f")"; h="$out/head.$(basename "$f")"
  case "$f" in
    *.sv|*.v)  "$vl" -E -P "$b" > "$b.pp"; "$vl" -E -P "$h" > "$h.pp" ;;
    *.cpp|*.h) g++ -std=c++17 -fpreprocessed -dD -E -P "$b" > "$b.pp"; g++ -std=c++17 -fpreprocessed -dD -E -P "$h" > "$h.pp" ;;
    *.md)      echo "$f: documentation file, not compiled"; continue ;;
    *)         echo "$f: UNHANDLED type"; rc=1; continue ;;
  esac
  sb=$(sha256sum < "$b.pp" | cut -d' ' -f1); sh=$(sha256sum < "$h.pp" | cut -d' ' -f1)
  raw=$(cmp -s "$b" "$h" && echo same || echo differs)
  if [ "$sb" = "$sh" ]; then v=IDENTICAL; else v=DIFFERENT; rc=1; fi
  echo "$f: raw $raw; preprocessed lines $(wc -l < "$b.pp")/$(wc -l < "$h.pp"); sha256 $sb / $sh: $v"
done
exit $rc
