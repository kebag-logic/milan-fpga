#!/bin/sh
# SPDX-License-Identifier: CERN-OHL-W-2.0
# probe_all.sh: the committed aecp_notify and pp_top suites against the head file
# (none) and against each reviewer control; three probes at a time.
P=$(cd "$(dirname "$0")/.." && pwd)
L=$P/scratch/lockstep/controls
printf '%s\n' none $L/override_set_only.sv $L/own_vs_new_row.sv $L/override_clr_only.sv \
  $L/reindex_late.sv $L/stamp_read_without_valid.sv $L/first_chunk_ignored.sv $L/key_swapped.sv |
xargs -P 3 -I{} sh -c 'n=$(basename {} .sv); "$0"/scripts/probe_committed.sh "$0"/scratch/head {} "$0"/scratch/probe/$n aecp_notify pp_top > "$0"/receipts/probe_$n.txt 2>&1' $P
