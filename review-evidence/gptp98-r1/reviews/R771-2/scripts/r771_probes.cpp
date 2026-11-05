// Reviewer probe rows for the Follow_Up TLV walk (FPGA-gPTP #98).
// Spliced into a copy of tb/verilator/parser/sim_main.cpp by
// probe_splice.py; uses only helpers present at base and head
// (Frame, Hdr, common, set_declared_to_physical, feed, feed_gap, feed_err,
// expect_eq, tick, dut, bank, ev_*), so the same rows run on both RTLs.
// Every row prints "PROBE <tag> ..." so the outcome is visible even when it
// is not an expectation failure.

namespace r771 {
struct Tlv { uint16_t type; uint16_t length; std::vector<uint8_t> value; };
static Tlv of(uint16_t type, const std::vector<uint8_t> &v) {
  return {type, static_cast<uint16_t>(v.size()), v};
}
//! 802.1AS-2011 Table 11-10 value (28 octets) with the given ids
static std::vector<uint8_t> info_value(uint32_t csro, uint16_t tbi,
                                       uint32_t oui = 0x0080C2,
                                       uint32_t sub = 1) {
  std::vector<uint8_t> v = {static_cast<uint8_t>(oui >> 16),
                            static_cast<uint8_t>(oui >> 8),
                            static_cast<uint8_t>(oui),
                            static_cast<uint8_t>(sub >> 16),
                            static_cast<uint8_t>(sub >> 8),
                            static_cast<uint8_t>(sub)};
  for (int s = 24; s >= 0; s -= 8) v.push_back(static_cast<uint8_t>(csro >> s));
  v.push_back(static_cast<uint8_t>(tbi >> 8));
  v.push_back(static_cast<uint8_t>(tbi));
  v.resize(24, 0x00);
  v.insert(v.end(), {0x00, 0x00, 0x01, 0x23});
  return v;
}
static Tlv info(uint32_t csro, uint16_t tbi) {
  return of(0x0003, info_value(csro, tbi));
}
static Frame fu(uint16_t seq, const std::vector<Tlv> &chain,
                uint16_t declared = 0, size_t pad = 0, uint8_t padbyte = 0) {
  Hdr h; h.mtype = 0x8; h.seq = seq; h.srcid = 0xAABBCCFFFE001122ull;
  h.srcpn = 1;
  Frame f = common(h, 10);
  f.u48(0x000012345678ull); f.u32(0x2FAF0800);
  for (const Tlv &t : chain) {
    f.u16(t.type); f.u16(t.length);
    for (uint8_t b : t.value) f.u8(b);
  }
  set_declared_to_physical(f);
  if (declared != 0) {
    f.b[16] = static_cast<uint8_t>(declared >> 8);
    f.b[17] = static_cast<uint8_t>(declared);
  }
  f.b.resize(f.b.size() + pad, padbyte);
  return f;
}
constexpr uint64_t W11 = (0xFFFFF000ull << 32) | (0x0007ull << 16);
}  // namespace r771

void RxParserHarness::r771_report(const char *tag, uint16_t d0) {
  printf("PROBE %-58s ev=%d code=%u drops=+%u w11=%s%016llx\n", tag,
         ev_count, ev_seen ? ev_code : 0,
         static_cast<unsigned>(static_cast<uint16_t>(dut->drop_cnt_o - d0)),
         bank.count(11) ? "" : "none:",
         static_cast<unsigned long long>(bank.count(11) ? bank[11] : 0));
}

void RxParserHarness::r771_accept(const char *tag, const Frame &f,
                                  uint64_t w11) {
  const uint16_t d0 = dut->drop_cnt_o;
  feed(f.b, false);
  r771_report(tag, d0);
  char n[128];
  snprintf(n, sizeof n, "R771 %s: event", tag);
  expect_eq(n, ev_seen ? ev_code : 0, 2);
  snprintf(n, sizeof n, "R771 %s: w11", tag);
  expect_eq(n, bank.count(11) ? bank[11] : ~0ull, w11);
  snprintf(n, sizeof n, "R771 %s: w4", tag);
  expect_eq(n, bank.count(4) ? bank[4] : ~0ull, 0x000012345678ull);
  snprintf(n, sizeof n, "R771 %s: w5", tag);
  expect_eq(n, bank.count(5) ? bank[5] : ~0ull, 0x2FAF0800ull);
  snprintf(n, sizeof n, "R771 %s: no drop", tag);
  expect_eq(n, dut->drop_cnt_o, d0);
}

void RxParserHarness::r771_refuse(const char *tag, const Frame &f) {
  const uint16_t d0 = dut->drop_cnt_o;
  feed(f.b, false);
  r771_report(tag, d0);
  char n[128];
  snprintf(n, sizeof n, "R771 %s: no event", tag);
  expect_eq(n, ev_seen, 0);
  snprintf(n, sizeof n, "R771 %s: one drop", tag);
  expect_eq(n, dut->drop_cnt_o, static_cast<uint16_t>(d0 + 1));
}

