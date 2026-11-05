#!/usr/bin/env python3
"""Derive a probe copy of sim_boot_sa.cpp that adds one boot after the leg's
own: reset, then configure_fabric() with its two MAC_ADDR writes dropped (so
AAF, LWSRP, MAAP and CRF are enabled with the pair unwritten), the AAF
bypass opened, 600 processor ms run; then both halves written and the run
continued until MAAP, AAF and CRF have each sent. Graded: no CSR-addressed
frame before the pair, every frame after it from the station MAC, each of
MAAP/AAF/CRF sent, A_TXARB_DIAG clean.
Usage: make_probe_harness.py <sim_boot_sa.cpp> <out.cpp>"""
import sys
from pathlib import Path
t = Path(sys.argv[1]).read_text()
def once(a, b):
    global t
    assert t.count(a) == 1, a
    t = t.replace(a, b)
once("    void csr_write(unsigned int offset, uint32_t value) {\n",
     "    bool drop_mac_ = false;\n    void early_enables();\n"
     "    void csr_write(unsigned int offset, uint32_t value) {\n"
     "        if (drop_mac_ && (offset == 0x108 || offset == 0x10C)) return;\n")
once("        pair_order(0x10C, 0x108, \"MAC_ADDR_HI\");\n",
     "        pair_order(0x10C, 0x108, \"MAC_ADDR_HI\");\n        early_enables();\n")
once("int BootSaHarness::run() {\n", r'''void BootSaHarness::early_enables() {
    reset();
    const size_t from = sent_.size();
    drop_mac_ = true;
    boot_fw_configure_fabric();
    drop_mac_ = false;
    write(0x654, read(0x654) | 0x2u);
    run_cycles(600 * kMsCyc);
    size_t early = 0;
    for (size_t i = from; i < sent_.size(); ++i) {
        if (sent_[i].kind != Kind::Gptp) {
            ++early;
            printf("[PROBE] early frame %s cycle %llu source %012llx\n",
                   kKindName[static_cast<size_t>(sent_[i].kind)],
                   static_cast<unsigned long long>(sent_[i].cyc),
                   static_cast<unsigned long long>(sent_[i].sa));
        }
    }
    check_.dec("[PROBE] early enables: no CSR-addressed frame before the pair is written", early, 0);
    const size_t rel = sent_.size();
    write(0x108, kStationMacLo);
    write(0x10C, kStationMacHi);
    auto seen = [this, rel](Kind k) {
        for (size_t i = rel; i < sent_.size(); ++i) if (sent_[i].kind == k) return true;
        return false;
    };
    const uint64_t end = cyc_ + kPastBoundCyc;
    while (cyc_ < end && !(seen(Kind::Maap) && seen(Kind::Aaf) && seen(Kind::Crf))) tick();
    std::array<uint64_t, kKindName.size()> n{};
    uint64_t wrong = 0;
    for (size_t i = rel; i < sent_.size(); ++i) {
        ++n[static_cast<size_t>(sent_[i].kind)];
        wrong += sent_[i].sa != kStationMac;
    }
    printf("[PROBE] after the pair:");
    for (size_t k = 0; k < kKindName.size(); ++k)
        if (n[k]) printf(" %s %llu", kKindName[k], static_cast<unsigned long long>(n[k]));
    printf("\n");
    check_.dec("[PROBE] early enables: every frame after the pair carries the station MAC", wrong, 0);
    check_.that("[PROBE] early enables: MAAP sends after the pair", seen(Kind::Maap));
    check_.that("[PROBE] early enables: AAF sends after the pair", seen(Kind::Aaf));
    check_.that("[PROBE] early enables: CRF sends after the pair", seen(Kind::Crf));
    const uint32_t diag = read(0x784);
    check_.hex("[PROBE] early enables: A_TXARB_DIAG no stall or abort", (diag >> 8) & 0xFFFF, 0);
}

int BootSaHarness::run() {
''')
inc = Path(sys.argv[1]).resolve().parent / '../../common'
t = t.replace('#include "../../common/', '#include "' + str(inc.resolve()) + '/')
Path(sys.argv[2]).write_text(t)
