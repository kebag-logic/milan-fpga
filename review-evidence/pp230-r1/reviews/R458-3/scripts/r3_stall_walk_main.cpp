// SPDX-License-Identifier: CERN-OHL-W-2.0
// srp_stream_fsms walk-record arms (issue #230) — independent expectations,
// never DUT logic.
//
// The tick walk publishes each declared record from its own copy: the
// talker's TSpec, priority, rank and latency always from distributed RAM,
// its {stream_id, DA, VLAN} and the listener's stream_id from the matcher's
// flops at one and two contexts and from distributed RAM from three. The
// Makefile builds this harness at four shapes (sources/sinks 1/1, 2/2, 3/5,
// 9/9), so both arms run, and starts every unreset memory at random contents
// (+verilator+rand+reset+2): a record the walk read before it was written
// would show. Each arm compares every FirstValue the walk hands the encoder
// with the record the harness itself declared, settled or tore down:
//   WK1  every source publishes its own declaration, with the idle gate face
//       on the last source declared and then on the highest index its width
//       can name (out of range at one, three and nine sources): the walk
//       never reads the gate face;
//   WK2  a re-declaration replaces every field of the record, in the opposite
//       order (the gate face now holds source 0);
//   WK3  a close names the record declared, not the values on the gate face;
//   WK4  a closed source re-opened publishes its new record beside the rest;
//   WK5  a reset empties the records: a close of a source not opened since
//       leaves VID 0 (the reset value), and the walk publishes only what was
//       declared after the reset;
//   WK6  every sink publishes its own settled stream_id, with the idle
//       control face on the last sink settled and then on its highest index;
//   WK7  a teardown names the settled stream_id, not the one on the control
//       face;
//   WK8  a re-settle replaces the stream_id, in the opposite order.
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <vector>
#include "Vsrp_walk_wrap.h"
#include "verilated.h"
#include "verilator_harness.hpp"

#ifndef TB_SOURCES
#error "TB_SOURCES (talker sources) must be defined by the build"
#endif
#ifndef TB_SINKS
#error "TB_SINKS (listener sinks) must be defined by the build"
#endif

constexpr int kSources = TB_SOURCES;
constexpr int kSinks = TB_SINKS;

// a failing check names the shape it failed at, sources/sinks
#define CHECK(cond, ...) do { \
  ++checks; \
  if (!(cond)) { \
    ++fails; printf("FAIL: " __VA_ARGS__); printf(" [%d/%d]\n", kSources, kSinks); \
  } \
} while (0)

