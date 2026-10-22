#!/usr/bin/env bash
# Processor CI mutation campaigns that run the ROM, at the head, one build
# at a time: the AECP dispatch campaign, then the deadline/hazard campaign.
set -u
cd $VALIDATION_STORAGE/scratch/632-a659/r3b/pp-final
export PATH=$VALIDATION_STORAGE/scratch/632-a659/r3/bin:$PATH
V=$VALIDATION_STORAGE/scratch/632-a659/r3/bin/verilator
O=$VALIDATION_STORAGE/scratch/632-a659/r3b/final-B2
rm -rf $O; mkdir -p $O
git rev-parse HEAD > $O/HEAD.txt
git status --short > $O/status_before.txt
date -Is > $O/start.txt
(cd tb/pp_top && python3 aecp_dispatch_mutants.py --output $O/aecp_dispatch --verilator $V --jobs 1) > $O/aecp_dispatch.summary 2>&1; echo $? > $O/aecp_dispatch.rc
(cd tb/pp_top && python3 aecp_mutants.py --output $O/aecp --jobs 1) > $O/aecp.summary 2>&1; echo $? > $O/aecp.rc
date -Is > $O/end.txt
echo DONE > $O/DONE
