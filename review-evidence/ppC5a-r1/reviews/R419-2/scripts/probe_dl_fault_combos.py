#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer probe (R419-2): the round-2 MVU / non-AEM answer under combined
conditions the lane's DL8 and DL9 grade only one at a time.

Adds arms to section DL of a SCRATCH copy of tb/pp_top/sim_main.cpp (never the
reviewed checkout) after DL11, and runs --deadline-only.

  R419-D1  a GET_MILAN_INFO queued behind DL1's stall past its deadline WITH
           the response memory failing reads: one answer, MVU NOT_IMPLEMENTED
           with the command echoed, byte-exact; the preempt's echo means no
           response-memory read, so no void is counted.
  R419-D2  an ADDRESS_ACCESS and an AVC command with the response memory
           failing reads, idle: NOT_IMPLEMENTED with the command echoed,
           byte-exact, no void counted (their answer never used the memory).
  R419-D3  after D1/D2, an AEM GET_CONFIGURATION is answered SUCCESS and all
           four RX slots are free.

Usage: probe_dl_fault_combos.py <scratch tree root> <verilator>
"""
import pathlib
import subprocess
import sys

ANCHOR = "    dl11_every_release_named_a_live_hold();\n  }\n"

PROBE = r'''
  void r419_dl_probe() {
    const int f0 = io.fails;
    // D1: deadline + read error on a queued GET_MILAN_INFO
    io.q_aecp.clear();
    io.dl_clear();
    io.ctr_hold = 1000;
    const uint16_t e0 = io.d->dbg_resp_err_o;
    const long ta = send(AEM_GET_COUNTERS, ti(0x0005, 0), 0xE101);
    (void)ta;
    io.rmem_rerr = true;
    const long tb = send(0, mvu_pl(), 0xE102, VU_COMMAND);
    long fa = -1, fb = -1;
    const auto a = answer(0xE101, &fa);
    const auto b = answer(0xE102, &fb);
    io.rmem_rerr = false;
    io.ctr_hold = 2;
    printf("R419-D1 stall status %d; MVU status %d, %zu bytes, %ld clocks after "
           "reception, voids counted %u, redirects %d\n", status(a), status(b),
           b.size(), fb - tb, unsigned(uint16_t(io.d->dbg_resp_err_o - e0)),
           io.dl_pre_rises);
    CHECK(b == aecp_frame(CTLR_MAC, OWN_MAC, VU_RESPONSE, AECP_NOT_IMPLEMENTED,
                          EID, CTLR_EID, 0xE102, MVU_PID_HI, mvu_pl()),
          "R419-D1 queued GET_MILAN_INFO past its deadline under a read error: "
          "MVU NOT_IMPLEMENTED with the command echoed, byte-exact");
    CHECK(fb - tb < RESP_CYC, "R419-D1 inside T-AECP-RESP (%ld)", fb - tb);
    // D2: non-AEM types idle under a read error
    std::vector<uint8_t> pl(10, 0);
    putbe(&pl[0], 0x0004, 2);
    const uint8_t mts[] = {2, 4};
    uint16_t s = 0xE201;
    for (uint8_t mt : mts) {
      io.q_aecp.clear();
      const uint16_t e1 = io.d->dbg_resp_err_o;
      io.rmem_rerr = true;
      io.feed(aecp_frame(OWN_MAC, CTLR_MAC, mt, 0, EID, CTLR_EID, s, 0x0001, pl));
      long f = -1;
      const auto r = answer(s, &f);
      io.rmem_rerr = false;
      printf("R419-D2 message_type %u: status %d, %zu bytes, voids %u\n",
             unsigned(mt), status(r), r.size(),
             unsigned(uint16_t(io.d->dbg_resp_err_o - e1)));
      CHECK(r == aecp_frame(CTLR_MAC, OWN_MAC, uint8_t(mt + 1),
                            AECP_NOT_IMPLEMENTED, EID, CTLR_EID, s, 0x0001, pl),
            "R419-D2 message_type %u under a read error: NOT_IMPLEMENTED with "
            "the command echoed, byte-exact", unsigned(mt));
      ++s;
    }
    // D3: healthy afterwards
    io.run_ms(20);
    CHECK(((io.snap(25) >> 3) & 0xFFFFu) == 4u,
          "R419-D3 %u of 4 RX slots free", (io.snap(25) >> 3) & 0xFFFFu);
    (void)send(AEM_GET_CONFIGURATION, {}, 0xE301);
    long f = -1;
    const auto g = answer(0xE301, &f);
    CHECK(status(g) == AECP_SUCCESS, "R419-D3 GET_CONFIGURATION SUCCESS (%d)",
          status(g));
    printf("R419 DL probe: %d failing checks\n", io.fails - f0);
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
    text = text.replace(ANCHOR, "    dl11_every_release_named_a_live_hold();\n"
                        "    r419_dl_probe();\n  }\n" + PROBE, 1)
    sim.write_text(text)
    tb = root / "tb/pp_top"
    subprocess.run(["make", "gsi-build", f"VERILATOR={verilator}"], cwd=tb,
                   check=True, stdout=subprocess.DEVNULL)
    r = subprocess.run(["./obj_dir/Vpp_top_sim", "--deadline-only"], cwd=tb,
                       capture_output=True, text=True)
    sys.stdout.write(r.stdout)
    sys.stderr.write(r.stderr)
    return r.returncode


if __name__ == "__main__":
    sys.exit(main())