namespace {

constexpr uint64_t MAC = 0x02AABBCCDDEEull;
constexpr uint32_t NOW = 100000;
// The MRPDU FirstValue busses are 272 bits, i.e. 34 bytes, wide.
constexpr int kFirstValueBytes = 34;
constexpr int kFirstValueMsb = 271;
// Guard on the wait for both walks to report a completed transmit
// opportunity: far more clock steps than a walk over nine contexts needs.
constexpr int kTxopPollSteps = 300;
// Ticks that bring every declaring applicant to the quiet QA state.
constexpr int kQuietTicks = 6;
// The wrap's index inputs are 4 bits wide and each FSM takes its low
// $clog2(contexts) bits (one bit at one context): all ones is the highest
// index the FSM's face can name, beyond the last context at 1, 3 and 9.
constexpr int kParkedIndex = 0xF;

// 802.1Q MSRP AttributeTypes, attribute events and the Listener declaration
constexpr uint8_t ATTR_TA = 1;
constexpr uint8_t ATTR_LISTENER = 3;
constexpr uint8_t EV_NEW = 0;
constexpr uint8_t EV_LV = 5;
constexpr uint8_t DECL_READY = 2;

struct Push {
  uint8_t type;
  uint8_t code;
  uint8_t fp;
  uint8_t val[kFirstValueBytes];
};
struct VOp { bool join; uint16_t vid; };

//! One talker declaration: every field the gate face carries.
struct Record {
  uint64_t sid;
  uint64_t da;
  uint16_t vid;
  uint16_t mfs;
  uint16_t mif;
  int prio;
  int rank;
  uint32_t lat;
};

//! The declaration of source s in phase p. The stream_id, DA, VLAN, TSpec and
//! latency differ between any two sources and any two phases, so a record
//! read for the wrong source, or kept from an earlier phase, never matches;
//! priority and rank vary as far as their 3 bits and 1 bit allow.
Record talker_record(int p, int s) {
  return Record{0x02AABBCC00000000ull + (static_cast<uint64_t>(p) << 24)
                    + (static_cast<uint64_t>(s) << 8) + 0x5A,
                0x91E0F0000000ull + (static_cast<uint64_t>(p) << 16)
                    + (static_cast<uint64_t>(s) << 4) + 3,
                static_cast<uint16_t>((0x100 * p + 0x10 * s + 2) & 0xFFF),
                static_cast<uint16_t>(64 + 32 * s + 512 * p),
                static_cast<uint16_t>(1 + s + 3 * p),
                (s + 2 * p + 1) & 7,
                (s + p) & 1,
                0x00010000u * static_cast<uint32_t>(p + 1) + 0x101u * static_cast<uint32_t>(s) + 0x33};
}

//! The {stream_id, DA, VLAN} sink k settles on in phase p.
struct SinkRecord { uint64_t sid; uint64_t da; uint16_t vid; };
SinkRecord sink_record(int p, int k) {
  return SinkRecord{0x0011223344550000ull + (static_cast<uint64_t>(p) << 12)
                        + (static_cast<uint64_t>(k) << 4) + 7,
                    0x91E0F0AA0000ull + (static_cast<uint64_t>(p) << 8) + k,
                    static_cast<uint16_t>((2 + k + 0x20 * p) & 0xFFF)};
}

// F10.7 Talker Advertise FirstValue (802.1Q §35.2.2.8): stream_id, DA,
// VLAN, MaxFrameSize, MaxIntervalFrames, {priority, rank}, latency; the
// 34-byte bus carries zeros past byte 25 for an Advertise.
std::vector<uint8_t> talker_first_value(const Record& r) {
  std::vector<uint8_t> b;
  for (int i = 7; i >= 0; i--) b.push_back((r.sid >> (8 * i)) & 0xFF);
  for (int i = 5; i >= 0; i--) b.push_back((r.da >> (8 * i)) & 0xFF);
  b.push_back(r.vid >> 8); b.push_back(r.vid & 0xFF);
  b.push_back(r.mfs >> 8); b.push_back(r.mfs & 0xFF);
  b.push_back(r.mif >> 8); b.push_back(r.mif & 0xFF);
  b.push_back(static_cast<uint8_t>((r.prio << 5) | (r.rank << 4)));
  for (int i = 3; i >= 0; i--) b.push_back((r.lat >> (8 * i)) & 0xFF);
  b.resize(kFirstValueBytes, 0);
  return b;
}

// F10.8 Listener FirstValue: the 8-byte stream_id, zeros after it.
std::vector<uint8_t> listener_first_value(uint64_t sid) {
  std::vector<uint8_t> b;
  for (int i = 7; i >= 0; i--) b.push_back((sid >> (8 * i)) & 0xFF);
  b.resize(kFirstValueBytes, 0);
  return b;
}

bool same_value(const Push& p, const std::vector<uint8_t>& fv) {
  return std::memcmp(p.val, fv.data(), kFirstValueBytes) == 0;
}

template <std::size_t N>
uint64_t wget(const VlWide<N>& w, int lo, int width) {
  uint64_t v = 0;
  for (int i = width - 1; i >= 0; --i) {
    int b = lo + i;
    v = (v << 1) | ((w[b >> 5] >> (b & 31)) & 1u);
  }
  return v;
}

struct Hw {
  Vsrp_walk_wrap* d;
  std::vector<Push> t_push;
  std::vector<Push> l_push;
  std::vector<VOp> t_vop;

