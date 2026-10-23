#!/usr/bin/env bash
# The processor CI's lint + every-suite step at the head, then the executed
# half of the traceability gate on that run. Pinned Verilator 5.050.
set -u
cd $VALIDATION_STORAGE/scratch/632-a659/r3b/pp-head
export PATH=$VALIDATION_STORAGE/scratch/632-a659/r3/bin:$PATH
O=$VALIDATION_STORAGE/scratch/632-a659/r3b/gates
mkdir -p $O
git rev-parse HEAD > $O/HEAD.txt
verilator --version > $O/verilator.txt
date -Is > $O/start.txt
./scripts/lint_hdl.sh > $O/lint_hdl.log 2>&1; echo $? > $O/lint_hdl.rc
REQ_TAG_LOG=$O/req-tags.txt ./scripts/run_suites.sh > $O/suites.txt 2>&1; echo $? > $O/suites.rc
python3 scripts/check-req-tags.py --suites $O/suites.txt --evidence $O/req-tags.txt > $O/req-tags-executed.log 2>&1; echo $? > $O/req-tags-executed.rc
date -Is > $O/end.txt
echo DONE > $O/DONE
