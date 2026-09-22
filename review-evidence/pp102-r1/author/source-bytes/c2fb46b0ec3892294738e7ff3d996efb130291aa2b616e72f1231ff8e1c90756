// SPDX-License-Identifier: CERN-OHL-W-2.0
// KL_pp_rx_slots suite — independent expectations, never DUT logic.
//
// The reference model below implements the POOL CONTRACT of 03 §2/§3
// (drop6 gate, V8 drop+count) from the documented behavior: 4 slots ×
// 576 bytes, lowest drop gate counts refused-while-full allocations
// (saturating 16-bit), wr_last_i closes the byte stream, wr_commit_i
// latches the accepted-byte count, wr_abort_i returns the slot, free_i
// returns occupied slots only. It does NOT assume a grant policy: the
// granted slot index is taken as an opaque handle and only required to
// have been free in the model. Byte-exactness is checked by streaming a
// generator-defined pattern in and reading every byte back through the
// one-cycle sync read port.
#include <cstdint>
#include <cstdio>
#include <cstring>
#include "VKL_pp_rx_slots.h"
#include "verilated.h"
#include "../common/verilator_harness.hpp"

//! The refused-while-full gate is a saturating 16-bit counter: it stops here
//! and never wraps, in the DUT and in the model below.
constexpr uint32_t kOverrunMax = 0xFFFFu;

//! Idle cycles the harness holds rst_n low before the first stimulus.
constexpr int kResetCycles = 4;

#define CHECK(cond, ...) do { \
  ++checks; \
  if (!(cond)) { ++fails; printf("FAIL: " __VA_ARGS__); printf("\n"); } \
} while (0)

// ---- independent reference model (contract, not DUT logic) -------------
struct RefPool {
  static constexpr unsigned N = 4;
  static constexpr unsigned CAP = 576;
  enum St { FREE, WR, OCC };
  St       st[N];
  uint8_t  mem[N][CAP];
  unsigned len[N];
  uint32_t ovr = 0;      // saturates at kOverrunMax
  int      cur = -1;     // slot being written (-1 = none)
  unsigned ptr = 0;
  bool     closed = false;

  RefPool() {
    for (unsigned i = 0; i < N; ++i) { st[i] = FREE; len[i] = 0; memset(mem[i], 0, CAP); }
  }
  unsigned nfree() const {
    unsigned c = 0;
    for (unsigned i = 0; i < N; ++i) c += (st[i] == FREE) ? 1u : 0u;
    return c;
  }
  // one cycle of alloc_req_i held high; returns whether a grant must appear
  bool allocCycle() {
    bool full = (nfree() == 0);
    if (full && ovr < kOverrunMax) ++ovr;   // the last drop gate counts, saturating
    return !full && cur < 0;           // no grant mid-write (frame-serial validator)
  }
  void bind(unsigned s) { st[s] = WR; cur = static_cast<int>(s); ptr = 0; closed = false; }
  void push(uint8_t b, bool last) {
    if (cur < 0 || closed || ptr >= CAP) return;  // closed / overflow bytes dropped
    mem[cur][ptr++] = b;
    if (last) closed = true;
  }
  void commit() {
    if (cur < 0) return;
    st[static_cast<unsigned>(cur)] = OCC;
    len[static_cast<unsigned>(cur)] = ptr;
    cur = -1;
  }
  void abort() {
    if (cur < 0) return;
    st[static_cast<unsigned>(cur)] = FREE;
    cur = -1;
  }
  void freeSlot(unsigned s) { if (s < N && st[s] == OCC) st[s] = FREE; }
};

// deterministic per-(slot, round) byte generator — the wire truth
static uint8_t pat(unsigned slot, unsigned round, unsigned i) {
  return static_cast<uint8_t>(0x35u + slot * 0x1Fu + round * 0x4Du + i * 7u);
}

struct Hn {
  VKL_pp_rx_slots* d;
  RefPool m;
  int checks = 0;
  int fails = 0;
  explicit Hn(VKL_pp_rx_slots* dd) : d(dd) {}

