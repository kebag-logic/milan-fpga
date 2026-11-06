#!/usr/bin/env bash
# fast-gates.sh <runs> <clone>: the processor's docs, lint, yosys and elaboration-guard gates, in order, each
# with its cmd/log/rc/start/end under <runs>; each runs whatever the previous one's rc
R=$1; C=$2
BASE=$WORKSPACE_HOME/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin
DOCS=$VALIDATION_STORAGE/scratch/pp214-a736/venv-docs/bin
mkdir -p $R
g() { n=$1; shift; echo "$*" > $R/$n.cmd; date +%s > $R/$n.start; (cd $C && "$@") > $R/$n.log 2>&1; echo $? > $R/$n.rc; date +%s > $R/$n.end; }
g make_check env PATH=$DOCS:$BASE make check
g gen_matrix_check env PATH=$BASE python3 scripts/gen_matrix.py --check
mmdc --version > $R/make_check.mmdc-version 2>&1 || PATH=$BASE mmdc --version > $R/make_check.mmdc-version 2>&1
g lint_hdl_5052 env PATH=$BASE bash scripts/lint_hdl.sh
verilator --version > $R/lint_hdl_5052.version 2>&1
g lint_hdl_5050 env PATH=$VALIDATION_TOOLS/verilator-v5.050/bin:$BASE bash scripts/lint_hdl.sh
$VALIDATION_TOOLS/verilator-v5.050/bin/verilator --version > $R/lint_hdl_5050.version 2>&1
g yosys_run env PATH=$BASE TMPDIR=$VALIDATION_STORAGE/scratch/pp214-a736b/tmp ./syn/yosys/run.sh
g elab_guards env PATH=$BASE TMPDIR=$VALIDATION_STORAGE/scratch/pp214-a736b/tmp python3 -B tb/elab_guards/guards.py --frontend yosys --jobs 4
