#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Disposable probe: instrument a COPY of the parent's
tb/verilator/gptp_shadow/sim_main.cpp (parent dev 574c29fa) so that it
reports, on stderr, for every graded egress result the addend the PHC ran at
when the frame launched and the reconstruction error, plus the servo
trajectory (every change of the applied addend) and the published offset
after each closed-loop pair. Graded checks are untouched: only fprintf lines
and bookkeeping vectors are added. Usage: instrument_gptp_shadow.py <sim_main.cpp>
(edits that file in place; run it on a scratch copy only)."""

import pathlib
import sys


def patch(src: str) -> str:
    """Return src with the probe's reporting lines inserted."""
    edits = [
        ("  std::vector<uint64_t> launch_ns;\n",
         "  std::vector<uint64_t> launch_ns;\n"
         "  std::vector<int32_t> probe_launch_adj;   // PROBE\n"
         "  std::vector<uint64_t> probe_launch_cyc;  // PROBE\n"
         "  int32_t probe_last_adj = 0;             // PROBE\n"),
        ("    if (dut->dbg_launch_v_o) launch_ns.push_back(dut->dbg_launch_phc_o);\n",
         "    if (dut->dbg_launch_v_o) launch_ns.push_back(dut->dbg_launch_phc_o);\n"
         "    if (dut->dbg_launch_v_o) {  // PROBE\n"
         "      probe_launch_adj.push_back(static_cast<int32_t>(dut->dbg_phc_adj_o));\n"
         "      probe_launch_cyc.push_back(cyc);\n"
         "    }\n"
         "    if (static_cast<int32_t>(dut->dbg_phc_adj_o) != probe_last_adj) {  // PROBE\n"
         "      probe_last_adj = static_cast<int32_t>(dut->dbg_phc_adj_o);\n"
         "      fprintf(stderr, \"PROBE ADJ cyc=%llu adj=%d offset=%d flags=%u\\n\",\n"
         "              static_cast<unsigned long long>(cyc), probe_last_adj,\n"
         "              static_cast<int32_t>(dut->pub_offset_o),\n"
         "              static_cast<unsigned>(dut->pub_flags_o));\n"
         "    }\n"),
        ("          const int64_t dev = err - kReconNominalNs;\n"
         "          if (dev < -kPhcTruncNs || dev > kPhcTruncNs) law_recon_wrong++;\n",
         "          const int64_t dev = err - kReconNominalNs;\n"
         "          if (dev < -kPhcTruncNs || dev > kPhcTruncNs) law_recon_wrong++;\n"
         "          {  // PROBE\n"
         "            const int32_t a = k < probe_launch_adj.size() ? probe_launch_adj[k] : 0;\n"
         "            fprintf(stderr, \"PROBE RECON %s k=%zu type=%d seq=%u cyc=%llu adj=%d dev=%lld\\n\",\n"
         "                    (dev < -kPhcTruncNs || dev > kPhcTruncNs) ? \"WRONG\" : \"ok\",\n"
         "                    k, ty, stamps[k].seq,\n"
         "                    static_cast<unsigned long long>(k < probe_launch_cyc.size() ? probe_launch_cyc[k] : 0),\n"
         "                    a, static_cast<long long>(dev));\n"
         "          }\n"),
        ("    rec_delayed.clear();\n  }\n\n  //! Release exactly one held record.\n",
         "    rec_delayed.clear();\n"
         "    probe_launch_adj.clear();  // PROBE\n"
         "    probe_launch_cyc.clear();  // PROBE\n"
         "  }\n\n  //! Release exactly one held record.\n"),
        ("    rec_delayed.clear();\n    cur.clear();\n",
         "    rec_delayed.clear();\n"
         "    probe_launch_adj.clear();  // PROBE\n"
         "    probe_launch_cyc.clear();  // PROBE\n"
         "    cur.clear();\n"),
        ("        send_wide(g.b);\n        run(4000);\n        sq++;\n",
         "        send_wide(g.b);\n        run(4000);\n"
         "        fprintf(stderr, \"PROBE LOOP k=%d offset=%d flags=%u adj=%d\\n\", k,\n"
         "                static_cast<int32_t>(dut->pub_offset_o),\n"
         "                static_cast<unsigned>(dut->pub_flags_o),\n"
         "                static_cast<int32_t>(dut->dbg_phc_adj_o));  // PROBE\n"
         "        sq++;\n"),
    ]
    for old, new in edits:
        if src.count(old) != 1:
            raise SystemExit(f"probe anchor not unique/absent: {old[:60]!r}")
        src = src.replace(old, new)
    return src


def main() -> None:
    """Patch the file named on the command line in place."""
    path = pathlib.Path(sys.argv[1])
    path.write_text(patch(path.read_text()))


if __name__ == "__main__":
    main()
