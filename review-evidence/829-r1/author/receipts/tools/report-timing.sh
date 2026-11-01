#!/usr/bin/env bash
# report-timing.sh <shape> <build>: signoff reports of a routed Arty checkpoint, both Slow and
# Fast models at both commercial endpoints, using the repository's timing_grade.tcl with the
# Arty's part. Read-only on the checkpoint; the AX7101 wrapper refuses another part.
set -u
shape=$1 build=$2
lane=$VALIDATION_STORAGE/829-a725/wt-bench
out=$VALIDATION_STORAGE/829-a725b/timing/$shape
mkdir -p "$out"
cat > "$out/report.tcl" <<TCL
set_param general.maxThreads 16
open_checkpoint {$build/gateware/digilent_arty_route.dcp}
source {$lane/sw/litex/timing_grade.tcl}
kl_timing_grade_configure {xc7a100tcsg324-1} {commercial} {0} {85} {Slow Fast}
kl_timing_grade_reports {$out/signoff}
report_utilization -file {$out/utilization.rpt}
report_route_status -file {$out/route_status.rpt}
exit
TCL
cd "$out" || exit 3
source $WORKSPACE_HOME/Xilinx2/2026.1/Vivado/settings64.sh
timeout --foreground 1500 vivado -mode batch -nojournal -notrace -log timing.log -source report.tcl > vivado.out 2>&1
rc=$?
echo "$rc" > "$out/rc"
echo "== END-OF-TIMING shape=$shape rc=$rc $(date -Iseconds)"
