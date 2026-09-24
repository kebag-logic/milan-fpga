// SPDX-License-Identifier: CERN-OHL-W-2.0
// Disposable review probe (not committed anywhere): MVU cases the pinned
// tb/pp_top M-section does not send. Each case prints the command and the
// frame the RTL emitted, so the offline model can be compared to the RTL
// byte for byte by r280_rtl_vs_model.py, and CHECKs the frame the engine
// source predicts (only a whole Figure 5.3 GET_MILAN_INFO is served).
struct R280MvuProbe {
  H& h;
  static void hexline(const char* tag, const char* name,
                      const std::vector<uint8_t>& f) {
    printf("R280 %s %s ", tag, name);
    for (uint8_t b : f) printf("%02x", b);
    printf("\n");
  }
  void one(const char* name, uint8_t mt, uint16_t hi,
           const std::vector<uint8_t>& pl, uint16_t seq, uint8_t want_st,
           const std::vector<uint8_t>& want_pl) {
    auto cmd = aecp_frame(OWN_MAC, CTLR_MAC, mt, 0, EID, CTLR_EID, seq, hi, pl);
    h.q_aecp.clear();
    h.feed(cmd);
    auto got = h.wait_any(h.q_aecp, 400);
    auto want = aecp_frame(CTLR_MAC, OWN_MAC, uint8_t(mt | 1), want_st, EID,
                           CTLR_EID, seq, hi, want_pl);
    hexline("CMD", name, cmd);
    hexline("GOT", name, got);
    CHECK(!got.empty(), "R280 %s: silence", name);
    CHECK(got == want, "R280 %s: not the engine-source prediction", name);
  }
  static std::vector<uint8_t> pl8(uint32_t lo, uint16_t ct, uint16_t rsv,
                                  size_t n) {
    std::vector<uint8_t> p(n, 0);
    if (n >= 4) putbe(&p[0], lo, 4);
    if (n >= 6) putbe(&p[4], ct, 2);
    if (n >= 8) putbe(&p[6], rsv, 2);
    return p;
  }
  void run() {
    const uint32_t LO = 0xC50AC100u;
    std::vector<uint8_t> info(20, 0);
    putbe(&info[0], LO, 4);
    putbe(&info[8], 1u, 4);
    for (uint16_t ct : {uint16_t(0x0001), uint16_t(0x0003), uint16_t(0x0004)}) {
      char nm[64];
      snprintf(nm, sizeof nm, "ct_%04x_fig5.3_shape", ct);
      auto p = pl8(LO, ct, 0, 8);
      one(nm, 6, 0x001B, p, uint16_t(0xE000 + ct), 1, p);
    }
    auto p7 = pl8(LO, 0x0000, 0, 7);
    one("gmi_7_octets_cdl19", 6, 0x001B, p7, 0xE010, 1, p7);
    auto p16 = pl8(LO, 0x0000, 0, 16);
    one("gmi_16_octets_cdl28_served", 6, 0x001B, p16, 0xE011, 0, info);
    auto junk = pl8(LO, 0x0000, 0xDEAD, 8);
    one("gmi_junk_reserved_served", 6, 0x001B, junk, 0xE012, 0, info);
    auto suid = pl8(LO, 0x0001, 0, 16);
    putbe(&suid[8], 0x0123456789ABCDEFull, 8);
    one("set_suid_fig5.5_cdl28", 6, 0x001B, suid, 0xE013, 1, suid);
    std::vector<uint8_t> smcri = pl8(LO, 0x0003, 0, 8);
    const uint8_t mid[8] = {0x01, 0, 0x80, 0x70, 0, 0, 0, 0};
    smcri.insert(smcri.end(), mid, mid + 8);
    const char* nm7 = "DEFAULT";
    std::vector<uint8_t> name(64, 0);
    for (size_t i = 0; i < 7; ++i) name[i] = uint8_t(nm7[i]);
    smcri.insert(smcri.end(), name.begin(), name.end());
    one("set_mcri_fig5.6_cdl92", 6, 0x001B, smcri, 0xE014, 1, smcri);
    auto gmcri = pl8(LO, 0x0004, 0x0000, 8);
    one("get_mcri_fig5.7_cdl20", 6, 0x001B, gmcri, 0xE015, 1, gmcri);
    for (uint8_t mt : {uint8_t(2), uint8_t(4), uint8_t(8), uint8_t(10),
                       uint8_t(12), uint8_t(14)}) {
      char nm[64];
      snprintf(nm, sizeof nm, "mt%u_with_milan_pid", mt);
      auto p = pl8(LO, 0x0000, 0, 8);
      one(nm, mt, 0x001B, p, uint16_t(0xE020 + mt), 1, p);
    }
  }
};
