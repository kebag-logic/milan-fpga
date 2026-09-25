#!/usr/bin/env bash
# Measure KL_mmcm_drp_servo OOC area at base and head with the repository
# recipe (syn/yosys/ooc.sh). The base RTL is swapped in temporarily and the
# exact head blob is restored and verified afterwards.
set -u
REPO=${REPO:-$REVIEWS/r301-1-545}
PKT=${PKT:-$REVIEWS/545-r301-1-packet}
BASE=5b73d3f47dfed519eb988c13d6beb1db664ef1e0
F=hdl/ieee1722/crf/KL_mmcm_drp_servo.sv
cd "$REPO" || exit 2
git show "$BASE:$F" > "$F"
mkdir -p "$PKT/scratch/ooc_base"
(cd syn/yosys && OOC_TMP="$PKT/scratch/ooc_base" ./ooc.sh KL_mmcm_drp_servo); rc=$?
git checkout -- "$F"
git diff --quiet -- "$F" && echo "restored $F to index/head bytes" || { echo "RESTORE FAILED"; exit 3; }
exit $rc
