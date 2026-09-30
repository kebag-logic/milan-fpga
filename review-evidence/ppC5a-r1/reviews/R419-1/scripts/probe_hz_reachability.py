#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer probe (R419-1): is an admission conflict reachable at
protocol_processor_top for NAME_WR, IDENTIFY and CLOCK_CFG against a class
ACMP presents?

The scoreboard matrix (KL_pp_scoreboard.sv rule 2) makes RO_SNAPSHOT conflict
with every write class on the same key, and hz_classify keys SET_NAME,
SET_CONTROL and SET_SAMPLING_RATE from the wire {descriptor_type,
descriptor_index}. An ACMP GET_RX_STATE of sink k presents RO_SNAPSHOT on
{STREAM_INPUT, k}. This probe adds arms to section HZ of a SCRATCH copy of
tb/pp_top/sim_main.cpp (never the reviewed checkout) and runs --hazards-only.

Usage: probe_hz_reachability.py <scratch tree root> <verilator>
"""
import pathlib
import subprocess
import sys

ANCHOR = "    hz8_the_other_classes_run_beside_a_stream_step();\n  }\n"

PROBE = r'''
  //! R419 probe arms: each prints its measured admission relation
  void r419_probe() {
    const int f0 = io.fails;
    std::vector<uint8_t> name_si1 = ti(DT_SI, 1, 72);
    putbe(&name_si1[6], CFGIX, 2);
    std::vector<uint8_t> name_si0 = ti(DT_SI, 0, 72);
    putbe(&name_si0[6], CFGIX, 2);
    std::vector<uint8_t> name_so2 = ti(DT_SO, 2, 72);
    putbe(&name_so2[6], CFGIX, 2);
    std::vector<uint8_t> rate_si1 = ti(DT_SI, 1, 8);
    putbe(&rate_si1[4], 96000u, 4);
    // control: another sink's key runs beside
    auto a0 = beside_or_after(10, 1, 0x0010, name_si0, true,
        "R419-P0 control: SET_NAME STREAM_INPUT 0 beside a held GET_RX_STATE sink 1");
    printf("R419-P0 status %d\n", status(a0));
    // NAME_WR (legal command) vs an ACMP read of the same sink
    auto a1 = beside_or_after(10, 1, 0x0010, name_si1, false,
        "R419-P1 NAME_WR: SET_NAME STREAM_INPUT 1 waits for a held ACMP GET_RX_STATE sink 1");
    printf("R419-P1 status %d\n", status(a1));
    auto a2 = beside_or_after(4, 2, 0x0010, name_so2, false,
        "R419-P2 NAME_WR: SET_NAME STREAM_OUTPUT 2 waits for a held ACMP GET_TX_STATE source 2");
    printf("R419-P2 status %d\n", status(a2));
    // IDENTIFY / CLOCK_CFG keyed from a wire descriptor_type the command
    // does not legally carry: reachable at admission only through a
    // malformed command
    auto a3 = beside_or_after(10, 1, 0x0018, ti(DT_SI, 1, 5), false,
        "R419-P3 IDENTIFY: SET_CONTROL carrying STREAM_INPUT 1 waits for a held GET_RX_STATE sink 1");
    printf("R419-P3 status %d\n", status(a3));
    auto a4 = beside_or_after(10, 1, 0x0014, rate_si1, false,
        "R419-P4 CLOCK_CFG: SET_SAMPLING_RATE carrying STREAM_INPUT 1 waits for a held GET_RX_STATE sink 1");
    printf("R419-P4 status %d\n", status(a4));
    printf("R419 probe: %d failing checks among its arms\n", io.fails - f0);
  }
'''


def main() -> int:
    root = pathlib.Path(sys.argv[1])
    verilator = sys.argv[2]
    sim = root / "tb/pp_top/sim_main.cpp"
    text = sim.read_text()
    if text.count(ANCHOR) != 1:
        print("anchor not unique", file=sys.stderr)
        return 2
    text = text.replace(ANCHOR,
                        "    hz8_the_other_classes_run_beside_a_stream_step();\n"
                        "    r419_probe();\n  }\n" + PROBE, 1)
    sim.write_text(text)
    tb = root / "tb/pp_top"
    subprocess.run(["make", "gsi-build", f"VERILATOR={verilator}"], cwd=tb,
                   check=True, stdout=subprocess.DEVNULL)
    r = subprocess.run(["./obj_dir/Vpp_top_sim", "--hazards-only"], cwd=tb,
                       capture_output=True, text=True)
    sys.stdout.write(r.stdout)
    sys.stderr.write(r.stderr)
    return r.returncode


if __name__ == "__main__":
    sys.exit(main())
