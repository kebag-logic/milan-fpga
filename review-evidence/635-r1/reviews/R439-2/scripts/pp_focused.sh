#!/usr/bin/env bash
# Build tb/pp_top of the processor pin in a scratch export and run the
# ADP-config (AD0..AD7, incl. AD6 roll-back) and deadline (DL1..DL9) sections.
# Usage: pp_focused.sh <clone> <scratch> <outdir> <verilator>
set -u
clone=$1; scr=$2; out=$3; V=$4; mkdir -p "$out"
rm -rf "$scr/pp" && mkdir -p "$scr/pp"
git -C "$clone/protocol-processor" archive 631eeb342ca1e3fa80e734077a56a943aee76ff1 | tar -x -C "$scr/pp"
cd "$scr/pp/tb/pp_top" || exit 2
make VERILATOR="$V" gsi-build >"$out/gsi_build.log" 2>&1; echo $? >"$out/gsi_build.rc"
[ "$(cat "$out/gsi_build.rc")" = 0 ] || exit 1
( ./obj_dir/Vpp_top_sim --adp-only >"$out/adp_only.log" 2>&1; echo $? >"$out/adp_only.rc" ) &
( ./obj_dir/Vpp_top_sim --deadline-only >"$out/deadline_only.log" 2>&1; echo $? >"$out/deadline_only.rc" ) &
wait
for f in "$out"/*.rc; do printf '%s rc=%s\n' "$(basename "$f" .rc)" "$(cat "$f")"; done
