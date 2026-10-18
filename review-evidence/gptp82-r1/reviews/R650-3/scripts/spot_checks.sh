#!/usr/bin/env bash
# Reviewer spot checks for FPGA-gPTP PR #83 at an exact head.
# Usage: spot_checks.sh <clone> <scratch-dir> <prev-head> <head>
# 1. Regenerate the default ROM image from the head generator and compare it
#    with every committed copy.
# 2. Generate the priority1-255 image and show ROM word 1022 for both.
# 3. Compare the comment-stripped parameter and port header of
#    KL_gptp_engine at prev-head and head.
set -euo pipefail
clone=$1; scr=$2; prev=$3; head=$4
mkdir -p "$scr"
cd "$clone"
test "$(git rev-parse HEAD)" = "$head"
gen=hdl/ucode/gen_gptp_ucode.py
python3 "$gen" -o "$scr/default.hex" >/dev/null
python3 "$gen" --p1 255 -o "$scr/p1_255.hex" >/dev/null
for f in syn/ooc/work/gptp_ucode.hex tb/tsngen/gptp_ucode.hex \
         tb/verilator/ucpu/gptp_ucode.hex; do
  if cmp -s "$scr/default.hex" "$f"; then echo "SAME   $f"; else echo "DIFFER $f"; fi
done
# the engine suite's copy is built with its own clock and cease arguments
python3 "$gen" --clk-hz 2000000 --cease-ms 3000 -o "$scr/engine.hex" >/dev/null
if cmp -s "$scr/engine.hex" tb/verilator/engine/gptp_ucode.hex; then
  echo "SAME   tb/verilator/engine/gptp_ucode.hex (engine GENARGS)"
else
  echo "DIFFER tb/verilator/engine/gptp_ucode.hex (engine GENARGS)"
fi
echo "word 1022 default: $(sed -n 1023p "$scr/default.hex")"
echo "word 1022 p1 255:  $(sed -n 1023p "$scr/p1_255.hex")"
echo "word 1023 default: $(sed -n 1024p "$scr/default.hex")"
hdr() {
  git show "$1:hdl/top/KL_gptp_engine.sv" |
    awk '/^module KL_gptp_engine/{on=1} on{print} on&&/^\);/{exit}' |
    sed -e 's://.*$::' -e 's/[[:space:]]\+$//' -e '/^[[:space:]]*$/d'
}
hdr "$prev" > "$scr/hdr-prev.txt"
hdr "$head" > "$scr/hdr-head.txt"
echo "header lines: $(wc -l < "$scr/hdr-head.txt")"
if cmp -s "$scr/hdr-prev.txt" "$scr/hdr-head.txt"; then
  echo "HEADER SAME prev=$prev head=$head"
else
  echo "HEADER DIFFER"; diff "$scr/hdr-prev.txt" "$scr/hdr-head.txt" || true
fi
sha256sum "$scr/hdr-head.txt" | cut -d' ' -f1