  void settle() { d->clk_i = 0; d->eval(); }  // pre-edge: combinational outputs
  void edge()   { d->clk_i = 1; d->eval(); }  // registers + memory update
  void clearIn() {
    d->alloc_req_i = 0; d->wr_valid_i = 0; d->wr_data_i = 0; d->wr_last_i = 0;
    d->wr_abort_i = 0; d->wr_commit_i = 0; d->rd_en_i = 0; d->free_i = 0;
  }
  void idle() { clearIn(); settle(); edge(); }

  // one alloc_req cycle with checks; returns granted slot or -1
  int allocCycle(const char* ph) {
    clearIn(); d->alloc_req_i = 1;
    settle();                                  // grant is combinational: sample pre-edge
    bool exp_gnt = m.allocCycle();
    int got = -1;
    CHECK((d->alloc_gnt_o != 0) == exp_gnt, "%s: gnt %d expected %d",
          ph, static_cast<int>(d->alloc_gnt_o), static_cast<int>(exp_gnt));
    if (d->alloc_gnt_o) {
      got = static_cast<int>(d->alloc_slot_o);
      CHECK(m.st[static_cast<unsigned>(got)] == RefPool::FREE,
            "%s: granted slot %d not free in model", ph, got);
      m.bind(static_cast<unsigned>(got));
    }
    edge(); clearIn();
    return got;
  }
  // alloc_req held while full, no per-cycle checks (saturation soak)
  void holdAllocFull(unsigned cycles) {
    clearIn(); d->alloc_req_i = 1;
    for (unsigned i = 0; i < cycles; ++i) { settle(); (void)m.allocCycle(); edge(); }
    clearIn();
  }
  void writeByte(uint8_t b, bool last, bool commit = false) {
    clearIn();
    d->wr_valid_i = 1; d->wr_data_i = b; d->wr_last_i = last ? 1 : 0;
    d->wr_commit_i = commit ? 1 : 0;
    settle();
    m.push(b, last);
    if (commit) m.commit();
    edge(); clearIn();
  }
  void commitCycle() { clearIn(); d->wr_commit_i = 1; settle(); m.commit(); edge(); clearIn(); }
  void abortCycle()  { clearIn(); d->wr_abort_i = 1;  settle(); m.abort();  edge(); clearIn(); }
  void freeCycle(unsigned s) {
    clearIn(); d->free_i = 1; d->free_slot_i = s;
    settle(); m.freeSlot(s); edge(); clearIn();
  }
  // stream a full frame into the granted slot; commit either with the last
  // byte (same cycle) or one cycle later — both length forms are legal
  void fillSlot(unsigned slot, unsigned round, unsigned len, bool same_cycle_commit) {
    for (unsigned i = 0; i < len; ++i) {
      bool last = (i == len - 1);
      writeByte(pat(slot, round, i), last, last && same_cycle_commit);
    }
    if (!same_cycle_commit) commitCycle();
  }
  uint8_t readByte(unsigned slot, unsigned addr) {
    clearIn();
    d->rd_en_i = 1; d->rd_slot_i = slot; d->rd_addr_i = addr;
    settle(); edge();
    clearIn();
    return d->rd_data_o;                       // registered: valid after the edge
  }
  unsigned slotLen(int slot) {                 // combinational on rd_slot_i: pre-edge
    if (slot < 0 || slot >= static_cast<int>(RefPool::N)) return 0xFFFFu;  // bad handle sentinel
    clearIn(); d->rd_slot_i = static_cast<unsigned>(slot);
    settle();
    unsigned l = d->slot_len_o;
    edge(); clearIn();
    return l;
  }
  unsigned freeNow() {                         // combinational: pre-edge
    clearIn(); settle();
    unsigned f = d->slots_free_o;
    edge();
    return f;
  }
  unsigned mismatches(int slot) {              // model-vs-DUT byte compare
    if (slot < 0 || slot >= static_cast<int>(RefPool::N)) return 9999u;    // bad handle sentinel
    unsigned bad = 0;
    for (unsigned a = 0; a < m.len[slot]; ++a)
      if (readByte(static_cast<unsigned>(slot), a) != m.mem[slot][a]) ++bad;
    return bad;
  }
};

namespace {

//! The DUT, its reference pool and the tally under one owner (Core Guidelines
//! I.2). `checks`/`fails` live in `Hn` because the BFM's own `allocCycle()`
//! counts too, and the run's phases are named for the contract clause each one
//! proves rather than for their T-number (F.3).
class RxSlotPoolHarness {
 public:
  RxSlotPoolHarness() : d(model.get()), h(d) {}

