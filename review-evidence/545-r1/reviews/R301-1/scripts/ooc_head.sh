#!/usr/bin/env bash
# Repository OOC recipe for the servo at the checked-out head (scratch TMP).
set -u
REPO=${REPO:-$REVIEWS/r301-1-545}
PKT=${PKT:-$REVIEWS/545-r301-1-packet}
mkdir -p "$PKT/scratch/ooc_head"
cd "$REPO/syn/yosys" && OOC_TMP="$PKT/scratch/ooc_head" ./ooc.sh KL_mmcm_drp_servo
