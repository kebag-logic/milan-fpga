#!/usr/bin/env bash
# Scratch: run the consumer gates that read the processor, with its gitlink at $1; print "rc cmd".
set -u
cd $VALIDATION_STORAGE/pp210-a708c/consumer || exit 1
d=$PWD/protocol-processor
[ "$(git -C "$d" rev-parse --show-toplevel)" = "$d" ] || { echo "not the submodule"; exit 1; }
git -C "$d" checkout -q "$1" || exit 1
git add protocol-processor
echo "processor at $(git -C "$d" rev-parse --short HEAD)"
while IFS= read -r c; do
  [ -z "$c" ] && continue
  log=$VALIDATION_STORAGE/pp210-a708c/clog/$2-$(echo "$c" | tr ' /' '__').log
  timeout 300 bash -c "$c" > "$log" 2>&1; echo "$? $c"
done <<'LIST'
python3 scripts/docs_check.py
python3 scripts/check_doc_paths.py
python3 scripts/check_submodule_docs.py
python3 scripts/check_submodule_docs.py --selftest
python3 docs/diagrams/submodule_boundaries.gen.py --check
python3 scripts/check_hygiene.py --check
python3 scripts/check_hygiene.py --selftest
python3 scripts/check_py_idiom.py
python3 scripts/check_py_idiom.py --selftest
python3 scripts/check_sh_idiom.py
python3 scripts/check_cpp_idiom.py
python3 scripts/check_sv_idiom.py
python3 scripts/check_todo_ownership.py
python3 scripts/check_todo_ownership.py --selftest
python3 scripts/measure_naming.py --check
python3 scripts/measure_fail_fast.py --check
python3 scripts/measure_test_evidence.py --check
python3 scripts/measure_control_flow.py --selftest
python3 scripts/measure_cohesion.py --selftest
python3 scripts/check_rtl_source_lists.py
python3 scripts/check_soc_sources.py
python3 scripts/pp_srcs.py --check --selftest
python3 scripts/check_port_contracts.py
python3 scripts/ci_scope.py --selftest
LIST
