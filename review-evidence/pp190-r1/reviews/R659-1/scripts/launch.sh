#!/usr/bin/env bash
# Start the reviewer's independent campaigns concurrently, each with its own
# log and rc file under receipts/run/. Usage: launch.sh PACKET REVIEW_CLONE
set -u
P=$1; CLONE=$2
S=$P/scratch; R=$P/receipts/run
mkdir -p "$R" "$S/bin" "$S/tmp"
ln -sf $VALIDATION_TOOLS/pinned-verilator-5.050/verilator "$S/bin/verilator"
export PATH=$S/bin:$PATH TMPDIR=$S/tmp
V=$S/bin/verilator
HEAD=83405d192c451e9fba0ea1fe4e051aafdbb332cc
BASE=246cbc22df280db8fcc09708882bb40b2e964c0e

fresh() {  # fresh() DIR REV: an exported tree of REV
  rm -rf "$1"; mkdir -p "$1"; git -C "$CLONE" archive "$2" | tar -x -C "$1"
}
fresh "$S/t_run_head" $HEAD
fresh "$S/t_run_base" $BASE
fresh "$S/t_mut" $HEAD
fresh "$S/t_probe" $HEAD
fresh "$S/t_lint_head" $HEAD
fresh "$S/t_lint_base" $BASE
rm -rf "$S/t_git"; git clone -q "$CLONE" "$S/t_git"; git -C "$S/t_git" checkout -q --detach $HEAD

bg() {  # bg NAME DIR CMD...: run CMD in DIR, log and rc to receipts/run
  local name=$1 dir=$2; shift 2
  ( cd "$dir" && "$@" ) > "$R/$name.log" 2>&1 < /dev/null; echo $? > "$R/$name.rc"
}
bg pp_top_head "$S/t_run_head/tb/pp_top" make VERILATOR=$V run &
bg pp_top_base "$S/t_run_base/tb/pp_top" make VERILATOR=$V run &
bg ts_arms "$S/t_mut" python3 tb/pp_top/acmp_mutants.py --output "$S/out_ts_arms" \
   --verilator $V --jobs 3 --only tspec_slot_zero tspec_slot_last tspec_no_allocator &
bg probes "$S" python3 -I "$P/scripts/reviewer_probes.py" "$S/t_probe" "$S/out_probes" $V 2 &
( bg lint_hdl_head "$S/t_lint_head" ./scripts/lint_hdl.sh
  bg lint_shapes_head "$S" bash "$P/scripts/lint_shapes.sh" "$S/t_lint_head" head
  bg lint_shapes_base "$S" bash "$P/scripts/lint_shapes.sh" "$S/t_lint_base" base ) &
( bg make_check_head "$S/t_git" make check
  bg gen_matrix_head "$S/t_git" python3 scripts/gen_matrix.py --check ) &
wait
