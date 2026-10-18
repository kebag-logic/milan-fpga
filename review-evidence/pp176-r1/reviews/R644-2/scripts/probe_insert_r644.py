#!/usr/bin/env python3
"""probe_insert_r644.py SIM_MAIN : reviewer length probe for SET_STREAM_INFO.

Inserted at the top of W24 in a disposable copy of tb/pp_top/sim_main.cpp.
Each command is a valid MSRP_ACC_LAT_VALID body on Stream Output 0 carrying
latency 600000 + cdl and a non-zero tail past the 2021 body, so the offset row
shows which command, if any, was applied. For every answer it prints status,
response cdl, the offset row, whether the answer is the byte-exact echo of the
command, and the count of non-zero response payload bytes after {type,index}.
Then a few longer bodies with other refusal causes (Stream Input target,
extra flag, bit-31 latency) show which refusal wins. The model exits after.
"""
import sys
from pathlib import Path

ANCHOR = "  void w24_set_stream_info() {\n"
PROBE = r"""  void w24_set_stream_info() {
    auto probe = [&](const char* tag, int len, uint16_t ty, uint32_t flags,
                     uint32_t lat) {
      std::vector<uint8_t> p(size_t(len) - 12, 0);
      if (p.size() >= 2) putbe(&p[0], ty, 2);
      if (p.size() >= 8) putbe(&p[4], flags, 4);
      if (p.size() >= 28) putbe(&p[24], lat, 4);
      for (size_t i = 84; i < p.size(); ++i) p[i] = uint8_t(0x5A + i);
      auto f = ask(AEM_SET_STREAM_INFO, p, uint16_t(0x7E00 + len));
      int nz = 0, echo = 0;
      if (f.size() >= 38) {
        size_t n = size_t(cdl(f)) > 12 ? size_t(cdl(f)) - 12 : 0;
        for (size_t i = 4; i < n && 38 + i < f.size(); ++i) nz += f[38 + i] != 0;
        echo = (n == p.size()) && std::equal(p.begin(), p.end(), f.begin() + 38);
      }
      std::printf("R644-PROBE %s cdl %d: status %d, response cdl %d, "
                  "offset row %u (valid %u), echo %d, nonzero-after-ti %d\n",
                  tag, len, f.empty() ? -1 : st(f), f.empty() ? -1 : cdl(f),
                  unsigned(h.d->aecp_pt_offset_o.at(0)),
                  unsigned(h.d->aecp_pt_offset_v_o & 1), echo, nz);
    };
    for (int len : {12, 16, 24, 40, 59, 60, 61, 72, 84, 95, 96, 97, 98, 100,
                    107, 108, 109, 140, 200, 300, 500})
      probe("out", len, 0x0006, 0x20000000u, uint32_t(600000 + len));
    for (int len : {60, 96, 97, 140})
      probe("in ", len, 0x0005, 0x20000000u, uint32_t(700000 + len));
    for (int len : {60, 96, 97, 140})
      probe("flg", len, 0x0006, 0x20000001u, uint32_t(800000 + len));
    for (int len : {60, 96, 97, 140})
      probe("b31", len, 0x0006, 0x20000000u, 0x80000000u | uint32_t(len));
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
