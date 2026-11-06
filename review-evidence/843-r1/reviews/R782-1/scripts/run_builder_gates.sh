#!/usr/bin/env bash
# The builder gates this change touches, in three concurrent groups on three
# disposable copies of the exact head (the bank writes under sw/builder/out).
# usage: run_builder_gates.sh <scratch-dir> <log-dir>
set -u
scratch=$1; logs=$2
mkdir -p "$logs"
run() { local n=$1 copy=$2 gates=$3
  ( cd "$scratch/$copy" && PYTHONUNBUFFERED=1 python3 sw/builder/test_builder.py --gates "$gates" > "$logs/$n.log" 2>&1; echo $? > "$logs/$n.rc" ) ; }
run builder_26b_26c run-a test_model_id_hashing,test_gptp_dataset_matches_engine_announce,test_gptp_clock_accuracy_per_board,test_builder_doc_key_map &
run builder_1b run-b test_baremetal_profile_contract &
run builder_rom_clock run-c test_rom_clock_contract &
wait
for n in builder_26b_26c builder_1b builder_rom_clock; do printf '%s rc=%s\n' "$n" "$(cat "$logs/$n.rc" 2>/dev/null)"; done
