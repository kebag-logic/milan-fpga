#!/usr/bin/env bash
# One census probe: <name> <form> [top]; run as xargs -P N -L 1 with PACKET set.
name=$1; shift
"${PACKET:?}/scripts/census_probe.sh" "${PACKET}/scratch/head-tree" "${PACKET}/scratch/census/$name" "$@"
echo "$name rc=$(cat "${PACKET}/scratch/census/$name/rc")"
