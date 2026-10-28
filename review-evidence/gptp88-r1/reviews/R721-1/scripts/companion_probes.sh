#!/bin/bash
# Reviewer-owned companion probes: copy the patched scratch parent, plant one
# defect, run one parent bench; record rc and FAIL lines. usage: <parent> <outdir>
set -u
src="$1"; out="$2"; mkdir -p "$out"; work=$(mktemp -d); trap 'rm -rf "$work"' EXIT
probe() {  # name file python-replace-old python-replace-new bench-cmd
  local name="$1" file="$2" old="$3" new="$4" cmd="$5" d="$work/$1"
  cp -a "$src" "$d"
  python3 -I - "$d/$file" "$old" "$new" <<'PY' || { echo "$name: pattern not unique" >> "$out/summary.txt"; return; }
import sys; p, o, n = sys.argv[1:]; t = open(p).read()
assert t.count(o) == 1, t.count(o); open(p, "w").write(t.replace(o, n))
PY
  ( cd "$d" && bash -c "$cmd" ) > "$out/$name.log" 2>&1; rc=$?
  echo "$name: rc=$rc $(grep -E '^[0-9]+ checks:' "$out/$name.log" | tail -1)" >> "$out/summary.txt"
  grep -E '^FAIL|\[FAIL\]' "$out/$name.log" >> "$out/summary.txt"
}
: > "$out/summary.txt"
probe C1-datapath-entry0-from-GM hdl/milan/milan_datapath.sv \
  "wire [63:0] asp_owner_head_w = GPTP_PLANE_EN_P ? gptp_pub_path_head_w" \
  "wire [63:0] asp_owner_head_w = GPTP_PLANE_EN_P ? cfg_adp_gptp_gm" \
  "make -C tb/verilator/milan_dp gptp" &
probe C2-shadow-generation-ignores-entry0 hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv \
  "      || (pub_path_next_w != pub_path_o);" \
  "      || (pub_path_next_w[8*64-1:64] != pub_path_o[8*64-1:64]);" \
  "make -C tb/verilator/gptp_shadow run" &
wait