  explicit Hw(Vsrp_walk_wrap* dd) : d(dd) {}

  void clear_logs() { t_push.clear(); l_push.clear(); t_vop.clear(); }

  void step() {
    d->now_ms_i = NOW;
    d->clk_i = 0; d->eval();
    // harvest (every face read here is registered or stable-from-registers;
    // the encoder and VLAN faces are tied ready, so each offer is one cycle)
    if (d->t_ev_valid_o) {
      Push p{d->t_ev_attr_type_o, d->t_ev_event_o, 0, {}};
      for (int i = 0; i < kFirstValueBytes; ++i)
        p.val[i] = static_cast<uint8_t>(wget(d->t_ev_value_o, kFirstValueMsb - 8 * i - 7, 8));
      t_push.push_back(p);
    }
    if (d->l_ev_valid_o) {
      Push p{d->l_ev_attr_type_o, d->l_ev_event_o, d->l_ev_fourpack_o, {}};
      for (int i = 0; i < kFirstValueBytes; ++i)
        p.val[i] = static_cast<uint8_t>(wget(d->l_ev_value_o, kFirstValueMsb - 8 * i - 7, 8));
      l_push.push_back(p);
    }
    if (d->t_user_valid_o)
      t_vop.push_back({d->t_user_join_o != 0, static_cast<uint16_t>(d->t_user_vid_o)});
    d->clk_i = 1; d->eval();
    // one-shot inputs auto-clear; the gate and control faces keep their
    // last values, as an idle requester's would
    d->evt_valid_i = 0; d->join_tick_i = 0; d->leaveall_own_i = 0;
    d->gate_valid_i = 0; d->ctl_valid_i = 0;
  }

  void idle(int n) { for (int i = 0; i < n; ++i) step(); }

  void reset() {
    d->rst_n = 0; d->p2p_i = 1; d->own_mac_i = MAC;
    d->evt_valid_i = 0; d->join_tick_i = 0; d->leaveall_own_i = 0;
    d->gate_valid_i = 0; d->ctl_valid_i = 0;
    idle(3);
    d->rst_n = 1;
    idle(2);
    clear_logs();
  }

  void gate(bool open, int src, const Record& r) {
    d->gate_valid_i = 1; d->gate_open_i = open; d->gate_src_i = src;
    d->gate_stream_id_i = r.sid; d->gate_da_i = r.da; d->gate_vid_i = r.vid;
    d->gate_max_frame_i = r.mfs; d->gate_max_interval_i = r.mif;
    d->gate_prio_i = r.prio; d->gate_rank_i = r.rank; d->gate_acc_lat_i = r.lat;
    step(); idle(2);
  }

  // An idle requester's gate or control face holds whatever it last drove;
  // the top drives the index of its last request, accepted or refused, so it
  // may name no context at all. Park it on the highest index the face's
  // width can name, with another record beside it.
  void park_gate(const Record& r) {
    d->gate_open_i = 1; d->gate_src_i = kParkedIndex;
    d->gate_stream_id_i = r.sid; d->gate_da_i = r.da; d->gate_vid_i = r.vid;
    d->gate_max_frame_i = r.mfs; d->gate_max_interval_i = r.mif;
    d->gate_prio_i = r.prio; d->gate_rank_i = r.rank; d->gate_acc_lat_i = r.lat;
  }
  void park_ctl(const SinkRecord& r) {
    d->ctl_settle_i = 1; d->ctl_sink_i = kParkedIndex;
    d->ctl_stream_id_i = r.sid; d->ctl_da_i = r.da; d->ctl_vid_i = r.vid;
  }

  void ctl(bool settle, int sink, const SinkRecord& r) {
    d->ctl_valid_i = 1; d->ctl_settle_i = settle; d->ctl_sink_i = sink;
    d->ctl_stream_id_i = r.sid; d->ctl_da_i = r.da; d->ctl_vid_i = r.vid;
    step(); idle(2);
  }

