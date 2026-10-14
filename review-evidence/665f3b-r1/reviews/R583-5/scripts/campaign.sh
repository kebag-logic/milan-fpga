#!/bin/sh
# R583-5 focused campaign: run independent checks concurrently, one log and rc file each.
# Usage: campaign.sh <clone> <packet>
# Superseded in part, kept as run: its service_bounds line needs the harness path (the arm runs
# inside fw_shard0), its em_dash line needs the pinned Markdown renderer, and its fw_shard0 job was
# invalidated by a build-directory collision. rerun.sh holds the commands as finally counted.
set -u
CLONE=$1
PKT=$2
R=$PKT/receipts/campaign
S=$PKT/scratch
mkdir -p "$R" "$S/tmp"
export TMPDIR=$S/tmp
export VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator
export PYTHONDONTWRITEBYTECODE=1
cd "$CLONE" || exit 2
job() { name=$1; shift; ( "$@" >"$R/$name.log" 2>&1; echo $? >"$R/$name.rc" ) & }
job ci_scope_selftest python3 scripts/ci_scope.py --selftest
job ci_events_check python3 scripts/ci_events.py --check
job service_bounds python3 sw/firmware/ctrl/test/ctrl_service_bounds.py
job maap_differential python3 sw/firmware/ctrl/test/maap_differential.py --self-test --keep "$S/maapdiff"
job fw_shard0 python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 0/4 --build-dir "$S/fw0"
job doc_style python3 scripts/check_doc_style.py
job doc_map python3 docs/DOC_MAP.gen.py --check
job em_dash python3 scripts/check_em_dash.py --base 6b4feeca5d2fab0ec35cf071322cc775a5b15cb5
echo started
