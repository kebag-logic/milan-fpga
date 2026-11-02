#!/bin/bash
# Run the given legs concurrently and wait for them. Each argument is one quoted leg.sh command line.
# usage: batch.sh "CHECKOUT NAME POINT GROUPS [args...]" ...
set -u
for leg in "$@"; do
    $MANAGEMENT/2026-09-23/665s2b-a683o/scripts/leg.sh $leg &
done
wait
