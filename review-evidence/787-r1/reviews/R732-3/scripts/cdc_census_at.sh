#!/bin/sh
# Run docs/diagrams/cdc_census.gen.py on an exported tree of each revision and
# compare its output with that revision's committed census.
# Usage: cdc_census_at.sh REPO WORKDIR REV...
set -eu
repo=$1; work=$2; shift 2
for r in "$@"; do
  t=$work/tree-$r; rm -rf "$t"; mkdir -p "$t"
  git -C "$repo" archive "$r" hdl sw/litex/milan_soc.py docs/diagrams/cdc_census.gen.py \
    docs/diagrams/cdc_census.svg docs/diagrams/cdc_census.drawio | tar -x -C "$t"
  (cd "$t" && python3 -I docs/diagrams/cdc_census.gen.py "$t/gen" >/dev/null)
  s=equal; cmp -s "$t/gen.svg" "$t/docs/diagrams/cdc_census.svg" || s=DIFFERS
  d=equal; cmp -s "$t/gen.drawio" "$t/docs/diagrams/cdc_census.drawio" || d=DIFFERS
  echo "$r svg=$s drawio=$d"
done