  // a registering Talker Advertise on the sink's exact {stream_id, DA, VLAN}
  void advertise(const SinkRecord& r) {
    d->evt_valid_i = 1; d->evt_msrp_i = 1; d->evt_attr_type_i = ATTR_TA;
    d->evt_stream_id_i = r.sid; d->evt_da_i = r.da; d->evt_vid_i = r.vid;
    d->evt_mrp_event_i = EV_NEW; d->evt_fourpacked_i = 0;
    d->evt_acc_latency_i = 500;
    step(); idle(3);
  }

  void la_own() { d->leaveall_own_i = 1; step(); idle(2); }

  bool tick() {
    d->join_tick_i = 1; step();
    bool td = false;
    bool ld = false;
    for (int i = 0; i < kTxopPollSteps && !(td && ld); ++i) {
      td |= (d->t_txop_done_o != 0); ld |= (d->l_txop_done_o != 0);
      if (td && ld) break;
      step();
    }
    idle(2);
    return td && ld;
  }

  // tick until a walk hands the encoder nothing (every applicant quiet)
  bool quiet() {
    for (int i = 0; i < kQuietTicks; ++i) {
      clear_logs();
      tick();
      if (t_push.empty() && l_push.empty()) return true;
    }
    return false;
  }

  int t_decl(int s) const { return (d->t_tk_decl_state_o >> (2 * s)) & 3; }
  int l_decl(int k) const { return (d->l_lstn_decl_state_o >> (2 * k)) & 3; }
};

class SrpWalkSuite {
 public:
  SrpWalkSuite() : h(model.get()) {}

  int run() {
    printf("walk records: %d sources, %d sinks\n", kSources, kSinks);
    talker_walk_publishes_each_declared_record();
    listener_walk_publishes_each_settled_stream_id();
    r3_offer_not_accepted();
    r3_settle_not_accepted();
    printf("%d checks: %d PASS, %d FAIL\n", checks, checks - fails, fails);
    return fails ? 1 : 0;
  }

 private:
  const milan::tb::Model<Vsrp_walk_wrap> model;
  Hw h;
  int checks = 0;
  int fails = 0;

  // an own LeaveAll then a tick: every declaring applicant sends (txLA!)
  void txla_walk() { h.clear_logs(); h.la_own(); h.tick(); }

  // the talker walk handed the encoder exactly `want`, in source order
  void expect_talker(const char* tag, const std::vector<Record>& want) {
    CHECK(h.t_push.size() == want.size(),
          "%s: the talker walk pushes %zu records (got %zu)", tag, want.size(),
          h.t_push.size());
    for (size_t i = 0; i < want.size() && i < h.t_push.size(); ++i) {
      CHECK(h.t_push[i].type == ATTR_TA && same_value(h.t_push[i], talker_first_value(want[i])),
            "%s: push %zu carries its source's declared record (type %d, stream_id "
            "%02x%02x..%02x%02x)", tag, i, h.t_push[i].type, h.t_push[i].val[0],
            h.t_push[i].val[1], h.t_push[i].val[6], h.t_push[i].val[7]);
    }
  }

  void expect_listener(const char* tag, const std::vector<uint64_t>& want) {
    CHECK(h.l_push.size() == want.size(),
          "%s: the listener walk pushes %zu stream_ids (got %zu)", tag, want.size(),
          h.l_push.size());
    for (size_t i = 0; i < want.size() && i < h.l_push.size(); ++i) {
      CHECK(h.l_push[i].type == ATTR_LISTENER && h.l_push[i].fp == DECL_READY
                && same_value(h.l_push[i], listener_first_value(want[i])),
            "%s: push %zu carries its sink's settled stream_id (type %d, fp %d, "
            "stream_id %02x%02x..%02x%02x)", tag, i, h.l_push[i].type, h.l_push[i].fp,
            h.l_push[i].val[0], h.l_push[i].val[1], h.l_push[i].val[6], h.l_push[i].val[7]);
    }
  }

