#!/usr/bin/env bash
# usage: parent_gates.sh <record-dir>   (the scratch parent, its protocol-processor gitlink staged)
rec="$1"; P=<data>/tmp/pp181-a635/parent
G=<data>/tmp/pp181-a635/pgate.sh
PY=/usr/bin/python3
export PYTHONDONTWRITEBYTECODE=1
mkdir -p "$rec"; : > "$rec/summary.txt"
git -C "$P" rev-parse HEAD > "$rec/parent-HEAD.txt"
git -C "$P" ls-files -s protocol-processor > "$rec/gitlink.txt"
git -C "$P/protocol-processor" rev-parse HEAD > "$rec/submodule-HEAD.txt"
git -C "$P" status --short > "$rec/parent-status-before.txt"
"$G" "$rec" bdd "$P/tests" $PY -m behave --no-capture -f plain
"$G" "$rec" feature_status "$P" $PY scripts/check_feature_status.py
"$G" "$rec" feature_status_selftest "$P" $PY scripts/check_feature_status.py --self-test
"$G" "$rec" pp_srcs "$P" $PY scripts/pp_srcs.py --check --selftest
for s in check_py_idiom check_cpp_idiom check_sv_idiom check_sh_idiom check_todo_ownership check_port_contracts check_rtl_source_lists check_soc_sources check_submodule_docs; do
  "$G" "$rec" "$s" "$P" $PY "scripts/$s.py"
  "$G" "$rec" "${s}_selftest" "$P" $PY "scripts/$s.py" --selftest
done
"$G" "$rec" check_hygiene "$P" $PY scripts/check_hygiene.py --check
"$G" "$rec" check_hygiene_selftest "$P" $PY scripts/check_hygiene.py --selftest
for s in measure_test_evidence measure_naming measure_fail_fast; do
  "$G" "$rec" "$s" "$P" $PY "scripts/$s.py" --check
  "$G" "$rec" "${s}_selftest" "$P" $PY "scripts/$s.py" --selftest
done
"$G" "$rec" measure_control_flow_selftest "$P" $PY scripts/measure_control_flow.py --selftest
"$G" "$rec" measure_cohesion_selftest "$P" $PY scripts/measure_cohesion.py --selftest
"$G" "$rec" check_nvm_record_space "$P" $PY scripts/check_nvm_record_space.py
"$G" "$rec" check_nvm_record_space_selftest "$P" $PY scripts/check_nvm_record_space.py --self-test
"$G" "$rec" check_entity_shape_selftest "$P" $PY scripts/check_entity_shape.py --self-test
"$G" "$rec" check_wire_accountability "$P" $PY scripts/check_wire_accountability.py
"$G" "$rec" lint_rtl "$P" $PY scripts/lint_rtl.py --check --self-test --jobs 4 --verilator <data>/tmp/pp181-a635/bin-parent/verilator
"$G" "$rec" ooc_record_rom_digests "$P/syn/yosys" ./ooc.sh --record-rom-digests tcam
git -C "$P" diff -- syn/yosys/rom_digests.tsv > "$rec/rom_digests.diff"
"$G" "$rec" ooc_selftest "$P" $PY syn/yosys/ooc_selftest.py
"$G" "$rec" ooc_verify "$P/syn/yosys" ./ooc.sh KL_pp_shadow
git -C "$P" checkout -- syn/yosys/rom_digests.tsv
git -C "$P" status --short > "$rec/parent-status-after.txt"
echo ALL-DONE > "$rec/parent.done"
