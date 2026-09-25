#!/bin/sh
# Reviewer R306-1 reproduction for PR #560 / issue #508 at exact head
# 6a9828c172aa4d5d8ee49725e357a10bae2caa52. Run from a clean checkout of that
# head with the three required submodules initialised, a Verilator 5.050 on
# PATH, and PACKET pointing at a writable directory. Every step is foreground.
# Build steps that honour VERILATOR_JOBS are capped at 8; the others run under
# `taskset -c 0-7`.
set -eu
ROOT=$(git rev-parse --show-toplevel)
PACKET=${PACKET:?set PACKET to a writable directory}
R=$PACKET/receipts; S=$PACKET/scratch; mkdir -p "$R" "$S"
cd "$ROOT"
test "$(git rev-parse HEAD)" = 6a9828c172aa4d5d8ee49725e357a10bae2caa52

# 1. The ROM digest rows are what the repository tool records (restore after).
cp -p syn/yosys/rom_digests.tsv "$S/rom_digests.orig"
(cd syn/yosys && OOC_TMP="$S/ooc_tmp" ./ooc.sh --record-rom-digests)
cmp syn/yosys/rom_digests.tsv "$S/rom_digests.orig" && echo IDENTICAL
cp -p "$S/rom_digests.orig" syn/yosys/rom_digests.tsv

# 2. Parent gates named by the round-2 assignment, and the docs/idiom set.
python3 scripts/check_port_contracts.py
python3 scripts/measure_naming.py --check
python3 scripts/measure_test_evidence.py --check
python3 scripts/measure_test_evidence.py --selftest
python3 scripts/pp_srcs.py --check --selftest
python3 scripts/check_rtl_source_lists.py
python3 scripts/lint_rtl.py --check
python3 scripts/docs_check.py
python3 scripts/check_doc_style.py
python3 scripts/check_doc_paths.py
python3 scripts/check_submodule_docs.py
python3 scripts/check_diagram_pngs.py
python3 docs/traceability/gen_module_matrix.py --check
python3 scripts/check_cpp_idiom.py
python3 scripts/check_py_idiom.py
# (these two need the pinned renderer: tools/markdown/requirements.txt in a venv)
python3 scripts/check_em_dash.py --base c266432dcb0cdd464205823a3d82cad260eedde2
python3 scripts/gen_toc.py --check
git diff --check 573f0052a0e4412e81f0845438fcec2086ce5d55 HEAD

# 3. Focused suites.
make -C tb/verilator/milan_dp notify VERILATOR_JOBS=8
(cd tb/verilator/milan_dp && taskset -c 0-7 python3 gsi_mutants.py)
python3 "$PACKET/probes.py" "$ROOT" "$S" "$R"
taskset -c 0-7 make -C tb/verilator/pp_shadow
taskset -c 0-7 make -C tb/verilator/nvm_cosim JOBS=8 POOL=4
taskset -c 0-7 make -C tb/verilator/milan_dp aclk VERILATOR_JOBS=8
taskset -c 0-7 make -C tb/verilator/milan_dp_render VERILATOR_JOBS=8

# 4. Processor line citations that moved with the pin.
python3 "$PACKET/cite_drift.py" "$ROOT" 09f9bf38 990f9652
python3 "$PACKET/cite_drift.py" "$ROOT" a8f8ce81 990f9652

# 5. Restore: remove ignored build outputs and prove the head bytes.
git clean -fdXq; git -C protocol-processor clean -fdXq
git diff --quiet HEAD && git diff --cached --quiet
test "$(git write-tree)" = e43b64d9421ce0892f1bc620de942fc1f1fe50f8
git submodule status
