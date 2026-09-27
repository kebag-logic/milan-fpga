#!/bin/sh
# Foreground gates at the review head (round-1 set plus the assigned builder gates); one receipt per gate.
# Usage: gates_r2.sh <repo> <outdir> <markdown-venv-python>
REPO=$1; OUT=$2; MD=$3
cd "$REPO" || exit 2
run() { name=$1; shift; "$@" > "$OUT/gate_$name.txt" 2>&1; echo "rc=$? $name: $*" | sed "s#$MD#<pinned-markdown-venv>/bin/python#" | tee -a "$OUT/gates_summary.txt"; }
: > "$OUT/gates_summary.txt"
run selftest python3 -B tb/verilator/fw_service_budget/run.py --self-test
run make_default make -C tb/verilator/fw_service_budget
run host_model python3 -B sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test
run nvm_capture python3 -B scripts/check_nvm_capture.py
run feature_status python3 -B scripts/check_feature_status.py --self-test
run pp_srcs python3 -B scripts/pp_srcs.py --check
run baremetal_only python3 -B scripts/check_baremetal_only.py --check
run entity_shape python3 -B scripts/check_entity_shape.py --self-test
run docs_check python3 -B scripts/docs_check.py
run doc_paths python3 -B scripts/check_doc_paths.py
run doc_style python3 -B scripts/check_doc_style.py
run archive python3 -B scripts/check_archive.py
run gen_toc "$MD" -B scripts/gen_toc.py --check
run em_dash "$MD" -B scripts/check_em_dash.py --base ac18b50968b12efe4d15c0a06301264b35656b31
run py_idiom python3 -B scripts/check_py_idiom.py
run cpp_idiom python3 -B scripts/check_cpp_idiom.py
run hygiene python3 -B scripts/check_hygiene.py --check
run test_evidence python3 -B scripts/measure_test_evidence.py --check
run diff_check git diff --check ac18b50968b12efe4d15c0a06301264b35656b31 HEAD
run untouched git diff --stat 7f997b60d5a74d46beca5c263d27496ccce0ae4f HEAD -- tb/verilator/nvm_capture_cpu sw/firmware/milan_baremetal
run untouched_base git diff --stat ac18b50968b12efe4d15c0a06301264b35656b31 HEAD -- tb/verilator/nvm_capture_cpu sw/firmware/milan_baremetal
