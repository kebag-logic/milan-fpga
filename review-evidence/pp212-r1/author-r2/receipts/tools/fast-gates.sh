#!/usr/bin/env bash
# fast-gates.sh <runs> <clone>: the processor's docs, lint, yosys and elaboration-guard gates, in order, each
# with its cmd/log/rc/start/end under <runs>; each runs whatever the previous one's rc
R=$1; C=$2
BASE=<home>/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin
mkdir -p $R
g() { n=$1; shift; echo "$*" > $R/$n.cmd; date +%s > $R/$n.start; (cd $C && "$@") > $R/$n.log 2>&1; echo $? > $R/$n.rc; date +%s > $R/$n.end; }
g make_check env PATH=$BASE make check
g lint_hdl_5052 env PATH=$BASE bash scripts/lint_hdl.sh
verilator --version > $R/lint_hdl_5052.version 2>&1
g lint_hdl_5050 env PATH=<toolchain>/verilator-v5.050/bin:$BASE bash scripts/lint_hdl.sh
<toolchain>/verilator-v5.050/bin/verilator --version > $R/lint_hdl_5050.version 2>&1
g yosys_run env PATH=$BASE ./syn/yosys/run.sh
g elab_guards env PATH=$BASE python3 -B tb/elab_guards/guards.py --frontend yosys --jobs 4
