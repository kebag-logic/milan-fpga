#!/usr/bin/env python3
"""Probe the parent gptp_shadow bench with a long slew. Right after phase 4's
twelve closed-loop pairs, the master jumps a further JUMP_NS while the plane
is synchronized, and the bench keeps sending Sync/Follow_Up pairs (Announce
every sixth) and answering Pdelay exactly as phase 4 does, for PAIRS more
pairs. Each pair prints the published offset, the PHC addend level, the
publish flags and the PHC-history refusal counter; the process then exits,
so nothing after the probe runs. Probe only: no check is changed.
With a fourth argument `first`, the bench first withholds Sync for 500 ms
(Announce continues), so the syncReceiptTimeout clears sync-ok and the first
pair after the jump is a FIRST synchronization.
Usage: make_wedge_probe_patch.py <sim_main.cpp> <jump_ns> <pairs> [first]"""
import sys
from pathlib import Path


def main() -> None:
    """Rewrite the file in place."""
    path, jump_ns, pairs = Path(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    first = len(sys.argv) > 4 and sys.argv[4] == "first"
    lapse = ("""        announce(0x2FF, 100, GMID);
        run_svc(1000000);
        fprintf(stderr, "WEDGE lapse cyc=%llu flags=%u adj=%d\\n", (unsigned long long)cyc,
                (unsigned)dut->pub_flags_o, static_cast<int32_t>(dut->dbg_phc_adj_o));
""" if first else "")
    s = path.read_text()
    old = """        run(4000);
        sq++;
      }
      expect("closed loop locked","""
    assert s.count(old) == 1
    new = f"""        run(4000);
        sq++;
      }}
      {{
        //! PROBE: a synchronized master jump of {jump_ns} ns, then keep going
        const uint64_t mst2 = mst_base + {jump_ns}ull;
{lapse}        for (int k = 0; k < {pairs}; k++) {{
          if ((k % 6) == 0) announce(static_cast<uint16_t>(0x300 + k), 100, GMID);
          run_svc(250000);
          uint64_t origin = mst2 + cyc * 8ull + cyc / 1250ull;
          Frame f = ptp(0x0, sq, 0, 0x0208, 10);
          f.ts(0);
          send_wide(f.b);
          run(30);
          Frame g = follow_up(sq, origin + static_cast<uint64_t>(D_NOM));
          send_wide(g.b);
          run(4000);
          sq++;
          fprintf(stderr, "WEDGE k=%d cyc=%llu offset=%d adj=%d flags=%u phcl=%u lost=%u\\n", k,
                  (unsigned long long)cyc, static_cast<int32_t>(dut->pub_offset_o),
                  static_cast<int32_t>(dut->dbg_phc_adj_o), (unsigned)dut->pub_flags_o,
                  (unsigned)dut->dbg_txts_phcl_o, (unsigned)dut->dbg_txts_lost_o);
        }}
        fprintf(stderr, "WEDGE-END\\n");
        fflush(stderr);
        std::exit(0);
      }}
      expect("closed loop locked","""
    s = s.replace(old, new)
    if "#include <cstdlib>" not in s:
        s = "#include <cstdlib>\n" + s
    path.write_text(s)


if __name__ == "__main__":
    main()
