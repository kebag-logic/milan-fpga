#!/bin/sh
# Independent OOC re-measurement under the shared exclusive Vivado lock,
# one Vivado session at a time:
#   head  - run.sh at the exact head (constrained flow, static + log gates)
#   main  - run.sh at main 5dce647a (unconstrained flow), then the head's
#           log check applied to main's logs (must fail by name)
#   port  - head with the micro-CPU clock port renamed in a scratch copy:
#           does the gate notice synthesis ran without its clock?
# Usage: vivado_runs.sh <clone> <scratch-dir> <receipts-dir> <lockfile>
CO=$1; S=$2; OUT=$3; LOCK=$4
HEAD=26622e27dfb629a6c59d22b77021012127e0c344
MAIN=5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d
mkdir -p "$S" "$OUT"
for t in head main port; do rm -rf "$S/$t"; mkdir -p "$S/$t"; done
git -C "$CO" archive $HEAD | tar -x -C "$S/head"
git -C "$CO" archive $MAIN | tar -x -C "$S/main"
git -C "$CO" archive $HEAD | tar -x -C "$S/port"
sed -i 's/\bclk_i\b/clk_x/g' "$S/port/hdl/ucpu/KL_gptp_ucpu.sv"
CHK="$S/head/syn/ooc/check_ooc_clock.py"
exec 9>"$LOCK"
date -u +"lock wait %FT%TZ" > "$OUT/lock.txt"
flock 9
date -u +"lock held %FT%TZ" >> "$OUT/lock.txt"
for t in head main; do
  ( cd "$S/$t" && sh syn/ooc/run.sh ) > "$OUT/run_$t.log" 2>&1
  echo $? > "$OUT/run_$t.rc"
done
( cd "$S/main/syn/ooc/work" && python3 -I "$CHK" --log ucpu_ooc.log engine_ooc.log ) > "$OUT/main_logs_under_head_check.log" 2>&1
echo $? > "$OUT/main_logs_under_head_check.rc"
( cd "$S/port" && python3 -I syn/ooc/check_ooc_clock.py \
  && . "${VIVADO_SETTINGS:-$HOME/Xilinx/2026.1/Vivado/settings64.sh}" \
  && mkdir -p syn/ooc/work && cd syn/ooc/work \
  && python3 ../../../hdl/ucode/gen_gptp_ucode.py -o gptp_ucode.hex \
  && vivado -mode batch -source ../ucpu_ooc.tcl -nojournal -log ucpu_ooc.log \
  ; python3 -I ../check_ooc_clock.py --log ucpu_ooc.log ) > "$OUT/run_port.log" 2>&1
echo $? > "$OUT/run_port.rc"
date -u +"lock released %FT%TZ" >> "$OUT/lock.txt"
for t in head main port; do
  mkdir -p "$OUT/$t"
  cp "$S/$t"/syn/ooc/work/*.rpt "$S/$t"/syn/ooc/work/*.log "$OUT/$t/" 2>/dev/null
done
