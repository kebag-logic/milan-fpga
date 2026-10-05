#!/bin/sh
# Reviewer probes of round R496-3 (PR #668, head 3ebd6ca3). Portable: give it
# an exported tree of the head (git archive HEAD | tar -x -C TREE) and a
# scratch directory; it writes nothing into the tree.
#
#   sh run_probes.sh TREE SCRATCH
#
# 1. probe_owed_bound.c   - the pass/accesses in which a restart's
#    ENTITY_AVAILABLE commits behind k owed ENTITY_DEPARTINGs (finding F1).
# 2. probe_owed_rules.c   - three legs of adp.h's owed-frame rule, on the head
#    and on three planted copies of adp.c (finding F2).
# 3. adp_reviewer_mutants.py - eight planted adp.c defects against the head's
#    own adp and port arms (finding F2 and the round-3 rule grading).
set -eu
TREE=$(cd "$1" && pwd)
OUT=$(mkdir -p "$2" && cd "$2" && pwd)
HERE=$(cd "$(dirname "$0")" && pwd)
F="$TREE/sw/firmware/ctrl"
INC=""
for d in mbx wire host port loop adp app test; do INC="$INC -I$F/$d"; done
COMMON="$F/mbx/mbx.c $F/loop/ctrl_loop.c $F/port/ctrl_pool.c $F/port/ctrl_debug.c $F/port/shlan_port.c \
$F/adp/adp_mbx.c $F/app/ctrl_app.c $F/host/mbx_model.c $F/host/mbx_plat_host.c $F/test/test_check.c"
CC=${CC:-gcc}

# shellcheck disable=SC2086
$CC -std=c11 -O2 -Wall -Wextra -pedantic $INC "$HERE/probe_owed_bound.c" $COMMON "$F/adp/adp.c" \
    -o "$OUT/probe_owed_bound"
"$OUT/probe_owed_bound"

python3 -B "$HERE/adp_reviewer_mutants.py" "$TREE" "$OUT/revmut"

for v in head link-loss-drops-owed-departing gm-change-drops-owed-available link-loss-keeps-owed-available; do
    if [ "$v" = head ]; then A="$F/adp/adp.c"; else A="$OUT/revmut/$v/sw/firmware/ctrl/adp/adp.c"; fi
    # shellcheck disable=SC2086
    $CC -std=c11 -O2 -Wall -Wextra -pedantic $INC "$HERE/probe_owed_rules.c" $COMMON "$A" -o "$OUT/rules_$v"
    echo "=== build: $v"
    "$OUT/rules_$v"
done
