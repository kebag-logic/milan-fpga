#!/usr/bin/env bash
# Launch the independent R552-2 campaigns concurrently, each detached with its
# own log and rc file under receipts/; poll with wait_rc.sh.
# usage: launch.sh SOURCE_REPO PACKET BASE_REV HEAD_REV
set -euo pipefail
src=$1; pk=$2; base=$3; head=$4
s="$pk/scripts"; r="$pk/receipts"; x="$pk/scratch"
mkdir -p "$r" "$x/tmp"
export TMPDIR="$x/tmp"
export WAVEDROM_VENV_BIN=${WAVEDROM_VENV_BIN:?}
export PINNED_VERILATOR=${PINNED_VERILATOR:?}
"$PINNED_VERILATOR" --version > "$r/verilator-identity.txt"
sha256sum "$(sed -n 's/.* \(\/[^ ]*\/usr\/bin\/verilator\) .*/\1/p' "$PINNED_VERILATOR")" >> "$r/verilator-identity.txt" || true
cat "$PINNED_VERILATOR" >> "$r/verilator-identity.txt"

bg() { # name cmd...
  local name=$1; shift
  rm -f "$r/$name.rc"
  nohup bash -c '"$@"; echo $? > "'"$r/$name"'.rc"' _ "$@" > "$r/$name.out" 2>&1 < /dev/null &
  echo "launched $name pid $!"
}

"$s/mkclone.sh" "$src" "$x/gates-head" "$head"
"$s/mkclone.sh" "$src" "$x/gates-base" "$base"
"$s/mkclone.sh" "$src" "$x/campaign-head" "$head"

bg gates-head "$s/gates.sh" "$x/gates-head" "$r/gates" head
bg gates-base "$s/gates.sh" "$x/gates-base" "$r/gates" base
bg negative-gates "$s/negative-gates.sh" "$src" "$x" "$r/negative" "$base" "$head"
bg doc-claim-probes python3 -I "$s/doc_claim_probes.py" --root "$x/campaign-head" \
   --scratch "$x/probes" --out "$r/probes" --verilator "$s/verilator-j8.sh" --jobs 4
bg acmp-fields-campaign python3 -I "$x/campaign-head/tb/pp_top/acmp_mutants.py" \
   --output "$r/acmp-fields-campaign" --verilator "$s/verilator-j8.sh" --jobs 2 \
   --only field_reset_blocked disconnect_not_accepted settled_vlan_truncated \
          unbind_talker_echo retry_status_cleared lock_status_13 \
          disconnect_invalid_success disconnect_changes_gate settlement_vlan_truncated \
          gsi_vlan_external parent_vlan_shifted retry_probe_status_cleared \
          lock_gate_bypassed stored_vlan_truncated probe_guard_current_controller \
          probe_retry_current_controller
