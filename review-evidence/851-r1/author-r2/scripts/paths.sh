#!/usr/bin/env bash
# paths.sh <routed.dcp> <out>: the worst setup and hold path of a routed checkpoint at every declared signoff corner,
# by report_timing (-max_paths 1 -nworst 1 -sort_by slack, over every path group), with the corner set-up taken from
# the platform declaration (sw/litex/platforms/ax7101_timing.py, the same hook the build and
# sw/litex/report_timing_grade.py use). Read-only: writes no checkpoint or bitstream. One Vivado run through the slot
# wrapper in its own scope. Writes <out>/<corner>_<T>C_worst_{setup,hold}.rpt, <out>/slacks.tsv (each corner's worst
# path slack beside get_timing_paths' worst slack) and <out>/rc.
set -u
dcp=$(readlink -f "$1"); out=$2
M=$HOME/milan-fpga-management/2026-09-23
REPO=$VALIDATION_STORAGE/scratch/851-a744b/gclone
mkdir -p "$out"; rm -f "$out/rc"
{
  echo "set_param general.maxThreads 8"
  echo "open_checkpoint {$dcp}"
  ( cd "$REPO/sw/litex" && python3 -c 'from platforms.ax7101_timing import configure_commands; print("\n".join(configure_commands()))' )
  cat <<EOF
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
EOF
} > "$out/paths.tcl"
cd "$out" || exit 2
bash "$M/vivado-slot.sh" systemd-run --user --scope --quiet --unit="milan-851-a744b-paths-$$" -p MemoryMax=10G \
  bash -c 'export PATH=$HOME/Xilinx/2026.1/Vivado/bin:$PATH; vivado -mode batch -nojournal -notrace -log paths.log -source paths.tcl > paths.out 2>&1'
rc=$?; echo "$rc" > "$out/rc"; exit $rc
