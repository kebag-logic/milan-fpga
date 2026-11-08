#!/bin/bash
# The all-fabric identity (both trees, then the compare and the self-test) and the full-split population.
G=$HOME/milan-fpga-management/2026-09-23/665s6-a745b/scripts/gate.sh
F=$VALIDATION_STORAGE/scratch/665s6-a745b/final
B=$VALIDATION_STORAGE/scratch/665s6-a745b/cmp-a9d69c77
O=$VALIDATION_STORAGE/scratch/665s6-a745b/gates
export PATH=/usr/local/bin:/usr/bin:/bin
$G identity-dump-head $F python3 sw/mailbox/placement_identity.py --dump $O/ident-head.json --jobs 4
$G identity-dump-base $F python3 sw/mailbox/placement_identity.py --dump $O/ident-base-a9d69c77.json --tree $B --jobs 4
$G identity-compare $F python3 sw/mailbox/placement_identity.py --compare $O/ident-base-a9d69c77.json $O/ident-head.json
$G identity-selftest $F python3 sw/mailbox/placement_identity.py --selftest --jobs 4
$G population-check $F python3 syn/ooc/split_population.py --check --jobs 6
$G population-selftest $F python3 syn/ooc/split_population.py --selftest
