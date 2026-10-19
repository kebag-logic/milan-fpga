#!/usr/bin/env bash
# usage: proc_gates.sh <root> <record-dir>   every processor gate, unpiped, through gate.sh
root="$1"; rec="$2"; mkdir -p "$rec"
G=$VALIDATION_STORAGE/pp185-a647/scripts/gate.sh
export PYTHONDONTWRITEBYTECODE=1
git -C "$root" rev-parse HEAD > "$rec/HEAD.txt"
git -C "$root" status --short > "$rec/status-before.txt"
"$G" "$rec" lint_hdl "$root" ./scripts/lint_hdl.sh
"$G" "$rec" gen_matrix "$root" python3 scripts/gen_matrix.py --check
"$G" "$rec" make_check "$root" make check
"$G" "$rec" yosys_run_033 "$root" ./syn/yosys/run.sh
GATE_BIN=$VALIDATION_STORAGE/pp185-a647/bin-parent "$G" "$rec" yosys_run_066 "$root" ./syn/yosys/run.sh
"$G" "$rec" elab_guards_yosys "$root" python3 -B tb/elab_guards/guards.py --frontend yosys --jobs 4
"$G" "$rec" run_suites "$root" env REQ_TAG_LOG="$rec/req-tags.txt" ./scripts/run_suites.sh
"$G" "$rec" req_tags_executed "$root" python3 scripts/check-req-tags.py --suites "$rec/run_suites.log" --evidence "$rec/req-tags.txt"
git -C "$root" status --short --ignored > "$rec/status-after.txt"
echo ALL-DONE > "$rec/proc.done"
