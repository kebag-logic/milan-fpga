#!/bin/bash
# Focused documentation and touched-language gates (check and selftest modes),
# including the round-2 assignment's explicitly named self-tests.
# Usage: 40_doc_static_gates.sh <clone>
set -u
C=${1:?clone}; cd "$C" || exit 2
rc_all=0
for cmd in \
  "scripts/docs_check.py" \
  "scripts/check_em_dash.py --base 9e9954e96bf55181edb9949ae94c9abd4ab6aaf5" \
  "scripts/check_doc_style.py" \
  "scripts/check_doc_paths.py" \
  "scripts/gen_toc.py --verify-anchors" \
  "scripts/gen_toc.py --check" \
  "scripts/check_solution_docs.py" \
  "scripts/check_baremetal_only.py --check" \
  "scripts/check_soc_sources.py" \
  "scripts/check_hygiene.py --check" \
  "scripts/check_py_idiom.py" \
  "scripts/check_sh_idiom.py" \
  "scripts/check_feature_status.py --self-test" \
  "scripts/check_sweep_shape.py --self-test" \
  "scripts/check_deploy_shape.py --self-test" \
  "scripts/check_entity_shape.py --self-test" \
  "scripts/check_em_dash.py --selftest" \
  "scripts/docs_check.py --selftest" \
  "scripts/check_baremetal_only.py --selftest" \
  "scripts/check_solution_docs.py --selftest" \
  "scripts/ci_scope.py --selftest" ; do
  out=$(python3 $cmd 2>&1); rc=$?; [ $rc -ne 0 ] && rc_all=1
  echo "rc $rc: $cmd :: $(tail -1 <<<"$out" | cut -c1-160)"
done
echo "--- git diff --check base..head"; git diff --check 9e9954e96bf55181edb9949ae94c9abd4ab6aaf5 HEAD; echo "rc $?"
echo "--- shellcheck-free bash -n"; bash -n sw/litex/sweep_extra.sh; echo "rc $?"
echo "overall rc=$rc_all"
