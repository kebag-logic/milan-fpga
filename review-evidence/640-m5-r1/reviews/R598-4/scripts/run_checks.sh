#!/bin/sh
# Commands this round ran, in the form they ran. Paths are arguments, not
# constants: CLONE is the exact-head clone with its submodules initialised,
# WT a disposable git clone of the same head (for suites that call git ls-files),
# PY an interpreter with tools/markdown/requirements.txt installed by hash,
# V the pinned Verilator 5.050, OUT the receipt directory.
# Usage: run_checks.sh CLONE WT PY V OUT
set -u
CLONE=$1 WT=$2 PY=$3 V=$4 OUT=$5
BASE=6bfeeb132fa0b1ad8a5b957446c66a498e633af7
SRC=c0cba330fd485e52fcb90d5ccc69169edf9f0c2b
HEAD_SHA=2bef9e50489a60f216a8073a9f5ea0645752b33f
mkdir -p "$OUT/gates" "$OUT/suites"
run() { n=$1; shift; ( "$@" > "$OUT/$n.log" 2>&1; echo $? > "$OUT/$n.rc" ) & }

# 1. Composition: the merge is the automatic merge, and only the plan moved after it.
( cd "$CLONE" && git merge-tree --write-tree --messages $SRC $BASE; git rev-parse da341a154882a9aa28f7fb224ab82a71a66e5fb5^{tree}
  git diff da341a154882a9aa28f7fb224ab82a71a66e5fb5 $HEAD_SHA ) > "$OUT/composition.txt" 2>&1

# 2. Documentation gates at the head (pinned renderer interpreter).
cd "$CLONE"
run gates/docs_check "$PY" scripts/docs_check.py
run gates/em_dash "$PY" scripts/check_em_dash.py --base $BASE
run gates/em_dash_vs_c0cba330 "$PY" scripts/check_em_dash.py --base $SRC
run gates/em_dash_selftest "$PY" scripts/check_em_dash.py --selftest
run gates/gen_toc_check "$PY" scripts/gen_toc.py --check
run gates/gen_toc_anchors "$PY" scripts/gen_toc.py --verify-anchors
run gates/gen_toc_selftest "$PY" scripts/gen_toc.py --selftest
run gates/doc_style "$PY" scripts/check_doc_style.py
run gates/doc_style_selftest "$PY" scripts/check_doc_style.py --selftest
run gates/doc_paths "$PY" scripts/check_doc_paths.py
run gates/gptp_docs "$PY" scripts/check_gptp_docs.py
run gates/module_matrix "$PY" docs/traceability/gen_module_matrix.py --check
run gates/test_evidence python3 scripts/measure_test_evidence.py --check
run gates/diff_check git diff --check $BASE $HEAD_SHA
wait
# 3. Repository scanners that need the registered submodules.
run gates/check_port_contracts python3 scripts/check_port_contracts.py
run gates/check_todo_ownership python3 scripts/check_todo_ownership.py
run gates/check_hygiene python3 scripts/check_hygiene.py --check
run gates/measure_naming python3 scripts/measure_naming.py --check
run gates/measure_fail_fast python3 scripts/measure_fail_fast.py --check
run gates/sv_idiom python3 scripts/check_sv_idiom.py
wait
cd "$WT"
run gates/check_rtl_source_lists python3 scripts/check_rtl_source_lists.py
run gates/check_feature_status python3 scripts/check_feature_status.py
run gates/lint_rtl env PATH="$(dirname "$V"):$PATH" python3 scripts/lint_rtl.py --check
wait
# 4. Focused suites (each bounded; the round ran them in a git-less export and in WT).
run suites/csr env MAKEFLAGS=w make -j8 -C tb/verilator/csr VERILATOR="$V"
run suites/tcam_csr make -C tb/verilator/tcam_csr VERILATOR="$V"
run suites/milan_dp_mclk make -C tb/verilator/milan_dp_mclk VERILATOR="$V" VERILATOR_JOBS=6
wait
# milan_dp: `make run` builds every leg and runs gptp, gptp-lat and gmstep, then
# hands twelve binaries to sim_pool.py (ceiling --jobs=2). The round ran the
# pool in three subsets after the build; the true-ratio aclk leg did not finish.
( cd tb/verilator/milan_dp && timeout 570 make VERILATOR="$V" VERILATOR_JOBS=8 ) > "$OUT/suites/milan_dp_attempt1_timeout.log" 2>&1
cd tb/verilator/milan_dp
python3 sim_pool.py --jobs=2 ./obj_dir/Vmilan_dp_sim ./obj_notify/Vmilan_dp_notify ./obj_crflic/Vmilan_dp_crflic ./obj_dynmap/Vmilan_dp_dynmap > "$OUT/suites/milan_dp_pool1.log" 2>&1
python3 sim_pool.py --jobs=2 ./obj_nxn/Vmilan_dp_nxn ./obj_nxndv/Vmilan_dp_nxndv ./obj_nxn8/Vmilan_dp_nxn8 ./obj_nxn4c/Vmilan_dp_nxn4c > "$OUT/suites/milan_dp_pool2.log" 2>&1
timeout 585 python3 sim_pool.py --jobs=2 ./obj_nolpf/Vmilan_dp_nolpf ./obj_prune/Vmilan_dp_prune ./obj_ax1x1/Vmilan_dp_ax1x1 ./obj_aclk/Vmilan_dp_aclk > "$OUT/suites/milan_dp_pool3.log" 2>&1
