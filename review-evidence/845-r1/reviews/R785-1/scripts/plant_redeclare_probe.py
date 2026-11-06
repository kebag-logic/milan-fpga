#!/usr/bin/env python3
"""Extend the planted pre-settle probe: re-declare after LINK_UP until it reads.

Usage: plant_redeclare_probe.py <sim_main.cpp already carrying the probe>

After LINK_UP the Talker is declared again every 30 ms, up to 200 times, and
the first declaration that reads Advertise is printed with its index, so the
probe separates "registers after a delay" from "never registers".
"""
import pathlib
import sys

path = pathlib.Path(sys.argv[1])
text = path.read_text()
OLD = ('            ck("PROBE no registration after LINK_UP before a new declaration", (up >> 6) & 1u, 0u);\n')
NEW = OLD + (
    '            int first_hit = -1;\n'
    '            for (int k = 0; k < 200 && first_hit < 0; ++k) {\n'
    '                register_talker(1, false);\n'
    '                const uint32_t rd = axi_read(A_ACMPL_STATE);\n'
    '                if ((rd >> 6) & 1u) first_hit = k;\n'
    '                if (k < 3 || k % 50 == 0 || first_hit >= 0) {\n'
    '                    printf("  [PROBE] re-declaration %d ACMPL_STATE=0x%08X\\n", k, rd);\n'
    '                }\n'
    '            }\n'
    '            printf("  [PROBE] first re-declaration that registered: %d\\n", first_hit);\n')
assert text.count(OLD) == 1, "the first probe is not planted"
path.write_text(text.replace(OLD, NEW))
print("planted")
