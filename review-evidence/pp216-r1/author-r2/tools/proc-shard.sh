#!/usr/bin/env bash
# proc-shard.sh <k> <N> <logs>: shard k of N of the processor's full suite sweep, run from the root of a clean clone.
# It runs the repository's own scripts/run_suites.sh text (its uPC map and M9 opcode checks first, then each suite's
# `make`, the PASS/FAIL/UNREADABLE lines, the closing tally and the exit status), with its one suite loop
# `for d in tb/*/; do` given the suites of this shard instead: suite i of the sorted list of tb/*/ directories that
# hold a Makefile (the glob the loop reads) belongs to shard i mod N. REQ_TAG_LOG is <logs>/req-tags.txt. The script
# text is passed to bash with the clone's scripts/run_suites.sh as $0, so its `cd "$(dirname "$0")/.."` lands on the
# clone root; nothing is written into the clone outside what the suites build.
set -euo pipefail
k=$1; n=$2; logs=$3
mkdir -p "$logs"
export REQ_TAG_LOG="$logs/req-tags.txt"
list=()
i=0
for d in tb/*/; do
  [ -f "$d/Makefile" ] || continue
  if [ $((i % n)) -eq "$k" ]; then list+=("$d"); fi
  i=$((i + 1))
done
printf 'shard %s/%s of %s suites: %s\n' "$k" "$n" "$i" "${list[*]}" | tee "$logs/assignment.txt"
src=scripts/run_suites.sh
[ "$(grep -c '^for d in tb/\*/; do$' "$src")" = 1 ] || { echo "the suite loop is not once in $src"; exit 99; }
text=$(sed "s#^for d in tb/\*/; do\$#for d in ${list[*]}; do#" "$src")
exec bash -c "$text" "$PWD/$src"
