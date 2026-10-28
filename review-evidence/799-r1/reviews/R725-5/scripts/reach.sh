#!/usr/bin/env bash
# Usage: reach.sh <repo> <base> <head>
# Lists changed SystemVerilog sources (parent range and the processor gitlink range) and the
# Verilator suites whose Makefile names one on a non-comment line. Name matching only, not
# an include-graph extraction; delegations to another suite's Makefile are listed separately.
set -eu
R=$1; B=$2; H=$3; cd "$R"
pb=$(git ls-tree "$B" protocol-processor | awk '{print $3}'); ph=$(git ls-tree "$H" protocol-processor | awk '{print $3}')
{ git diff --name-only "$B" "$H" -- '*.sv' '*.svh' '*.v'
  git -C protocol-processor diff --name-only "$pb" "$ph" -- '*.sv' '*.svh' '*.v' | sed 's#^#protocol-processor/#'; } | sort -u > /tmp/reach.$$
echo "processor $pb..$ph"; echo "changed sources:"; sed 's/^/  /' /tmp/reach.$$
echo "suites naming a changed source (non-comment Makefile lines):"
for mk in tb/verilator/*/Makefile; do
  s=$(basename "$(dirname "$mk")"); hits=""
  while read -r f; do b=$(basename "$f"); grep -vE '^\s*#' "$mk" | grep -qF "$b" && hits="$hits $b"; done < /tmp/reach.$$
  [ -n "$hits" ] && echo "  $s:$hits"
done
echo "suites delegating to another suite's Makefile:"
grep -lE '\$\(MAKE\) -C \.\./' tb/verilator/*/Makefile | while read -r mk; do
  echo "  $(basename "$(dirname "$mk")"): $(grep -oE '\$\(MAKE\) -C \.\./[A-Za-z0-9_]+ ?[A-Za-z0-9_-]*' "$mk" | sort -u | tr '\n' ';')"; done
rm -f /tmp/reach.$$
