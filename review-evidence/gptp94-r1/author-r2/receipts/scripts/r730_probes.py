#!/usr/bin/env python3
"""Run the R730-1 reviewer probes (probe.cpp.inc) against a tree copy.

usage: r730_probes.py <tree> <probe.cpp.inc> <out-dir> [probe|focused]
The same insertion and build flags as the reviewer's run_probes.py, but the
tree is a directory (a copy of the working tree), not a committed head.
"""
import subprocess
import sys
import time
from pathlib import Path

tree, inc, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
case = sys.argv[4] if len(sys.argv) > 4 else "probe"
out.mkdir(parents=True, exist_ok=True)
src = tree / "tb/verilator/engine/sim_main.cpp"
s = src.read_text()
start = s.index("  int run_suite() {")
end = s.index("\n private:", start)
s = s[:start] + '''  int run_suite() {
    independent_port_probes();
    printf("%d checks: %d PASS, %d FAIL\\n", checks, checks - fails, fails);
    return fails ? 1 : 0;
  }
''' + s[end:]
s = s.replace("\n private:", "\n private:\n" + inc.read_text(), 1)
if case == "focused":
    s = s.replace("    independent_port_probes();", '''    bring_the_engine_out_of_reset();
    settle_as_capable_master("focused setup");
    boot_watch = false;
    end_the_cease_on_a_port_toggle();
    drop_ascapable_at_a_link_loss();
    drop_a_frame_built_across_the_fall();
    keep_the_countdown_exit();''')
src.write_text(s)
work = tree / "tb/verilator/engine"
subprocess.run(["python3", "../../../hdl/ucode/gen_gptp_ucode.py", "--clk-hz",
                "2000000", "--cease-ms", "3000", "-o", "gptp_ucode.hex"],
               cwd=work, check=True)
rtl = tree / "hdl"
sources = ["ucpu/gptp_ucpu_pkg.sv", "ucpu/KL_gptp_ucpu.sv",
           "wire/KL_gptp_rx_parser.sv", "wire/KL_gptp_tx_slot.sv",
           "common/KL_gptp_timer.sv", "top/KL_gptp_engine.sv"]
cmd = ["verilator", "--cc", "--exe", "--build", "-j", "8",
       "--top-module", "KL_gptp_engine", "-Wall", "-Wno-fatal",
       "-Wno-DECLFILENAME", "-Wno-UNUSEDSIGNAL", "-Wno-WIDTHEXPAND",
       "-Wno-WIDTHTRUNC", "-Wno-UNUSEDPARAM",
       '-GUCODE_HEX_P="gptp_ucode.hex"', "-GCLK_HZ_P=2000000",
       "-CFLAGS", "-std=c++17 -O2 -Wall -Wextra",
       *[str(rtl / x) for x in sources], "sim_main.cpp", "-o", "Vprobe"]
for name, command in [(case + "-build", cmd), (case + "-run", ["./obj_dir/Vprobe"])]:
    t = time.monotonic()
    with (out / (name + ".log")).open("w") as log:
        log.write("command: " + repr(command) + "\n")
        log.flush()
        r = subprocess.run(command, cwd=work, stdout=log, stderr=subprocess.STDOUT, timeout=540)
    (out / (name + ".rc")).write_text(str(r.returncode) + "\n")
    print(name, "rc", r.returncode, "seconds", round(time.monotonic() - t, 2), flush=True)
    if name.endswith("-build") and r.returncode:
        raise SystemExit(r.returncode)
