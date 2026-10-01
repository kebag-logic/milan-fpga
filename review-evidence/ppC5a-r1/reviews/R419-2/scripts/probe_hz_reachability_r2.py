#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer probe (R419-2): the round-1 reachability probe re-run at the
round-2 head, plus three round-2 additions.

Adds arms to section HZ of a SCRATCH copy of tb/pp_top/sim_main.cpp (never the
reviewed checkout) after the last HZ call, and runs --hazards-only.

  R419-P0..P4  the round-1 arms, unchanged (P2 is the talker-side pair held
               from the ACMP side).
  R419-P2b     how long a talker GET_TX_STATE / DISCONNECT_TX keeps its
               scoreboard key under the same TX-pool stall (the premise P2
               needs), against a listener GET_RX_STATE as the control.
  R419-P5      the 03 section 6 sentence "one on STREAM_OUTPUT k and a
               GET_TX_STATE or GET_TX_CONNECTION of source k" exclude each
               other: a held SET_NAME on STREAM_OUTPUT 1 vs GET_TX_CONNECTION
               of source 1 (HZ9 grades GET_TX_STATE only).
  R419-P6      REGISTRY_OP held (REGISTER) vs an ACMP GET_TX_STATE of source 1
               and a DISCONNECT_TX of source 1: both admitted beside.

Usage: probe_hz_reachability_r2.py <scratch tree root> <verilator>
"""
import pathlib
import subprocess
import sys

ANCHOR = ("    hz12_a_stream_named_by_another_class_conflicts_with_its_read();\n"
          "  }\n")

PROBE = r'''
  //! R419-2 probe arms: each prints its measured admission relation
  long r419_hold_clocks(uint8_t msg, uint16_t uid) {
    io.hz_clear();
    fill_tx_pool();
    io.hz_clear();
    (void)send_acmp(msg, uid, seq++);
    long adm = -1;
    for (int c = 0; c < 2000 && adm < 0; ++c) {
      io.step();
      if (!io.hz_adms.empty()) adm = io.hz_adms.back().t;
    }
    long held = 0;
    for (int c = 0; c < 3000; ++c) {
      if (io.d->dbg_acmp_sb_active_o) ++held;
      io.step();
    }
    release_mac();
    return adm < 0 ? -1 : held;
  }
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
    auto a0 = beside_or_after(10, 1, 0x0010, name_si0, true,
        "R419-P0 control: SET_NAME STREAM_INPUT 0 beside a held GET_RX_STATE sink 1");
    printf("R419-P0 status %d\n", status(a0));
    auto a1 = beside_or_after(10, 1, 0x0010, name_si1, false,
        "R419-P1 NAME_WR: SET_NAME STREAM_INPUT 1 waits for a held ACMP GET_RX_STATE sink 1");
    printf("R419-P1 status %d\n", status(a1));
    auto a2 = beside_or_after(4, 2, 0x0010, name_so2, false,
        "R419-P2 NAME_WR: SET_NAME STREAM_OUTPUT 2 waits for a held ACMP GET_TX_STATE source 2");
    printf("R419-P2 status %d\n", status(a2));
    auto a3 = beside_or_after(10, 1, 0x0018, ti(DT_SI, 1, 5), false,
        "R419-P3 IDENTIFY: SET_CONTROL carrying STREAM_INPUT 1 waits for a held GET_RX_STATE sink 1");
    printf("R419-P3 status %d\n", status(a3));
    auto a4 = beside_or_after(10, 1, 0x0014, rate_si1, false,
        "R419-P4 CLOCK_CFG: SET_SAMPLING_RATE carrying STREAM_INPUT 1 waits for a held GET_RX_STATE sink 1");
    printf("R419-P4 status %d\n", status(a4));
    printf("R419 round-1 arms: %d failing checks\n", io.fails - f0);

    const int f1 = io.fails;
    printf("R419-P2b hold clocks: listener GET_RX_STATE sink 1 %ld, talker "
           "GET_TX_STATE source 1 %ld, talker DISCONNECT_TX source 1 %ld "
           "(of 3000 observed)\n",
           r419_hold_clocks(10, 1), r419_hold_clocks(4, 1),
           r419_hold_clocks(2, 1));
    auto r5 = acmp_beside_or_after(AEM_SET_NAME,
        name_pl(DT_SO, 1, "R419 source one"), 12, 1, false,
        "R419-P5 a GET_TX_CONNECTION of source 1 vs a held SET_NAME on STREAM_OUTPUT 1");
    printf("R419-P5 held SET_NAME status %d\n", status(r5));
    auto r6a = acmp_beside_or_after(0x0024, std::vector<uint8_t>(4, 0), 4, 1,
        true, "R419-P6a a GET_TX_STATE of source 1 vs a held REGISTER");
    auto r6b = acmp_beside_or_after(0x0025, {}, 2, 1, true,
        "R419-P6b a DISCONNECT_TX of source 1 vs a held DEREGISTER");
    printf("R419-P6 held REGISTER status %d, DEREGISTER status %d\n",
           status(r6a), status(r6b));
    printf("R419 round-2 arms: %d failing checks\n", io.fails - f1);
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
                        "    hz12_a_stream_named_by_another_class_conflicts_"
                        "with_its_read();\n    r419_probe();\n  }\n" + PROBE, 1)
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
