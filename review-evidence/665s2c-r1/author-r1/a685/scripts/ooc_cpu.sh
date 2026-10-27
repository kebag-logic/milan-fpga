#!/bin/bash
# The CPU netlists out of context, one after the other, with the L11b core-pricing synthesis
# (docs/design/MARK_II_AREA_PLAN.md "Reproduce L11b core pricing": AreaOptimized_high,
# xc7a100t-fgg484-2, no constraint), then the same synthesis placed and routed at the shipping
# clocks (cpu_clk 20 ns, the 50 MHz CPU; litex_clk 10 ns, the 100 MHz bus; asynchronous, the
# core's own crossing) for timing. Each netlist is copied with its two RAM models into its own
# directory and hashed first. Run only under the exclusive Vivado lock:
#   setsid nohup flock $VIVADO_LOCK bash ooc_cpu.sh WORK NETLIST.v... > log 2>&1 &
set -u
W=$1; shift
source $WORKSPACE_HOME/Xilinx/2026.1/Vivado/settings64.sh
for net in "$@"; do
    top=$(basename "$net" .v)
    d="$W/$top"
    [ -e "$d" ] && { echo "$d exists"; exit 2; }
    mkdir -p "$d"
    cp "$net" "$(dirname "$net")/Ram_1w_1rs_Generic.v" "$(dirname "$net")/Ram_1w_1ra_Generic.v" "$d/"
    (cd "$d" && sha256sum "$top.v" Ram_1w_1rs_Generic.v Ram_1w_1ra_Generic.v > sources.sha256)
    cat > "$d/ooc.tcl" <<EOF
set_param general.maxThreads 8
read_verilog [list Ram_1w_1rs_Generic.v Ram_1w_1ra_Generic.v $top.v]
synth_design -mode out_of_context -directive AreaOptimized_high -part xc7a100t-fgg484-2 -top $top
report_utilization -file synth_util.rpt
report_utilization -hierarchical -hierarchical_depth 4 -hierarchical_min_primitive_count 0 -file synth_hier.rpt
create_clock -period 20.000 -name cpu_clk [get_ports cpu_clk]
create_clock -period 10.000 -name litex_clk [get_ports litex_clk]
set_clock_groups -asynchronous -group cpu_clk -group litex_clk
opt_design
place_design
route_design
report_utilization -file route_util.rpt
report_utilization -hierarchical -hierarchical_depth 4 -hierarchical_min_primitive_count 0 -file route_hier.rpt
report_timing_summary -delay_type min_max -file timing.rpt
report_route_status -file route.rpt
puts "PRICED $top"
EOF
    echo "== $top start $(date -Is) memavail_kb=$(awk '/MemAvailable/{print $2}' /proc/meminfo)"
    rc=0
    (cd "$d" && vivado -mode batch -nojournal -log vivado.log -source ooc.tcl > vivado.out 2>&1) || rc=$?
    echo "$rc" > "$d/rc"
    echo "== $top rc=$rc end $(date -Is)"
done