  int run() {
    hold_reset_then_release();

    check_reset_state();
    fill_all_four_slots_with_distinct_patterns();
    check_fifth_alloc_is_refused_and_counted();
    check_abort_mid_frame_returns_the_slot();
    check_free_and_realloc_walk_leaks_nothing();
    check_write_one_slot_while_reading_another();
    check_bytes_after_last_are_ignored();
    check_overflow_clamps_at_slot_capacity();
    check_freeing_a_free_slot_is_a_no_op();
    check_alloc_refused_mid_write_is_not_an_overrun();
    check_overrun_counter_saturates();
    check_final_consistency();

    printf("%d checks: %d PASS, %d FAIL\n", h.checks, h.checks - h.fails, h.fails);
    return h.fails ? 1 : 0;
  }

 private:
  void hold_reset_then_release() {
    h.clearIn();
    d->rst_n = 0;
    for (int i = 0; i < kResetCycles; ++i) h.idle();
    d->rst_n = 1;
    h.idle();
  }

  // ---- T1: reset state -------------------------------------------------
  void check_reset_state() {
    CHECK(h.freeNow() == 4, "T1 slots_free after reset got %u", h.freeNow());
    CHECK(d->rx_overrun_count_o == 0, "T1 overrun zero got %u",
          static_cast<unsigned>(d->rx_overrun_count_o));
  }

  // ---- T2: fill all four slots, distinct patterns + lengths ------------
  // lengths cover min Ethernet, a typical ACMPDU, the 536 max command PDU,
  // and the full 576 slot; commit alternates same-cycle / one-cycle-later
  void fill_all_four_slots_with_distinct_patterns() {
    static constexpr unsigned lens2[4] = { 60, 82, 536, 576 };
    int handle2[4] = { -1, -1,
                       -1, -1 };
    for (unsigned k = 0; k < 4; ++k) {
      handle2[k] = h.allocCycle("T2 alloc");
      if (handle2[k] < 0) continue;
      h.fillSlot(static_cast<unsigned>(handle2[k]), 0, lens2[k], (k % 2) == 0);
      CHECK(h.slotLen(handle2[k]) == lens2[k],
            "T2 slot %d len got %u want %u", handle2[k],
            h.slotLen(handle2[k]), lens2[k]);
    }
    CHECK(h.freeNow() == 0, "T2 pool full got %u", h.freeNow());
    for (unsigned k = 0; k < 4; ++k)
      if (handle2[k] >= 0)
        CHECK(h.mismatches(handle2[k]) == 0,
              "T2 slot %d byte-exact readback", handle2[k]);
    CHECK(d->rx_overrun_count_o == 0, "T2 no overrun yet got %u",
          static_cast<unsigned>(d->rx_overrun_count_o));
  }

  // ---- T3: 5th alloc refused + counted ---------------------------------
  void check_fifth_alloc_is_refused_and_counted() {
    int r5 = h.allocCycle("T3 refused");
    CHECK(r5 == -1, "T3 no grant while full got %d", r5);
    CHECK(d->rx_overrun_count_o == 1, "T3 overrun 1 got %u",
          static_cast<unsigned>(d->rx_overrun_count_o));
    h.holdAllocFull(3);
    CHECK(d->rx_overrun_count_o == 4, "T3 overrun 4 after held req got %u",
          static_cast<unsigned>(d->rx_overrun_count_o));
    CHECK(d->rx_overrun_count_o == h.m.ovr, "T3 model agrees got %u vs %u",
          static_cast<unsigned>(d->rx_overrun_count_o), h.m.ovr);
  }

