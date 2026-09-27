#!/bin/sh
# Foreground static gates at the review head; one receipt per gate.
# Usage: gates.sh <repo> <outdir> <markdown-venv-python>
REPO=$1; OUT=$2; MD=$3
cd "$REPO" || exit 2
run() { name=$1; shift; "$@" > "$OUT/gate_$name.txt" 2>&1; echo "rc=$? $name: $*" | tee -a "$OUT/gates_summary.txt"; }
: > "$OUT/gates_summary.txt"
run selftest python3 -B tb/verilator/fw_service_budget/run.py --self-test
run nvm_capture python3 -B scripts/check_nvm_capture.py
run feature_status python3 -B scripts/check_feature_status.py --self-test
run docs_check python3 -B scripts/docs_check.py
run doc_paths python3 -B scripts/check_doc_paths.py
run doc_style python3 -B scripts/check_doc_style.py
run archive python3 -B scripts/check_archive.py
run gen_toc "$MD" -B scripts/gen_toc.py --check
run em_dash "$MD" -B scripts/check_em_dash.py --base ac18b50968b12efe4d15c0a06301264b35656b31
run diff_check git diff --check ac18b50968b12efe4d15c0a06301264b35656b31 HEAD
run untouched git diff --stat ac18b50968b12efe4d15c0a06301264b35656b31 HEAD -- tb/verilator/nvm_capture_cpu sw/firmware/milan_baremetal
