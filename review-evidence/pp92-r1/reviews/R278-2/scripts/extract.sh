#!/usr/bin/env bash
# extract.sh <commit> <dest>: a disposable copy of the reviewed tree at <commit>
# (git archive, so the review clone's working tree and index are never touched)
set -euo pipefail
SRC=${SRC:-$REVIEWS/r278-2-pp92}
case "$2" in
  $REVIEWS/pp92-r278-2-packet/scratch/*) ;;
  *) echo "refusing: dest must be under the packet scratch dir" >&2; exit 2 ;;
esac
mkdir -p "$2"
git -C "$SRC" archive "$1" | tar -x -C "$2"
# cap the simulator's build parallelism in the copy (review budget: at most 8
# concurrent jobs = 4 suites x -j 2); nothing else in the copy is changed here
find "$2/tb" -name Makefile -exec sed -i 's/--build -j 0/--build -j 2/' {} +
