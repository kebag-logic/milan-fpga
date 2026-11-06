#!/usr/bin/env bash
# sweep.sh <runs> <clone>: the full processor sweep with REQ_TAG_LOG (pinned Verilator 5.050, make -j16),
# then the executed traceability check over its output
R=$1; C=$2
BASE=$WORKSPACE_HOME/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin
mkdir -p $R $VALIDATION_STORAGE/scratch/pp214-a736b/tmp/sweep
g() { n=$1; shift; echo "$*" > $R/$n.cmd; date +%s > $R/$n.start; (cd $C && "$@") > $R/$n.log 2>&1; echo $? > $R/$n.rc; date +%s > $R/$n.end; }
rm -f $R/req-tags.txt
g run_suites env PATH=$VALIDATION_TOOLS/verilator-v5.050/bin:$BASE MAKEFLAGS=-j16 TMPDIR=$VALIDATION_STORAGE/scratch/pp214-a736b/tmp/sweep REQ_TAG_LOG=$R/req-tags.txt bash scripts/run_suites.sh
cp $R/run_suites.log $R/suites.txt
g check_req_tags_exec env PATH=$BASE python3 scripts/check-req-tags.py --suites $R/suites.txt --evidence $R/req-tags.txt
