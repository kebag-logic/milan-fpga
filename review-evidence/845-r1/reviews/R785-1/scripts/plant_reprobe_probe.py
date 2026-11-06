#!/usr/bin/env python3
"""Replace the re-declaration loop: show what a settled input does across a link change.

Usage: plant_reprobe_probe.py <sim_main.cpp carrying the re-declaration probe>

After LINK_UP this counts the listener's own probes (CONNECT_TX_COMMAND at the
talker) since the link change, re-declares the Talker, then answers the newest
probe through the harness's bind helper. If the input left settled, a probe
appears and the Talker reads Advertise only after the answer settles it.
"""
import pathlib
import re
import sys

path = pathlib.Path(sys.argv[1])
text = path.read_text()
LOOP = re.compile(r"            int first_hit = -1;\n.*?first re-declaration that registered: %d\\n\", first_hit\);\n", re.S)
NEW = (
    '            auto probes_since = [&](size_t from) {\n'
    '                int n = 0;\n'
    '                for (size_t i = from; i < tx_frames.size(); ++i) {\n'
    '                    const std::vector<uint8_t>& b = tx_frames[i].bytes;\n'
    '                    if (classify(tx_frames[i]) == FR_ACMP && b.size() >= 70\n'
    '                        && (b[15] & 0xF) == 0 && get_be(b, 34, 8) == U_TALKER_EID) ++n;\n'
    '                }\n'
    '                return n;\n'
    '            };\n'
    '            run_idle(200000);\n'
    '            printf("  [PROBE] listener probes since the link change: %d\\n", probes_since(probe_at));\n'
    '            register_talker(1, false);\n'
    '            const uint32_t rd = axi_read(A_ACMPL_STATE);\n'
    '            printf("  [PROBE] after re-declaration, unanswered probe ACMPL_STATE=0x%08X\\n", rd);\n'
    '            bind_sink_zero_over_acmp();\n'
    '            run_idle(3000);\n'
    '            const uint32_t rs = axi_read(A_ACMPL_STATE);\n'
    '            printf("  [PROBE] after the probe was answered ACMPL_STATE=0x%08X\\n", rs);\n'
    '            ck("PROBE re-declared Talker reads Advertise once the input settles again", (rs >> 6) & 1u, 1u);\n')
assert len(LOOP.findall(text)) == 1, "the re-declaration probe is not planted"
text = LOOP.sub(lambda _: NEW, text)
MARK = '            axi_write(0x71C, 0x0);\n            run_idle(3000);\n            const uint32_t dn'
assert text.count(MARK) == 1
text = text.replace(MARK, '            const size_t probe_at = tx_frames.size();\n' + MARK)
path.write_text(text)
print("planted")
