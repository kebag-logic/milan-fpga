#!/usr/bin/env bash
# Run the code gates of lane 730 in parallel; one log and one rc file per gate.
set -u
G=$1
cd $LANES/730-act-cpusets || exit 2
mkdir -p "$G"
export PATH=$VALIDATION_STORAGE/730-a607/venv312/bin:$PATH
run() { local name=$1; shift; ( "$@" > "$G/$name.log" 2>&1; echo $? > "$G/$name.rc" ) & }
run act-ci-selftest python3 scripts/act_ci.py --selftest
run ci-events-check python3 scripts/ci_events.py --check
run ci-events-selftest python3 scripts/ci_events.py --selftest
run slot-proof-selftest scripts/act_slot_proof.sh --selftest
run py-idiom python3 scripts/check_py_idiom.py
run py-idiom-selftest python3 scripts/check_py_idiom.py --selftest
run baremetal-check python3 scripts/check_baremetal_only.py --check
run baremetal-selftest python3 scripts/check_baremetal_only.py --selftest
run diff-check git diff --check dc4d06cb
wait
python3 --version
for f in "$G"/*.rc; do echo "$(basename "$f" .rc) rc=$(cat "$f") | $(tail -1 "${f%.rc}.log" | cut -c1-110)"; done
