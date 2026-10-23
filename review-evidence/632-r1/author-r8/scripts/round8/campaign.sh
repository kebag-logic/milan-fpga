#!/usr/bin/env bash
# Round 8: one explicit campaign in its own clean clone at <rev> (as
# round7/campaign.sh, scratch r8), with its own log, rc, command and stamps.
# usage: campaign.sh <name> <rev> <suite-dir> <make target and variables>...
set -u
name=$1; rev=$2; dir=$3; shift 3
R7=$MANAGEMENT/2026-09-23/632-a659/scripts/round7
C=$VALIDATION_STORAGE/scratch/632-a659/r8/clone-$name
O=$VALIDATION_STORAGE/scratch/632-a659/r8/camp/$name
mkdir -p "$O"
[ -d "$C" ] || bash "$R7/make_clone.sh" "$C" "$rev" > "$O/clone.log" 2>&1
source "$R7/env.sh"
export TSN_GEN_ROOT=$VALIDATION_STORAGE/scratch/632-a659/tsn-gen
cd "$C" || exit 2
git rev-parse HEAD > "$O/HEAD.txt"
git status --short > "$O/status.txt"
printf 'make -C %s %s\n' "$dir" "$*" > "$O/command.txt"
date -Is > "$O/start"
make -C "$dir" "$@" > "$O/log" 2>&1
echo $? > "$O/rc"
date -Is > "$O/end"
