#!/usr/bin/env bash
# The AECP deadline and hazard-class campaign (a processor CI gate) at the
# head, one build at a time, in the second clean clone.
set -u
cd $VALIDATION_STORAGE/scratch/632-a659/r3b/pp-final-m
export PATH=$VALIDATION_STORAGE/scratch/632-a659/r3/bin:$PATH
O=$VALIDATION_STORAGE/scratch/632-a659/r3b/final-B3
rm -rf $O; mkdir -p $O
git rev-parse HEAD > $O/HEAD.txt
git status --short > $O/status_before.txt
date -Is > $O/start.txt
(cd tb/pp_top && python3 aecp_mutants.py --output $O/aecp --jobs 1) > $O/aecp.summary 2>&1; echo $? > $O/aecp.rc
date -Is > $O/end.txt
echo DONE > $O/DONE
