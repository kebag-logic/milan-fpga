#!/usr/bin/env python3
"""Measure probing_status either side of a link change on a settled input.

Usage: plant_probing_status_probe.py <sim_main.cpp carrying the earlier probes>

Reads a solicited GET_STREAM_INFO on STREAM_INPUT 0 before the link drops and
after it returns, and prints probing_status (3 COMPLETED, 1 PASSIVE, 2 ACTIVE)
and the three stream-valid flags, which are valid only while settled.
"""
import pathlib
import sys

path = pathlib.Path(sys.argv[1])
text = path.read_text()


def status(tag: str, seq: str) -> str:
    return ('            {\n'
            f'                const std::vector<uint8_t> g = gsi_input0({seq});\n'
            '                if (g.size() >= 94) {\n'
            f'                    printf("  [PROBE] {tag}: probing_status=%u stream_flags=0x%02X\\n",\n'
            '                           static_cast<unsigned>(g[90] >> 5),\n'
            '                           static_cast<unsigned>(g[42] & G_STREAM_FLAGS));\n'
            '                } else {\n'
            f'                    printf("  [PROBE] {tag}: short response %zu\\n", g.size());\n'
            '                }\n'
            '            }\n')


BEFORE = '            const size_t probe_at = tx_frames.size();\n'
AFTER = '            auto probes_since = [&](size_t from) {\n'
assert text.count(BEFORE) == 1 and text.count(AFTER) == 1, "the earlier probes are not planted"
text = text.replace(BEFORE, status("settled, before the link change", "0x07E0") + BEFORE)
text = text.replace(AFTER, status("after LINK_DOWN and LINK_UP", "0x07E1") + AFTER)
path.write_text(text)
print("planted")
