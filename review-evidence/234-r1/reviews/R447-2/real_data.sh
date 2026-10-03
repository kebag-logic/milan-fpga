#!/usr/bin/env bash
# Run the head's gate (check, read-only) on the existing A and B measurement directories.
# Usage: real_data.sh <repo checkout> <validation storage root holding A/ and B/> <output dir>
set -u
repo=$1 store=$2 out=$3
mkdir -p "$out"
while read -r name dir endpoint; do
  python3 -B "$repo/syn/ooc/pp_resource_gate.py" check "$store/$dir" --endpoint "$endpoint" \
    > "$out/$name.log" 2>&1
  echo $? > "$out/$name.rc"
done <<'LIST'
A-route A/work/ax7101/gateware route-1x1
A-ooc-1x1 A/work/ax7101-ooc ooc-1x1
A-ooc-8x8 A/work/ax8x8-ooc ooc-8x8
A-ooc-1x1-10ns A/work/ax7101-ooc10 ooc-1x1
B-route B/work/ax7101/gateware route-1x1
B-ooc-1x1 B/work/ax7101-ooc ooc-1x1
B-ooc-8x8 B/work/ax8x8-ooc ooc-8x8
LIST
