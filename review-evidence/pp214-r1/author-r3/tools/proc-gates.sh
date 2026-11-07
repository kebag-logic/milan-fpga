#!/usr/bin/env bash
# proc-gates.sh <runs> <clone>: on a clean clone, the docs gates (make check, the matrix), the changed suites with the
# pinned Verilator, the HDL lint and the whitespace check; each runs whatever the previous one's rc
R=$1; C=$2
. "$(dirname "$0")/common.sh"
mkdir -p "$R" "$S/tmp/proc"
export TMPDIR=$S/tmp/proc MAKEFLAGS=-j8
mmdc_v=$(PATH=$BASE mmdc --version 2>&1); echo "$mmdc_v" > "$R/make_check.mmdc-version"
g "$R" "$C" "$D" "$D/bin:$BASE" make_check make check
g "$R" "$C" "$V" "$V/bin:$BASE" gen_matrix_check python3 scripts/gen_matrix.py --check
g "$R" "$C" "$V" "$V/bin:$VL:$BASE" srp_encoder make -C tb/srp_encoder
g "$R" "$C" "$V" "$V/bin:$VL:$BASE" srp_top make -C tb/srp_top
g "$R" "$C" "$V" "$V/bin:$VL:$BASE" lint_hdl_5050 bash scripts/lint_hdl.sh
g "$R" "$C" "$V" "$V/bin:$BASE" diff_check git diff --check 9210065779b0f698fd7bdb22323a1ed5b8482677 HEAD
