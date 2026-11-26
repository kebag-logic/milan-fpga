#!/bin/sh
# usage: old_gen_milan_dp.sh <repo> <out>
# Runs the head-built milan_dp gptp leg binary against the previous pin's
# engine image (1213ac5b generator, the leg's own options) with the head's
# other two ROM images, from a disposable directory at the leg's own depth
# (the leg calls the AEM builder by a relative path); the directory is removed.
repo=$1; out=$2; dp=$repo/tb/verilator/milan_dp
d=$repo/tb/verilator/r937_probe_dp; rm -rf "$d"; mkdir -p "$d"
git -C "$repo/gptp-processor" show 1213ac5b9e09b8759ba76cc70c53652b5e108996:hdl/ucode/gen_gptp_ucode.py > "$d/generate.py"
(cd "$d" && python3 generate.py -o gptp_ucode.hex --mac 0x02A1B2C3D4E5 --p1 248 --clk-hz 2000000 --clock-accuracy 0x22 --cease-ms 3000 > gen.log 2>&1) || exit 3
cp "$dp/ltn_rom.hex" "$dp/ucode.hex" "$d/"
sha256sum "$d/gptp_ucode.hex" "$dp/gptp_ucode.hex" | sed "s#$repo/##" > "$out/old_gen_milan_dp_images.txt"
(cd "$d" && "$dp/obj_gptp/Vmilan_dp_gptp" > "$out/old_gen_milan_dp_gptp.log" 2>&1)
echo "milan_dp gptp at the 1213ac5b image rc=$?" >> "$out/old_gen_milan_dp_images.txt"
rm -rf "$d"
