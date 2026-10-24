#!/usr/bin/env bash
# Elaborate milan_datapath at one shape with scratch copies (outside the tree) of the
# datapath, the AAF packetizer and KL_crf_tx that print the #773 derived constants as
# elaboration $info lines. Lint-only; nothing is built or written into the tree.
# usage: elab_constants.sh <lane> <scratch-dir> <shape-incdir-name> <-G...>...
set -euo pipefail
lane=$1; scratch=$2; shape=$3; shift 3
mkdir -p "$scratch"
cp "$lane/hdl/milan/milan_datapath.sv" "$scratch/dp.sv"
cp "$lane/hdl/ieee1722/aaf/KL_aaf_packetizer.sv" "$scratch/pkt.sv"
cp "$lane/hdl/ieee1722/crf/KL_crf_tx.sv" "$scratch/crf.sv"
python3 -I - "$scratch" <<'EOF'
import sys
from pathlib import Path
d = Path(sys.argv[1])
def patch(name, anchor, text):
    p = d / name
    s = p.read_text()
    assert s.count(anchor) >= 1, (name, anchor)
    p.write_text(s.replace(anchor, text + anchor, 1))
patch('dp.sv', "  wire [63:0] aaf_tbase_w;\n  KL_aaf_packetizer",
      '  if (1) begin : g_dbg773\n'
      '    $info("DBG773 DP B=%0d SPAN=%0d AGE=%0d WALK=%0d AAF_IN=%0d CRF_EV=%0d",\n'
      '          DOM_MARK_LAT_NS_C, TLK_SPAN_NS_C, TLK_AGE_CYC_C, TLK_WALK_CYC_C, TLK_AAF_IN_NS_C,\n'
      '          TLK_CRF_EV_NS_C);\n'
      '  end\n')
patch('pkt.sv', "  localparam int unsigned TIDXW_C = (N_TALKERS_P <= 1) ? 1",
      '  if (LEAD_P) begin : g_dbg773\n'
      '    $info("DBG773 PKT PIPE=%0d LATE=%0d DELAY_PER=%0d LEAD_NS=%0d", PIPE_CYC_C, LATE_NS_C, DELAY_PER_C, LEAD_NS_C);\n'
      '  end\n')
patch('crf.sv', "  if (TC_P && CLK_HZ_P == 0) begin : g_tc_clock",
      '  if (TC_P) begin : g_dbg773\n'
      '    $info("DBG773 CRF PIPE=%0d LATE=%0d TC_PER=%0d TC_NS=%0d", PIPE_CYC_C, LATE_NS_C, TC_PER_C, TC_NS_C);\n'
      '  end\n')
EOF
cd "$lane/tb/verilator/milan_dp"
srcs=$(make -s --no-print-directory print-srcs DP_SRC="$scratch/dp.sv")
list=()
for f in $srcs; do
  case "$f" in
    */KL_aaf_packetizer.sv) list+=("$scratch/pkt.sv");;
    */KL_crf_tx.sv) list+=("$scratch/crf.sv");;
    *) list+=("$f");;
  esac
done
incs=()
for f in $(make -s --no-print-directory print-dp-vflags); do
  case "$f" in +incdir+*|-G*) incs+=("$f");; esac
done
verilator --lint-only -Wno-fatal -Wno-lint -Wno-style --top-module milan_datapath \
  "${incs[@]}" "+incdir+../../../configs/generated/$shape" "$@" "${list[@]}" 2>&1 \
  | grep -E "DBG773|%Error" || true
