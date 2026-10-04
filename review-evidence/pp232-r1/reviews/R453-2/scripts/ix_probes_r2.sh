#!/bin/sh
# SPDX-License-Identifier: CERN-OHL-W-2.0
# ix_probes_r2.sh: [R453-2] round-2 extras around the unchanged round-1 probe script.
#  1. every round-1 control (scratch/lockstep/controls/*.sv, planted unchanged by
#     scripts/lockstep/make_controls.py) through the committed tb/aecp_notify only,
#     by the unchanged scripts/probe_committed.sh, four at a time;
#  2. the head's tb/aecp_notify against main 83999eba's KL_aecp_notify.sv (the new
#     IX5/IX6/TS checks must pass on unchanged behaviour) and against f4167536's.
# Receipts: receipts/ix_ctl_<name>.txt, receipts/ix_on_main_<rev>.txt
P=$(cd "$(dirname "$0")/.." && pwd)
L=$P/scratch/lockstep/controls
ls "$L"/*.sv | xargs -P 4 -I{} sh -c 'n=$(basename {} .sv); "$0"/scripts/probe_committed.sh "$0"/scratch/head {} "$0"/scratch/ixprobe/$n aecp_notify > "$0"/receipts/ix_ctl_$n.txt 2>&1; grep -E "^ *(FAIL|PASS)" "$0"/scratch/ixprobe/$n/aecp_notify.log >> "$0"/receipts/ix_ctl_$n.txt' "$P"
for rev in main:83999eba f4167536:f4167536; do
  name=${rev%%:*}; sha=${rev#*:}
  git -C "$P/../r453-2-pp232" show "$sha:hdl/aecp/KL_aecp_notify.sv" > "$P/scratch/notify_$name.sv"
  "$P"/scripts/probe_committed.sh "$P"/scratch/head "$P/scratch/notify_$name.sv" "$P/scratch/ixmain/$name" aecp_notify \
    > "$P/receipts/ix_on_main_$name.txt" 2>&1
  grep -E "^ *(FAIL|PASS)" "$P/scratch/ixmain/$name/aecp_notify.log" >> "$P/receipts/ix_on_main_$name.txt"
done
echo done
