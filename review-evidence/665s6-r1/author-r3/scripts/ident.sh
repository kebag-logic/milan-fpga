#!/bin/bash
# The all-fabric identity: the head and the a9d69c77 base dumped by the head's tool, then compared.
export GATES=$VALIDATION_STORAGE/scratch/665s6-a745c/gates
G=$HOME/milan-fpga-management/2026-09-23/665s6-a745c/scripts/gate.sh
F=$VALIDATION_STORAGE/scratch/665s6-a745c/final
B=$VALIDATION_STORAGE/scratch/665s6-a745b/cmp-a9d69c77
export PATH=/usr/local/bin:/usr/bin:/bin
$G identity-dump-head $F python3 sw/mailbox/placement_identity.py --dump $GATES/ident-head.json --jobs 4
$G identity-dump-base $F python3 sw/mailbox/placement_identity.py --dump $GATES/ident-base-a9d69c77.json --tree $B --jobs 4
$G identity-compare $F python3 sw/mailbox/placement_identity.py --compare $GATES/ident-base-a9d69c77.json $GATES/ident-head.json
