#!/usr/bin/env python3
"""Add a frame-injection probe to a DISPOSABLE copy of the pinned tb/pp_top.

Usage: patch_pp_top_probe.py <copy>/tb/pp_top/sim_main.cpp

After the pinned harness's own MilanInfoPhase (so the device is in exactly
the state the M1..M9 MVU checks run in), the probe reads one hex frame per
line from $PROBE_IN, feeds each into the MAC RX trunk, waits for the AECP
answer, and writes `RSP <hex>` or `RSP SILENCE` plus the engine's command
and response counter deltas to $PROBE_OUT, then exits.  No check of the
pinned suite is changed; the phases after MilanInfoPhase are not run.
"""
import sys

ANCHOR = "    MilanInfoPhase{h, d, image_entity}.run();\n"
PROBE = r'''    if (const char* pin = std::getenv("PROBE_IN")) {
      FILE* fi = std::fopen(pin, "r");
      FILE* fo = std::fopen(std::getenv("PROBE_OUT"), "w");
      static char line[16384];
      while (fi && fo && std::fgets(line, sizeof line, fi)) {
        std::vector<uint8_t> f;
        for (char* p = line; p[0] && p[1] && p[0] != '\n'; p += 2) {
          unsigned b = 0;
          std::sscanf(p, "%2x", &b);
          f.push_back(uint8_t(b));
        }
        if (f.empty()) continue;
        const uint16_t c0 = d->dbg_aecp_cmd_o;
        const uint16_t r0 = d->dbg_aecp_resp_o;
        h.q_aecp.clear();
        h.feed(f);
        auto got = h.wait_any(h.q_aecp, 200);
        h.idle(50);
        std::fprintf(fo, "RSP ");
        if (got.empty()) std::fprintf(fo, "SILENCE");
        for (uint8_t b : got) std::fprintf(fo, "%02x", b);
        std::fprintf(fo, " cmd+%u rsp+%u extra=%zu\n",
                     unsigned(uint16_t(d->dbg_aecp_cmd_o - c0)),
                     unsigned(uint16_t(d->dbg_aecp_resp_o - r0)),
                     h.q_aecp.size());
      }
      if (fo) std::fclose(fo);
      if (fi) std::fclose(fi);
      std::printf("PROBE DONE after MilanInfoPhase: %d checks, %d FAIL\n",
                  h.checks, h.fails);
      std::exit(h.fails ? 1 : 0);
    }
'''

path = sys.argv[1]
src = open(path, encoding="utf-8").read()
assert src.count(ANCHOR) == 1, "anchor not found exactly once"
assert "#include <cstdlib>" not in src
src = src.replace('#include <cstdint>\n', '#include <cstdint>\n#include <cstdlib>\n', 1)
src = src.replace(ANCHOR, ANCHOR + PROBE, 1)
open(path, "w", encoding="utf-8").write(src)
print("patched", path)
