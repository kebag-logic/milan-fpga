#!/usr/bin/env bash
# Diff module headers (parameter + port lists) and parameter declarations between two revisions.
set -u
repo=$1 base=$2 head=$3; shift 3
for f in "$@"; do
  hdr() { git -C "$repo" show "$1:$f" | awk '/^[[:space:]]*module[[:space:]]/{m=1} m{print} m&&/^[[:space:]]*\);/{exit}'; }
  par() { git -C "$repo" show "$1:$f" | grep -E '^\s*(parameter|localparam)\b' ; }
  echo "=== $f header diff"; diff <(hdr "$base") <(hdr "$head") && echo "(none)"
  echo "=== $f parameter/localparam diff"; diff <(par "$base") <(par "$head") && echo "(none)"
done
