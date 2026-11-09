#!/usr/bin/env bash
# proc-gates2.sh <runs> <clone> <main>: on a clean clone of the head, every processor CI gate except the suite sweep
# (run as shard units by proc-shards.py, then check-req-tags on the merged record): make check (docs-gates), the
# matrix check, the zero-tolerance HDL lint, the portability elaboration and the elaboration guards (portability),
# the nvm_port figure gate (suites job; PR #13's ref fetched read-only first, as CI fetches it), and the whitespace
# check against main. Each gate runs whatever the previous one's rc.
R=$1; C=$2; M=$3
. "$(dirname "$0")/common.sh"
mkdir -p "$R" "$S/tmp/proc"
export TMPDIR=$S/tmp/proc MAKEFLAGS=-j16
(PATH=$BASE mmdc --version) > "$R/make_check.mmdc-version" 2>&1
g "$R" "$C" "$D" "$D/bin:$BASE" make_check make check
g "$R" "$C" "$V" "$V/bin:$BASE" gen_matrix_check python3 scripts/gen_matrix.py --check
g "$R" "$C" "$V" "$V/bin:$VL:$BASE" lint_hdl_5050 bash scripts/lint_hdl.sh
g "$R" "$C" "$V" "$VALIDATION_TOOLS/sv2v-v0.0.12:$V/bin:$BASE" yosys_portability bash syn/yosys/run.sh
g "$R" "$C" "$V" "$VALIDATION_TOOLS/sv2v-v0.0.12:$V/bin:$BASE" elab_guards python3 -B tb/elab_guards/guards.py --frontend yosys --jobs 4
g "$R" "$C" "$V" "$V/bin:$BASE" fetch_pr13 git fetch --no-tags https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan.git refs/pull/13/head
g "$R" "$C" "$V" "$V/bin:$VL:$BASE" nvm_port_figures make -C tb/nvm_port figures
g "$R" "$C" "$V" "$V/bin:$BASE" diff_check git diff --check "$M" HEAD
