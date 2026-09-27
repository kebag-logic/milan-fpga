#!/usr/bin/env bash
# Run the assigned documentation/policy gates in one tree and print rc per gate.
# Usage: run_gates.sh TREE PYTHON LABEL [git|nogit]
# Every gate runs in the foreground with a timeout; output is kept verbatim.
set -u
tree=$1; py=$2; label=$3; mode=${4:-git}
cd "$tree" || exit 2
echo "== gates: $label; tree HEAD: $( [ "$mode" = git ] && git rev-parse HEAD || echo no-git )"
run() {
  echo "--- \$ $*"
  timeout 600 "$@"
  echo "--- rc=$? :: $*"
}
if [ "$mode" = git ]; then
  run "$py" scripts/docs_check.py
  run "$py" scripts/check_doc_style.py
  run "$py" scripts/check_doc_style.py --selftest
  run "$py" scripts/gen_toc.py --check
  run "$py" scripts/check_em_dash.py --base 8bc97021f28fb7f729418d3a00851c84ea0b50fd
  run "$py" scripts/check_doc_paths.py
  run "$py" scripts/ci_scope.py --selftest
  run "$py" scripts/check_baremetal_only.py --check
  run "$py" scripts/check_feature_status.py --self-test
  run git diff --check 8bc97021f28fb7f729418d3a00851c84ea0b50fd HEAD
  run git diff --check
else
  run "$py" scripts/docs_check.py
  run "$py" scripts/check_feature_status.py
fi
