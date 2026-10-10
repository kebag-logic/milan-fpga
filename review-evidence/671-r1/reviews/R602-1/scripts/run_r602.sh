#!/bin/sh
# R602-1 reviewer commands for #671 / PR #715 at f54dbe3e393e2b1b027f1825c4acb736cf502cda.
# CLONE is a clean checkout of that head (protocol-processor, gptp-processor and
# third_party/verilog-axis initialised); PACKET is this packet; PINNED_VERILATOR_DIR
# holds the pinned Verilator 5.050 wrapper. Each step writes its log and rc file.
set -u
: "${CLONE:?}" "${PACKET:?}" "${PINNED_VERILATOR_DIR:?}"
R="$PACKET/receipts"; S="$PACKET/scratch"; mkdir -p "$R" "$S/tmp" "$S/base"
export PYTHONDONTWRITEBYTECODE=1 TMPDIR="$S/tmp"
cd "$CLONE" || exit 2
git show e8454e2751d05b02ee8e5a571857589ab358ab86:sw/firmware/milan_baremetal/milan_baremetal.c > "$S/base/milan_baremetal.c"

# 1. the writer gate with its planted controls, every shipped shape
python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test > "$R/hosttest_selftest_head.log" 2>&1; echo $? > "$R/hosttest_selftest_head.rc"
# 2. the co-simulation suite, pinned Verilator
PATH="$PINNED_VERILATOR_DIR:$PATH" make -C tb/verilator/nvm_cosim run PYTHON=python3 JOBS=6 POOL=6 > "$R/nvm_cosim_run.log" 2>&1; echo $? > "$R/nvm_cosim_run.rc"
# 3. reviewer probes on both product shapes
for c in endstation_ax7101_1x1_tdm8 endstation_ax7101_8x8; do
  for p in base_repro plants scenarios extra_plants; do
    python3 -I "$PACKET/scripts/r602_probes.py" "$CLONE" "$S/probe_${p}_$c" "$c" "$p" "$S/base/milan_baremetal.c" \
      > "$R/probe_${p}_$c.log" 2>&1; echo $? > "$R/probe_${p}_$c.rc"
  done
done
# 4. capture receipt and documentation gates (the em-dash and TOC gates need
#    tools/markdown/requirements.txt installed with --require-hashes)
(cd scripts && python3 check_nvm_capture.py) > "$R/check_nvm_capture_head.log" 2>&1; echo "rc=$?" >> "$R/check_nvm_capture_head.log"
python3 scripts/docs_check.py > "$R/docs_check_head.log" 2>&1; echo "rc=$?" >> "$R/docs_check_head.log"
python3 scripts/check_em_dash.py --base e8454e2751d05b02ee8e5a571857589ab358ab86 > "$R/em_dash_head.log" 2>&1; echo "rc=$?" >> "$R/em_dash_head.log"
python3 scripts/gen_toc.py --check > "$R/gen_toc_check_head.log" 2>&1; echo "rc=$?" >> "$R/gen_toc_check_head.log"
python3 scripts/check_doc_style.py > "$R/doc_style_head.log" 2>&1; echo "rc=$?" >> "$R/doc_style_head.log"
