#!/usr/bin/env bash
# Reviewer probe runner: run each mutated copy's self-test beside an
# unmutated control, concurrently, one log and one rc file per run.
# Usage: run_probes.sh <scratch-dir> <log-dir> <python>
set -u
S=$1
L=$2
PY=$3
export PYTHONDONTWRITEBYTECODE=1
mkdir -p "$L"

run() { # name, working directory, command...
    local name=$1 dir=$2
    shift 2
    (
        cd "$dir" || exit 97
        "$@" > "$L/$name.log" 2>&1
        echo $? > "$L/$name.rc"
    ) &
}

run control-baremetal_selftest "$S/probe" "$PY" scripts/check_baremetal_only.py --selftest
run m1-baremetal_selftest "$S/m1" "$PY" scripts/check_baremetal_only.py --selftest
run control-avtp_wire_truth "$S/probe" "$PY" tb/tools/avtp_wire_truth.py --self-test
run m2-avtp_wire_truth "$S/m2" "$PY" tb/tools/avtp_wire_truth.py --self-test
run control-behave_wire_truth "$S/probe/tests" "$PY" -m behave --no-capture -f plain features/wire_truth_avtp.feature
run m2-behave_wire_truth "$S/m2/tests" "$PY" -m behave --no-capture -f plain features/wire_truth_avtp.feature
run control-torture_campaign "$S/probe" "$PY" tb/tools/torture_campaign.py --self-test
run m3-torture_campaign "$S/m3" "$PY" tb/tools/torture_campaign.py --self-test
wait

for f in "$L"/*.rc; do
    n=$(basename "$f" .rc)
    printf '%s\trc=%s\t%s\n' "$n" "$(cat "$f")" "$(tail -n 1 "$L/$n.log" | cut -c1-160)"
done
