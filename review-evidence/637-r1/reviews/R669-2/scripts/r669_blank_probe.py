#!/usr/bin/env python3
"""Reviewer probe for #637 round 2: add, to a DISPOSABLE copy of the dynmap
leg, two restore cases whose window holds ONLY a map record that is framed
but fails one term of the validated-record test (a payload byte changed
under the old crc16; a wrong record id, re-sealed), and grade PP_STAT as the
D3 rule states it: done 1, fail 0, blank 1 (no record validated, none failed).
No GET page is graded, so the leg's vacuity count is unchanged.

Usage: python3 r669_blank_probe.py SUITE_DIR   (patches SUITE_DIR/sim_nxn.cpp)
"""
import sys
from pathlib import Path

src = Path(sys.argv[1]) / "sim_nxn.cpp"
text = src.read_text()
anchor = ("        maprec_pass0_abort_section(x);\n"
          "        //! every page above ran: a GET that never answered would otherwise\n")
probe = (
    "        maprec_pass0_abort_section(x);\n"
    "        {   // reviewer probe: a window holding only one framed map record\n"
    "            const std::string rec = map_record(0x60, x.in_saved, maprec_in_entries());\n"
    "            std::vector<uint8_t> area;\n"
    "            RecAt at;\n"
    "            const bool ok = maprec_codec_window({rec}, &area, &at) && at.count(0x60);\n"
    "            ck(\"[PROBE] the codec frames the lone map record\", static_cast<unsigned long>(ok), 1);\n"
    "            if (ok) {\n"
    "                std::vector<uint8_t> a = area;\n"
    "                a[at[0x60].first + 8 + 5] ^= 0x04;\n"
    "                nmem = a;\n"
    "                maprec_power_cycle(\"probe crc-bad lone record\", false);\n"
    "                maprec_grade_stat(\"probe crc-bad lone record\", false, true);\n"
    "                a = area;\n"
    "                a[at[0x60].first + 3] = 0x61;\n"
    "                maprec_reseal(&a, at[0x60].first);\n"
    "                nmem = a;\n"
    "                maprec_power_cycle(\"probe wrong-id lone record\", false);\n"
    "                maprec_grade_stat(\"probe wrong-id lone record\", false, true);\n"
    "            }\n"
    "        }\n"
    "        //! every page above ran: a GET that never answered would otherwise\n")
if text.count(anchor) != 1:
    sys.exit("anchor not found exactly once")
src.write_text(text.replace(anchor, probe))
print("patched", src)
