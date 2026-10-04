#!/bin/sh
# Campaign 1: the gates this PR adds or changes, run alone in a disposable
# copy of the exact head. Usage: c1_focused_gates.sh <tree> <receipt dir>
# Needs the pinned Verilator 5.050 wrapper first on PATH (set by caller).
T=$1; R=$2; mkdir -p "$R"
cd "$T" || exit 9
echo "head $(git rev-parse HEAD) tree $(git rev-parse HEAD^{tree})" > "$R/c1_head.txt"
verilator --version >> "$R/c1_head.txt"; python3 --version >> "$R/c1_head.txt"
run() { n=$1; shift; "$@" > "$R/$n.log" 2>&1; echo $? > "$R/$n.rc"; }
TB="import sys; sys.path.insert(0,'sw/builder'); import test_builder as t"
run gate38 python3 -c "$TB; t.test_name_count_fits_the_nvm_name_block()"
run gate24a python3 -c "$TB; t.test_d8_role_pools()"
run gate24a_reject python3 -c "$TB; t.test_d8_role_pools_reject()"
run nvm_space python3 scripts/check_nvm_record_space.py
run nvm_space_self python3 scripts/check_nvm_record_space.py --self-test
for m in short_allocation_row long_allocation_row stale_allocation_table; do
  run "nvm_mutate_$m" python3 scripts/check_nvm_record_space.py "--mutate=$m"
done
for t in yosys_sweep resmap_models resmap_tables resmap_map soc_sweep; do
  run "resmap_$t" python3 syn/resmap/$t.py --selftest
done
run docs_check python3 scripts/docs_check.py
run doc_paths python3 scripts/check_doc_paths.py
run doc_style python3 scripts/check_doc_style.py
run gen_toc python3 scripts/gen_toc.py --check
run em_dash_c0280fc0 python3 scripts/check_em_dash.py --base c0280fc008ef9c5c1650402a58bab3e47a92127b
run em_dash_6c22d3ca python3 scripts/check_em_dash.py --base 6c22d3cad7c8c24ed3f0c5eab535922a3428c8d5
run py_idiom python3 scripts/check_py_idiom.py
run lint_rtl python3 scripts/lint_rtl.py --check
run entity_shape python3 scripts/check_entity_shape.py --self-test
run sweep_shape python3 scripts/check_sweep_shape.py --self-test
wc -l scripts/check_nvm_record_space.py scripts/nvm_allocation_table.py \
  syn/resmap/yosys_sweep.py syn/resmap/yosys_sweep_selftest.py syn/resmap/resmap_models.py > "$R/line_counts.txt"
git status --porcelain --ignored=no > "$R/c1_status_after.txt"
echo done > "$R/c1.done"
