// SPDX-License-Identifier: CERN-OHL-W-2.0
// KL_srp_decoder suite — independent expectations, never DUT logic.
//
// Every MRPDU is hand-built byte-exact against 10 §3 (F10.6/F10.7/F10.8) and
// every expected event is an explicit constant, computed by hand from the
// vector-value-k rule — the harness never re-implements the decoder. Covers:
// the certified-bench Domain shape (NumberOfValues = 2 from FirstValue
// {5, 2, VID} — class A surfaced as value 1 with priority 3, THE +k
// regression), range-reconstructed talker vectors, Talker Failed fields,
// Listener four-packed pairing (all four codes), MVRP VID decode, the dual
// EndMark framing truth (a single-EndMark PDU is malformed), a lying MSRP
// AttributeListLength (counted + flagged, framing survives), the Milan
// §4.2.7.1.2 tolerance list per F09.4 (truncation mid-FirstValue,
// mid-vector, bad AttributeLength with subsequent messages discarded,
// out-of-alphabet three-packed digit), and per-application LeaveAll.
#include <cstdint>
#include <cstdio>
#include <vector>
#include "VKL_srp_decoder.h"
#include "verilated.h"
#include "../common/verilator_harness.hpp"
#define CHECK(cond, ...) do { \
  ++checks; \
  if (!(cond)) { ++fails; printf("FAIL: " __VA_ARGS__); printf("\n"); } \
} while (0)

struct Evt {
  bool     msrp;
  unsigned attr;
  unsigned vid;
  unsigned ev;
  unsigned fp;
  unsigned mfs;
  unsigned mif;
  unsigned prio;
  unsigned rank;
  unsigned fcode;
  unsigned cid;
  bool     ca;
  uint64_t sid;
  uint64_t da;
  uint64_t sysid;
  uint32_t lat;
};
struct Done {
  bool ok;
  bool mal;
};

// harness timing guards, in clock cycles
constexpr int kResetCycles     = 4;      // reset held before release
constexpr int kFeedGuardCycles = 30000;  // byte-feed watchdog
constexpr int kDrainCycles     = 16;     // clocked after the last byte

struct Harness {
  VKL_srp_decoder* dut;
  std::vector<Evt>  evts;
  std::vector<Done> dones;
  int la_msrp = 0;
  int la_mvrp = 0;
  int llbad = 0;
  unsigned llcnt_at_bad = 0;

  explicit Harness(VKL_srp_decoder* d) : dut(d) {}

  void clear() {
    evts.clear(); dones.clear();
    la_msrp = la_mvrp = llbad = 0; llcnt_at_bad = 0;
  }

  // pre-edge sampling: settle inputs, observe registered strobes, then edge
  bool tick() {
    dut->clk_i = 0; dut->eval();
    bool acc = dut->mrp_valid_i && dut->mrp_ready_o;
    if (dut->evt_valid_o) {
      Evt e;
      e.msrp = dut->evt_msrp_o;
      e.attr = dut->evt_attr_type_o;
      e.sid  = dut->evt_stream_id_o;
      e.da   = dut->evt_da_o;
      e.vid  = dut->evt_vid_o;
      e.ev   = dut->evt_mrp_event_o;
      e.fp   = dut->evt_fourpacked_o;
      e.mfs  = dut->evt_max_frame_size_o;
      e.mif  = dut->evt_max_interval_frames_o;
      e.prio = dut->evt_priority_o;
      e.rank = dut->evt_rank_o;
      e.lat  = dut->evt_acc_latency_o;
      e.sysid = dut->evt_failure_system_id_o;
      e.fcode = dut->evt_failure_code_o;
      e.cid  = dut->evt_class_id_o;
      e.ca   = dut->evt_class_a_o;
      evts.push_back(e);
    }
    if (dut->la_msrp_o) ++la_msrp;
    if (dut->la_mvrp_o) ++la_mvrp;
    if (dut->listlen_bad_o) { ++llbad; llcnt_at_bad = dut->dbg_listlen_cnt_o; }
    if (dut->pdu_done_o) dones.push_back({static_cast<bool>(dut->pdu_ok_o),
                                          static_cast<bool>(dut->pdu_malformed_o)});
    dut->clk_i = 1; dut->eval();
    return acc;
  }

