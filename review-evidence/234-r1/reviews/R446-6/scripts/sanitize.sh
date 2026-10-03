#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
# Turn every receipt's raw output (<name>.raw) into its published log (<name>.log) and scrub local paths from every
# .log and .txt under <receipts>: run root, scratch, packet, checkout, reviews and tools directories, the executor's
# run tree, temporary directories and the home directory become placeholders.
# Usage: sanitize.sh <packet> <checkout> <executor-run-tree>
set -eu
P=$(cd "$1" && pwd); REPO=$(cd "$2" && pwd); EXEC=$3
scrub() {
  sed -e "s#$P/scratch/run#<run-root>#g" -e "s#$P/scratch#<scratch>#g" -e "s#$P#<packet>#g" \
      -e "s#$REPO#<checkout>#g" -e "s#$(dirname "$P")#<reviews>#g" -e "s#$EXEC#<executor-run-tree>#g" \
      -e "s#[A-Za-z0-9/._-]*packet/scratch#<scratch>#g" -e "s#$(dirname "$(dirname "$P")")/tools#<tools>#g" -e "s#/tmp/[A-Za-z0-9._-]*#<tmp>#g" -e "s#$HOME#<home>#g"
}
find "$P/receipts" -name '*.raw' -print0 | while IFS= read -r -d '' raw; do
  scrub < "$raw" > "${raw%.raw}.log" && rm "$raw"
done
find "$P/receipts" \( -name '*.log' -o -name '*.txt' -o -name '*.list' \) -print0 | while IFS= read -r -d '' log; do
  scrub < "$log" > "$log.tmp" && mv "$log.tmp" "$log"
done
