#!/bin/sh
# Focused documentation gates for PR #537 at the exact head, run from the
# review clone. Read-only gates only; the builder, Verilator, Yosys and
# processor banks are deliberately NOT run here.
# Usage: run_doc_gates.sh <clone> <base-sha>
set -u
clone=$1; base=$2
cd "$clone" || exit 2
echo "HEAD $(git rev-parse HEAD)"
run() {
  printf '\n=== %s\n' "$*"
  "$@" > /tmp/r274_gate_out.$$ 2>&1
  rc=$?
  tail -n 6 /tmp/r274_gate_out.$$
  echo "exit=$rc"
  rm -f /tmp/r274_gate_out.$$
}
run python3 -B scripts/docs_check.py
run python3 -B scripts/check_em_dash.py --base "$base"
run python3 -B scripts/check_em_dash.py --selftest
run python3 -B scripts/check_feature_status.py
run python3 -B scripts/check_feature_status.py --self-test
run python3 -B scripts/check_baremetal_only.py --check
run python3 -B docs/traceability/gen_module_matrix.py --check
run python3 -B scripts/check_gptp_docs.py --with-submodule
run python3 -B scripts/check_doc_style.py
run python3 -B scripts/gen_toc.py --check
run python3 -B scripts/gen_toc.py --verify-anchors
run python3 -B scripts/check_doc_paths.py
run python3 -B scripts/check_submodule_docs.py
run git diff --check "$base" HEAD