  void feed(const std::vector<uint8_t>& b, bool msrp) {
    size_t i = 0;
    int guard = 0;
    while (i < b.size() && guard++ < kFeedGuardCycles) {
      dut->mrp_valid_i = 1;
      dut->mrp_data_i  = b[i];
      dut->mrp_last_i  = (i + 1 == b.size());
      dut->mrp_msrp_i  = msrp;
      if (tick()) ++i;
    }
    dut->mrp_valid_i = 0; dut->mrp_last_i = 0;
    for (int k = 0; k < kDrainCycles; ++k) tick();
  }
};

// ---- byte-exact builders (wire order, big-endian fields) ------------------
static void P8 (std::vector<uint8_t>& v, uint8_t x)  { v.push_back(x); }
static void P16(std::vector<uint8_t>& v, uint16_t x) { v.push_back(uint8_t(x >> 8)); v.push_back(uint8_t(x)); }
static void P32(std::vector<uint8_t>& v, uint32_t x) { for (int i = 3; i >= 0; --i) v.push_back(uint8_t(x >> (8 * i))); }
static void P48(std::vector<uint8_t>& v, uint64_t x) { for (int i = 5; i >= 0; --i) v.push_back(uint8_t(x >> (8 * i))); }
static void P64(std::vector<uint8_t>& v, uint64_t x) { for (int i = 7; i >= 0; --i) v.push_back(uint8_t(x >> (8 * i))); }

// F10.7 Talker Advertise FirstValue (25 B)
static void talker_fv(std::vector<uint8_t>& v, uint64_t sid, uint64_t da,
                      uint16_t vid, uint16_t mfs, uint16_t mif,
                      uint8_t prbyte, uint32_t lat) {
  P64(v, sid); P48(v, da); P16(v, vid); P16(v, mfs); P16(v, mif);
  P8(v, prbyte); P32(v, lat);
}

// shared field constants
constexpr uint64_t SIDB = 0x0011223344550000ull;      // stream_id base (MAC + uid)
constexpr uint64_t DAB  = 0x91E0F0000E80ull;          // destination MAC base
constexpr uint8_t  PRB  = 0x70;                       // priority 3, rank 1
constexpr uint32_t LATB = 200000;                     // accumulated_latency

// ---- the suite ----------------------------------------------------------
// One object owns the model, the byte-feed harness and the tally, so every
// phase below is a named member function rather than another stretch of a
// `main` nobody can scope (Core Guidelines I.2, F.3).
namespace {
class SrpDecoderSuite {
 public:
  int run();

 private:
  void reset_releases_the_decoder();
  void the_certified_domain_shape_surfaces_class_a_at_plus_k();
  void a_multi_value_talker_advertise_reconstructs_the_range();
  void talker_failed_surfaces_the_failure_information();
  void listener_four_packed_decodes_all_four_codes();
  void mvrp_vid_decodes_without_a_list_length();
  void a_single_endmark_pdu_is_malformed();
  void a_lying_list_length_is_counted_and_framing_survives();
  void truncation_mid_first_value_is_tolerated();
  void truncation_mid_vector_keeps_the_prefix();
  void a_bad_attribute_length_recovers_on_the_next_pdu();
  void a_malformed_message_discards_every_later_message();
  void leave_all_is_per_application();
  void an_out_of_alphabet_three_packed_digit_is_malformed();
  void an_explicit_endmark_makes_frame_padding_inert();
  void a_multi_message_msrp_pdu_decodes_every_message();

  const milan::tb::Model<VKL_srp_decoder> model;
  VKL_srp_decoder* const dut = model.get();
  Harness h{dut};
  int checks = 0;
  int fails = 0;
};
}  // namespace

void SrpDecoderSuite::reset_releases_the_decoder() {
  dut->rst_n = 0; dut->mrp_valid_i = 0; dut->mrp_last_i = 0;
  dut->mrp_data_i = 0; dut->mrp_msrp_i = 0;
  for (int i = 0; i < kResetCycles; ++i) h.tick();
  dut->rst_n = 1;
  h.tick();
}

