#!/usr/bin/env bash
# Reviewer gate runner: runs one named gate in a clean clone of the exact head and
# records <name>.cmd/.log/.rc/.start/.end under the receipts directory.
# usage: run-gates.sh <clone-dir> <receipts-dir> <name> <command...>
set -u
clone=$1; out=$2; name=$3; shift 3
mkdir -p "$out"
printf '%s\n' "$*" > "$out/$name.cmd"
date +%s > "$out/$name.start"
( cd "$clone" && eval "$@" ) > "$out/$name.log" 2>&1
echo $? > "$out/$name.rc"
date +%s > "$out/$name.end"
