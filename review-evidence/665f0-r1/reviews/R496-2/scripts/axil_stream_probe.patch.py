#!/usr/bin/env python3
"""Reviewer probe (R496-2): add one data-checked back-to-back write stream to a
SCRATCH copy of tb/verilator/mbx/axil_checks.hpp. Four writes to four
registers, AW and W re-offered together the cycle after both handshook; each
register read back afterwards. Usage: axil_stream_probe.patch.py AXIL_CHECKS_HPP"""
import sys
from pathlib import Path

p = Path(sys.argv[1])
s = p.read_text()
probe = r'''
    void reviewer_stream() {
        const std::uint32_t regs[4] = {MBX_REG_OWN_EID_LO, MBX_REG_OWN_EID_HI, MBX_REG_MAAP_BASE_LO,
                                       MBX_REG_TMR_DEADLINE};
        d_->s_bready_i = 1;
        unsigned next = 0, bs = 0;
        for (unsigned i = 0; i < 40 && bs < 4; ++i) {
            if (!d_->s_awvalid_i && !d_->s_wvalid_i && next < 4) {
                offer_aw(regs[next]);
                offer_w(0xA0000000u + next);
                ++next;
            }
            bs += clock().b ? 1u : 0u;
        }
        d_->s_awvalid_i = 0;
        d_->s_wvalid_i = 0;
        d_->s_bready_i = 0;
        ck_.dec("RP0 four back-to-back writes each get one B", bs, 4);
        for (unsigned k = 0; k < 4; ++k) {
            ck_.hex("RP0 each back-to-back write lands at its own address", b_.read(regs[k]), 0xA0000000u + k);
        }
    }
'''
anchor = "    void split_aw_first();\n"
assert s.count(anchor) == 1
s = s.replace(anchor, probe + anchor)
run_anchor = "        b_.reset();\n        reset_mid_transaction();\n"
assert s.count(run_anchor) == 1
s = s.replace(run_anchor, run_anchor + "        b_.reset();\n        reviewer_stream();\n")
p.write_text(s)