// ==== A: certified-bench Domain shape — THE +k regression pin ==========
// 802.1Q §35.2.2.9's worked example: NumberOfValues = 2 from FirstValue
// {SRclassID 5, SRclassPriority 2, VID 2} -> class A arrives as value 1
// with priority 3. Both events JoinIn.
void SrpDecoderSuite::the_certified_domain_shape_surfaces_class_a_at_plus_k() {
  h.clear();
  std::vector<uint8_t> p;
  P8(p, 0);                       // ProtocolVersion
  P8(p, 4); P8(p, 4);             // AttributeType Domain, AttributeLength 4
  P16(p, 9);                      // AttributeListLength: 2+4+1+2 = 9
  P16(p, 0x0002);                 // VectorHeader: LA=0, NumberOfValues=2
  P8(p, 5); P8(p, 2); P16(p, 2);  // FirstValue {5, 2, VID 2}
  P8(p, 42);                      // ThreePacked [JoinIn, JoinIn, pad]
  P16(p, 0); P16(p, 0);           // dual EndMark
  h.feed(p, true);

  CHECK(h.evts.size() == 2, "A evts 2 got %zu", h.evts.size());
  if (h.evts.size() == 2) {
    CHECK(h.evts[0].attr == 4, "A v0 attr Domain got %u", h.evts[0].attr);
    CHECK(h.evts[0].msrp, "A v0 application MSRP");
    CHECK(h.evts[0].cid == 5, "A v0 SRclassID 5 got %u", h.evts[0].cid);
    CHECK(h.evts[0].prio == 2, "A v0 prio 2 got %u", h.evts[0].prio);
    CHECK(h.evts[0].vid == 2, "A v0 VID 2 got %u", h.evts[0].vid);
    CHECK(!h.evts[0].ca, "A v0 is NOT class A");
    CHECK(h.evts[0].ev == 1, "A v0 JoinIn got %u", h.evts[0].ev);
    CHECK(h.evts[1].cid == 6, "A v1 SRclassID 6 got %u", h.evts[1].cid);
    CHECK(h.evts[1].prio == 3, "A v1 prio 3 (+k) got %u", h.evts[1].prio);
    CHECK(h.evts[1].vid == 2, "A v1 VID unchanged got %u", h.evts[1].vid);
    CHECK(h.evts[1].ca, "A v1 IS class A (surfaced at value 1)");
    CHECK(h.evts[1].ev == 1, "A v1 JoinIn got %u", h.evts[1].ev);
  }
  CHECK(h.dones.size() == 1, "A one done got %zu", h.dones.size());
  CHECK(!h.dones.empty() && h.dones[0].ok && !h.dones[0].mal, "A done ok");
  CHECK(h.llbad == 0, "A AttributeListLength truthful");
  CHECK(h.la_msrp == 0 && h.la_mvrp == 0, "A no LeaveAll");
}