  // ---- T4: abort mid-frame frees the slot for the next alloc -----------
  void check_abort_mid_frame_returns_the_slot() {
    h.freeCycle(2);
    CHECK(h.freeNow() == 1, "T4 one free after free(2) got %u", h.freeNow());
    int a1 = h.allocCycle("T4 realloc");
    CHECK(a1 == 2, "T4 the freed slot is regranted got %d", a1);
    for (unsigned i = 0; i < 100; ++i) h.writeByte(pat(9, 9, i), false);
    h.abortCycle();
    CHECK(h.freeNow() == 1, "T4 abort returns the slot got %u", h.freeNow());
    int a2 = h.allocCycle("T4 alloc after abort");
    CHECK(a2 == 2, "T4 aborted slot allocatable got %d", a2);
    h.fillSlot(2, 1, 48, false);
    CHECK(h.slotLen(2) == 48, "T4 new len got %u", h.slotLen(2));
    CHECK(h.mismatches(2) == 0, "T4 new content, not the aborted bytes");
    CHECK(h.mismatches(3) == 0, "T4 neighbor slot 3 undisturbed");
  }

  // ---- T5: free/realloc walks the pool 3 full cycles, no leaks ---------
  void check_free_and_realloc_walk_leaks_nothing() {
    for (unsigned s = 0; s < 4; ++s) h.freeCycle(s);
    CHECK(h.freeNow() == 4, "T5 all returned got %u", h.freeNow());
    for (unsigned round = 1; round <= 3; ++round) {
      int hs[4] = { -1, -1,
                    -1, -1 };
      for (unsigned k = 0; k < 4; ++k) {
        hs[k] = h.allocCycle("T5 alloc");
        if (hs[k] < 0) continue;
        h.fillSlot(static_cast<unsigned>(hs[k]), round, 10 * (k + 1) + round, (k % 2) == 1);
      }
      CHECK(h.freeNow() == 0, "T5 round %u pool full got %u", round, h.freeNow());
      for (unsigned k = 0; k < 4; ++k) {
        if (hs[k] < 0) continue;
        CHECK(h.slotLen(hs[k]) == 10 * (k + 1) + round,
              "T5 round %u slot %d len got %u", round, hs[k],
              h.slotLen(hs[k]));
        CHECK(h.mismatches(hs[k]) == 0,
              "T5 round %u slot %d byte-exact", round, hs[k]);
      }
      for (unsigned s = 0; s < 4; ++s) h.freeCycle(s);
      CHECK(h.freeNow() == 4, "T5 round %u no leak got %u", round, h.freeNow());
    }
  }

  // ---- T6: interleaved — write one slot while reading another ----------
  void check_write_one_slot_while_reading_another() {
    int sb = h.allocCycle("T6 alloc B");
    if (sb >= 0) h.fillSlot(static_cast<unsigned>(sb), 4, 32, false);
    int sa = h.allocCycle("T6 alloc A");
    CHECK(sa >= 0 && sb >= 0 && sa != sb, "T6 two distinct slots %d %d", sa, sb);
    unsigned bad_b = (sa >= 0 && sb >= 0) ? 0u : 9999u;  // bad handles: skip, fail below
    for (unsigned i = 0; sa >= 0 && sb >= 0 && i < 32; ++i) {  // byte into A, read B
      h.clearIn();
      d->wr_valid_i = 1; d->wr_data_i = pat(static_cast<unsigned>(sa), 5, i);
      d->wr_last_i = (i == 31) ? 1 : 0;
      d->rd_en_i = 1; d->rd_slot_i = static_cast<unsigned>(sb); d->rd_addr_i = i;
      h.settle();
      h.m.push(pat(static_cast<unsigned>(sa), 5, i), i == 31);
      h.edge();
      if (d->rd_data_o != h.m.mem[static_cast<unsigned>(sb)][i]) ++bad_b;
      h.clearIn();
    }
    h.commitCycle();
    CHECK(bad_b == 0, "T6 reads of B during A writes: %u bad", bad_b);
    CHECK(h.slotLen(sa) == 32, "T6 A len got %u", h.slotLen(sa));
    CHECK(h.mismatches(sa) == 0, "T6 A byte-exact after interleave");
  }

  // ---- T9: bytes after wr_last_i are ignored ---------------------------
  void check_bytes_after_last_are_ignored() {
    int s9 = h.allocCycle("T9 alloc");
    CHECK(s9 >= 0, "T9 grant got %d", s9);
    for (unsigned i = 0; i < 10; ++i) h.writeByte(pat(static_cast<unsigned>(s9), 6, i), i == 9);
    for (unsigned i = 0; i < 5; ++i)  h.writeByte(0xEE, false);  // must be dropped
    h.commitCycle();
    CHECK(h.slotLen(s9) == 10, "T9 len stops at last got %u",
          h.slotLen(s9));
    CHECK(h.mismatches(s9) == 0, "T9 content byte-exact");
  }

