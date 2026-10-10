#!/bin/sh
# Scope proof: tree identities at base, round-1 head and this head; changed paths.
set -u; . "$(dirname "$0")/env.sh"
B=09e357fb4bf3d35c8a9deba9a787e13f74d08c83 R1=c3864686c0b254bd2d7b7f733078ec302fb9be62
cd "$SRC" || exit 2
for d in hdl syn scripts .github tb/pp_top tb/common Makefile docs/guides docs/diagrams docs/traceability \
         docs/architecture/01_overview.md docs/architecture/02_interfaces.md docs/architecture/07_memory_maps.md; do
  b=$(git rev-parse $B:$d) r=$(git rev-parse $R1:$d) h=$(git rev-parse $HEAD_SHA:$d)
  [ "$b" = "$h" ] && [ "$r" = "$h" ] && s=IDENTICAL || s=DIFFERS
  echo "$s $d base=$b r1=$r head=$h"
done
echo "--- changed paths base..head"; git diff --name-status $B $HEAD_SHA
echo "--- changed paths r1..head"; git diff --name-status $R1 $HEAD_SHA
echo "--- commits r1..head"; git log --format='%H %s' $R1..$HEAD_SHA
echo "--- head DESC_NAME_ENTRIES_P default"; git grep -n 'parameter int unsigned DESC_NAME_ENTRIES_P' $HEAD_SHA -- hdl/top