// ==== B: multi-value Talker Advertise — range reconstruction ============
void SrpDecoderSuite::a_multi_value_talker_advertise_reconstructs_the_range() {
  h.clear();
  std::vector<uint8_t> p;
  P8(p, 0);
  P8(p, 1); P8(p, 25);            // Talker Advertise, 25 B
  P16(p, 31);                     // 2+25+2+2
  P16(p, 0x0005);                 // NumberOfValues = 5
  talker_fv(p, SIDB + 1, DAB, 2, 217, 1, PRB, LATB);
  P8(p, 8);                       // [New, JoinIn, In]
  P8(p, 132);                     // [JoinMt, Mt, pad]
  P16(p, 0); P16(p, 0);
  h.feed(p, true);

  CHECK(h.evts.size() == 5, "B evts 5 got %zu", h.evts.size());
  if (h.evts.size() == 5) {
    constexpr unsigned evs[5] = {0, 1, 2, 3, 4};
    for (int k = 0; k < 5; ++k) {
      CHECK(h.evts[k].sid == SIDB + 1 + k, "B v%d stream_id +k got %llx",
            k, static_cast<unsigned long long>(h.evts[k].sid));
      CHECK(h.evts[k].da == DAB + k, "B v%d DA +k got %llx",
            k, static_cast<unsigned long long>(h.evts[k].da));
      CHECK(h.evts[k].ev == evs[k], "B v%d event got %u", k, h.evts[k].ev);
    }
    CHECK(h.evts[0].attr == 1, "B attr TalkerAdv got %u", h.evts[0].attr);
    CHECK(h.evts[0].vid == 2, "B vlan_id got %u", h.evts[0].vid);
    CHECK(h.evts[0].mfs == 217, "B MaxFrameSize got %u", h.evts[0].mfs);
    CHECK(h.evts[0].mif == 1, "B MaxIntervalFrames got %u", h.evts[0].mif);
    CHECK(h.evts[0].prio == 3, "B PCP got %u", h.evts[0].prio);
    CHECK(h.evts[0].rank == 1, "B rank got %u", h.evts[0].rank);
    CHECK(h.evts[0].lat == LATB, "B acc_latency got %u", h.evts[0].lat);
    CHECK(h.evts[4].mfs == 217 && h.evts[4].lat == LATB,
          "B TSpec rides every value");
  }
  CHECK(h.dones.size() == 1 && h.dones[0].ok, "B done ok");
}

// ==== C: Talker Failed — FailureInformation surfaced ====================
void SrpDecoderSuite::talker_failed_surfaces_the_failure_information() {
  h.clear();
  std::vector<uint8_t> p;
  P8(p, 0);
  P8(p, 2); P8(p, 34);            // Talker Failed, 34 B
  P16(p, 39);                     // 2+34+1+2
  P16(p, 0x0001);
  talker_fv(p, SIDB + 2, DAB, 2, 217, 1, PRB, LATB);
  P64(p, 0xAABBCCDDEEFF0001ull);  // FailureInformation system id
  P8(p, 1);                       // failure code 1 (insufficient bandwidth)
  P8(p, 180);                     // [Lv]
  P16(p, 0); P16(p, 0);
  h.feed(p, true);

  CHECK(h.evts.size() == 1, "C evts 1 got %zu", h.evts.size());
  if (h.evts.size() == 1) {
    CHECK(h.evts[0].attr == 2, "C attr TalkerFailed got %u", h.evts[0].attr);
    CHECK(h.evts[0].ev == 5, "C event Lv got %u", h.evts[0].ev);
    CHECK(h.evts[0].sysid == 0xAABBCCDDEEFF0001ull, "C system id got %llx",
          static_cast<unsigned long long>(h.evts[0].sysid));
    CHECK(h.evts[0].fcode == 1, "C failure code got %u", h.evts[0].fcode);
    CHECK(h.evts[0].sid == SIDB + 2, "C stream_id got %llx",
          static_cast<unsigned long long>(h.evts[0].sid));
    CHECK(h.evts[0].da == DAB, "C DA got %llx",
          static_cast<unsigned long long>(h.evts[0].da));
  }
  CHECK(h.dones.size() == 1 && h.dones[0].ok, "C done ok");
}

// ==== D: Listener four-packed — all four declaration codes ==============
void SrpDecoderSuite::listener_four_packed_decodes_all_four_codes() {
  h.clear();
  std::vector<uint8_t> p;
  P8(p, 0);
  P8(p, 3); P8(p, 8);             // Listener, 8 B
  P16(p, 15);                     // 2+8+2+1+2
  P16(p, 0x0004);
  P64(p, SIDB + 0x100);
  P8(p, 44);                      // [JoinIn, JoinIn, In]
  P8(p, 144);                     // [Mt, pad, pad]
  P8(p, 0x1B);                    // {Ignore, AskingFailed, Ready, ReadyFailed}
  P16(p, 0); P16(p, 0);
  h.feed(p, true);

  CHECK(h.evts.size() == 4, "D evts 4 got %zu", h.evts.size());
  if (h.evts.size() == 4) {
    constexpr unsigned fps[4] = {0, 1, 2, 3};
    constexpr unsigned evs[4] = {1, 1, 2, 4};
    for (int k = 0; k < 4; ++k) {
      CHECK(h.evts[k].fp == fps[k], "D v%d fourpacked got %u", k, h.evts[k].fp);
      CHECK(h.evts[k].ev == evs[k], "D v%d three-packed got %u", k, h.evts[k].ev);
    }
    CHECK(h.evts[3].sid == SIDB + 0x100 + 3, "D v3 stream_id +k got %llx",
          static_cast<unsigned long long>(h.evts[3].sid));
    CHECK(h.evts[0].attr == 3, "D attr Listener got %u", h.evts[0].attr);
    CHECK(h.evts[0].da == 0, "D Listener has no DA");
  }
  CHECK(h.dones.size() == 1 && h.dones[0].ok, "D done ok");
}

