#!/bin/bash
# KL_mbx out of context, MAILBOX_SPLIT.md "Measured area" recipe (tb_mbx_top, HOST_P=0,
# xc7a100tfgg484-2, 10 ns, synth + opt + place + route), at each revision given, one after
# the other. Each revision's sources are exported with `git show` into its own directory,
# so the lane tree can change while this runs. Run only under the exclusive Vivado lock:
#   setsid nohup flock $VIVADO_LOCK bash kl_mbx_ooc.sh <repo> <work> <rev>... > log 2>&1 &
set -eu
REPO=$1 W=$2; shift 2
SETTINGS=$WORKSPACE_HOME/Xilinx/2026.1/Vivado/settings64.sh
FILES="hdl/milan/mailbox/KL_mbx_pkg.sv hdl/milan/mailbox/KL_mbx_ring.sv hdl/milan/mailbox/KL_mbx_rx.sv
hdl/milan/mailbox/KL_mbx_tx.sv hdl/milan/mailbox/KL_mbx_evt.sv hdl/milan/mailbox/KL_mbx.sv
hdl/milan/mailbox/KL_mbx_wb.sv hdl/milan/mailbox/KL_mbx_axil.sv tb/verilator/mbx/tb_mbx_top.sv"
source "$SETTINGS"
for rev in "$@"; do
    sha=$(git -C "$REPO" rev-parse "$rev")
    d="$W/ooc-${sha:0:8}"
    [ -e "$d" ] && { echo "$d exists"; exit 2; }
    mkdir -p "$d/hdl/milan/mailbox" "$d/tb/verilator/mbx"
    for f in $FILES; do git -C "$REPO" show "$sha:$f" > "$d/$f"; done
    (cd "$d" && sha256sum $FILES > sources.sha256)
    cat > "$d/ooc.tcl" <<'EOF'
read_verilog -sv [list hdl/milan/mailbox/KL_mbx_pkg.sv hdl/milan/mailbox/KL_mbx_ring.sv \
  hdl/milan/mailbox/KL_mbx_rx.sv hdl/milan/mailbox/KL_mbx_tx.sv hdl/milan/mailbox/KL_mbx_evt.sv \
  hdl/milan/mailbox/KL_mbx.sv hdl/milan/mailbox/KL_mbx_wb.sv hdl/milan/mailbox/KL_mbx_axil.sv \
  tb/verilator/mbx/tb_mbx_top.sv]
synth_design -mode out_of_context -top tb_mbx_top -part xc7a100tfgg484-2 -generic HOST_P=0
create_clock -period 10.000 -name clk [get_ports clk_i]
opt_design
place_design
route_design
report_utilization -hierarchical -file util_hier.rpt
report_utilization -file util.rpt
report_timing_summary -delay_type max -file timing.rpt
report_route_status -file route.rpt
EOF
    echo "== $rev $sha start $(date -Is)"
    rc=0
    (cd "$d" && vivado -mode batch -nojournal -source ooc.tcl > vivado.out 2>&1) || rc=$?
    echo "== $rev $sha rc=$rc end $(date -Is)"
done
