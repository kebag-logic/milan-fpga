#!/usr/bin/env bash
# proc-gates.sh <runs> <clone> <main>: on a clean clone of the head, the processor's CI gates the change touches,
# each run whatever the previous one's rc: make check (the docs-gates job), the matrix check, the zero-tolerance HDL
# lint, the full suite sweep with the requirement-tag evidence and its executed traceability check (the suites job),
# the portability elaboration and the elaboration guards (the portability job), and the whitespace check against main
R=$1; C=$2; M=$3
. "$(dirname "$0")/common.sh"
mkdir -p "$R" "$S/tmp/proc"
export TMPDIR=$S/tmp/proc MAKEFLAGS=-j16
(PATH=$BASE mmdc --version) > "$R/make_check.mmdc-version" 2>&1
g "$R" "$C" "$D" "$D/bin:$BASE" make_check make check
g "$R" "$C" "$V" "$V/bin:$BASE" gen_matrix_check python3 scripts/gen_matrix.py --check
g "$R" "$C" "$V" "$V/bin:$VL:$BASE" lint_hdl_5050 bash scripts/lint_hdl.sh
g "$R" "$C" "$V" "$V/bin:$VL:$BASE" sweep env REQ_TAG_LOG="$R/req-tags.txt" bash scripts/run_suites.sh
g "$R" "$C" "$V" "$V/bin:$BASE" req_tags_executed python3 scripts/check-req-tags.py --suites "$R/sweep.log" --evidence "$R/req-tags.txt"
g "$R" "$C" "$V" "$VALIDATION_TOOLS/sv2v-v0.0.12:$V/bin:$BASE" yosys_portability bash syn/yosys/run.sh
g "$R" "$C" "$V" "$VALIDATION_TOOLS/sv2v-v0.0.12:$V/bin:$BASE" elab_guards python3 -B tb/elab_guards/guards.py --frontend yosys --jobs 4
g "$R" "$C" "$V" "$V/bin:$BASE" diff_check git diff --check "$M" HEAD
