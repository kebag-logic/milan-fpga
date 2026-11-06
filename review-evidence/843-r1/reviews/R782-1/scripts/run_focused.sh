#!/usr/bin/env bash
# Focused reviewer runs on disposable copies of the exact head. Each step
# writes <logs>/<name>.log and <logs>/<name>.rc. Chains run concurrently and
# the script waits for all of them (it is run in the foreground).
# usage: run_focused.sh <scratch-dir> <log-dir> <verilator> <chain>...
#   chain a: milan_dp gptp leg, then gptp_shadow       (copy run-a)
#   chain b: milan_dp gptp-lat leg, then gptp_plane    (copy run-b)
#   chain c: builder gates, fw_service_budget, docs inventory (copy run-c)
set -u
scratch=$1; logs=$2; V=$3; shift 3
mkdir -p "$logs"
step() { local n=$1; shift; "$@" > "$logs/$n.log" 2>&1; echo $? > "$logs/$n.rc"; }
chain() {
  case $1 in
    a) cd "$scratch/run-a" || return 2
       step milan_dp_gptp make -C tb/verilator/milan_dp gptp VERILATOR="$V" VERILATOR_JOBS=4
       step gptp_shadow make -C tb/verilator/gptp_shadow run VERILATOR="$V" VERILATOR_JOBS=2 ;;
    b) cd "$scratch/run-b" || return 2
       step milan_dp_gptp_lat make -C tb/verilator/milan_dp gptp-lat VERILATOR="$V" VERILATOR_JOBS=4
       step gptp_plane make -C tb/verilator/gptp_plane run VERILATOR="$V" ;;
    c) cd "$scratch/run-c" || return 2
       step builder_gates env PYTHONUNBUFFERED=1 python3 sw/builder/test_builder.py --gates test_rom_clock_contract,test_baremetal_profile_contract,test_model_id_hashing,test_gptp_dataset_matches_engine_announce,test_gptp_clock_accuracy_per_board,test_builder_doc_key_map
       step fw_service_budget make -C tb/verilator/fw_service_budget
       step docs_inventory python3 scripts/docs_inventory.py --check ;;
  esac
}
for c in "$@"; do chain "$c" & done
wait
for f in "$logs"/*.rc; do printf '%s rc=%s\n' "$(basename "$f" .rc)" "$(cat "$f")"; done
