#!/usr/bin/env bash
# Reproduce the reviewer-owned evidence for issue #443 / PR #561, round R321-2.
#
#   reproduce.sh <clean-clone-at-exact-head> <packet-dir>
#
# The clone must be at 5beebb7c7edd908d08be34e52286c9eee441f5b3 with its
# submodules at the recorded gitlinks. Nothing here edits that clone: every
# build, probe and gate runs in a copy under <packet-dir>/scratch. Put a
# Verilator 5.050 first on PATH; the docs gates need the pinned renderer in
# tools/markdown/requirements.txt. Scripts are taken from this packet's
# scripts/ directory (probe_mutants.py is round 1's script, byte-identical).
set -euo pipefail
SRC=$(cd "$1" && pwd); P=$(mkdir -p "$2" && cd "$2" && pwd)
HERE=$(cd "$(dirname "$0")" && pwd)
BASE=0755923d983218ca6ca9db6891a558cbe6425b8d
R1=c9bbb03cc3d4da9c6ee28996b91addbb081efa7e
HEAD=5beebb7c7edd908d08be34e52286c9eee441f5b3
R=$P/receipts; S=$P/scratch; mkdir -p "$R/probes" "$S/r1probes" "$S/r2probes"
test "$(git -C "$SRC" rev-parse HEAD)" = "$HEAD"
verilator --version

git -C "$SRC" diff "$R1" "$HEAD" > "$R/delta-c9bbb03c-5beebb7c.diff"
cp -a "$SRC" "$S/head"

# the standalone CSR benches (five executables) and the explicit campaign
(cd "$S/head" && make -C tb/verilator/csr VERILATOR_JOBS=8) > "$R/csr-bench-all.log" 2>&1
(cd "$S/head" && make -C tb/verilator/milan_dp render-csr-controls VERILATOR_JOBS=8) \
  > "$R/render-csr-controls.log" 2>&1

# round-1 probes, unchanged (<= 4 parallel builds x 2 compile jobs)
python3 "$HERE/probe_mutants.py" "$S/head" "$S/r1probes" \
  clean_aclk dp_rails_from_underruns dp_prefill_conv_swapped csr_ignore_direction \
  csr_row_select_zeroes csr_drop_read_window clean_multi csr_alias_to_listener0 \
  > "$R/probe-mutants.jsonl"
PROBE_PARALLEL=2 PROBE_VERILATOR_JOBS=4 python3 "$HERE/probe_mutants.py" "$S/head" "$S/r1probes" \
  csr_row_select_as_window_aclk csr_row_select_as_window_multi > "$R/probe-row-select.jsonl"

# round-2 probes against the benches this round changed
python3 "$HERE/probe_csr_bench.py" "$S/head" "$S/r2probes" \
  clean@main clean@win window_sem@main window_sem@win lsn0_keep_dir@win \
  ignore_direction@main ignore_direction@win alias_listener0@main alias_listener0@win \
  drop_read_window@main drop_read_window@win rails_truncated@main rails_truncated@win \
  neighbour_alias@main > "$R/probe-csr-bench.jsonl"
PROBE_PARALLEL=1 PROBE_VERILATOR_JOBS=8 python3 "$HERE/probe_csr_bench.py" "$S/head" "$S/r2probes" \
  lsn0_keep_dir@aclk > "$R/probe-csr-bench-aclk.jsonl"
cp "$S"/r1probes/*.log "$S"/r2probes/*.log "$R/probes/"

# the default aclk leg, which carries the new bit-9 check into the sweep
(cd "$S/head" && make -C tb/verilator/milan_dp aclk VERILATOR_JOBS=8) > "$R/aclk-default.log" 2>&1

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
GIT_DIR=/dev/null $PY scripts/docs_check.py > "$R/docs-docs-check-no-git.log" 2>&1
$PY scripts/check_doc_style.py            > "$R/docs-doc-style.log" 2>&1
$PY scripts/check_doc_paths.py            > "$R/docs-doc-paths.log" 2>&1
$PY scripts/check_em_dash.py --base "$BASE" > "$R/docs-em-dash.log" 2>&1
python3 scripts/lint_rtl.py --check       > "$R/static-lint-rtl.log" 2>&1
python3 scripts/check_sv_idiom.py         > "$R/static-sv-idiom.log" 2>&1
python3 scripts/check_port_contracts.py   > "$R/static-port-contracts.log" 2>&1
python3 scripts/check_cpp_idiom.py        > "$R/static-cpp-idiom.log" 2>&1
python3 scripts/check_py_idiom.py         > "$R/static-py-idiom.log" 2>&1
python3 scripts/check_rtl_source_lists.py > "$R/static-rtl-source-lists.log" 2>&1
python3 scripts/measure_test_evidence.py --check    > "$R/static-test-evidence.log" 2>&1
python3 scripts/measure_test_evidence.py --selftest > "$R/static-test-evidence-selftest.log" 2>&1
git diff --check "$BASE" "$HEAD"          > "$R/static-diff-check-base.log" 2>&1
git diff --check "$R1" "$HEAD"            > "$R/static-diff-check-delta.log" 2>&1
echo "reproduce.sh: all commands returned 0"