// ==== E: MVRP VID decode (no AttributeListLength field) =================
void SrpDecoderSuite::mvrp_vid_decodes_without_a_list_length() {
  h.clear();
  std::vector<uint8_t> p;
  P8(p, 0);
  P8(p, 1); P8(p, 2);             // VID attribute, 2 B — NO list length
  P16(p, 0x0003);
  P16(p, 2);                      // FirstValue VID 2
  P8(p, 7);                       // [New, JoinIn, JoinIn]
  P16(p, 0); P16(p, 0);
  h.feed(p, false);

  CHECK(h.evts.size() == 3, "E evts 3 got %zu", h.evts.size());
  if (h.evts.size() == 3) {
    CHECK(h.evts[0].vid == 2 && h.evts[1].vid == 3 && h.evts[2].vid == 4,
          "E VIDs +k got %u %u %u", h.evts[0].vid, h.evts[1].vid, h.evts[2].vid);
    CHECK(h.evts[0].ev == 0 && h.evts[1].ev == 1 && h.evts[2].ev == 1,
          "E events got %u %u %u", h.evts[0].ev, h.evts[1].ev, h.evts[2].ev);
    CHECK(h.evts[0].attr == 1, "E attr VID got %u", h.evts[0].attr);
    CHECK(!h.evts[0].msrp, "E application MVRP");
  }
  CHECK(h.dones.size() == 1 && h.dones[0].ok, "E done ok");
}

// ==== F: dual-EndMark framing — a single-EndMark PDU is malformed =======
void SrpDecoderSuite::a_single_endmark_pdu_is_malformed() {
  h.clear();
  std::vector<uint8_t> p;
  P8(p, 0);
  P8(p, 4); P8(p, 4);
  P16(p, 9);
  P16(p, 0x0002);
  P8(p, 5); P8(p, 2); P16(p, 2);
  P8(p, 42);
  P16(p, 0);                      // AttributeList EndMark ONLY — then EOF
  h.feed(p, true);

  CHECK(h.evts.size() == 2, "F prefix events stand got %zu", h.evts.size());
  CHECK(h.evts.size() == 2 && h.evts[1].prio == 3, "F prefix still +k");
  CHECK(h.dones.size() == 1 && !h.dones[0].ok, "F done NOT ok");
  CHECK(h.dones.size() == 1 && h.dones[0].mal, "F malformed reported");
}

// ==== G: AttributeListLength lies — counted + flagged, framing survives =
void SrpDecoderSuite::a_lying_list_length_is_counted_and_framing_survives() {
  h.clear();
  std::vector<uint8_t> p;
  P8(p, 0);
  P8(p, 4); P8(p, 4);
  P16(p, 13);                     // LIE: actual list is 9 octets
  P16(p, 0x0002);
  P8(p, 5); P8(p, 2); P16(p, 2);
  P8(p, 42);
  P16(p, 0);                      // list EndMark — message 2 follows anyway
  P8(p, 3); P8(p, 8);             // Listener message, truthful length 14
  P16(p, 14);
  P16(p, 0x0001);
  P64(p, SIDB + 0x200);
  P8(p, 36);                      // [JoinIn]
  P8(p, 0x80);                    // {Ready, -, -, -}
  P16(p, 0);
  P16(p, 0);                      // MRPDU EndMark
  h.feed(p, true);

  CHECK(h.llbad == 1, "G one lying list flagged got %d", h.llbad);
  CHECK(h.llcnt_at_bad == 9, "G counted 9 octets got %u", h.llcnt_at_bad);
  CHECK(h.evts.size() == 3, "G framing survives: 3 evts got %zu", h.evts.size());
  if (h.evts.size() == 3) {
    CHECK(h.evts[2].fp == 2, "G listener Ready got %u", h.evts[2].fp);
    CHECK(h.evts[2].sid == SIDB + 0x200, "G listener stream_id got %llx",
          static_cast<unsigned long long>(h.evts[2].sid));
  }
  CHECK(h.dones.size() == 1 && h.dones[0].ok, "G done ok — a lie is flagged, not fatal");
}

