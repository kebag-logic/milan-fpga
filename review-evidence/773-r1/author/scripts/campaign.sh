#!/usr/bin/env bash
# One explicit campaign in its own clean clone of the lane at <rev>, with its
# own log, exit status, command and start/end stamps under camp/<name>/.
# The pinned Verilator 5.050 and CPython 3.12.3 (a scratch venv with PyYAML,
# which the builder needs) come first on PATH.
# usage: campaign.sh <name> <rev> <suite-dir> <make target and variables>...
set -u
name=$1; rev=$2; dir=$3; shift 3
here=$(cd "$(dirname "$0")" && pwd)
S=$VALIDATION_STORAGE/scratch/773-a664
C=$S/clone-$name
O=$S/camp/$name
mkdir -p "$O"
[ -d "$C" ] || bash "$here/make_clone.sh" "$C" "$rev" > "$O/clone.log" 2>&1
export PATH=$VALIDATION_TOOLS/pinned-verilator-5.050:$VALIDATION_STORAGE/scratch/773-a664/venv312/bin:$PATH
export TMPDIR=$S/tmp
mkdir -p "$TMPDIR"
cd "$C" || exit 2
git rev-parse HEAD > "$O/HEAD.txt"
git status --short > "$O/status.txt"
verilator --version > "$O/tools.txt"; python3 --version >> "$O/tools.txt"; make --version | head -1 >> "$O/tools.txt"
printf 'make -C %s %s\n' "$dir" "$*" > "$O/command.txt"
date -Is > "$O/start"
make -C "$dir" "$@" > "$O/log" 2>&1
echo $? > "$O/rc"
date -Is > "$O/end"
