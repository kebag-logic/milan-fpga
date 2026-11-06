#!/usr/bin/env python3
"""Plant a disposable pre-settle probe in pp_shadow's U group of a scratch copy.

Usage: plant_presettle_probe.py <sim_main.cpp of a disposable copy>

The Talker is declared BEFORE the bind, the sink settles, and the Talker
attribute must read at the settle with no further declaration. LINK_CTRL[0]
then drops and restores the effective link, and the registration must be gone.
The unchanged U arms then run on the same sink.
"""
import pathlib
import sys

path = pathlib.Path(sys.argv[1])
text = path.read_text()
OLD = ('        printf("[U] a registered Talker attribute, as a bound sink reads it\\n");\n'
       '        bind_sink_zero_over_acmp();\n')
NEW = ('        printf("[U] a registered Talker attribute, as a bound sink reads it\\n");\n'
       '        register_talker(1, false);\n'
       '        bind_sink_zero_over_acmp();\n'
       '        run_idle(3000);\n'
       '        {\n'
       '            const uint32_t st = axi_read(A_ACMPL_STATE);\n'
       '            printf("  [PROBE] after settle ACMPL_STATE=0x%08X\\n", st);\n'
       '            ck("PROBE pre-settle Talker reads Advertise at the settle", (st >> 6) & 1u, 1u);\n'
       '            axi_write(0x71C, 0x0);\n'
       '            run_idle(3000);\n'
       '            const uint32_t dn = axi_read(A_ACMPL_STATE);\n'
       '            printf("  [PROBE] link down ACMPL_STATE=0x%08X\\n", dn);\n'
       '            ck("PROBE LINK_DOWN ended the settled registration", (dn >> 6) & 1u, 0u);\n'
       '            ck("PROBE the sink stays bound across the link change", (dn >> 3) & 1u, 1u);\n'
       '            axi_write(0x71C, 0x1);\n'
       '            run_idle(3000);\n'
       '            const uint32_t up = axi_read(A_ACMPL_STATE);\n'
       '            printf("  [PROBE] link up ACMPL_STATE=0x%08X\\n", up);\n'
       '            ck("PROBE no registration after LINK_UP before a new declaration", (up >> 6) & 1u, 0u);\n'
       '        }\n')
assert text.count(OLD) == 1, "the U group's opening moved"
path.write_text(text.replace(OLD, NEW))
print("planted")