// ==== H: tolerance — truncation mid-FirstValue ==========================
void SrpDecoderSuite::truncation_mid_first_value_is_tolerated() {
  h.clear();
  std::vector<uint8_t> p;
  P8(p, 0);
  P8(p, 1); P8(p, 25);
  P16(p, 31);
  P16(p, 0x0001);
  for (int i = 0; i < 10; ++i) P8(p, uint8_t(i));  // 10 of 25 FV bytes
  h.feed(p, true);

  CHECK(h.evts.empty(), "H no events got %zu", h.evts.size());
  CHECK(h.dones.size() == 1 && h.dones[0].mal, "H malformed");
}

// ==== I: tolerance — truncation mid-vector, prefix emitted ==============
void SrpDecoderSuite::truncation_mid_vector_keeps_the_prefix() {
  h.clear();
  std::vector<uint8_t> p;
  P8(p, 0);
  P8(p, 1); P8(p, 25);
  P16(p, 31);
  P16(p, 0x0006);                 // NumberOfValues 6 needs 2 packed bytes
  talker_fv(p, SIDB + 0x300, DAB, 2, 217, 1, PRB, LATB);
  P8(p, 8);                       // [New, JoinIn, In] — byte 2 never arrives
  h.feed(p, true);

  CHECK(h.evts.size() == 3, "I prefix 3 evts got %zu", h.evts.size());
  if (h.evts.size() == 3) {
    CHECK(h.evts[0].ev == 0 && h.evts[1].ev == 1 && h.evts[2].ev == 2,
          "I prefix events got %u %u %u",
          h.evts[0].ev, h.evts[1].ev, h.evts[2].ev);
    CHECK(h.evts[2].sid == SIDB + 0x300 + 2, "I prefix +k got %llx",
          static_cast<unsigned long long>(h.evts[2].sid));
  }
  CHECK(h.dones.size() == 1 && h.dones[0].mal, "I malformed");
}

// ==== J: tolerance — bad AttributeLength, then clean recovery ===========
void SrpDecoderSuite::a_bad_attribute_length_recovers_on_the_next_pdu() {
  h.clear();
  std::vector<uint8_t> p;
  P8(p, 0);
  P8(p, 1); P8(p, 24);            // Talker Advertise with WRONG length
  P8(p, 0xDE); P8(p, 0xAD); P8(p, 0xBE); P8(p, 0xEF); P8(p, 0x00);
  h.feed(p, true);
  CHECK(h.evts.empty(), "J bad-length PDU emits nothing got %zu", h.evts.size());
  CHECK(h.dones.size() == 1 && h.dones[0].mal, "J malformed");

  h.clear();
  std::vector<uint8_t> q;         // decoder recovered: next PDU decodes
  P8(q, 0);
  P8(q, 3); P8(q, 8);
  P16(q, 14);
  P16(q, 0x0001);
  P64(q, SIDB + 0x400);
  P8(q, 36); P8(q, 0x80);
  P16(q, 0); P16(q, 0);
  h.feed(q, true);
  CHECK(h.evts.size() == 1, "J recovery evt got %zu", h.evts.size());
  CHECK(h.evts.size() == 1 && h.evts[0].fp == 2 && h.evts[0].ev == 1,
        "J recovery fields");
  CHECK(h.evts.size() == 1 && h.evts[0].sid == SIDB + 0x400, "J recovery sid");
  CHECK(h.dones.size() == 1 && h.dones[0].ok, "J recovery done ok");
}

