#!/usr/bin/env bash
# Re-run the offline gates this review recorded, from a clean clone at the
# exact head. Usage: run_offline_gates.sh <clone> <receipts-dir> [<venv-python>]
# <venv-python> must have tools/markdown/requirements.txt installed with
# --require-hashes; without it the em-dash and Contents gates refuse (rc 2).
set -u
clone=$1
out=$2
venv=${3:-python3}
base=7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a
mkdir -p "$out"
cd "$clone" || exit 2
run() {
    local name=$1
    shift
    "$@" >"$out/$name.log" 2>&1
    echo "$name rc=$?" | tee -a "$out/summary.txt"
}
run selftest_isolated python3 -I scripts/act_ci.py --selftest
run selftest_docs_contract_form python3 scripts/act_ci.py --selftest
run slot_proof_selftest bash scripts/act_slot_proof.sh --selftest
run ci_events_check python3 scripts/ci_events.py --check
run ci_events_selftest python3 scripts/ci_events.py --selftest
run docs_check python3 -B scripts/docs_check.py
run em_dash "$venv" scripts/check_em_dash.py --base "$base"
run gen_toc "$venv" scripts/gen_toc.py --check
run doc_style python3 scripts/check_doc_style.py
run py_idiom python3 scripts/check_py_idiom.py
run sh_idiom python3 scripts/check_sh_idiom.py
run doc_paths python3 scripts/check_doc_paths.py
run baremetal python3 scripts/check_baremetal_only.py --check
run diff_check git diff --check "$base" HEAD
