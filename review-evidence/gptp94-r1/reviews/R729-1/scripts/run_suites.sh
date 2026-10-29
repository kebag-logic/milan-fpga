#!/bin/sh
# Run one repository gate in a clone, with the pinned simulator first on PATH.
# usage: run_suites.sh <clone> <logdir> <name> <command...>
clone=$1; logdir=$2; name=$3; shift 3
PATH="$(dirname "$0")/../scratch/bin:$PATH"; export PATH
cd "$clone" || exit 2
( "$@" ) > "$logdir/$name.log" 2>&1
echo $? > "$logdir/$name.rc"
