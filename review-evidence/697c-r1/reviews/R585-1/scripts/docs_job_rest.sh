#!/bin/bash
# The docs-check job's repository gates that read sw/firmware, run as the hosted job does:
# verilog-axis, protocol-processor and gptp-processor initialised, tsn-c-stack not.
# usage: docs_job_rest.sh <clone> <python>
cd "$1" || exit 2
PY=$2; fails=0
while IFS= read -r cmd; do
  [ -z "$cmd" ] && continue
  out=$(eval "$PY -B $cmd" 2>&1); rc=$?
  printf 'rc=%s  %s\n' "$rc" "$cmd"
  [ "$rc" -ne 0 ] && { fails=$((fails+1)); printf '%s\n' "$out" | tail -12 | sed 's/^/    /'; }
done <<'CMDS'
scripts/check_baremetal_only.py --check
scripts/measure_naming.py --check
scripts/check_port_contracts.py
scripts/measure_fail_fast.py --check
scripts/check_todo_ownership.py
scripts/measure_test_evidence.py --check
scripts/check_hygiene.py --check
scripts/check_cpp_idiom.py
scripts/check_cpp_idiom.py --selftest
scripts/check_py_idiom.py
scripts/check_py_idiom.py --selftest
scripts/check_sh_idiom.py
scripts/check_archive.py
scripts/gen_toc.py --verify-anchors
scripts/gen_toc.py --check
scripts/check_rtl_source_lists.py
scripts/check_soc_sources.py
CMDS
echo "docs job repository gates: $fails failing"
[ "$fails" -eq 0 ]
