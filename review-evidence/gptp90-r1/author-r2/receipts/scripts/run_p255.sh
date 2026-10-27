#!/bin/bash
# Run R720's p255_probe.py unchanged, the way R720 ran it: plant into a copy of
# <tree>, build the engine harness, generate the priority1-255 image, run the
# fourth pass (+not-gm-capable). usage: run_p255.sh <tree> <workdir> <log>
source <scratch>/scripts/env.sh
T=$(cd "$1" && pwd); W=$2; LOG=$3
rm -rf "$W"; mkdir -p "$W"; cp -a "$T/hdl" "$T/tb" "$W/"
python3 -I <scratch>/probes/p255_probe.py "$W" || exit 2
d=$W/tb/verilator/engine; cd "$d" || exit 2
verilator --cc --exe --build -j 4 --top-module KL_gptp_engine -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -GUCODE_HEX_P='"gptp_ucode.hex"' -GCLK_HZ_P=2000000 -CFLAGS "-std=c++17 -O2 -I$d -Wall -Wextra" ../../../hdl/ucpu/gptp_ucpu_pkg.sv ../../../hdl/ucpu/KL_gptp_ucpu.sv ../../../hdl/wire/KL_gptp_rx_parser.sv ../../../hdl/wire/KL_gptp_tx_slot.sv ../../../hdl/common/KL_gptp_timer.sv ../../../hdl/top/KL_gptp_engine.sv sim_main.cpp -o Vengine_sim > build.log 2>&1 || { echo BUILD-FAIL >> "$LOG"; tail -n 20 build.log; exit 2; }
mkdir -p p1run && python3 -I ../../../hdl/ucode/gen_gptp_ucode.py --clk-hz 2000000 --cease-ms 3000 --p1 255 -o p1run/gptp_ucode.hex >/dev/null && cd p1run && ../obj_dir/Vengine_sim +not-gm-capable > "$LOG" 2>&1; echo "rc=$?" >> "$LOG"
grep -E '^R720|checks:|^rc=' "$LOG"
