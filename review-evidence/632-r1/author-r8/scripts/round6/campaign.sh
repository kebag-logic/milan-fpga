#!/usr/bin/env bash
# One explicit campaign in its own clean clone of the lane at <rev>, with its
# own log, exit status, command and start/end stamps under camp/<name>/.
# The pinned Verilator 5.050 and CPython 3.12 come first on PATH (env.sh).
# usage: campaign.sh <name> <rev> <suite-dir> <make target and variables>...
set -u
name=$1; rev=$2; dir=$3; shift 3
here=$(cd "$(dirname "$0")" && pwd)
S=$VALIDATION_STORAGE/scratch/632-a659/r6
C=$S/clone-$name
O=$S/camp/$name
mkdir -p "$O"
[ -d "$C" ] || bash "$here/make_clone.sh" "$C" "$rev" > "$O/clone.log" 2>&1
source "$here/env.sh"
cd "$C" || exit 2
git rev-parse HEAD > "$O/HEAD.txt"
git status --short > "$O/status.txt"
printf 'make -C %s %s\n' "$dir" "$*" > "$O/command.txt"
date -Is > "$O/start"
make -C "$dir" "$@" > "$O/log" 2>&1
echo $? > "$O/rc"
date -Is > "$O/end"
