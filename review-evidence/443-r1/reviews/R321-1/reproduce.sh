#!/usr/bin/env bash
# Reproduce the reviewer-owned evidence for issue #443 / PR #561, round R321-1.
#
#   reproduce.sh <clean-clone-at-exact-head> <packet-dir>
#
# The clone must be at c9bbb03cc3d4da9c6ee28996b91addbb081efa7e with its
# submodules at the recorded gitlinks. Nothing here edits that clone: every
# build, probe and synthesis runs in copies under <packet-dir>/scratch. Put a
# Verilator 5.050 first on PATH; yosys and sv2v must be on PATH; the docs
# gates need the pinned renderer in tools/markdown/requirements.txt.
set -euo pipefail
SRC=$(cd "$1" && pwd); P=$(mkdir -p "$2" && cd "$2" && pwd)
BASE=0755923d983218ca6ca9db6891a558cbe6425b8d
HEAD=c9bbb03cc3d4da9c6ee28996b91addbb081efa7e
R=$P/receipts; S=$P/scratch; mkdir -p "$R" "$S"
test "$(git -C "$SRC" rev-parse HEAD)" = "$HEAD"
verilator --version > "$R/probe-verilator-version.txt"

# disposable copies: head for builds/probes, base for the synthesis delta
cp -a "$SRC" "$S/head"; cp -a "$SRC" "$S/base"
git -C "$S/base" -c advice.detachedHead=false checkout -q "$BASE"

# generic cell counts, base and head, one top at a time
for t in milan_csr milan_datapath; do
  short=${t#milan_}; short=${short/datapath/dp}
  for side in base head; do
    (cd "$S/$side" && syn/yosys/run.sh --top "$t" --no-structural \
       --results "$S/ys-$side") > "$R/yosys-$short-$side.log" 2>&1
  done
done

# the explicit control campaign the PR adds
(cd "$S/head" && make -C tb/verilator/milan_dp render-csr-controls VERILATOR_JOBS=8) \
  > "$R/render-csr-controls.log" 2>&1

# reviewer mutation probes (<= 4 parallel builds x 2 compile jobs)
python3 "$P/probe_mutants.py" "$S/head" "$S" \
  clean_aclk dp_rails_from_underruns dp_prefill_conv_swapped csr_ignore_direction \
  csr_row_select_zeroes csr_drop_read_window clean_multi csr_alias_to_listener0 \
  > "$R/probe-mutants.jsonl"
PROBE_PARALLEL=2 PROBE_VERILATOR_JOBS=4 python3 "$P/probe_mutants.py" "$S/head" "$S" \
  csr_row_select_as_window_aclk csr_row_select_as_window_multi \
  > "$R/probe-row-select.jsonl"

# the standalone CSR bench's 0x8DC check (finding F1)
(cd "$S/head/tb/verilator/csr" && make obj_dir/Vcsr_sim VERILATOR_JOBS=8 \
   && ./obj_dir/Vcsr_sim) > "$R/csr-bench-run.log" 2>&1

# documentation and static gates at head
python3 -m venv "$S/docs-env"
"$S/docs-env/bin/python" -m pip install -q --require-hashes \
  -r "$S/head/tools/markdown/requirements.txt"
PY=$S/docs-env/bin/python3
cd "$S/head"
$PY scripts/gen_toc.py --check            > "$R/docs-toc-check.log" 2>&1
$PY scripts/gen_toc.py --verify-anchors   > "$R/docs-toc-verify-anchors.log" 2>&1
$PY scripts/gen_toc.py --selftest         > "$R/docs-gen-toc-selftest.log" 2>&1
$PY scripts/docs_check.py                 > "$R/docs-docs-check.log" 2>&1
$PY scripts/check_doc_style.py            > "$R/docs-doc-style.log" 2>&1
$PY scripts/check_doc_paths.py            > "$R/docs-doc-paths.log" 2>&1
$PY scripts/check_em_dash.py --base "$BASE" > "$R/docs-em-dash.log" 2>&1
python3 scripts/lint_rtl.py --check       > "$R/static-lint-rtl.log" 2>&1
python3 scripts/check_sv_idiom.py         > "$R/static-sv-idiom.log" 2>&1
python3 scripts/check_port_contracts.py   > "$R/static-port-contracts.log" 2>&1
python3 scripts/check_cpp_idiom.py        > "$R/static-cpp-idiom.log" 2>&1
python3 scripts/check_py_idiom.py         > "$R/static-py-idiom.log" 2>&1
python3 scripts/check_rtl_source_lists.py > "$R/static-rtl-source-lists.log" 2>&1
python3 scripts/measure_test_evidence.py --check > "$R/static-test-evidence.log" 2>&1
git diff --check "$BASE" "$HEAD"          > "$R/static-diff-check.log" 2>&1
echo "reproduce.sh: all commands returned 0"
