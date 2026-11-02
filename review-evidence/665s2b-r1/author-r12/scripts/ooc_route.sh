#!/bin/bash
# The split CPU and its firmware memory out of context (ooc_soc.py's top `sim`: the product split CPU netlist on
# the bus clock with no CPU clock of its own, rom and sram from the 1x1 image, the CPU's LiteDRAM port brought out
# to pins), synthesized with the L11b core-pricing directive (AreaOptimized_high, xc7a100t-fgg484-2) and placed
# and routed with sys_clk, the one clock the CPU, its memory and its bus run on, at PERIOD_NS (10 ns: 100 MHz).
# The top's milan_clk port clocks nothing (the test SoC has no datapath) and is left unconstrained. One run per
# period, each in its own directory with its sources hashed. Run only under the exclusive Vivado lock:
#   setsid nohup flock $VIVADO_LOCK bash ooc_route.sh WORK GATEWARE_DIR NETLIST.v PERIOD_NS... > log 2>&1 &
set -u
W=$1 G=$2 NET=$3; shift 3
source $WORKSPACE_HOME/Xilinx/2026.1/Vivado/settings64.sh
V=$(dirname "$NET")
for period in "$@"; do
    d="$W/ooc-sys-$period"
    [ -e "$d" ] && { echo "$d exists"; exit 2; }
    mkdir -p "$d"
    cp "$G/sim.v" "$G"/*.init "$NET" "$V/Ram_1w_1rs_Generic.v" "$V/Ram_1w_1ra_Generic.v" "$d/"
    (cd "$d" && sha256sum sim.v ./*.init "$(basename "$NET")" Ram_1w_1rs_Generic.v Ram_1w_1ra_Generic.v > sources.sha256)
    {
        echo "set_param general.maxThreads 8"
        echo "read_verilog [list Ram_1w_1rs_Generic.v Ram_1w_1ra_Generic.v $(basename "$NET") sim.v]"
        echo "synth_design -mode out_of_context -directive AreaOptimized_high -part xc7a100t-fgg484-2 -top sim"
        echo "report_utilization -file synth_util.rpt"
        echo "create_clock -period $period -name sys_clk [get_ports sys_clk]"
        echo "opt_design"
        echo "place_design"
        echo "route_design"
        echo "report_utilization -file route_util.rpt"
        echo "report_utilization -hierarchical -hierarchical_depth 4 -hierarchical_min_primitive_count 0 -file route_hier.rpt"
        echo "report_timing_summary -delay_type min_max -file timing.rpt"
        echo "report_timing -delay_type max -max_paths 10 -group sys_clk -file paths_sys.rpt"
        echo "report_clock_interaction -file clock_interaction.rpt"
        echo "report_route_status -file route.rpt"
        echo "puts \"ROUTED sys_clk $period ns\""
    } > "$d/ooc.tcl"
    echo "== $(basename "$d") start $(date -Is) memavail_kb=$(awk '/MemAvailable/{print $2}' /proc/meminfo)"
    rc=0
    (cd "$d" && vivado -mode batch -nojournal -log vivado.log -source ooc.tcl > vivado.out 2>&1) || rc=$?
    echo "$rc" > "$d/rc"
    echo "== $(basename "$d") rc=$rc end $(date -Is)"
done
