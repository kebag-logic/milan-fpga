#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Insert the R281-1 differential probe phase into a DISPOSABLE copy of the
pinned tb/pp_top/sim_main.cpp (never the submodule checkout).

The pinned suite runs unchanged up to and including its MilanInfoPhase (the
M1..M9 checks), then the probe feeds every frame listed in $R281_CASES and
writes the engine's answer (or NONE for silence within 200 ms) to $R281_OUT,
and the run stops. Usage:  pp_top_probe.py <scratch-copy>/tb/pp_top/sim_main.cpp
"""
import sys
from pathlib import Path

PROBE = r'''
// ==== R281-1 reviewer probe (disposable scratch copy only) ================
#include <cstdlib>
#include <fstream>
#include <sstream>
#include <string>
struct R281Probe {
  H& h;
  void run() {
    const char* in = std::getenv("R281_CASES");
    const char* out = std::getenv("R281_OUT");
    CHECK(in && out, "R281: R281_CASES and R281_OUT must be set");
    if (!in || !out) return;
    std::ifstream fi(in);
    std::ofstream fo(out);
    std::string line;
    int n = 0;
    while (std::getline(fi, line)) {
      std::istringstream ls(line);
      std::string name, hex;
      if (!(ls >> name >> hex)) continue;
      std::vector<uint8_t> f;
      for (size_t i = 0; i + 1 < hex.size(); i += 2)
        f.push_back(static_cast<uint8_t>(std::stoul(hex.substr(i, 2), nullptr, 16)));
      h.q_aecp.clear();
      h.feed(f);
      auto got = h.wait_any(h.q_aecp, 200);
      fo << name << ' ';
      if (got.empty()) {
        fo << "NONE";
      } else {
        static const char* d = "0123456789abcdef";
        for (uint8_t b : got) fo << d[b >> 4] << d[b & 15];
      }
      fo << '\n';
      ++n;
    }
    printf("R281 probe: %d cases answered into %s\n", n, out);
  }
};
'''

ANCHOR_STRUCT = "struct Suite {"
ANCHOR_RUN = "    MilanInfoPhase{h, d, image_entity}.run();\n"


def main() -> int:
    p = Path(sys.argv[1])
    t = p.read_text(encoding="utf-8")
    assert t.count(ANCHOR_STRUCT) == 1 and t.count(ANCHOR_RUN) == 1, "anchors moved"
    t = t.replace(ANCHOR_STRUCT, PROBE + "\n" + ANCHOR_STRUCT)
    t = t.replace(ANCHOR_RUN, ANCHOR_RUN + "    R281Probe{h}.run();\n    return;\n")
    p.write_text(t, encoding="utf-8")
    print("probe inserted into", p)
    return 0


if __name__ == "__main__":
    sys.exit(main())