  void talker_walk_publishes_each_declared_record() {
    std::vector<Record> rec(kSources);
    h.reset();
    // WK1: ascending, so the gate face is left on the last source
    for (int s = 0; s < kSources; ++s) { rec[s] = talker_record(1, s); h.gate(true, s, rec[s]); }
    txla_walk();
    expect_talker("WK1", rec);
    h.park_gate(talker_record(7, kSources - 1));
    txla_walk();
    expect_talker("WK1", rec);

    // WK2: every field re-declared, descending, so the gate face is left on 0
    for (int s = kSources - 1; s >= 0; --s) { rec[s] = talker_record(2, s); h.gate(true, s, rec[s]); }
    txla_walk();
    expect_talker("WK2", rec);

    // WK3: the close carries another record on the gate face; the Leave
    // names the one declared
    const int k = kSources / 2;
    CHECK(h.quiet(), "WK3 precondition: every talker applicant goes quiet");
    h.clear_logs();
    h.gate(false, k, talker_record(7, k));
    h.tick();
    CHECK(h.t_push.size() == 1 && h.t_push[0].code == EV_LV && h.t_push[0].type == ATTR_TA
              && same_value(h.t_push[0], talker_first_value(rec[k])),
          "WK3: the close of source %d sends one Leave of its declared record (pushes %zu)",
          k, h.t_push.size());

    // WK4: the closed source re-opened beside the others
    rec[k] = talker_record(3, k);
    h.gate(true, k, rec[k]);
    txla_walk();
    expect_talker("WK4", rec);

    // WK5: a reset empties the records. Source 0 has not been opened since,
    // so its close leaves the reset value, VID 0, never a VID from before.
    h.reset();
    h.gate(false, 0, talker_record(7, 0));
    h.idle(4);
    CHECK(h.t_vop.size() == 1 && !h.t_vop[0].join && h.t_vop[0].vid == 0,
          "WK5: a close after the reset leaves VID 0, not a pre-reset VID (ops %zu, vid %u)",
          h.t_vop.size(), h.t_vop.empty() ? 0u : unsigned{h.t_vop[0].vid});
    const int last = kSources - 1;
    std::vector<Record> after{talker_record(4, last)};
    h.gate(true, last, after[0]);
    txla_walk();
    expect_talker("WK5", after);
    CHECK(h.t_decl(last) == 1, "WK5: the source declared after the reset advertises");
  }


  // R458-3 probe arm (disposable): a gate open offered while a decoder event
  // holds gate_ready low is not published by the walk before it is accepted.
  void r3_offer_not_accepted() {
    std::vector<Record> rec(kSources);
    h.reset();
    for (int s = 0; s < kSources; ++s) { rec[s] = talker_record(1, s); h.gate(true, s, rec[s]); }
    CHECK(h.quiet(), "R3 precondition: every talker applicant goes quiet");
    const int k = kSources - 1;
    const Record nr = talker_record(5, k);
    h.la_own();
    h.clear_logs();
    for (int i = 0; i < 60; ++i) {
      h.d->join_tick_i = (i == 0);
      // a Listener value on a stream no context declares: matches nothing
      h.d->evt_valid_i = 1; h.d->evt_msrp_i = 1; h.d->evt_attr_type_i = ATTR_LISTENER;
      h.d->evt_stream_id_i = 0xFEEDFACE00000000ull + i; h.d->evt_da_i = 0; h.d->evt_vid_i = 0;
      h.d->evt_mrp_event_i = 1; h.d->evt_fourpacked_i = 0;
      // the re-declaration of k offered, held, never ready while the event bus is busy
      h.d->gate_valid_i = 1; h.d->gate_open_i = 1; h.d->gate_src_i = k;
      h.d->gate_stream_id_i = nr.sid; h.d->gate_da_i = nr.da; h.d->gate_vid_i = nr.vid;
      h.d->gate_max_frame_i = nr.mfs; h.d->gate_max_interval_i = nr.mif;
      h.d->gate_prio_i = nr.prio; h.d->gate_rank_i = nr.rank; h.d->gate_acc_lat_i = nr.lat;
      h.d->eval();
      CHECK(h.d->gate_ready_o == 0, "R3 precondition: gate not ready while the event bus is busy");
      h.step();
    }
    expect_talker("R3 walk during the unaccepted offer", rec);
    // released: the offer is accepted now, and the next walk publishes it
    h.d->gate_valid_i = 1; h.step(); h.idle(2);
    rec[k] = nr;
    txla_walk();
    expect_talker("R3 walk after acceptance", rec);
  }


