#!/usr/bin/env python3
"""Insert a reviewer race probe into a SCRATCH copy of tb/acmp_talker/sim_main.cpp.

The probe sends GET_TX_STATE for an enabled source with listener fields
0xF1E2D3C4B5A69788 / 0x8C17 and clears that source's cfg_src_en_i bit k
clocks after the command is consumed (k = 0..3; k counts from the clock after
the consume edge, applied before that clock's evaluation). It prints the
status and listener fields of each response. The bit is restored after each
send. It runs after every graded case, just before the suite's report.

Usage: race_probe.py PATH/TO/SCRATCH/sim_main.cpp
"""
import sys
from pathlib import Path

EDITS = [
    # state
    ("  int consumed = 0;\n",
     "  int consumed = 0;\n"
     "  bool race_arm = false; int race_k = -1; int race_cnt = -1; uint32_t race_mask = 0;\n"),
    # drop at the top of the tick
    ("  void tick() {\n",
     "  void tick() {\n"
     "    if (race_arm && race_cnt >= 0 && race_cnt == race_k) {\n"
     "      d->cfg_src_en_i = d->cfg_src_en_i & ~race_mask; race_arm = false;\n"
     "    }\n"),
    # count clocks from the consume edge
    ("    if (d->txn_ready_o && d->txn_valid_i) ++consumed;\n",
     "    if (d->txn_ready_o && d->txn_valid_i) { ++consumed; if (race_arm) race_cnt = 0; }\n"
     "    else if (race_arm && race_cnt >= 0) ++race_cnt;\n"),
    # the probe itself
    ("  return report();\n}\n",
     "  {\n"
     "    uint32_t en = uint32_t(d->cfg_src_en_i);\n"
     "    int src = -1;\n"
     "    for (int s = 0; s < N_SRC; ++s) if ((en >> s) & 1) { src = s; break; }\n"
     "    printf(\"RACE enabled mask %02x, probing source %d\\n\", en, src);\n"
     "    for (int k = 0; k < 4 && src >= 0; ++k) {\n"
     "      resps.clear();\n"
     "      race_mask = 1u << src; race_k = k; race_cnt = -1; race_arm = true;\n"
     "      bool ok = send(MT_GTXS, uint16_t(src), C1, uint16_t(0x7B00 + k), L_DIST, 0x8C17, 0xFFFF);\n"
     "      race_arm = false;\n"
     "      if (resps.empty()) { printf(\"RACE k=%d consumed=%d no response\\n\", k, ok); }\n"
     "      else {\n"
     "        const Resp& r = resps.front();\n"
     "        printf(\"RACE k=%d status=%u leid=%016llx luid=%04x sid=%016llx\\n\", k, r.status,\n"
     "               static_cast<unsigned long long>(r.leid), r.luid,\n"
     "               static_cast<unsigned long long>(r.sid));\n"
     "      }\n"
     "      d->cfg_src_en_i = en; run(200);\n"
     "    }\n"
     "  }\n"
     "  return report();\n}\n"),
]


def main() -> int:
    path = Path(sys.argv[1])
    text = path.read_text()
    for old, new in EDITS:
        if text.count(old) != 1:
            print("edit refused, count", text.count(old), repr(old[:40]))
            return 2
        text = text.replace(old, new)
    path.write_text(text)
    print("race probe inserted")
    return 0


if __name__ == "__main__":
    sys.exit(main())
