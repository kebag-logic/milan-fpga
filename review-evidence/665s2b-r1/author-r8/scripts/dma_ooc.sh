#!/bin/bash
# The record mover out of context with the mailbox's recipe (MAILBOX_SPLIT.md: xc7a100tfgg484-2, 10 ns, default
# directives), its sources copied from a checkout and hashed first. Run only under the exclusive Vivado lock.
# usage: dma_ooc.sh WORK CHECKOUT
set -u
W=$1 T=$2
source $WORKSPACE_HOME/Xilinx/2026.1/Vivado/settings64.sh
d="$W/dma-ooc"
[ -e "$d" ] && { echo "$d exists"; exit 2; }
mkdir -p "$d/src"
for f in hdl/milan/mailbox/KL_mbx_pkg.sv hdl/milan/mailbox/KL_mbx_dma.sv; do cp "$T/$f" "$d/src/"; done
(cd "$d" && sha256sum src/* > sources.sha256 && git -C "$T" rev-parse HEAD > head.txt)
cat > "$d/ooc.tcl" <<TCL
set_param general.maxThreads 4
read_verilog -sv [list src/KL_mbx_pkg.sv src/KL_mbx_dma.sv]
synth_design -mode out_of_context -top KL_mbx_dma -part xc7a100tfgg484-2
report_utilization -file synth_util.rpt
create_clock -period 10.000 -name clk [get_ports clk_i]
opt_design
place_design
route_design
report_utilization -file route_util.rpt
report_timing_summary -delay_type min_max -file timing.rpt
report_route_status -file route.rpt
puts "PRICED KL_mbx_dma"
TCL
echo "== dma-ooc start $(date -Is) memavail_kb=$(awk '/MemAvailable/{print $2}' /proc/meminfo)"
rc=0
(cd "$d" && vivado -mode batch -nojournal -log vivado.log -source ooc.tcl > vivado.out 2>&1) || rc=$?
echo "$rc" > "$d/rc"
echo "== dma-ooc rc=$rc end $(date -Is)"