  // ---- T10: overflow clamps at the slot capacity -----------------------
  void check_overflow_clamps_at_slot_capacity() {
    int s10 = h.allocCycle("T10 alloc");
    CHECK(s10 >= 0, "T10 grant got %d", s10);
    for (unsigned i = 0; i < RefPool::CAP + 20; ++i)
      h.writeByte(pat(static_cast<unsigned>(s10), 7, i), false);
    h.commitCycle();
    CHECK(h.slotLen(s10) == RefPool::CAP, "T10 len clamps got %u",
          h.slotLen(s10));
    CHECK(h.mismatches(s10) == 0, "T10 first 576 bytes byte-exact");
  }

  // ---- T11: freeing a free slot is a no-op -----------------------------
  void check_freeing_a_free_slot_is_a_no_op() {
    CHECK(h.freeNow() == 0, "T11 precondition: pool full got %u", h.freeNow());
    h.freeCycle(0);                              // occupied -> free
    CHECK(h.freeNow() == 1, "T11 free(occupied) got %u", h.freeNow());
    h.freeCycle(0);                              // already free: must not double-count
    CHECK(h.freeNow() == 1, "T11 free-of-free no-op got %u", h.freeNow());
  }

  // ---- T12: alloc refused mid-write, without an overrun count ----------
  void check_alloc_refused_mid_write_is_not_an_overrun() {
    h.freeCycle(1);                              // second free slot: pool NOT full
    CHECK(h.freeNow() == 2, "T12 two free got %u", h.freeNow());
    uint32_t ovr12 = d->rx_overrun_count_o;
    int s12 = h.allocCycle("T12 alloc");
    CHECK(s12 >= 0, "T12 grant got %d", s12);
    h.writeByte(0x77, false);                    // in flight; one slot still free
    int r12 = h.allocCycle("T12 refused mid-write");
    CHECK(r12 == -1, "T12 no grant mid-write got %d", r12);
    CHECK(d->rx_overrun_count_o == ovr12, "T12 not an overrun got %u want %u",
          static_cast<unsigned>(d->rx_overrun_count_o), ovr12);
    h.abortCycle();
  }

  // ---- T8: the overrun counter saturates, never wraps ------------------
  void check_overrun_counter_saturates() {
    for (unsigned k = 0; k < 2; ++k) {           // refill so the pool is full
      int s8 = h.allocCycle("T8 refill");
      CHECK(s8 >= 0, "T8 grant got %d", s8);
      h.fillSlot(static_cast<unsigned>(s8), 8 + k, 12, false);
    }
    CHECK(h.freeNow() == 0, "T8 pool full got %u", h.freeNow());
    h.holdAllocFull(40000);
    CHECK(d->rx_overrun_count_o == h.m.ovr, "T8 midpoint model agrees got %u vs %u",
          static_cast<unsigned>(d->rx_overrun_count_o), h.m.ovr);
    h.holdAllocFull(30000);                      // total > 65,535: must saturate
    CHECK(d->rx_overrun_count_o == kOverrunMax, "T8 saturated got %u",
          static_cast<unsigned>(d->rx_overrun_count_o));
    h.holdAllocFull(100);
    CHECK(d->rx_overrun_count_o == kOverrunMax, "T8 no wrap got %u",
          static_cast<unsigned>(d->rx_overrun_count_o));
  }

  // ---- final consistency ----------------------------------------------
  void check_final_consistency() {
    h.idle();
    CHECK(h.freeNow() == h.m.nfree(), "final slots_free got %u want %u",
          h.freeNow(), h.m.nfree());
  }

  const milan::tb::Model<VKL_pp_rx_slots> model;
  VKL_pp_rx_slots* const d;
  Hn h;

  //! `CHECK` names `checks`/`fails` unqualified, so the phases above reach the
  //! same two counters `Hn`'s own checked helpers move. Declared after `h` so
  //! they bind to a member that is already constructed.
  int& checks = h.checks;
  int& fails = h.fails;
};

}  // namespace

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  RxSlotPoolHarness harness;
  return harness.run();
}
