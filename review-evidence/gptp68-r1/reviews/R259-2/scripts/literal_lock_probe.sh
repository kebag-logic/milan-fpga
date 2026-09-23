#!/bin/sh
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Build the probe harness in a disposable copy and run it against (a) the
# head's generator and (b) the head's generator with the SRTO leg's one
# S_LOCK write removed, the narrowing the PR body names.
set -eu
. "$(dirname "$0")/env.sh"
work="$SCRATCH/probe"
echo "# verilator: $(verilator --version); head $HEAD_SHA"
rm -rf "$work"
mkdir -p "$work"
git -C "$CLONE" archive "$HEAD_SHA" | tar -x -C "$work"
eng="$work/tb/verilator/engine"
cp "$eng/sim_main.cpp" "$work/sim_main.orig.cpp"
python3 "$PACKET/scripts/make_literal_lock_probe.py" "$eng/sim_main.cpp"
diff -u "$work/sim_main.orig.cpp" "$eng/sim_main.cpp" \
  | sed "s|$work/||g" > "$PACKET/scripts/probe-literal-lock.patch" || true
gen="$work/hdl/ucode/gen_gptp_ucode.py"
python3 - "$gen" "$work/gen_narrow.py" <<'PY'
import sys
s = open(sys.argv[1]).read()
pat = ('    e_flags(p, andm=FL_PRESENT_C | FL_AMGM_C | FL_ASCAP_C)\n'
       '    p.emit("WRST", ra=0, imm=RG_SCR | S_LOCK, fmt=FMT_Q)\n'
       '    p.emit("COMMIT")\n')
assert s.count(pat) == 1
open(sys.argv[2], "w").write(s.replace(pat, pat.replace(
    '    p.emit("WRST", ra=0, imm=RG_SCR | S_LOCK, fmt=FMT_Q)\n', '')))
PY
cd "$eng"
verilator --cc --exe --build -j 8 --top-module KL_gptp_engine -Wall -Wno-fatal \
  -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC \
  -Wno-UNUSEDPARAM -GUCODE_HEX_P='"gptp_ucode.hex"' -GCLK_HZ_P=2000000 \
  -CFLAGS "-std=c++17 -O2 -I$eng -Wall -Wextra" \
  ../../../hdl/ucpu/gptp_ucpu_pkg.sv ../../../hdl/ucpu/KL_gptp_ucpu.sv \
  ../../../hdl/wire/KL_gptp_rx_parser.sv ../../../hdl/wire/KL_gptp_tx_slot.sv \
  ../../../hdl/common/KL_gptp_timer.sv ../../../hdl/top/KL_gptp_engine.sv \
  sim_main.cpp -o Vprobe >/dev/null
for v in head narrow; do
  mkdir -p "$work/run_$v"
  if [ "$v" = head ]; then g=$gen; else g="$work/gen_narrow.py"; fi
  python3 "$g" --clk-hz 2000000 --cease-ms 3000 -o "$work/run_$v/gptp_ucode.hex" >/dev/null
  echo "== generator: $v (probe phase) =="
  ( cd "$work/run_$v" && R259_PROBE=1 "$eng/obj_dir/Vprobe" ) | grep -E 'PROBE|FAIL|checks:' || true
done
echo "== generator: narrow (the whole unmodified suite, probe off) =="
( cd "$work/run_narrow" && "$eng/obj_dir/Vprobe" ) | grep -E 'FAIL|checks:' | cut -c1-120 || true
