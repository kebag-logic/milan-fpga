#!/usr/bin/env python3
"""Add an environment-driven link flap to a COPY of sim_boot_sa.cpp.

BOOTSA_FLAP_AT / BOOTSA_FLAP_LEN (cycles) drop i_link_up once, as the PHY's
auto-negotiation restart does; BOOTSA_FLAP_STALL=1 also stops the MAC taking
beats for that window. Prints tx_sa_ok_w and o_mac_reinit at the edges of the
window and the first frames after it. Unset, the leg is unchanged.
usage: patch_flap.py <sim_boot_sa.cpp>
"""
import sys
p = sys.argv[1]
s = open(p).read()
hook = '''void BootSaHarness::tick() {
    {
        static const uint64_t at = getenv("BOOTSA_FLAP_AT") ? strtoull(getenv("BOOTSA_FLAP_AT"), nullptr, 0) : 0;
        static const uint64_t len = getenv("BOOTSA_FLAP_LEN") ? strtoull(getenv("BOOTSA_FLAP_LEN"), nullptr, 0) : 0;
        static const bool stall = getenv("BOOTSA_FLAP_STALL") != nullptr;
        static bool reinit_q = false;
        const auto* r0 = dut_->rootp;
        if (at && cyc_ == at) {
            printf("[FLAP] link down at cycle %llu: tx_sa_ok=%d\\n", (unsigned long long)cyc_,
                   (int)r0->milan_datapath__DOT__tx_sa_ok_w);
            dut_->i_link_up = 0;
            if (stall) dut_->m_axis_mac_tx_tready = 0;
        }
        if (at && cyc_ == at + len) {
            printf("[FLAP] link up at cycle %llu: tx_sa_ok=%d frames so far %zu\\n", (unsigned long long)cyc_,
                   (int)r0->milan_datapath__DOT__tx_sa_ok_w, sent_.size());
            dut_->i_link_up = 1;
            dut_->m_axis_mac_tx_tready = 1;
        }
        if (at && (bool)dut_->o_mac_reinit != reinit_q) {
            reinit_q = dut_->o_mac_reinit;
            printf("[FLAP] o_mac_reinit=%d at cycle %llu: tx_sa_ok=%d\\n", (int)reinit_q,
                   (unsigned long long)cyc_, (int)r0->milan_datapath__DOT__tx_sa_ok_w);
        }
    }
'''
assert s.count("void BootSaHarness::tick() {\n") == 1
s = s.replace("void BootSaHarness::tick() {\n", hook)
tail = '''    s.before_mac = !(wrote_lo_ && wrote_hi_);
    {
        static const uint64_t at = getenv("BOOTSA_FLAP_AT") ? strtoull(getenv("BOOTSA_FLAP_AT"), nullptr, 0) : 0;
        static const uint64_t len = getenv("BOOTSA_FLAP_LEN") ? strtoull(getenv("BOOTSA_FLAP_LEN"), nullptr, 0) : 0;
        static unsigned shown = 0;
        if (at && cyc_ > at + len && shown < 6) {
            ++shown;
            printf("[FLAP] after the flap: frame at cycle %llu kind %d sa %012llx\\n",
                   (unsigned long long)cyc_, (int)s.kind, (unsigned long long)s.sa);
        }
    }
'''
assert s.count("    s.before_mac = !(wrote_lo_ && wrote_hi_);\n") == 1
s = s.replace("    s.before_mac = !(wrote_lo_ && wrote_hi_);\n", tail)
s = s.replace('#include "Vmilan_datapath.h"\n', '#include "Vmilan_datapath.h"\n#include <cstdlib>\n#include <cstdio>\n', 1)
open(p, "w").write(s)
