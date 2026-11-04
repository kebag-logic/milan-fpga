#!/usr/bin/env bash
# final-gates.sh <runs> <clone>: the fast gates, then the full sweep with REQ_TAG_LOG and the executed
# traceability check over its output, at the final head
R=$1; C=$2
T=<scratch>
BASE=<home>/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin
$T/tools/fast-gates.sh $R $C
g() { n=$1; shift; echo "$*" > $R/$n.cmd; date +%s > $R/$n.start; (cd $C && "$@") > $R/$n.log 2>&1; echo $? > $R/$n.rc; date +%s > $R/$n.end; }
rm -f $R/req-tags.txt
g run_suites env PATH=<toolchain>/verilator-v5.050/bin:$BASE MAKEFLAGS=-j8 TMPDIR=$T<tmp>/sweep2 REQ_TAG_LOG=$R/req-tags.txt bash scripts/run_suites.sh
cp $R/run_suites.log $R/suites.txt
g check_req_tags_exec env PATH=$BASE python3 scripts/check-req-tags.py --suites $R/suites.txt --evidence $R/req-tags.txt