// ==== K: malformed vector attribute MID-PDU — prefix stands, ============
// rest of list AND subsequent messages discarded (F09.4 row)
void SrpDecoderSuite::a_malformed_message_discards_every_later_message() {
  h.clear();
  std::vector<uint8_t> p;
  P8(p, 0);
  P8(p, 4); P8(p, 4);             // message 1: good Domain
  P16(p, 9);
  P16(p, 0x0002);
  P8(p, 5); P8(p, 2); P16(p, 2);
  P8(p, 42);
  P16(p, 0);
  P8(p, 1); P8(p, 10);            // message 2: bad AttributeLength
  // message 3 would be a fully valid Listener — MUST stay discarded
  P16(p, 14);
  P16(p, 0x0001);
  P64(p, SIDB + 0x500);
  P8(p, 36); P8(p, 0x80);
  P16(p, 0); P16(p, 0);
  h.feed(p, true);

  CHECK(h.evts.size() == 2, "K only the Domain prefix got %zu", h.evts.size());
  CHECK(h.evts.size() == 2 && h.evts[1].cid == 6, "K prefix +k intact");
  CHECK(h.dones.size() == 1 && h.dones[0].mal, "K malformed");
}

// ==== L: LeaveAll is PER APPLICATION (corrected §6.5 rule) ==============
void SrpDecoderSuite::leave_all_is_per_application() {
  h.clear();
  std::vector<uint8_t> p;         // MSRP Domain LeaveAll, NumberOfValues 0
  P8(p, 0);
  P8(p, 4); P8(p, 4);
  P16(p, 8);                      // 2+4+2
  P16(p, 0x2000);                 // LeaveAllEvent = 1, NumberOfValues = 0
  P8(p, 5); P8(p, 2); P16(p, 2);  // FirstValue present even with 0 values
  P16(p, 0); P16(p, 0);
  h.feed(p, true);
  CHECK(h.la_msrp == 1, "L MSRP LeaveAll fires got %d", h.la_msrp);
  CHECK(h.la_mvrp == 0, "L MVRP registrars untouched got %d", h.la_mvrp);
  CHECK(h.evts.empty(), "L zero values emit nothing got %zu", h.evts.size());
  CHECK(h.dones.size() == 1 && h.dones[0].ok, "L done ok");

  h.clear();
  std::vector<uint8_t> q;         // MVRP VID LeaveAll + one value
  P8(q, 0);
  P8(q, 1); P8(q, 2);
  P16(q, 0x2001);                 // LeaveAllEvent = 1, NumberOfValues = 1
  P16(q, 5);                      // VID 5
  P8(q, 36);                      // [JoinIn]
  P16(q, 0); P16(q, 0);
  h.feed(q, false);
  CHECK(h.la_mvrp == 1, "L MVRP LeaveAll fires got %d", h.la_mvrp);
  CHECK(h.la_msrp == 0, "L MSRP registrars untouched got %d", h.la_msrp);
  CHECK(h.evts.size() == 1 && h.evts[0].vid == 5, "L VID 5 joined");
  CHECK(h.dones.size() == 1 && h.dones[0].ok, "L done ok");
}

// ==== M: out-of-alphabet three-packed digit (> 215) =====================
void SrpDecoderSuite::an_out_of_alphabet_three_packed_digit_is_malformed() {
  h.clear();
  std::vector<uint8_t> p;
  P8(p, 0);
  P8(p, 1); P8(p, 25);
  P16(p, 31);
  P16(p, 0x0006);
  talker_fv(p, SIDB + 0x600, DAB, 2, 217, 1, PRB, LATB);
  P8(p, 8);                       // [New, JoinIn, In] — valid
  P8(p, 220);                     // first digit 6: outside the alphabet
  P16(p, 0); P16(p, 0);           // present but must be discarded
  h.feed(p, true);

  CHECK(h.evts.size() == 3, "M prefix 3 evts got %zu", h.evts.size());
  CHECK(h.dones.size() == 1 && h.dones[0].mal, "M malformed");
}

