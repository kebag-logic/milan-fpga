// SPDX-License-Identifier: CERN-OHL-W-2.0
// KL_pp_tx_slots suite — independent expectations, never DUT logic.
//
// Proves the 03 §7/§8 TX slot pool contract, F01.5 "P-TX 4x576 + 1600":
// plain allocation walks slots 0..3 lowest-first and NEVER returns the
// oversize slot; an oversize allocation (the Δ8 READ_DESCRIPTOR class,
// Milan §5.4.1) is granted slot 4 only, and waits for slot 4 even while
// 0..3 sit free. Byte-exact alloc/write/commit/serialize over all five
// slots with header-after-payload random-access writes; serialization
// stalls — never skips — under random ser_ready_i drops; the slot
// auto-frees on the final consumed byte and is immediately reusable; two
// committed slots are serviced strictly one at a time; 1-byte and
// full-size (576 / 1600) frames; writes after commit are discarded.
//
// The reference model is contract-level bookkeeping (slot lifecycle, its
// own byte images, free/ready accounting) — it shares no pipeline, no
// skid and no address math with the DUT.
#include <array>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <utility>
#include <vector>
#include "VKL_pp_tx_slots.h"
#include "verilated.h"
#include "../common/verilator_harness.hpp"

// ---- pool geometry, F01.5 "P-TX 4x576 + 1600" ------------------------------
constexpr int kSlots         = 5;     // slots 0..3 plain, slot 4 oversize
constexpr int kPlainSlots    = 4;     // the slots a plain allocation may take
constexpr int kOversizeSlot  = 4;     // the only slot an oversize alloc gets
constexpr int kPlainBytes    = 576;   // capacity of slots 0..3
constexpr int kOversizeBytes = 1600;  // capacity of slot 4

// full-std, 1-byte, mid, mid, full-oversize
constexpr std::array<int, kSlots> lens = {kPlainBytes, 1, 137, 42, kOversizeBytes};
constexpr std::array<int, kSlots> hdrs = {14, 0, 12, 5, 22};

#define CHECK(cond, ...) do { \
  ++checks; \
  if (!(cond)) { ++fails; printf("FAIL: " __VA_ARGS__); printf("\n"); } \
} while (0)

namespace {

// ---- independent contract model -------------------------------------------
struct RefPool {
  enum St { FREE, ALLOC, READY, STREAM };
  St      st[kSlots];
  int     len[kSlots];
  uint8_t img[kSlots][kOversizeBytes];

  RefPool() { for (int i = 0; i < kSlots; ++i) { st[i] = FREE; len[i] = 0; }
              memset(img, 0, sizeof img); }

  static int cap(int s) { return s == kOversizeSlot ? kOversizeBytes : kPlainBytes; }

  int alloc(bool oversize) {
    if (oversize) {
      if (st[kOversizeSlot] == FREE) {
        st[kOversizeSlot] = ALLOC;
        return kOversizeSlot;
      }
      return -1;
    }
    for (int i = 0; i < kPlainSlots; ++i)
      if (st[i] == FREE) { st[i] = ALLOC; return i; }
    return -1;
  }
  void write(int s, int a, uint8_t d) {
    if (st[s] == ALLOC && a < cap(s)) img[s][a] = d;      // else: discarded
  }
  void commit(int s, int l) {
    if (st[s] == ALLOC) { st[s] = READY; len[s] = l; }
  }
  void start(int s)    { if (st[s] == READY) st[s] = STREAM; }
  void freeSlot(int s) { st[s] = FREE; }

  int nfree() const {
    int n = 0; for (int i = 0; i < kSlots; ++i) n += (st[i] == FREE); return n;
  }
  uint32_t readyMask() const {
    uint32_t m = 0;
    for (int i = 0; i < kSlots; ++i) if (st[i] == READY) m |= 1u << i;
    return m;
  }
};

// ---- harness ---------------------------------------------------------------
struct Harness {
  VKL_pp_tx_slots* dut;
  RefPool ref;
  uint32_t rng = 0xC0FFEE01u;

  int checks = 0;   // the tally the CHECK macro keeps
  int fails = 0;

