#!/bin/bash
# Usage: run_probes.sh <clone> <packet> -- detached reviewer probes, log/rc in receipts.
P=$2; S=$P/scratch
export PATH=$S/bin:$PATH VERILATOR=$S/bin/verilator TMPDIR=$S/tmp
( python3 -I "$P/scripts/reviewer_probes.py" "$1" "$S/probes" --jobs 6 >"$P/receipts/reviewer_probes.log" 2>&1; echo $? >"$P/receipts/reviewer_probes.rc" ) &
wait
