#!/bin/bash
# The split CPU and its firmware memory out of context (ooc_soc.py's top `sim`: the product split CPU netlist,
# rom and sram from the 1x1 image, the CPU's LiteDRAM crossing brought out to pins), synthesized with the
# L11b core-pricing directive (AreaOptimized_high, xc7a100t-fgg484-2) and placed and routed with the CPU clock
# (milan_clk, the generator's cpu_clk) at CPU_PERIOD_NS and the bus (sys_clk, its litex_clk) at BUS_PERIOD_NS
# (10 ns, the shipping 100 MHz, when not given),
# asynchronous, the generator's and LiteX's own crossings between them. One run per period, each in its own
# directory with its sources hashed. Run only under the exclusive Vivado lock, as its own unit:
#   flock -x $VIVADO_LOCK bash ooc_route.sh WORK GATEWARE_DIR NETLIST.v CPU_PERIOD_NS[/BUS_PERIOD_NS]...
set -u
W=$1 G=$2 NET=$3; shift 3
source $WORKSPACE_HOME/Xilinx/2026.1/Vivado/settings64.sh
V=$(dirname "$NET")
for spec in "$@"; do
    period=${spec%%/*} bus=10.000
    [ "$spec" != "$period" ] && bus=${spec#*/}
    d="$W/ooc-$period"
    [ "$bus" != 10.000 ] && d="$W/ooc-$period-bus-$bus"
    [ -e "$d" ] && { echo "$d exists"; exit 2; }
    mkdir -p "$d"
    cp "$G/sim.v" "$G"/*.init "$NET" "$V/Ram_1w_1rs_Generic.v" "$V/Ram_1w_1ra_Generic.v" "$d/"
    (cd "$d" && sha256sum sim.v ./*.init "$(basename "$NET")" Ram_1w_1rs_Generic.v Ram_1w_1ra_Generic.v > sources.sha256)
    cat > "$d/ooc.tcl" <<EOF
set_param general.maxThreads 8
read_verilog [list Ram_1w_1rs_Generic.v Ram_1w_1ra_Generic.v $(basename "$NET") sim.v]
synth_design -mode out_of_context -directive AreaOptimized_high -part xc7a100t-fgg484-2 -top sim
report_utilization -file synth_util.rpt
create_clock -period $period -name cpu_clk [get_ports milan_clk]
create_clock -period $bus -name litex_clk [get_ports sys_clk]
set_clock_groups -asynchronous -group cpu_clk -group litex_clk
opt_design
place_design
route_design
report_utilization -file route_util.rpt
report_utilization -hierarchical -hierarchical_depth 4 -hierarchical_min_primitive_count 0 -file route_hier.rpt
report_timing_summary -delay_type min_max -file timing.rpt
report_timing -delay_type max -max_paths 10 -group cpu_clk -file paths_cpu.rpt
report_timing -delay_type max -max_paths 10 -group litex_clk -file paths_bus.rpt
report_route_status -file route.rpt
puts "ROUTED cpu_clk $period ns litex_clk $bus ns"
EOF
    echo "== $(basename "$d") start $(date -Is) memavail_kb=$(awk '/MemAvailable/{print $2}' /proc/meminfo)"
    rc=0
    (cd "$d" && vivado -mode batch -nojournal -log vivado.log -source ooc.tcl > vivado.out 2>&1) || rc=$?
    echo "$rc" > "$d/rc"
    echo "== $(basename "$d") rc=$rc end $(date -Is)"
done