// ==== N: explicit EndMark then frame padding (10 §3 padding rule) =======
void SrpDecoderSuite::an_explicit_endmark_makes_frame_padding_inert() {
  h.clear();
  std::vector<uint8_t> p;
  P8(p, 0);
  P8(p, 4); P8(p, 4);
  P16(p, 9);
  P16(p, 0x0002);
  P8(p, 5); P8(p, 2); P16(p, 2);
  P8(p, 42);
  P16(p, 0); P16(p, 0);
  for (int i = 0; i < 6; ++i) P8(p, 0);  // min-frame padding
  h.feed(p, true);

  CHECK(h.dones.size() == 1 && h.dones[0].ok, "N one ok done, padding inert");
  CHECK(h.evts.size() == 2, "N evts got %zu", h.evts.size());
}

// ==== O: multi-message MSRP PDU — Domain + Talker + Listener ============
void SrpDecoderSuite::a_multi_message_msrp_pdu_decodes_every_message() {
  h.clear();
  std::vector<uint8_t> p;
  P8(p, 0);
  P8(p, 4); P8(p, 4);             // Domain, certified shape
  P16(p, 9);
  P16(p, 0x0002);
  P8(p, 5); P8(p, 2); P16(p, 2);
  P8(p, 42);
  P16(p, 0);
  P8(p, 1); P8(p, 25);            // Talker Advertise, 2 values
  P16(p, 30);                     // 2+25+1+2
  P16(p, 0x0002);
  talker_fv(p, SIDB + 0x700, DAB, 2, 217, 1, PRB, LATB);
  P8(p, 42);                      // [JoinIn, JoinIn, pad]
  P16(p, 0);
  P8(p, 3); P8(p, 8);             // Listener, 1 value
  P16(p, 14);
  P16(p, 0x0001);
  P64(p, SIDB + 0x800);
  P8(p, 36); P8(p, 0x80);
  P16(p, 0);
  P16(p, 0);                      // MRPDU EndMark
  h.feed(p, true);

  CHECK(h.evts.size() == 5, "O 2+2+1 evts got %zu", h.evts.size());
  if (h.evts.size() == 5) {
    CHECK(h.evts[1].cid == 6, "O domain value 1 is class A");
    CHECK(h.evts[3].sid == SIDB + 0x701, "O talker value 1 +k got %llx",
          static_cast<unsigned long long>(h.evts[3].sid));
    CHECK(h.evts[3].ev == 1, "O talker value 1 JoinIn got %u", h.evts[3].ev);
    CHECK(h.evts[4].fp == 2, "O listener Ready got %u", h.evts[4].fp);
  }
  CHECK(h.dones.size() == 1 && h.dones[0].ok, "O done ok");
  CHECK(h.llbad == 0, "O every AttributeListLength truthful");
}

int SrpDecoderSuite::run() {
  reset_releases_the_decoder();
  the_certified_domain_shape_surfaces_class_a_at_plus_k();
  a_multi_value_talker_advertise_reconstructs_the_range();
  talker_failed_surfaces_the_failure_information();
  listener_four_packed_decodes_all_four_codes();
  mvrp_vid_decodes_without_a_list_length();
  a_single_endmark_pdu_is_malformed();
  a_lying_list_length_is_counted_and_framing_survives();
  truncation_mid_first_value_is_tolerated();
  truncation_mid_vector_keeps_the_prefix();
  a_bad_attribute_length_recovers_on_the_next_pdu();
  a_malformed_message_discards_every_later_message();
  leave_all_is_per_application();
  an_out_of_alphabet_three_packed_digit_is_malformed();
  an_explicit_endmark_makes_frame_padding_inert();
  a_multi_message_msrp_pdu_decodes_every_message();

  printf("%d checks: %d PASS, %d FAIL\n", checks, checks - fails, fails);
  return fails ? 1 : 0;
}

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  SrpDecoderSuite suite;
  return suite.run();
}
