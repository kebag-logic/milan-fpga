#!/usr/bin/env bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Lint-only elaboration of milan_datapath under a chosen generated shape, with
# the milan_dp DP flag set (print-dp-vflags) and source list (print-srcs), in
# the disposable exact-head tree copy. Used to elaborate the crf_sink:false
# branch of the #529 wiring, which no suite leg elaborates.
#
# usage: lint_shape.sh <shape incdir, relative to the tree root> <dp_src.sv> <tag> [-G...]
set -uo pipefail
shape=$1; dp_src=$(readlink -f "$2"); tag=$3; shift 3
PACKET=${PACKET:-$(cd "$(dirname "$0")/.." && pwd)}
S=$PACKET/scratch; RUN=$S/tree/tb/verilator/milan_dp
: "${VERILATOR:?set VERILATOR to the pinned simulator}"
cd "$RUN"
srcs=$(sed "s#\.\./\.\./\.\./hdl/milan/milan_datapath\.sv#${dp_src}#" "$S/srcs.txt")
vflags=$(sed -e 's/--cc --exe --build -j 0/--lint-only/' -e 's/-CFLAGS "[^"]*"//' "$S/dpvflags.txt")
LOG=$PACKET/receipts/lint_${tag}.log
# shellcheck disable=SC2086
eval "\"$VERILATOR\" +incdir+../../../$shape $vflags $* $srcs" > "$S/lint_${tag}.full.log" 2>&1
rc=$?
{
  echo "# lint-only tag=$tag shape=$shape dp_src_sha256=$(sha256sum "$dp_src" | cut -d' ' -f1) extra=$*"
  echo "# simulator: $("$VERILATOR" --version)"
  echo "# exit $rc"
  echo "# %Error lines: $(grep -c '^%Error' "$S/lint_${tag}.full.log")"
  echo "# %Warning lines: $(grep -c '^%Warning' "$S/lint_${tag}.full.log")"
  echo "# %Warning/%Error lines naming milan_datapath.sv:"
  grep -E '^%(Warning|Error)' "$S/lint_${tag}.full.log" | grep 'milan_datapath' \
    | sed -e "s#$PACKET#<packet>#g" -e "s#$HOME#\$HOME#g" | sort | uniq -c
} > "$LOG"
cat "$LOG"