//! cycles from the eof byte's edge to the ev_valid_o edge, with an
//! optional idle cycle after every byte
int RxParserHarness::r771_event_latency(const std::vector<uint8_t> &b,
                                        bool gaps) {
  bank.clear(); ev_seen = false; ev_count = 0; ev_w0.clear();
  int since = -1, lat = -1;
  for (size_t i = 0; i < b.size(); i++) {
    dut->rx_valid_i = 1; dut->rx_data_i = b[i];
    dut->rx_sof_i = (i == 0); dut->rx_eof_i = (i + 1 == b.size());
    dut->rx_err_i = 0;
    tick();
    if (i + 1 == b.size()) since = 0;
    if (gaps && i + 1 != b.size()) {
      dut->rx_valid_i = 0; dut->rx_sof_i = 0; dut->rx_eof_i = 0;
      dut->rx_data_i = 0xA5;
      tick();
    }
  }
  dut->rx_valid_i = 0; dut->rx_sof_i = 0; dut->rx_eof_i = 0;
  for (int i = 0; i < 8; i++) {
    const bool before = ev_seen;
    tick(); since++;
    if (!before && ev_seen && lat < 0) lat = since;
  }
  return lat;
}

void RxParserHarness::check_r771_probes() {
  using namespace r771;
  const Tlv INFO = info(0xFFFFF000, 0x0007);
  const Tlv OTHER = of(0x0003, {0x12, 0x34, 0x56, 0xAB, 0xCD, 0xEF, 0x55, 0xAA});

  // -- information TLV with the wrong lengthField, alone and before a real one
  {
    std::vector<uint8_t> v30 = info_value(0xFFFFF000, 0x0007);
    v30.push_back(0); v30.push_back(0);
    std::vector<uint8_t> v26 = info_value(0xFFFFF000, 0x0007);
    v26.resize(26);
    r771_refuse("info TLV lengthField 30 alone", fu(0xA001, {of(3, v30)}));
    r771_refuse("info TLV lengthField 26 alone (min-len ok)",
                fu(0xA002, {of(3, v26), of(0x000A, {})}));
    r771_accept("info TLV lengthField 30 then real info",
                fu(0xA003, {of(3, v30), INFO}), W11);
  }
  // -- two information TLVs, first one first: word 11 from the first
  r771_accept("two info TLVs, info first",
              fu(0xA004, {INFO, info(0x00000FFF, 0x0009)}), W11);
  // -- zero-length TLVs: first, between, last at messageLength, then padding
  r771_accept("zero-len, info, zero-len at messageLength, padded",
              fu(0xA005, {of(0x000A, {}), INFO, of(0x0003, {})}, 0, 20, 0xFF),
              W11);
  r771_accept("org-ext zero-length first", fu(0xA006, {of(0x0003, {}), INFO}),
              W11);
  // -- the walk ending exactly at messageLength after an unknown first
  r771_accept("unknown first, walk ends at messageLength",
              fu(0xA007, {OTHER, INFO}), W11);
  // -- huge lengthField
  r771_refuse("unknown TLV lengthField 0xFFFE first",
              fu(0xA008, {{0x000A, 0xFFFE, {}}, INFO}));
  // -- information TLV only in physical padding past messageLength
  {
    Frame f = fu(0xA009, {OTHER, of(0x000A, std::vector<uint8_t>(20, 0x5A))});
    const size_t declared_end = f.b.size();
    f.u16(0x0003); f.u16(28);
    for (uint8_t b : INFO.value) f.u8(b);
    (void)declared_end;
    r771_refuse("info TLV only in padding past messageLength", f);
  }
  // -- maximum messageLength 1500, long unknown TLV first and last
  {
    const size_t unk = 1500 - 34 - 10 - 32 - 4;
    r771_accept("messageLength 1500, long unknown first",
                fu(0xA00A, {of(0x7FFE, std::vector<uint8_t>(unk, 0x11)), INFO}),
                W11);
    r771_accept("messageLength 1500, long unknown last",
                fu(0xA00B, {INFO, of(0x7FFE, std::vector<uint8_t>(unk, 0x11))}),
                W11);
  }
  // -- physically truncated inside the information TLV value (declared full)
  {
    Frame f = fu(0xA00C, {OTHER, INFO});
    f.b.resize(f.b.size() - 6);
    r771_refuse("frame cut 6 octets before messageLength", f);
  }
  // -- trailing TLV with an odd lengthField after the information TLV
  r771_refuse("odd lengthField after info", fu(0xA00D, {INFO, of(0x000A, {1, 2, 3})}));
  // -- rx_err on the gmTimeBaseIndicator byte of an info TLV behind an unknown
  {
    Frame f = fu(0xA00E, {OTHER, INFO});
    const size_t tbi = 58 + 12 + 15;
    const uint16_t d0 = dut->drop_cnt_o;
    feed_err(f.b, tbi, tbi);
    r771_report("rx_err on info TBI byte, unknown first", d0);
    expect_eq("R771 rx_err on info TBI byte: no event", ev_seen, 0);
    expect_eq("R771 rx_err on info TBI byte: one drop", dut->drop_cnt_o,
              static_cast<uint16_t>(d0 + 1));
  }
  // -- back to back, no idle cycle: refused cut chain then unknown-first FU,
  //    and unknown-first FU then an Announce
  {
    Frame cut = fu(0xA00F, {INFO});
    cut.u8(0x00); cut.u8(0x0A); set_declared_to_physical(cut);
    Frame good = fu(0xA010, {OTHER, INFO});
    const uint16_t d0 = dut->drop_cnt_o;
    feed_gap(cut.b, good.b, 0);
    r771_report("back-to-back: cut chain then unknown-first", d0);
    expect_eq("R771 b2b cut then unknown-first: one event", ev_count, 1);
    expect_eq("R771 b2b cut then unknown-first: ev_seq", ev_seq, 0xA010);
    expect_eq("R771 b2b cut then unknown-first: w11", bank.count(11) ? bank[11] : 0, W11);
    expect_eq("R771 b2b cut then unknown-first: one drop", dut->drop_cnt_o,
              static_cast<uint16_t>(d0 + 1));
    Frame ann = announce_frame(0xA011, AGM, 1, ASRC, {AGM});
    const uint16_t d1 = dut->drop_cnt_o;
    feed_gap(good.b, ann.b, 0);
    r771_report("back-to-back: unknown-first then Announce", d1);
    expect_eq("R771 b2b unknown-first then ann: two events", ev_count, 2);
    expect_eq("R771 b2b unknown-first then ann: last code", ev_code, 3);
    expect_eq("R771 b2b unknown-first then ann: no drop", dut->drop_cnt_o, d1);
    feed_gap(ann.b, good.b, 0);
    r771_report("back-to-back: Announce then unknown-first", d1);
    expect_eq("R771 b2b ann then unknown-first: two events", ev_count, 2);
    expect_eq("R771 b2b ann then unknown-first: w11", bank.count(11) ? bank[11] : 0, W11);
    expect_eq("R771 b2b ann then unknown-first: no drop", dut->drop_cnt_o, d1);
  }
  // -- event latency after eof: plain vs unknown first vs padded, with and
  //    without idle cycles between bytes
  {
    const int l_plain = r771_event_latency(fu(0xA012, {INFO}).b, false);
    const int l_unk = r771_event_latency(fu(0xA013, {OTHER, INFO}).b, false);
    const int l_pad = r771_event_latency(fu(0xA014, {OTHER, INFO}, 0, 30).b, false);
    const int l_gap = r771_event_latency(fu(0xA015, {OTHER, INFO}).b, true);
    const uint64_t w11_gap = bank.count(11) ? bank[11] : 0;
    printf("PROBE latency eof->event plain=%d unknown-first=%d padded=%d gapped=%d\n",
           l_plain, l_unk, l_pad, l_gap);
    expect_eq("R771 latency unknown-first == plain", l_unk, l_plain);
    expect_eq("R771 latency padded == plain", l_pad, l_plain);
    expect_eq("R771 latency gapped == plain", l_gap, l_plain);
    expect_eq("R771 gapped unknown-first: w11", w11_gap, W11);
  }
  // -- informational: an oversize physical frame (cnt_r wraps at 2048)
  {
    const uint16_t d0 = dut->drop_cnt_o;
    feed(fu(0xA016, {INFO}, 0, 2100, 0x00).b, false);
    r771_report("INFO-ONLY plain FU with 2100 padding octets (index wrap)", d0);
  }

  // -- round 2: malformed headers around the information TLV (#98)
  {
    const Tlv BADLEN = {0x000A, 0x0100, {}};
    const Tlv ODD = {0x000A, 0x0001, {}};
    const Tlv ZL = of(0x000A, {});
    r771_refuse("R2 past-messageLength header after info, then zero-len at end",
                fu(0xA101, {INFO, BADLEN, ZL}));
    r771_refuse("R2 odd header after info, then zero-len at end",
                fu(0xA102, {INFO, ODD, ZL}));
    r771_refuse("R2 past-messageLength header ahead of info, padded 8",
                fu(0xA103, {BADLEN, INFO}, 0, 8));
    r771_refuse("R2 two malformed headers ahead of info",
                fu(0xA104, {BADLEN, ODD, INFO}));
    r771_refuse("R2 odd header after info, then other TLV to the end",
                fu(0xA105, {INFO, ODD, OTHER}));
  }
}
