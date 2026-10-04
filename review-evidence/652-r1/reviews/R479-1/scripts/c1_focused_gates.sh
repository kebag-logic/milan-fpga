#!/bin/sh
# Campaign 1: the gates this PR adds or changes, run alone in a disposable
# copy of the exact head. Usage: c1_focused_gates.sh <tree> <receipt dir>
# Needs the pinned Verilator 5.050 wrapper first on PATH (set by caller).
T=$1; R=$2; mkdir -p "$R"
cd "$T" || exit 9
echo "head $(git rev-parse HEAD) tree $(git rev-parse HEAD^{tree})" > "$R/c1_head.txt"
verilator --version >> "$R/c1_head.txt"
run() { n=$1; shift; "$@" > "$R/$n.log" 2>&1; echo $? > "$R/$n.rc"; }
run gate38 python3 -c "import sys; sys.path.insert(0,'sw/builder'); import test_builder as t; t.test_name_count_fits_the_nvm_name_block(); print('SKIPS', t.SKIPS if hasattr(t,'SKIPS') else 'n/a')"
run gate24 python3 -c "import sys; sys.path.insert(0,'sw/builder'); import test_builder as t; t.test_d8_role_pools()"
run nvm_space python3 scripts/check_nvm_record_space.py
run nvm_space_self python3 scripts/check_nvm_record_space.py --self-test
for t in yosys_sweep resmap_models resmap_tables resmap_map soc_sweep; do
  run "resmap_$t" python3 syn/resmap/$t.py --selftest
done
run docs_check python3 scripts/docs_check.py
run doc_paths python3 scripts/check_doc_paths.py
run gen_toc python3 scripts/gen_toc.py --check
run em_dash python3 scripts/check_em_dash.py --base 6c22d3cad7c8c24ed3f0c5eab535922a3428c8d5
run lint_rtl python3 scripts/lint_rtl.py --check
run sv_idiom python3 scripts/check_sv_idiom.py
run py_idiom python3 scripts/check_py_idiom.py
run entity_shape python3 scripts/check_entity_shape.py --self-test
run wire_acc python3 scripts/check_wire_accountability.py --self-test
git status --porcelain --ignored=no > "$R/c1_status_after.txt"
echo done > "$R/c1.done"
