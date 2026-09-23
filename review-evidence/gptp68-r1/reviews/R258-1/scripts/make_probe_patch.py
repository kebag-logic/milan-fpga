#!/usr/bin/env python3
"""Instrument a copy of the parent gptp_shadow sim_main.cpp so every egress
result prints its reconstruction deviation and the PHC addend in force at
launch and at delivery, plus the phase-4 pair trajectory. Probe only: it
adds prints, changes no check. Usage: make_probe_patch.py <sim_main.cpp>"""
import sys
from pathlib import Path


def rep(s: str, old: str, new: str, count: int = 1) -> str:
    """Replace an exact snippet that must occur `count` times."""
    assert s.count(old) == count, (old, s.count(old))
    return s.replace(old, new)


def main() -> None:
    """Rewrite the file in place."""
    path = Path(sys.argv[1])
    s = path.read_text()
    s = rep(s, "struct Stamp { uint16_t seq; uint8_t type; uint64_t ns; uint8_t ok; };",
            "struct Stamp { uint16_t seq; uint8_t type; uint64_t ns; uint8_t ok; int32_t adj; uint64_t cy; };")
    s = rep(s, """                        dut->dbg_eng_txts_ns_o,
                        static_cast<uint8_t>(dut->dbg_eng_txts_ok_o)});""",
            """                        dut->dbg_eng_txts_ns_o,
                        static_cast<uint8_t>(dut->dbg_eng_txts_ok_o),
                        static_cast<int32_t>(dut->dbg_phc_adj_o), cyc});""")
    s = rep(s, "    if (dut->dbg_launch_v_o) launch_ns.push_back(dut->dbg_launch_phc_o);",
            """    if (dut->dbg_launch_v_o) { launch_ns.push_back(dut->dbg_launch_phc_o);
      probe_launch_adj.push_back(static_cast<int32_t>(dut->dbg_phc_adj_o)); }""")
    s = rep(s, "  std::vector<uint64_t> launch_ns;\n",
            "  std::vector<uint64_t> launch_ns;\n  std::vector<int32_t> probe_launch_adj;   // probe: addend at launch\n")
    s = rep(s, "          if (dev < -kPhcTruncNs || dev > kPhcTruncNs) law_recon_wrong++;",
            """          if (dev < -kPhcTruncNs || dev > kPhcTruncNs) law_recon_wrong++;
          fprintf(stderr, "PROBE result k=%zu type=%d seq=%u ok=1 dev_ns=%lld adj_launch=%d adj_deliver=%d cyc=%llu %s\\n",
                  k, stamps[k].type, stamps[k].seq, (long long)dev,
                  k < probe_launch_adj.size() ? probe_launch_adj[k] : 0, stamps[k].adj,
                  (unsigned long long)stamps[k].cy,
                  (dev < -kPhcTruncNs || dev > kPhcTruncNs) ? "WRONG" : "ok");""")
    s = rep(s, """      if (stamps[k].ok && k < launch_ns.size() && k < rec_delayed.size()) {""",
            """      if (!stamps[k].ok)
        fprintf(stderr, "PROBE result k=%zu type=%d seq=%u ok=0 adj_deliver=%d cyc=%llu LOST\\n",
                k, stamps[k].type, stamps[k].seq, stamps[k].adj, (unsigned long long)stamps[k].cy);
      if (stamps[k].ok && k < launch_ns.size() && k < rec_delayed.size()) {""")
    s = rep(s, "    launch_ns.clear();\n    rec_delayed.clear();",
            "    launch_ns.clear();\n    probe_launch_adj.clear();\n    rec_delayed.clear();", 2)
    s = rep(s, "    rec_delayed.clear();\n  }\n\n  //! Release exactly one held record.",
            """    rec_delayed.clear();
    fprintf(stderr, "PROBE epoch-close cyc=%llu phcl=%u\\n", (unsigned long long)cyc, (unsigned)dut->dbg_txts_phcl_o);
  }

  //! Release exactly one held record.""")
    s = rep(s, """        run(4000);
        sq++;
      }""", """        run(4000);
        fprintf(stderr, "PROBE phase4 pair k=%d cyc=%llu offset=%d adj=%d flags=%u phcl=%u\\n", k,
                (unsigned long long)cyc, static_cast<int32_t>(dut->pub_offset_o),
                static_cast<int32_t>(dut->dbg_phc_adj_o), (unsigned)dut->pub_flags_o,
                (unsigned)dut->dbg_txts_phcl_o);
        sq++;
      }""")
    path.write_text(s)


if __name__ == "__main__":
    main()
