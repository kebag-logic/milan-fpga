#!/usr/bin/env bash
# R595-1: copy the published lane B15 tools to a scratch directory and replace the two redacted
# identity placeholders in tone_points_b15.py with neutral values, so its offline control runs.
# usage: prepare_tools.sh <published author/tools dir> <scratch tools dir>
set -eu
mkdir -p "$2"
cp "$1"/*.py "$2"/
sed -i 's/"<peer-eid>"/"0200000000aa0000"/; s/bytes.fromhex("<peer-id>")/bytes.fromhex("0200000000aa")/' "$2/tone_points_b15.py"
grep -c '<peer-' "$2/tone_points_b15.py" || true
