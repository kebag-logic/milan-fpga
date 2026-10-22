#!/usr/bin/env bash
# Processor gates at the head, slot 1: make check, the CI lint + every suite,
# then the executed half of the traceability gate. Pinned Verilator 5.050.
set -u
cd $VALIDATION_STORAGE/scratch/632-a659/r3b/pp-final
export PATH=$VALIDATION_STORAGE/scratch/632-a659/r3/bin:$PATH
O=$VALIDATION_STORAGE/scratch/632-a659/r3b/final-A
rm -rf $O; mkdir -p $O
git rev-parse HEAD > $O/HEAD.txt
verilator --version > $O/verilator.txt
date -Is > $O/start.txt
make check > $O/make_check.log 2>&1; echo $? > $O/make_check.rc
./scripts/lint_hdl.sh > $O/lint_hdl.log 2>&1; echo $? > $O/lint_hdl.rc
REQ_TAG_LOG=$O/req-tags.txt ./scripts/run_suites.sh > $O/suites.txt 2>&1; echo $? > $O/suites.rc
python3 scripts/check-req-tags.py --suites $O/suites.txt --evidence $O/req-tags.txt > $O/req_tags_executed.log 2>&1; echo $? > $O/req_tags_executed.rc
date -Is > $O/end.txt
echo DONE > $O/DONE
