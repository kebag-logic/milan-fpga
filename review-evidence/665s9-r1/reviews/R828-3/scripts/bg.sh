#!/bin/sh
# bg.sh <name> <cwd> <cmd...>: run a command detached with its own log and rc file under receipts/
P=$REVIEWS/665s9-r828-3-packet/receipts
name=$1; cwd=$2; shift 2
rm -f "$P/$name.log" "$P/$name.rc"
( cd "$cwd" && { echo "# cwd $cwd"; echo "# head $(git rev-parse HEAD) tree $(git rev-parse HEAD^{tree})"; echo "# cmd $*"; echo "# start $(date -Is)"; } > "$P/$name.log"; "$@" >> "$P/$name.log" 2>&1; rc=$?; echo "# end $(date -Is) rc=$rc" >> "$P/$name.log"; echo $rc > "$P/$name.rc" ) </dev/null &
