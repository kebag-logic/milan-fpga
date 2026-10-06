#!/usr/bin/env python3
"""Print-only probe of tb/pp_top section DN (PR #164, R502-2).

Plants printf lines (no logic change) in a copy of tb/pp_top/notify_phases.hpp
so the run prints: every frame to controller A with its clock, each stimulus
clock, each MRPDU's last-byte clock and feed()'s return, and last_sent at each
space_out() return. Usage: probe_dn_clocks.py TREE   (TREE = a copy of the head)
"""
import sys
from pathlib import Path

p = Path(sys.argv[1]) / "tb/pp_top/notify_phases.hpp"
s = p.read_text()
edits = [
    ("  void space_out() {\n    while (io.t < last_sent + SPACING) tick();\n  }\n",
     "  void space_out() {\n    while (io.t < last_sent + SPACING) tick();\n"
     "    printf(\"  [probe] space_out returns at %llu (last_sent %llu)\\n\",\n"
     "           (unsigned long long)io.t, (unsigned long long)last_sent);\n  }\n"),
    ("    feed(mrpdu_frame(true, T1_MAC, {dom}));\n  }\n",
     "    const auto fr = mrpdu_frame(true, T1_MAC, {dom});\n"
     "    const uint64_t tb = io.t;\n    feed(fr);\n"
     "    printf(\"  [probe] MRPDU vid %u: %zu bytes, last byte at %llu, feed() returns at %llu\\n\",\n"
     "           unsigned(vid), fr.size(), (unsigned long long)(tb + fr.size()),\n"
     "           (unsigned long long)io.t);\n  }\n"),
    ("    io.d->link_up_i = 0;\n    one_notification(",
     "    io.d->link_up_i = 0;\n"
     "    printf(\"  [probe] link down at %llu\\n\", (unsigned long long)io.t);\n    one_notification("),
    ("    io.d->link_up_i = 1;\n    one_notification(",
     "    io.d->link_up_i = 1;\n"
     "    printf(\"  [probe] link up at %llu\\n\", (unsigned long long)io.t);\n    one_notification("),
    ("    printf(\"  [i] DN: %u ms of the timebase after the registration",
     "    for (size_t i = 0; i < seen.size(); ++i)\n"
     "      if (da_of(seen[i].f) == CTLR_MAC)\n"
     "        printf(\"  [probe] frame to A #%zu at %llu: u %d ct 0x%04x seq %u status %u\\n\", i,\n"
     "               (unsigned long long)seen[i].t, int(unsolicited(seen[i].f)), ct_of(seen[i].f),\n"
     "               seq_of(seen[i].f), status_of(seen[i].f));\n"
     "    printf(\"  [i] DN: %u ms of the timebase after the registration"),
]
for old, new in edits:
    assert s.count(old) == 1, old
    s = s.replace(old, new)
p.write_text(s)
print("planted", len(edits), "print-only edits in", p)