  // R458-3 probe arm (disposable): a settle offered while a decoder event
  // holds ctl_ready low is not published by the listener walk before it is accepted.
  void r3_settle_not_accepted() {
    std::vector<uint64_t> sid(kSinks);
    h.reset();
    for (int k = 0; k < kSinks; ++k) { SinkRecord r = sink_record(1, k); sid[k] = r.sid; h.ctl(true, k, r); h.advertise(r); }
    CHECK(h.quiet(), "R3L precondition: every listener applicant goes quiet");
    const int k = kSinks - 1;
    const SinkRecord nr = sink_record(5, k);
    h.la_own();
    h.clear_logs();
    for (int i = 0; i < 60; ++i) {
      h.d->join_tick_i = (i == 0);
      h.d->evt_valid_i = 1; h.d->evt_msrp_i = 1; h.d->evt_attr_type_i = ATTR_LISTENER;
      h.d->evt_stream_id_i = 0xFEEDFACE00000000ull + i; h.d->evt_da_i = 0; h.d->evt_vid_i = 0;
      h.d->evt_mrp_event_i = 1; h.d->evt_fourpacked_i = 0;
      h.d->ctl_valid_i = 1; h.d->ctl_settle_i = 1; h.d->ctl_sink_i = k;
      h.d->ctl_stream_id_i = nr.sid; h.d->ctl_da_i = nr.da; h.d->ctl_vid_i = nr.vid;
      h.d->eval();
      CHECK(h.d->ctl_ready_o == 0, "R3L precondition: control not ready while the event bus is busy");
      h.step();
    }
    expect_listener("R3L walk during the unaccepted offer", sid);
  }

  void listener_walk_publishes_each_settled_stream_id() {
    std::vector<uint64_t> sid(kSinks);
    h.reset();
    // WK6: ascending, so the control face is left on the last sink
    for (int k = 0; k < kSinks; ++k) {
      SinkRecord r = sink_record(1, k);
      sid[k] = r.sid;
      h.ctl(true, k, r);
      h.advertise(r);
    }
    txla_walk();
    expect_listener("WK6", sid);
    h.park_ctl(sink_record(7, kSinks - 1));
    txla_walk();
    expect_listener("WK6", sid);

    // WK7: the teardown carries another stream_id on the control face; the
    // Leave names the one settled
    const int k = kSinks / 2;
    CHECK(h.quiet(), "WK7 precondition: every listener applicant goes quiet");
    h.clear_logs();
    h.ctl(false, k, sink_record(7, k));
    h.tick();
    CHECK(h.l_push.size() == 1 && h.l_push[0].code == EV_LV
              && same_value(h.l_push[0], listener_first_value(sid[k])),
          "WK7: the teardown of sink %d sends one Leave of its settled stream_id (pushes %zu)",
          k, h.l_push.size());

    // WK8: every sink re-settled on a new stream, descending, so the control
    // face is left on sink 0
    for (int j = kSinks - 1; j >= 0; --j) {
      SinkRecord r = sink_record(2, j);
      sid[j] = r.sid;
      h.ctl(true, j, r);
      h.advertise(r);
    }
    txla_walk();
    expect_listener("WK8", sid);
    CHECK(h.l_decl(0) == DECL_READY, "WK8: the re-settled sink declares Ready");
  }
};

}  // namespace

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  SrpWalkSuite suite;
  return suite.run();
}
