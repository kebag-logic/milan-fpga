#!/usr/bin/env bash
# docs_gates.sh <tree> <out dir>: the docs workflow's own check commands that need nothing installed, one rc each.
tree=$1 out=$2; mkdir -p "$out"; cd "$tree" || exit 3
base=${BASE:-1f29f189279f9fc0132f4918e47342b87d22f33a}
run() { name=$1; shift; "$@" > "$out/$name.log" 2>&1; echo "$? $*" > "$out/$name.rc"; }
run em_dash python3 scripts/check_em_dash.py --base "$base" &
run feature python3 scripts/check_feature_status.py &
run wire python3 scripts/check_wire_accountability.py &
run docmap python3 docs/DOC_MAP.gen.py --check &
run timesync python3 docs/diagrams/timesync_chain.gen.py --check &
run solution python3 scripts/check_solution_docs.py &
run naming python3 scripts/measure_naming.py --check &
wait
run failfast python3 scripts/measure_fail_fast.py --check &
run todo python3 scripts/check_todo_ownership.py &
run testevidence python3 scripts/measure_test_evidence.py --check &
run hygiene python3 scripts/check_hygiene.py --check &
run svidiom python3 scripts/check_sv_idiom.py &
run cppidiom python3 scripts/check_cpp_idiom.py &
run pyidiom python3 scripts/check_py_idiom.py &
run shidiom python3 scripts/check_sh_idiom.py &
wait
