#!/usr/bin/env bash
# Run keep.tcl, boundary.tcl and loads.tcl (u_dyn and u_srp) sequentially on one
# checkpoint, detached; caller polls <outdir>/probes_rc.txt.
# Usage: run_probes_detached.sh <probe-dir> <dcp> <outdir> <tag>
set -euo pipefail
probes="$1"; dcp="$2"; out="$3"; tag="$4"
mkdir -p "$out"; cd "$out"; rm -f probes_rc.txt
setsid nohup bash -c '
export PATH=${VIVADO_BIN:?set VIVADO_BIN to the Vivado 2026.1 bin directory}:$PATH
p="$0"; d="$1"; t="$2"; rc=0
vivado -mode batch -nojournal -log keep.log -source "$p/keep.tcl" -tclargs "$d" "keep_$t.txt" > /dev/null 2>&1 || rc=1
vivado -mode batch -nojournal -log boundary.log -source "$p/boundary.tcl" -tclargs "$d" "boundary_$t.tsv" > /dev/null 2>&1 || rc=1
vivado -mode batch -nojournal -log loads_udyn.log -source "$p/loads.tcl" -tclargs "$d" milan_datapath/pp_shadow/u_pp/u_aecp/u_dyn "loads_udyn_$t.tsv" > /dev/null 2>&1 || rc=1
vivado -mode batch -nojournal -log loads_srp.log -source "$p/loads.tcl" -tclargs "$d" milan_datapath/pp_shadow/u_pp/u_srp "loads_srp_$t.tsv" > /dev/null 2>&1 || rc=1
vivado -mode batch -nojournal -log loads_wrapper.log -source "$p/loads.tcl" -tclargs "$d" milan_datapath/pp_shadow "loads_wrapper_$t.tsv" > /dev/null 2>&1 || rc=1
echo $rc > probes_rc.txt' "$probes" "$dcp" "$tag" < /dev/null > /dev/null 2>&1 &
echo "launched pid $!"
