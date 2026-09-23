#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Disposable probe on a COPY of the parent gptp_shadow bench (parent dev
574c29fa): the #68 acceptance case "a 900 ms offset slews" run through the
parent's real consumer (timestamp_counter + KL_gptp_shadow/KL_gptp_txret)
for 20 s of simulated time while the harness peer keeps answering every
Pdelay_Req and a +0 ppm master keeps sending Sync/Follow_Up and Announce.

The probe replaces everything after check_announce_adoption_and_path_trace()
(the plane is then asCapable, slave to GMID, never synchronized, integrator
zero) with one phase that logs, per Sync/Follow_Up pair: the published
offset, the flags (bit 2 asCapable, bit 3 sync-ok), the applied addend, the
parent's PHC-history loss count (dbg_txts_phcl_o: egress results refused
because the PHC trajectory, here the addend envelope, was outside the model)
and the count of step pulses. It grades nothing about the donor; it reports.
The master is FIRST_OFF_NS behind our clock at the first pair (offset local
minus master = +FIRST_OFF_NS). Usage:
  probe_long_slew.py <sim_main.cpp> [FIRST_OFF_NS] (in place, scratch copy only)"""

import pathlib
import sys

CALL_OLD = "    check_sync_offset_and_closed_loop_lock();\n"
CALL_NEW = ("    probe_long_slew();   // PROBE: replaces the rest of the run\n"
            "    printf(\"%d checks: %d PASS, %d FAIL\\n\", checks, checks - fails, fails);\n"
            "    return fails ? 1 : 0;\n"
            "    check_sync_offset_and_closed_loop_lock();\n")

FN_ANCHOR = "  //! The sync half of phase 4: one pair puts the offset in range, then a\n"


def probe_fn(first_off_ns: int) -> str:
    """The C++ probe phase, spliced in ahead of the closed-loop phase."""
    return f"""  //! PROBE (review only): a {first_off_ns} ns first synchronization, then
  //! 20 s of a live master and a live Pdelay peer.
  void probe_long_slew() {{
    const int64_t kFirstOff = {first_off_ns}ll;
    expect("probe: asCapable before the slew", dut->pub_flags_o & FL_ASCAP,
           FL_ASCAP);
    expect("probe: never synchronized before the slew",
           dut->pub_flags_o & FL_SYNCOK, 0);
    // master = our clock - kFirstOff at the first pair, nominal rate
    const uint64_t mst_base = phc() - static_cast<uint64_t>(kFirstOff)
                              - cyc * 8ull;
    uint16_t sq = 0x700;
    uint32_t steps = 0, last_adj_seen = 0;
    int ascap_fell_at = -1, ascap_back_at = -1;
    for (int k = 0; k < 160; k++) {{
      if ((k % 6) == 0) announce(static_cast<uint16_t>(0x700 + k), 100, GMID);
      const uint16_t phcl0 = dut->dbg_txts_phcl_o;
      run_svc(250000);
      uint64_t origin = mst_base + cyc * 8ull;
      Frame f = ptp(0x0, sq, 0, 0x0208, 10);
      f.ts(0);
      send_wide(f.b);
      run(30);
      Frame g = follow_up(sq, origin + static_cast<uint64_t>(D_NOM));
      send_wide(g.b);
      run(4000);
      sq++;
      const uint32_t fl = dut->pub_flags_o;
      const int32_t adj = static_cast<int32_t>(dut->dbg_phc_adj_o);
      if (ascap_fell_at < 0 && !(fl & FL_ASCAP)) ascap_fell_at = k;
      if (ascap_fell_at >= 0 && ascap_back_at < 0 && (fl & FL_ASCAP))
        ascap_back_at = k;
      last_adj_seen = static_cast<uint32_t>(adj);
      fprintf(stderr,
              "PROBE SLEW k=%d t_ms=%llu offset=%d flags=%u ascap=%u syncok=%u "
              "adj=%d phcl=%u phcl_new=%u lost=%u\\n",
              k, static_cast<unsigned long long>(cyc / 2000ull),
              static_cast<int32_t>(dut->pub_offset_o), fl, (fl >> 2) & 1u,
              (fl >> 3) & 1u, adj, static_cast<unsigned>(dut->dbg_txts_phcl_o),
              static_cast<unsigned>(dut->dbg_txts_phcl_o - phcl0),
              static_cast<unsigned>(dut->dbg_txts_lost_o));
    }}
    (void)steps;
    (void)last_adj_seen;
    fprintf(stderr, "PROBE SUMMARY ascap_fell_at=%d ascap_back_at=%d "
            "final_flags=%u final_adj=%d final_phcl=%u\\n",
            ascap_fell_at, ascap_back_at,
            static_cast<unsigned>(dut->pub_flags_o),
            static_cast<int32_t>(dut->dbg_phc_adj_o),
            static_cast<unsigned>(dut->dbg_txts_phcl_o));
  }}

"""


def main() -> None:
    """Apply the probe to the file named on the command line."""
    path = pathlib.Path(sys.argv[1])
    first_off = int(sys.argv[2]) if len(sys.argv) > 2 else 900_000_000
    src = path.read_text()
    for anchor in (CALL_OLD, FN_ANCHOR):
        if src.count(anchor) != 1:
            raise SystemExit(f"probe anchor not unique/absent: {anchor!r}")
    src = src.replace(CALL_OLD, CALL_NEW)
    src = src.replace(FN_ANCHOR, probe_fn(first_off) + FN_ANCHOR)
    path.write_text(src)


if __name__ == "__main__":
    main()
