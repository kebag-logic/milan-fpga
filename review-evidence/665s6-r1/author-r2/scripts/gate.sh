#!/bin/bash
# gate.sh NAME DIR COMMAND...: run COMMAND in DIR (a clean clone), unpiped; its output to
# $GATES/NAME.log, whose first line names the clone's head and the command, and its exit status to $GATES/NAME.rc.
GATES=${GATES:-$VALIDATION_STORAGE/scratch/665s6-a745b/gates}
mkdir -p "$GATES"
name=$1; dir=$2; shift 2
cd "$dir" || exit 2
rm -f "$GATES/$name.rc"
{ echo "# head $(git rev-parse HEAD 2>/dev/null) in $(basename "$dir"): $*"; "$@"; } > "$GATES/$name.log" 2>&1
rc=$?
echo "$rc" > "$GATES/$name.rc"
echo "$name rc=$rc"