  // pre-edge observation of the serialize port (what the arbiter sees)
  int o_valid = 0;
  int o_last = 0;
  int o_ready = 0;
  uint8_t o_data = 0;

  bool last_pulse_ok = false;   // grant was a one-cycle pulse

  explicit Harness(VKL_pp_tx_slots* d) : dut(d) {}

  uint32_t rnd() { rng ^= rng << 13; rng ^= rng >> 17; rng ^= rng << 5; return rng; }

  void tick() {
    // settle combinational logic with this cycle's inputs
    dut->clk_i = 0; dut->eval();
    // observe the stream handshake PRE-EDGE (what the registers see)
    o_valid = dut->ser_valid_o; o_last = dut->ser_last_o;
    o_ready = dut->ser_ready_i; o_data = dut->ser_data_o;
    // rising edge: registers update
    dut->clk_i = 1; dut->eval();
  }

  // one request pulse per try; grant is registered — visible after the edge
  int alloc_dut(bool ov, int tries = 3) {
    int got = -1;
    for (int k = 0; k < tries; ++k) {
      dut->alloc_req_i = 1; dut->oversize_i = ov;
      tick();
      dut->alloc_req_i = 0; dut->oversize_i = 0;
      if (dut->alloc_gnt_o) got = dut->alloc_slot_o;
      tick();                                       // pulse must clear here
      if (got >= 0) { last_pulse_ok = (dut->alloc_gnt_o == 0); break; }
      if (dut->alloc_gnt_o) { got = dut->alloc_slot_o; break; }  // late = defect elsewhere
    }
    return got;
  }

  void wr(int s, int a, uint8_t d) {
    dut->wr_slot_i = s; dut->wr_addr_i = a; dut->wr_data_i = d;
    dut->wr_valid_i = 1;
    tick();
    dut->wr_valid_i = 0;
    ref.write(s, a, d);
  }

  void commit(int s, int l) {
    dut->wr_slot_i = s; dut->wr_len_i = l; dut->wr_commit_i = 1;
    tick();
    dut->wr_commit_i = 0;
    ref.commit(s, l);
  }

  static uint8_t pat(int s, int a, int epoch) {
    return static_cast<uint8_t>(0x35 * s + 7 * a + 0x11 + 0x4D * epoch);
  }

  // builders write headers AFTER payloads: offsets [hdr..len) first, then [0..hdr)
  void fill_ha(int s, int len, int hdr, int epoch) {
    for (int a = hdr; a < len; ++a) wr(s, a, pat(s, a, epoch));
    for (int a = 0; a < hdr; ++a)   wr(s, a, pat(s, a, epoch));
  }

  struct SRes {
    std::vector<uint8_t> bytes;
    bool done = false;
    int  hold_viol = 0;      // a stall changed/skipped the presented byte
    int  spurious  = 0;      // ser_valid after the frame completed
    int  last_pos  = -1;     // byte index where ser_last was consumed
    int  consume_span = 0;   // cycles from first to last consume, inclusive
    uint32_t mid_ready = 0;  // slots_ready_o sampled just after first valid
  };

  SRes stream(int slot, size_t explen, int ready_pct, int maxcyc,
              int bg_slot = -1, bool assert_req = true, bool drain = true) {
    SRes r;
    ref.start(slot);
    if (assert_req) { dut->ser_req_i = 1; dut->ser_slot_i = slot; }
    bool req_up = true;
    bool stall_pending = false;
    uint8_t stall_data = 0;
    int stall_last = 0;
    int first_c = -1;
    int last_c = -1;
    bool mid_sampled = false;

    for (int cyc = 0; cyc < maxcyc && !r.done; ++cyc) {
      dut->ser_ready_i = (rnd() % 100u) < static_cast<uint32_t>(ready_pct);
      tick();
      if (o_valid && req_up) {
        // frame accepted: drop our request (or hand the line to bg_slot)
        req_up = false;
        if (bg_slot >= 0) dut->ser_slot_i = bg_slot;
        else              dut->ser_req_i = 0;
      }
      if (o_valid && !mid_sampled) {
        r.mid_ready = dut->slots_ready_o;
        mid_sampled = true;
      }
      if (stall_pending &&
          (!o_valid || o_data != stall_data || o_last != stall_last))
        r.hold_viol++;
      if (o_valid && !o_ready) {
        stall_pending = true; stall_data = o_data; stall_last = o_last;
      } else {
        stall_pending = false;
      }
      if (o_valid && o_ready) {
        if (first_c < 0) first_c = cyc;
        last_c = cyc;
        r.bytes.push_back(o_data);
        if (o_last) { r.last_pos = static_cast<int>(r.bytes.size()) - 1; r.done = true; }
        else if (r.bytes.size() > explen) break;      // runaway guard
      }
    }
    if (first_c >= 0) r.consume_span = last_c - first_c + 1;
    if (r.done) ref.freeSlot(slot);                   // documented auto-free
    if (drain) {
      dut->ser_req_i = 0; dut->ser_ready_i = 1;
      for (int k = 0; k < 4; ++k) { tick(); if (o_valid) r.spurious++; }
    }
    return r;
  }

