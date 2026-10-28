#!/usr/bin/env bash
# Run the fast static and generator gates in the current tree, one after
# another, printing each command's own rc. Exit 1 if any rc is non-zero.
set -u
export SV2V=<tools>/sv2v-v0.0.12/sv2v YOSYS=/usr/bin/yosys VERILATOR=<tools>/pinned-verilator-5.050/verilator PYTHONHASHSEED=0
fail=0
step() {
  echo "=== STEP: $*"
  "$@"
  rc=$?
  echo "=== RC $rc: $*"
  [ $rc -eq 0 ] || fail=1
}
step python3 sw/mailbox/gen_mailbox.py --check --crosscheck
step python3 sw/mailbox/gen_mailbox.py --selftest
step python3 sw/mailbox/publication_census.py --check --selftest --jobs 4
step python3 scripts/check_submodule_docs.py
step python3 scripts/lint_rtl.py --check
step python3 scripts/check_cpp_idiom.py
step python3 scripts/check_py_idiom.py
step python3 syn/ooc/pp_resource_gate.py check-baseline
step bash -c 'cd tests && behave --no-capture -f plain -k features/milan_streaming_licence.feature features/torture_campaign_plan.feature'
step bash -c 'cd tests && behave -f progress'
echo "=== LIGHT GATES fail=$fail"
exit $fail
