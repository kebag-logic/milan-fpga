#!/usr/bin/env python3
"""Append two reviewer checks (RV1, RV2) to a COPY of tb/verilator/mbx/suite.hpp.

RV1: a bound talker's ENTITY_AVAILABLE on interface 0 with the next frame
     (index 1) queued right behind it, so that frame's first byte and its
     interface are presented while the first frame's verdict is pending.
RV2: (two or more interfaces) on interface 1, a frame stalled inside its
     identity while its entry owes a copy (BOUND_EN set again alone) reaches
     no ring; the Q19 check repeated on interface 1.
Usage: r530_2_suite_patch.py <copy>/tb/verilator/mbx/suite.hpp
"""
import sys
from pathlib import Path

p = Path(sys.argv[1])
t = p.read_text()
anchor = '    ck_.dec("Q21 and the old one never does", older, 32);\n}\n'
assert t.count(anchor) == 1, "anchor"
add = r'''    ck_.dec("Q21 and the old one never does", older, 32);
    // ---- R530-2 reviewer checks ----
    clear_bound();
    set_bound(0, 0, talker, true);
    b_.idle(settle);
    {
        const std::uint32_t p0 = rx_pass(kAdp);
        b_.send_frame(available, 0);
        b_.send_frame(mbx_tb::adpdu(0, other), 1);
        b_.drain_rx();
        const std::uint32_t got = (rx_pass(kAdp) - p0) & 0xFFFFu;
        ck_.dec("RV1 a bound talker's AVAILABLE on interface 0, the next frame (index 1) queued behind it, passes alone",
                got, 1);
        for (std::uint32_t k = 0; k < got; ++k) {
            release(kAdp, peek(kAdp));
        }
        b_.ms(kRefillMs);
    }
#if MBX_N_IF >= 2
    clear_bound();
    set_bound(1, 0, talker, true);
    b_.idle(settle);
    {
        const std::uint32_t p1 = rx_pass(kAdp);
        b_.send_bytes(std::vector<std::uint8_t>(available.begin(), available.begin() + static_cast<std::ptrdiff_t>(cut)),
                      1, false);
        b_.drain_rx();
        wr(bnd_reg(1, 0, MBX_BND_REG_BOUND_EN), 1u);
        b_.idle(settle);
        b_.send_bytes(std::vector<std::uint8_t>(available.begin() + static_cast<std::ptrdiff_t>(cut), available.end()),
                      1, true);
        b_.drain_rx();
        const std::uint32_t got = (rx_pass(kAdp) - p1) & 0xFFFFu;
        ck_.dec("RV2 on interface 1, a frame stalled while its entry owes a copy reaches no ring", got, 0);
        for (std::uint32_t k = 0; k < got; ++k) {
            release(kAdp, peek(kAdp));
        }
        b_.ms(kRefillMs);
        const std::uint32_t p2 = rx_pass(kAdp);
        b_.send_frame(available, 1);
        b_.drain_rx();
        const std::uint32_t next = (rx_pass(kAdp) - p2) & 0xFFFFu;
        ck_.dec("RV2 the next one on interface 1 passes", next, 1);
        for (std::uint32_t k = 0; k < next; ++k) {
            release(kAdp, peek(kAdp));
        }
        b_.ms(kRefillMs);
    }
#endif
}
'''
p.write_text(t.replace(anchor, add))
print("patched", p)