  std::pair<SRes, uint32_t> frame(const char* tag, int slot, int ready_pct,
                                  int bg = -1, bool assert_req = true,
                                  bool drain = true);

  int run();
  void reset_leaves_the_pool_quiescent();
  void allocation_walks_plain_slots_and_reserves_the_oversize();
  void fills_header_after_payload_then_commits();
  void an_uncommitted_slot_never_streams();
  void serializes_all_five_out_of_order_under_backpressure();
  void two_committed_slots_are_serviced_one_at_a_time();
  void a_freed_slot_is_reusable_and_late_writes_are_discarded();
  void a_zero_length_commit_is_freed_on_service();
  void cancellation_releases_an_allocated_builder_slot();
  void a_held_slot_survives_serialization_for_an_exact_retry();
  void the_idle_pool_stays_quiescent();
};

std::pair<Harness::SRes, uint32_t> Harness::frame(
    const char* tag, int slot, int ready_pct, int bg,
    bool assert_req, bool drain) {
  int len = ref.len[slot];
  std::vector<uint8_t> exp(ref.img[slot], ref.img[slot] + len);
  uint32_t exp_mid = ref.readyMask() & ~(1u << slot);
  auto r = stream(slot, static_cast<size_t>(len), ready_pct, len * 6 + 200,
                    bg, assert_req, drain);
  CHECK(r.done, "%s completes", tag);
  CHECK(r.bytes == exp, "%s byte-exact (%zu of %d bytes)", tag,
        r.bytes.size(), len);
  CHECK(r.last_pos == len - 1, "%s ser_last on byte %d exp %d", tag,
        r.last_pos, len - 1);
  CHECK(r.hold_viol == 0, "%s backpressure stalls, never skips (%d viol)",
        tag, r.hold_viol);
  if (drain)
    CHECK(r.spurious == 0, "%s no bytes after ser_last (%d)", tag, r.spurious);
  CHECK(dut->slots_free_o == static_cast<uint32_t>(ref.nfree()) &&
        dut->slots_ready_o == ref.readyMask(),
        "%s auto-freed on eof (free %u exp %d)", tag,
        static_cast<unsigned>(dut->slots_free_o), ref.nfree());
  return std::make_pair(r, exp_mid);
}

// ---- A: reset state -------------------------------------------------
void Harness::reset_leaves_the_pool_quiescent() {
  dut->rst_n = 0;
  for (int i = 0; i < 4; ++i) tick();
  dut->rst_n = 1;
  tick();
  CHECK(dut->slots_free_o == kSlots, "A all five slots free after reset");
  CHECK(dut->slots_ready_o == 0, "A nothing ready after reset");
  CHECK(dut->alloc_gnt_o == 0 && dut->ser_valid_o == 0, "A quiescent outputs");
}

// ---- B: allocation policy ------------------------------------------
void Harness::allocation_walks_plain_slots_and_reserves_the_oversize() {
  for (int k = 0; k < kPlainSlots; ++k) {
    int exp = ref.alloc(false);
    int got = alloc_dut(false);
    CHECK(got == exp, "B plain alloc #%d got %d exp %d", k, got, exp);
  }
  CHECK(last_pulse_ok, "B grant is a one-cycle pulse");
  CHECK(dut->slots_free_o == 1, "B one slot (the oversize) left free");
  {
    int exp = ref.alloc(false);                    // -1: std slots exhausted
    int got = alloc_dut(false, 6);
    CHECK(got == exp && got == -1,
          "B plain alloc NEVER returns slot 4 (got %d)", got);
  }
  {
    int exp = ref.alloc(true);                     // 4
    int got = alloc_dut(true);
    CHECK(got == exp && got == kOversizeSlot,
          "B oversize alloc returns 4 (got %d)", got);
  }
  CHECK(dut->slots_free_o == 0, "B pool exhausted");
  {
    int exp = ref.alloc(true);                     // -1: slot 4 busy
    int got = alloc_dut(true, 4);
    CHECK(got == exp && got == -1,
          "B oversize alloc waits for slot 4 (got %d)", got);
  }
  {
    int got = alloc_dut(false, 4);
    CHECK(got == -1, "B plain alloc denied when all busy (got %d)", got);
  }
}

// ---- C: fill (header after payload) + commit ------------------------
void Harness::fills_header_after_payload_then_commits() {
  for (int s = 0; s < kSlots; ++s) fill_ha(s, lens[s], hdrs[s], 0);
  CHECK(dut->ser_valid_o == 0, "C no stream during fill");
  commit(0, lens[0]);
  commit(1, lens[1]);
  commit(2, lens[2]);
}

// ---- D: serialize request on a non-READY (still ALLOC) slot ---------
void Harness::an_uncommitted_slot_never_streams() {
  {
    dut->ser_req_i = 1; dut->ser_slot_i = 3;
    bool sawv = false;
    for (int k = 0; k < 3; ++k) { tick(); sawv |= (o_valid != 0); }
    dut->ser_req_i = 0;
    tick();
    CHECK(!sawv, "D uncommitted slot never streams");
    CHECK(dut->slots_ready_o == ref.readyMask() && dut->slots_free_o == 0,
          "D state untouched by the ignored request (rdy %02x)",
          static_cast<unsigned>(dut->slots_ready_o));
  }
  commit(3, lens[3]);
  commit(4, lens[4]);
  CHECK(dut->slots_ready_o == 0x1F, "C+D all five committed -> ready 0x1F");
  CHECK(dut->slots_free_o == 0, "C+D none free while all queued");
}

// ---- E: serialize all five, out of order, random backpressure -------
void Harness::serializes_all_five_out_of_order_under_backpressure() {
  {
    auto [r, exp_mid] = frame("E slot2", 2, 60);
    CHECK(r.mid_ready == exp_mid,
          "E others stay ready mid-stream (got %02x exp %02x)",
          r.mid_ready, exp_mid);
  }
  frame("E slot0 (full 576)", 0, 70);
  frame("E slot4 (full 1600 oversize)", 4, 55);
  {
    auto [r, exp_mid] = frame("E slot1 (1-byte)", 1, 100);
    (void)exp_mid;
    CHECK(r.consume_span == 1, "E 1-byte frame consumed in one cycle (%d)",
          r.consume_span);
  }
  {
    auto [r, exp_mid] = frame("E slot3", 3, 100);
    (void)exp_mid;
    CHECK(r.consume_span == lens[3],
          "E full-ready streams one byte per cycle (span %d exp %d)",
          r.consume_span, lens[3]);
  }
  CHECK(dut->slots_free_o == kSlots && dut->slots_ready_o == 0,
        "E pool fully drained");
}

// ---- F: two committed slots, serviced one at a time -----------------
void Harness::two_committed_slots_are_serviced_one_at_a_time() {
  {
    int a = ref.alloc(false);
    int ga = alloc_dut(false);
    int b = ref.alloc(false);
    int gb = alloc_dut(false);
    CHECK(ga == a && a == 0, "F re-alloc lowest freed slot (got %d)", ga);
    CHECK(gb == b && b == 1, "F second alloc next lowest (got %d)", gb);
    fill_ha(a, 96, 14, 1); commit(a, 96);
    fill_ha(b, 64, 9, 1);  commit(b, 64);
    CHECK(dut->slots_ready_o == 0x03, "F both committed");
    // stream A while holding ser_req for B the whole time
    auto [ra, mid_a] = frame("F slotA", a, 65, /*bg=*/b,
                             /*assert_req=*/true, /*drain=*/false);
    (void)mid_a;
    CHECK((ra.mid_ready >> b) & 1, "F B stays ready while A streams");
    // request line is still up for B: it must now stream, intact
    frame("F slotB", b, 80, -1, /*assert_req=*/false, /*drain=*/true);
  }
}

// ---- G: reuse + write-after-commit is discarded ---------------------
void Harness::a_freed_slot_is_reusable_and_late_writes_are_discarded() {
  {
    int exp = ref.alloc(false);
    int got = alloc_dut(false);
    CHECK(got == exp && got == 0, "G freed slot is reusable (got %d)", got);
    fill_ha(0, 33, 4, 2);
    commit(0, 33);
    wr(0, 3, 0xEE);            // rogue write after commit: must not land
    frame("G reused slot0", 0, 60);
  }
}

// ---- H: zero-length commit is freed on service, no bytes ------------
void Harness::a_zero_length_commit_is_freed_on_service() {
  {
    int exp = ref.alloc(false);
    int got = alloc_dut(false);
    CHECK(got == exp && got == 0, "H alloc for the empty frame (got %d)", got);
    commit(0, 0);
    CHECK((dut->slots_ready_o & 1) == 1, "H zero-length commit shows ready");
    dut->ser_req_i = 1; dut->ser_slot_i = 0;
    bool sawv = false;
    for (int k = 0; k < 3; ++k) { tick(); sawv |= (o_valid != 0); }
    dut->ser_req_i = 0;
    tick();
    ref.freeSlot(0);
    CHECK(!sawv, "H empty frame emits no bytes");
    CHECK(dut->slots_free_o == kSlots && dut->slots_ready_o == 0,
          "H empty frame freed on service");
  }
}

// ---- I: cancellation releases an allocated builder slot -------------
void Harness::cancellation_releases_an_allocated_builder_slot() {
  {
    int exp = ref.alloc(false);
    int got = alloc_dut(false);
    CHECK(got == exp && got == 0, "I alloc for cancelled builder frame");
    dut->release_slot_i = 0; dut->release_valid_i = 1;
    tick();
    dut->release_valid_i = 0;
    ref.freeSlot(0);
    CHECK(dut->slots_free_o == kSlots && dut->slots_ready_o == 0,
          "I release frees an uncommitted allocated slot");
  }
}

// ---- J: held-slot exact retry ---------------------------------------
// A held originator slot must survive one complete serialization so the
// retry is the exact same byte image. Only release returns it to FREE.
void Harness::a_held_slot_survives_serialization_for_an_exact_retry() {
  {
    int exp = ref.alloc(false);
    int got = alloc_dut(false);
    CHECK(got == exp && got == 0, "J alloc for held originator frame");
    fill_ha(0, 47, 14, 3);
    commit(0, 47);
    std::vector<uint8_t> want(ref.img[0], ref.img[0] + 47);

    dut->hold_slot_i = 0; dut->hold_valid_i = 1;
    tick();
    dut->hold_valid_i = 0;

    auto first = stream(0, 47, 61, 500);
    CHECK(first.done && first.bytes == want,
          "J first held transmission is byte-exact");
    CHECK((dut->slots_ready_o & 1u) != 0 && dut->slots_free_o == 4,
          "J held slot returns to READY after eof");
    ref.st[0] = RefPool::READY;

    auto retry = stream(0, 47, 53, 500);
    CHECK(retry.done && retry.bytes == want && retry.bytes == first.bytes,
          "J retry reuses the exact byte image");
    CHECK((dut->slots_ready_o & 1u) != 0 && dut->slots_free_o == 4,
          "J held slot remains READY after retry");
    ref.st[0] = RefPool::READY;

    dut->release_slot_i = 0; dut->release_valid_i = 1;
    tick();
    dut->release_valid_i = 0;
    ref.freeSlot(0);
    CHECK(dut->slots_free_o == kSlots && dut->slots_ready_o == 0,
          "J release frees the held slot");

    // A cancellation can arrive on the final serializer beat. The release
    // must win that edge instead of leaving an unheld READY slot stranded.
    exp = ref.alloc(false);
    got = alloc_dut(false);
    CHECK(got == exp && got == 0, "J alloc for release-at-eof frame");
    fill_ha(0, 1, 0, 4);
    commit(0, 1);
    dut->hold_slot_i = 0; dut->hold_valid_i = 1;
    tick();
    dut->hold_valid_i = 0;
    dut->ser_req_i = 1; dut->ser_slot_i = 0; dut->ser_ready_i = 1;
    tick();
    dut->ser_req_i = 0;
    bool release_at_eof = false;
    for (int cyc = 0; cyc < 8 && !release_at_eof; ++cyc) {
      dut->clk_i = 0;
      dut->eval();
      if (dut->ser_valid_o && dut->ser_last_o) {
        dut->release_slot_i = 0;
        dut->release_valid_i = 1;
        release_at_eof = true;
      }
      tick();
    }
    dut->release_valid_i = 0;
    ref.freeSlot(0);
    CHECK(release_at_eof && o_valid && o_last,
          "J release-at-eof coincides with the final consumed beat");
    CHECK(dut->slots_free_o == kSlots && dut->slots_ready_o == 0,
          "J release-at-eof frees the held slot");

    // A release may arrive on the first serializer-request edge, before the
    // pool accepts the frame. Release wins that boundary and no byte starts.
    exp = ref.alloc(false);
    got = alloc_dut(false);
    CHECK(got == exp && got == 0, "J alloc for release-at-start frame");
    fill_ha(0, 3, 1, 5);
    commit(0, 3);
    dut->hold_slot_i = 0; dut->hold_valid_i = 1;
    tick();
    dut->hold_valid_i = 0;
    dut->ser_req_i = 1; dut->ser_slot_i = 0; dut->ser_ready_i = 1;
    dut->release_slot_i = 0; dut->release_valid_i = 1;
    tick();
    dut->ser_req_i = 0;
    dut->release_valid_i = 0;
    ref.freeSlot(0);
    bool release_at_start_byte = false;
    for (int i = 0; i < 8; ++i) {
      tick();
      release_at_start_byte |= o_valid;
    }
    CHECK(!release_at_start_byte,
          "J release-at-start suppresses the unaccepted frame");
    CHECK(dut->slots_free_o == kSlots && dut->slots_ready_o == 0,
          "J release-at-start frees the slot without entering STREAM");
  }
}

// ---- K: quiescence ---------------------------------------------------
void Harness::the_idle_pool_stays_quiescent() {
  {
    bool spur = false;
    for (int k = 0; k < 10; ++k) {
      tick();
      spur |= (dut->alloc_gnt_o != 0) || (o_valid != 0);
    }
    CHECK(!spur, "K no spurious grants or bytes when idle");
    CHECK(dut->slots_free_o == kSlots && dut->slots_ready_o == 0, "K final state clean");
  }
}

int Harness::run() {
  dut->alloc_req_i = 0; dut->oversize_i = 0;
  dut->wr_slot_i = 0; dut->wr_addr_i = 0; dut->wr_data_i = 0;
  dut->wr_valid_i = 0; dut->wr_commit_i = 0; dut->wr_len_i = 0;
  dut->hold_valid_i = 0; dut->hold_slot_i = 0;
  dut->release_valid_i = 0; dut->release_slot_i = 0;
  dut->ser_req_i = 0; dut->ser_slot_i = 0; dut->ser_ready_i = 0;

  reset_leaves_the_pool_quiescent();
  allocation_walks_plain_slots_and_reserves_the_oversize();
  fills_header_after_payload_then_commits();
  an_uncommitted_slot_never_streams();
  serializes_all_five_out_of_order_under_backpressure();
  two_committed_slots_are_serviced_one_at_a_time();
  a_freed_slot_is_reusable_and_late_writes_are_discarded();
  a_zero_length_commit_is_freed_on_service();
  cancellation_releases_an_allocated_builder_slot();
  a_held_slot_survives_serialization_for_an_exact_retry();
  the_idle_pool_stays_quiescent();

  printf("%d checks: %d PASS, %d FAIL\n", checks, checks - fails, fails);
  return fails ? 1 : 0;
}

}  // namespace

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  const milan::tb::Model<VKL_pp_tx_slots> model;
  Harness harness(model.get());
  return harness.run();
}
