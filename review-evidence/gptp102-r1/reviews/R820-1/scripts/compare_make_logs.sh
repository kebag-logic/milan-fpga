#!/bin/bash
# Compare the author's before/after `make all` logs (public evidence) with
# per-line timestamps, the two clone paths and Verilator's wall-time
# summary line normalised away. usage: compare_make_logs.sh <before.log> <after.log>
norm() { sed -E 's/^ *[0-9]+\.[0-9]+ //; s#/data-2/milan/tmp/gptp102-a762/(before/clone|head/after)#<CLONE>#g; s/Walltime .*/Walltime <T>/; s#-o [^ ]*\.o [^ ]*#<OBJ>#' "$1"; }
diff <(norm "$1") <(norm "$2"); rc=$?
echo "normalised make.log diff rc=$rc (0 = identical), lines compared: $(norm "$1" | wc -l)"
exit $rc
