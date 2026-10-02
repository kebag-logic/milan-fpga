#!/bin/sh
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
# R433-3 campaign: independent jobs on disposable copies of the exact head,
# run concurrently in ONE foreground invocation, each with its own log and rc.
# Usage: campaign.sh <packet dir>
#   expects <packet>/scratch/{hA,hB,hC,hD,hE} (copies of the head checkout),
#   <packet>/scratch/m43bin/make (GNU make 4.3 built from the GNU tarball,
#   sha256 e05fdde47c5f7ca45cb697e973894ff4f5d79e13b750ed57d7b66d8defc78e19),
#   and the unchanged prior-review scripts in <packet>/scripts/.
P=$(cd "$1" && pwd); S=$P/scratch; R=$P/receipts
mkdir -p "$R"
VDIR=$VALIDATION_TOOLS/pinned-verilator-5.050
export PATH="$VDIR:$PATH" VERILATOR_JOBS=4
job() { name=$1; shift; ( "$@" > "$R/$name.log" 2>&1; echo $? > "$R/$name.rc" ) & }
job make43_checks       sh "$P/scripts/make43_checks.sh" "$S/hA" "$S/m43bin"
job r433_2_meter_probes python3 "$P/scripts/meter_probes.py" "$S/hB" "$S/probes433"
job r432_2_meter_probes python3 "$P/scripts/reviewer_meter_probes_r2.py" "$S/hC" "$S/probes432" 4
job meter_suite         make -C "$S/hD/tb/verilator/aaf_clock_meter"
job gate_plain_make43   env PATH="$S/m43bin:$PATH" sh -c "cd '$S/hE' && make --version | head -1 && python3 scripts/check_entity_shape.py"
wait
for f in "$R"/*.rc; do printf '%s rc=%s\n' "$(basename "$f" .rc)" "$(cat "$f")"; done
