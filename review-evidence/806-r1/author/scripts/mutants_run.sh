#!/usr/bin/env bash
# mutants_run.sh <rev> <stream> <tag...>: parent_mutants.py in its own clean clone at <rev>, the clean pass C0 first.
set -u
rev=$1; stream=$2; shift 2
X=$VALIDATION_STORAGE/scratch/806-a701; C=$X/clone-mut$stream-${rev:0:8}; O=$X/r/mutants-${rev:0:8}/stream$stream
D=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$O"
[ -d "$C" ] || bash "$D/make_clone.sh" "$C" "$rev" > "$O/clone.log" 2>&1 || exit 2
source "$D/env.sh"
git -C "$C" rev-parse HEAD > "$O/head.txt"
python3 "$D/parent_mutants.py" "$C" "$O" C0 "$@"
