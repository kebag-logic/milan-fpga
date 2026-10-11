#!/usr/bin/env bash
# Disposable gate probes on an exported copy of the donor head.
# usage: gate_probes.sh DONOR_REPO SCRATCH_DIR
set -u
src=$1; work=$2
run() {  # name, then a sed program applied to one file, then the file
  local name=$1 prog=$2 file=$3 d="$work/$1"
  rm -rf "$d"; mkdir -p "$d"; git -C "$src" archive HEAD | tar -x -C "$d"
  sed -i "$prog" "$d/$file"
  git -C "$src" diff --no-index --stat -- "$src/$file" "$d/$file" >/dev/null 2>&1
  (cd "$d" && python3 -I scripts/check_docs.py >"$d.log" 2>&1); local rc=$?
  printf '%-34s check_docs rc=%s  %s\n' "$name" "$rc" "$(tail -1 "$d.log")"
}
# P0 control: unmodified head
run p0_head_control 's/^$//' README.md
# P1 RESIDUE fix candidate keeps the required gate token
run p1_residue_fix_integration 's/verification-only comparison builds only/verification comparison builds only/' docs/INTEGRATION.md
run p1_residue_fix_readme 's/verification-only comparison builds only/verification comparison builds only/' README.md
# P2 semantic regression the gate does not see: default-off wording
run p2_default_off_integration 's/Parent integration enables \[`GPTP_PLANE_EN_P` by default\]/Parent integration disables [`GPTP_PLANE_EN_P` by default]/' docs/INTEGRATION.md
# P3 broken fragment anchor
run p3_broken_anchor 's/INTEGRATION.md#option-off-behavior/INTEGRATION.md#option-of-behaviour/' README.md
# P4 stale parent revision in a pinned citation
run p4_stale_parent_sha 's/ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5\/hdl\/milan\/milan_datapath.sv#L73/3178b13638d11d67376a24ca52ee1332cbe23ad3\/hdl\/milan\/milan_datapath.sv#L89/' README.md
# P5 removal of the required token stays caught
run p5_drop_required_token 's/comparison builds only/comparison builds/' docs/INTEGRATION.md
# P6 an eleven-word sentence in the new subsection stays caught
run p6_long_sentence 's/^Review the \[remaining acceptance gaps\](MANAGER.md#open-risks) before product adoption\./Review the [remaining acceptance gaps](MANAGER.md#open-risks) carefully before any product adoption decision./' docs/INTEGRATION.md
