#!/bin/sh
# Reproduce the reviewer's focused parent legs for FPGA-gPTP PR #86.
#
#   parent_legs.sh WORK FPGA_GPTP_CLONE VERILATOR_DIR [COMPANION_PATCH]
#
# WORK            empty scratch directory (disposable)
# FPGA_GPTP_CLONE a clone of Mister-M-alt/FPGA-gPTP holding e4869fd0, 43acfbcc
#                 and 53ac2e9d
# VERILATOR_DIR   directory whose `verilator` is the pinned 5.050
# COMPANION_PATCH the published parent-adoption-gptp_shadow-85.patch
#
# Parent snapshot: kebag-logic/milan-fpga dev e9cbb676 (depth 1), with the
# protocol-processor (2cbed0a9) and verilog-axis (48ff7a7e) gitlinks it pins.
# The gptp-processor directory is filled from an exported FPGA-gPTP tree:
#   devpin = e4869fd0 (the parent's own pin), base = 43acfbcc, head = 53ac2e9d.
# Legs: tb/verilator/gptp_shadow `make run` (base, head, head+companion) and
# tb/verilator/milan_dp `make gptp` (devpin, base, head). Nothing is pushed.
set -eu
W=$1; G=$2; V=$3; PATCH=${4:-}
PARENT=e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f
export PATH="$V:$PATH"
mkdir -p "$W/pfull"
cd "$W/pfull"
git init -q . && git fetch -q --depth 1 https://github.com/kebag-logic/milan-fpga.git $PARENT
git checkout -q FETCH_HEAD
for spec in "protocol-processor https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan.git 2cbed0a987c1e68402658d69459ab7e5aa571adc" \
            "third_party/verilog-axis https://github.com/alexforencich/verilog-axis 48ff7a7e2ef782cf778d47910cf85835c64b1bce"; do
  set -- $spec
  mkdir -p "$1"; (cd "$1" && git init -q . && git fetch -q --depth 1 "$2" "$3" && git checkout -q FETCH_HEAD)
done
for pair in devpin:e4869fd0c42889b2ac806587cc5c78afb1c33461 base:43acfbcc098f5af1be20a4a5458770ead3717622 head:53ac2e9d75ceb381c2d2b04854e760304d9ae43f; do
  tag=${pair%%:*}; rev=${pair#*:}
  mkdir -p "$W/p_$tag/gptp-processor"
  cp -a "$W/pfull/." "$W/p_$tag/"
  git -C "$G" archive "$rev" | tar -x -C "$W/p_$tag/gptp-processor"
done
mkdir -p "$W/p_adopt"; cp -a "$W/p_head/." "$W/p_adopt/"
[ -n "$PATCH" ] && (cd "$W/p_adopt" && patch -p1 < "$PATCH")
for tag in base head adopt; do
  (cd "$W/p_$tag/tb/verilator/gptp_shadow" && make run VERILATOR_JOBS=4 > "$W/shadow_$tag.log" 2>&1; echo $? > "$W/shadow_$tag.rc") &
done
for tag in devpin base head; do
  (cd "$W/p_$tag/tb/verilator/milan_dp" && make gptp VERILATOR_JOBS=6 > "$W/milan_dp_gptp_$tag.log" 2>&1; echo $? > "$W/milan_dp_gptp_$tag.rc") &
done
wait
grep -H 'checks:' "$W"/shadow_*.log "$W"/milan_dp_gptp_*.log
