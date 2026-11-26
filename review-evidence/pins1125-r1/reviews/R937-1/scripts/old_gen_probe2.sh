#!/bin/sh
# usage: old_gen_probe2.sh <repo> <work> <out> <pin> <suite>
repo=$1; work=$2; out=$3; pin=$4; suite=$5; short=$(echo $pin | cut -c1-8)
d=$work/$suite-$short; rm -rf "$d"; mkdir -p "$d"
git -C "$repo/gptp-processor" show "$pin:hdl/ucode/gen_gptp_ucode.py" > "$d/generate.py"
if [ $suite = plane ]; then
  (cd "$d" && python3 generate.py --clk-hz 2000000 -o gptp_ucode.hex > gen.log 2>&1)
  (cd "$d" && "$repo/tb/verilator/gptp_plane/obj_dir/Vgptp_plane_sim" > "$out/old_gen_plane_$short.log" 2>&1); echo "plane $short rc=$?" >> "$out/old_gen_summary.txt"
else
  (cd "$d" && python3 generate.py --clk-hz 2000000 --cease-ms 3000 -o gptp_ucode.hex > gen.log 2>&1)
  (cd "$d" && "$repo/tb/verilator/gptp_shadow/obj_dir/Vgptp_shadow_sim" > "$out/old_gen_shadow_$short.log" 2>&1); echo "shadow $short rc=$?" >> "$out/old_gen_summary.txt"
fi
sha256sum "$d/gptp_ucode.hex" | sed "s#$work/##" >> "$out/old_gen_summary.txt"
