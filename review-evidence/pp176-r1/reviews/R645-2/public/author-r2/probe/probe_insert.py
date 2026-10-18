#!/usr/bin/env python3
"""probe_insert.py SIM_MAIN : insert the SET_STREAM_INFO length probe at the top
of W24 in a scratch copy of tb/pp_top/sim_main.cpp. Each length carries a valid
MSRP_ACC_LAT_VALID body on Stream Output 0 with latency 600000 + cdl, so the
offset row shows which command, if any, was applied. The model exits after the
probe."""
import sys
from pathlib import Path

ANCHOR = """  void w24_set_stream_info() {
"""
PROBE = """  void w24_set_stream_info() {
    for (int len : {59, 60, 61, 95, 96, 97, 100, 140}) {
      std::vector<uint8_t> p(size_t(len) - 12, 0);
      putbe(&p[0], 0x0006, 2); putbe(&p[4], 0x20000000u, 4);
      putbe(&p[24], uint32_t(600000 + len), 4);
      auto f = ask(AEM_SET_STREAM_INFO, p, uint16_t(0x7E00 + len));
      std::printf("SINFO-PROBE cdl %d: status %d, response cdl %d, "
                  "offset row %u (valid %u)\\n", len, f.empty() ? -1 : st(f),
                  cdl(f), unsigned(h.d->aecp_pt_offset_o.at(0)),
                  unsigned(h.d->aecp_pt_offset_v_o & 1));
    }
    std::fflush(stdout);
    std::exit(0);
"""


def main() -> int:
    p = Path(sys.argv[1])
    s = p.read_text()
    if s.count(ANCHOR) != 1:
        print("anchor not found once")
        return 1
    p.write_text(s.replace(ANCHOR, PROBE))
    return 0


if __name__ == "__main__":
    sys.exit(main())
