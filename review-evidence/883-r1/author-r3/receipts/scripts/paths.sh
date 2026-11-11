#!/usr/bin/env bash
# paths.sh <routed.dcp> <out> <repo>: the worst setup and hold path of a routed checkpoint at every declared signoff
# corner, by report_timing, with the corner set-up from sw/litex/platforms/ax7101_timing.py. Read-only. One Vivado run
# through the slot wrapper in its own scope. Writes <out>/<corner>_<T>C_worst_{setup,hold}.rpt, <out>/slacks.tsv, <out>/rc.
set -u
dcp=$(readlink -f "$1"); out=$2; REPO=$3
M=<mgmt>/2026-09-23
mkdir -p "$out"; rm -f "$out/rc"
{
  echo "set_param general.maxThreads 8"
  echo "open_checkpoint {$dcp}"
  ( cd "$REPO/sw/litex" && python3 -c 'from platforms.ax7101_timing import configure_commands; print("\n".join(configure_commands()))' )
  cat <<EOT
set f [open {$out/slacks.tsv} w]
puts \$f "corner\tsetup_slack_ns\thold_slack_ns\tsetup_levels"
foreach temp {0 85} {
  set_operating_conditions -junction_temp \$temp
  foreach corner {Slow Fast} {
    config_timing_corners -corner \$corner -delay_type min_max
    foreach other {Slow Fast} { if {\$other ne \$corner} { config_timing_corners -corner \$other -delay_type none } }
    set stem "$out/\${corner}_\${temp}C"
    report_timing -delay_type max -max_paths 1 -nworst 1 -sort_by slack -input_pins -file \${stem}_worst_setup.rpt
    report_timing -delay_type min -max_paths 1 -nworst 1 -sort_by slack -input_pins -file \${stem}_worst_hold.rpt
    set s [get_timing_paths -delay_type max -max_paths 1 -nworst 1 -sort_by slack]
    set h [get_timing_paths -delay_type min -max_paths 1 -nworst 1 -sort_by slack]
    puts \$f "\${corner}_\${temp}C\t[get_property SLACK \$s]\t[get_property SLACK \$h]\t[expr {[catch {get_property LOGIC_LEVELS \$s} l] ? "na" : \$l}]"
  }
}
close \$f
exit
EOT
} > "$out/paths.tcl"
cd "$out" || exit 2
bash "$M/vivado-slot.sh" systemd-run --user --scope --quiet --unit="milan-883-a768-paths-$$" -p MemoryMax=10G \
  bash -c 'export PATH=<xilinx>/2026.1/Vivado/bin:$PATH; vivado -mode batch -nojournal -notrace -log paths.log -source paths.tcl > paths.out 2>&1'
rc=$?; echo "$rc" > "$out/rc"; exit $rc
