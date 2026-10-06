// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// test_port_loop.cpp - the HAL's own half, on the host model (#665 lanes F0
// and FT; GoogleTest):
//
//   P   the static pool behind lwSRP's shlan_malloc/calloc/free: classes,
//       exhaustion, release, double and foreign frees, calloc's overflow,
//       alignment, the high-water mark, and the four shlan_* functions;
//   S   the debug sink behind shlan_printf: delivery, truncation, discard;
//   D   the mailbox driver on the model: RX records byte for byte, a
//       malformed record resynchronised, TX records and their refusals, every
//       event type decoded, timers, the coherent grandmaster read;
//   L   the event loop: the order ctrl_loop_open brings the mailbox up in,
//       the per-pass bounds, the TICK fan-out to centisecond consumers.
//
// One test per labelled step; each assertion carries the check's name from
// the hand-rolled suite it replaces (README.md, "The port").

#include <gtest/gtest.h>

#include <cstddef>
#include <cstdint>
#include <cstring>

#include "ctrl_debug.h"
#include "ctrl_loop.h"
#include "ctrl_pool.h"
#include "fw_gtest.hpp"
#include "mbx.h"
#include "mbx_model.h"
#include "mbx_wire.h"
#include "shlan_port.h"

FW_TALLY_LABEL("ctrl port, driver and loop (host model)");

namespace {

mbx_model model;

alignas(std::max_align_t) std::uint8_t arena[4096];

const ctrl_pool_class classes[] = {{32u, 4u}, {64u, 2u}};

// CTRL_POOL_ALIGN, which ctrl_pool.h spells with C11's _Alignof, in C++.
constexpr std::size_t kPoolAlign = alignof(std::max_align_t);

// Every test starts from a reset model bound behind mbx_hal.h.
class Model : public ::testing::Test {
 protected:
    void SetUp() override {
        mbx_model_reset(&model);
        mbx_model_bind(&model, nullptr, nullptr);
    }
};

std::uint8_t* bytes_of(void* p) {
    return static_cast<std::uint8_t*>(p);
}

// Whether a block lies inside size class k of the pool: a block from
// anywhere else, a heap's included, is not the pool's whatever its address.
bool in_bin(const ctrl_pool& pool, unsigned k, const void* block) {
    const auto at = reinterpret_cast<std::uintptr_t>(block);
    const auto base = reinterpret_cast<std::uintptr_t>(pool.bins[k].base);
    return block != nullptr && at >= base && at - base < std::uintptr_t{pool.bins[k].blocks} * pool.bins[k].stride;
}

// ---- P: the pool ----------------------------------------------------------

TEST(Pool, P0Refusals) {
    ctrl_pool pool;
    const std::size_t need = ctrl_pool_arena_bytes(classes, 2);
    const ctrl_pool_class unordered[] = {{64u, 2u}, {32u, 4u}};
    const ctrl_pool_class empty[] = {{32u, 0u}};
    EXPECT_FALSE(ctrl_pool_init(&pool, arena, need - 1u, classes, 2)) << "P0 an arena one byte short is refused";
    EXPECT_FALSE(ctrl_pool_init(&pool, arena + 1, need, classes, 2)) << "P0 a misaligned arena is refused";
    EXPECT_FALSE(ctrl_pool_init(&pool, arena, need, unordered, 2)) << "P0 classes that do not grow are refused";
    EXPECT_FALSE(ctrl_pool_init(&pool, arena, need, empty, 1)) << "P0 an empty class is refused";
    EXPECT_TRUE(ctrl_pool_init(&pool, arena, need, classes, 2)) << "P0 the exact arena is accepted";
}

// The pool after P1's allocations: four small blocks, the spill and the last.
struct FullPool {
    ctrl_pool pool;
    void* small[4];
    void* spill;
    void* last;
};

void fill(FullPool& f) {
    ASSERT_TRUE(ctrl_pool_init(&f.pool, arena, sizeof arena, classes, 2));
    for (void*& block : f.small) {
        block = ctrl_pool_alloc(&f.pool, 24u);
    }
    f.spill = ctrl_pool_alloc(&f.pool, 8u);
    f.last = ctrl_pool_alloc(&f.pool, 64u);
}

TEST(Pool, P1ClassesExhaustionAndRefusals) {
    ctrl_pool pool;
    ASSERT_TRUE(ctrl_pool_init(&pool, arena, sizeof arena, classes, 2));
    void* small[4];
    bool aligned = true;
    for (void*& block : small) {
        block = ctrl_pool_alloc(&pool, 24u);
        aligned = aligned && block != nullptr && reinterpret_cast<std::uintptr_t>(block) % kPoolAlign == 0u;
    }
    EXPECT_TRUE(aligned) << "P1 four 24-byte blocks come from the 32-byte class, aligned";
    void* spill = ctrl_pool_alloc(&pool, 8u);
    EXPECT_TRUE(spill != nullptr && bytes_of(spill) >= pool.bins[1].base)
        << "P1 an exhausted class spills into the next larger one";
    EXPECT_EQ(ctrl_pool_alloc(&pool, 65u), nullptr) << "P1 a size no class holds is refused";
    EXPECT_EQ(ctrl_pool_alloc(&pool, 0u), nullptr) << "P1 a zero-byte allocation is refused";
    EXPECT_EQ(pool.refused, 2u) << "P1 refusals are counted";
    EXPECT_NE(ctrl_pool_alloc(&pool, 64u), nullptr) << "P1 the last block of the large class";
    EXPECT_EQ(ctrl_pool_alloc(&pool, 1u), nullptr) << "P1 then nothing is left";
    EXPECT_EQ(ctrl_pool_in_use(&pool), 6u) << "P1 every block is in use";
}

TEST(Pool, P2ReleaseAndBadFrees) {
    FullPool f;
    ASSERT_NO_FATAL_FAILURE(fill(f));
    ctrl_pool_free(&f.pool, f.small[2]);
    EXPECT_EQ(ctrl_pool_alloc(&f.pool, 32u), f.small[2]) << "P2 a released block is the next one handed out";
    ctrl_pool_free(&f.pool, f.small[1]);
    ctrl_pool_free(&f.pool, f.small[1]);
    EXPECT_EQ(f.pool.bad_frees, 1u) << "P2 a double free is refused and counted";
    ctrl_pool_free(&f.pool, bytes_of(f.small[0]) + 8);
    EXPECT_EQ(f.pool.bad_frees, 2u) << "P2 a free into the middle of a block is refused";
    ctrl_pool_free(&f.pool, &f.pool);
    EXPECT_EQ(f.pool.bad_frees, 3u) << "P2 a free of a pointer the pool never handed out is refused";
    ctrl_pool_free(&f.pool, nullptr);
    EXPECT_EQ(f.pool.bad_frees, 3u) << "P2 a free of NULL is a no-op";
    EXPECT_EQ(f.pool.bins[0].high_water, 4u) << "P2 the high-water mark of the small class";
}

TEST(Pool, P3CallocZeroesAndRefusesAWrap) {
    ctrl_pool pool;
    ASSERT_TRUE(ctrl_pool_init(&pool, arena, sizeof arena, classes, 2));
    std::uint8_t* dirty = bytes_of(ctrl_pool_alloc(&pool, 32u));
    ASSERT_NE(dirty, nullptr);
    std::memset(dirty, 0xA5, 32u);
    ctrl_pool_free(&pool, dirty);
    const std::uint8_t* clean = bytes_of(ctrl_pool_calloc(&pool, 4u, 8u));
    bool zero = clean != nullptr;
    for (unsigned k = 0; zero && k < 32u; ++k) {
        zero = clean[k] == 0u;
    }
    EXPECT_TRUE(zero) << "P3 calloc hands out a zeroed block, even a reused one";
    EXPECT_EQ(ctrl_pool_calloc(&pool, SIZE_MAX / 4u + 2u, 4u), nullptr)
        << "P3 calloc refuses a count times size that wraps to a small size";
}

TEST(Pool, P4ShlanFunctionsDrawOnTheBoundPool) {
    ctrl_pool pool;
    ASSERT_TRUE(ctrl_pool_init(&pool, arena, sizeof arena, classes, 2));
    shlan_port_bind_pool(nullptr);
    EXPECT_EQ(shlan_malloc(16u), nullptr) << "P4 shlan_malloc before the pool is bound refuses";
    shlan_port_bind_pool(&pool);
    void* a = shlan_malloc(40u);
    void* b = shlan_calloc(2u, 8u);
    EXPECT_TRUE(in_bin(pool, 1, a) && in_bin(pool, 0, b)) << "P4 shlan_malloc and shlan_calloc draw on the bound pool";
    const unsigned before = ctrl_pool_in_use(&pool);
    shlan_free(a);
    shlan_free(b);
    EXPECT_EQ(ctrl_pool_in_use(&pool), before - 2u) << "P4 shlan_free returns both blocks";
    shlan_port_bind_pool(nullptr);
}

// ---- S: the debug sink ----------------------------------------------------

struct SinkCapture {
    char text[256];
    std::size_t len;
    unsigned calls;
};

void capture_sink(void* ctx, const char* text, std::size_t len) {
    auto* c = static_cast<SinkCapture*>(ctx);
    std::memcpy(c->text, text, len);
    c->text[len] = '\0';
    c->len = len;
    c->calls++;
}

TEST(DebugSink, S0NoSinkDiscardsAndCounts) {
    const std::uint32_t before = ctrl_debug_discarded();
    ctrl_debug_bind(nullptr, nullptr);
    EXPECT_EQ(shlan_printf("lost %d", 1), 0) << "S0 with no sink bound shlan_printf emits nothing";
    EXPECT_EQ(ctrl_debug_discarded() - before, 1u) << "S0 and counts the discard";
}

TEST(DebugSink, S1FormattedToTheSink) {
    SinkCapture cap{};
    ctrl_debug_bind(capture_sink, &cap);
    const int n = shlan_printf("mrp port %u attr %02x", 3u, 0x2Au);
    EXPECT_TRUE(n == 18 && std::strcmp(cap.text, "mrp port 3 attr 2a") == 0)
        << "S1 shlan_printf reaches the bound sink formatted";
    ctrl_debug_bind(nullptr, nullptr);
}

TEST(DebugSink, S2TruncatedToTheLine) {
    SinkCapture cap{};
    const std::uint32_t before = ctrl_debug_truncated();
    ctrl_debug_bind(capture_sink, &cap);
    char longer[200];
    std::memset(longer, 'x', sizeof longer - 1u);
    longer[sizeof longer - 1u] = '\0';
    const int n = shlan_printf("%s", longer);
    EXPECT_EQ(static_cast<unsigned>(n), CTRL_DEBUG_LINE_BYTES) << "S2 a line over the buffer is truncated to it";
    EXPECT_EQ(cap.len, CTRL_DEBUG_LINE_BYTES) << "S2 and the sink receives that many bytes";
    EXPECT_EQ(cap.calls, 1u) << "S2 in one call";
    EXPECT_EQ(ctrl_debug_truncated() - before, 1u) << "S2 the truncation is counted";
    ctrl_debug_bind(nullptr, nullptr);
}

// ---- D: the driver on the model -------------------------------------------

void build_frame(std::uint8_t* f, std::size_t len, std::uint16_t ethertype, std::uint8_t sub, std::uint8_t msg) {
    std::memset(f, 0, len);
    wire_put_be(f, 0x91E0F0010000ull, 6);
    wire_put_be(f + 6, 0x001122334455ull, 6);
    wire_put_be(f + 12, ethertype, 2);
    f[14] = sub;
    f[15] = msg;
    for (std::size_t k = 26; k < len; ++k) {
        f[k] = static_cast<std::uint8_t>(k * 7u);
    }
}

// The ring word the model's RX tail points at on the ADP channel.
std::uint32_t& adp_rx_tail_word() {
    const std::uint32_t at = MBX_CH_ADP_RX_BASE + 4u * (model.ch[MBX_CH_ADP].rx_tail & (MBX_CH_ADP_RX_WORDS - 1u));
    return model.window[at / 4u];
}

using Driver = Model;

TEST_F(Driver, D0RxRecordByteForByte) {
    static mbx_frame got;
    std::uint8_t f[82];
    build_frame(f, sizeof f, 0x22F0, 0xFA, 2);
    EXPECT_TRUE(mbx_open()) << "D0 mbx_open accepts the model's contract";
    mbx_filter_set_own_eid(0x1122334455667788ull);
    mbx_filter_open(1u << MBX_CH_ADP);
    mbx_model_advance_ms(&model, 9);
    EXPECT_TRUE(mbx_model_rx(&model, f, sizeof f, 0)) << "D0 the model commits a DISCOVER";
    EXPECT_EQ(mbx_rx_take(MBX_CH_ADP, &got), MBX_STATUS_OK) << "D0 mbx_rx_take returns it";
    EXPECT_TRUE(got.len == sizeof f && std::memcmp(got.bytes, f, sizeof f) == 0 && got.interface == 0u &&
                got.arrival_ms == 9u)
        << "D0 byte for byte, with its length, interface and arrival";
    EXPECT_EQ(model.ch[MBX_CH_ADP].rx_tail, model.ch[MBX_CH_ADP].rx_head) << "D0 the release moved RX_TAIL to RX_HEAD";
    EXPECT_EQ(mbx_rx_take(MBX_CH_ADP, &got), MBX_STATUS_EMPTY) << "D0 an empty ring";
}

TEST_F(Driver, D1MalformedRecordResynchronises) {
    static mbx_frame got;
    std::uint8_t f[82];
    build_frame(f, sizeof f, 0x22F0, 0xFA, 2);
    ASSERT_TRUE(mbx_open());
    mbx_filter_set_own_eid(0x1122334455667788ull);
    mbx_filter_open(1u << MBX_CH_ADP);
    ASSERT_TRUE(mbx_model_rx(&model, f, sizeof f, 0));
    ASSERT_TRUE(mbx_model_rx(&model, f, sizeof f, 0));
    adp_rx_tail_word() ^= 1u << MBX_RXREC_W0_KIND_LSB;
    EXPECT_EQ(mbx_rx_take(MBX_CH_ADP, &got), MBX_STATUS_BAD) << "D1 a record with the wrong KIND is refused";
    EXPECT_EQ(model.ch[MBX_CH_ADP].rx_tail, model.ch[MBX_CH_ADP].rx_head)
        << "D1 and the ring is resynchronised to RX_HEAD, the next record included";
    EXPECT_EQ(mbx_rx_take(MBX_N_CH, &got), MBX_STATUS_BAD) << "D1 bad channel";
}

TEST_F(Driver, D2TxRecordAndRefusals) {
    std::uint8_t f[82];
    build_frame(f, sizeof f, 0x22F0, 0xFA, 0);
    ASSERT_TRUE(mbx_open());
    EXPECT_EQ(mbx_tx_send(MBX_CH_ADP, 0, f, sizeof f), MBX_STATUS_OK) << "D2 a frame becomes a TX record";
    const mbx_model_tx* sent = mbx_model_tx_frame(&model, 0);
    EXPECT_TRUE(sent != nullptr && sent->len == sizeof f && std::memcmp(sent->bytes, f, sizeof f) == 0 &&
                sent->channel == MBX_CH_ADP)
        << "D2 and leaves the merge byte for byte";
    EXPECT_EQ(mbx_tx_send(MBX_CH_ADP, 0, f, 13u), MBX_STATUS_BAD) << "D2 a 13-byte frame is refused";
    EXPECT_EQ(mbx_tx_send(MBX_CH_ADP, 0, f, MBX_CH_ADP_MAX_FRAME_BYTES + 2u), MBX_STATUS_BAD)
        << "D2 a frame over max_frame_bytes is refused";
    EXPECT_EQ(mbx_tx_send(MBX_CH_ADP, MBX_N_IF, f, sizeof f), MBX_STATUS_BAD) << "D2 an unknown interface is refused";
}

TEST_F(Driver, D3HeldMergeFillsAndOrderAcrossChannels) {
    std::uint8_t f[82];
    build_frame(f, sizeof f, 0x22F0, 0xFA, 0);
    ASSERT_TRUE(mbx_open());
    mbx_model_tx_pause(&model, true);
    unsigned taken = 0;
    while (mbx_tx_send(MBX_CH_ADP, 0, f, sizeof f) == MBX_STATUS_OK) {
        taken++;
    }
    EXPECT_EQ(taken, MBX_CH_ADP_TX_WORDS / (MBX_TX_HDR_WORDS + (sizeof f + 3u) / 4u))
        << "D3 a held merge fills the ring to its last whole record";
    mbx_model_tx_pause(&model, false);
    EXPECT_EQ(model.tx_sent, taken) << "D3 once drained every record leaves";
    EXPECT_EQ(model.ch[MBX_CH_ADP].tx_err, 0u) << "D3 and none was refused";
    std::uint8_t acmp[70];
    std::uint8_t aecp[64];
    build_frame(acmp, sizeof acmp, 0x22F0, 0xFC, 1);
    build_frame(aecp, sizeof aecp, 0x22F0, 0xFB, 1);
    const std::uint32_t first = model.tx_sent;
    mbx_model_tx_pause(&model, true);
    static_cast<void>(mbx_tx_send(MBX_CH_ACMP, 0, acmp, sizeof acmp));
    static_cast<void>(mbx_tx_send(MBX_CH_ACMP, 0, acmp, sizeof acmp));
    static_cast<void>(mbx_tx_send(MBX_CH_AECP, 0, aecp, sizeof aecp));
    mbx_model_tx_pause(&model, false);
    const mbx_model_tx* t0 = mbx_model_tx_frame(&model, first);
    const mbx_model_tx* t1 = mbx_model_tx_frame(&model, first + 1u);
    const mbx_model_tx* t2 = mbx_model_tx_frame(&model, first + 2u);
    EXPECT_TRUE(t0 != nullptr && t1 != nullptr && t2 != nullptr && t0->channel == MBX_CH_ACMP &&
                t1->channel == MBX_CH_ACMP && t2->channel == MBX_CH_AECP)
        << "D3 ACMP, ACMP, AECP committed by the driver behind a held merge leave in that order";
}

TEST_F(Driver, D4EveryEventTypeDecoded) {
    mbx_event ev;
    ASSERT_TRUE(mbx_open());
    mbx_model_advance_ms(&model, 4);
    mbx_model_set_link(&model, 0, true);
    EXPECT_TRUE(mbx_event_take(&ev) && ev.type == MBX_EV_TYPE_LINK && ev.link_up && ev.now_ms == 4u)
        << "D4 a LINK event";
    mbx_model_gm_change(&model, 0, 0xA1A2A3A4A5A6A7A8ull, 5);
    EXPECT_TRUE(mbx_event_take(&ev) && ev.type == MBX_EV_TYPE_GM && ev.gm_id == 0xA1A2A3A4A5A6A7A8ull &&
                ev.domain == 5u)
        << "D4 a GM event with the identity and domain";
    mbx_timer_arm(7, 0xBEEF, mbx_now_ms() + 3u);
    mbx_model_advance_ms(&model, 3);
    EXPECT_TRUE(mbx_event_take(&ev) && ev.type == MBX_EV_TYPE_TIMER && ev.timer_slot == 7u && ev.timer_tag == 0xBEEFu &&
                ev.deadline_ms == 7u)
        << "D4 a TIMER event with slot, tag and deadline";
    mbx_timer_arm(8, 1, mbx_now_ms() + 2u);
    mbx_timer_cancel(8);
    mbx_model_advance_ms(&model, 5);
    EXPECT_FALSE(mbx_event_take(&ev)) << "D4 a cancelled timer posts nothing";
    mbx_tick_enable(true);
    mbx_model_advance_ms(&model, 3u * MBX_TICK_MS);
    unsigned ticks = 0;
    while (mbx_event_take(&ev)) {
        ticks += ev.type == MBX_EV_TYPE_TICK ? ev.tick_count : 0u;
    }
    EXPECT_EQ(ticks, 3u) << "D4 TICK events count the centiseconds";
}

TEST_F(Driver, D5CoherentGrandmasterRead) {
    ASSERT_TRUE(mbx_open());
    mbx_model_set_gm(&model, 0, 0x0102030405060708ull, 9);
    std::uint8_t dom = 0;
    EXPECT_TRUE(mbx_gm_id(0, &dom) == 0x0102030405060708ull && dom == 9u) << "D5 the grandmaster read is coherent";
}

// ---- L: the event loop -----------------------------------------------------

struct LoopProbe {
    unsigned rx;
    unsigned events;
    unsigned polls;
    unsigned ticks_a;
    unsigned ticks_b;
    std::uint32_t order;  // the tick consumers' call order, two bits per call
    unsigned calls;
    bool owing;  // what the probe's poll reports
};

LoopProbe probe;

void probe_rx(void*, const mbx_frame*) {
    probe.rx++;
}
void probe_event(void*, const mbx_event*) {
    probe.events++;
}

bool probe_poll(void*) {
    probe.polls++;
    return probe.owing;
}

void tick_a() {
    probe.ticks_a++;
    probe.order |= 1u << (2u * (probe.calls++ % 16u));
}

void tick_b() {
    probe.ticks_b++;
    probe.order |= 2u << (2u * (probe.calls++ % 16u));
}

struct OpenOrder {
    int own_eid_hi_at;
    int filter_en_at;
    int tick_ctl_at;
    std::uint32_t tick_ctl;
    std::uint32_t filter_en;
    int n;
};

OpenOrder order;

void trace_open(void*, bool write, std::uint32_t off, std::uint32_t value) {
    order.n++;
    if (!write) {
        return;
    }
    if (off == MBX_REG_OWN_EID_HI) {
        order.own_eid_hi_at = order.n;
    } else if (off == MBX_REG_FILTER_EN) {
        if (order.filter_en_at == 0 && value != 0u) {
            order.filter_en_at = order.n;
        }
        order.filter_en = value;
    } else if (off == MBX_REG_TICK_CTL) {
        order.tick_ctl_at = order.n;
        order.tick_ctl = value;
    }
}

bool bind_probe(ctrl_loop* l) {
    return ctrl_loop_bind_rx(l, MBX_CH_ADP, probe_rx, nullptr) && ctrl_loop_add_sink(l, probe_event, nullptr) &&
           ctrl_loop_add_poll(l, probe_poll, nullptr) && ctrl_loop_add_tick(l, tick_a) && ctrl_loop_add_tick(l, tick_b);
}

void drain(ctrl_loop* l) {
    for (unsigned passes = 0; passes < 1000u && ctrl_loop_service(l) != 0u; ++passes) {}
}

// Every event ring record taken by a timer expiring now: the ring full.
void fill_event_ring(std::uint16_t tag) {
    for (unsigned s = 0; s < MBX_EVT_WORDS / MBX_EV_WORDS; ++s) {
        mbx_timer_arm(s % MBX_N_TIMERS, tag, mbx_now_ms());
    }
}

// Binding and opening, from a reset model.
using LoopBring = Model;

// The probe bound into an opened loop, as L0 and L1 leave it.
class Loop : public Model {
 protected:
    void SetUp() override {
        Model::SetUp();
        probe = LoopProbe{};
        ctrl_loop_init(&loop_);
        ASSERT_TRUE(bind_probe(&loop_));
        ASSERT_TRUE(ctrl_loop_open(&loop_, 0));
    }
    ctrl_loop loop_;
};

TEST_F(LoopBring, L0BindingsFitTheirTables) {
    static ctrl_loop loop;
    probe = LoopProbe{};
    ctrl_loop_init(&loop);
    EXPECT_TRUE(bind_probe(&loop)) << "L0 bindings fit their tables";
    EXPECT_FALSE(ctrl_loop_bind_rx(&loop, MBX_N_CH, probe_rx, nullptr)) << "L0 an unknown channel cannot be bound";
}

TEST_F(LoopBring, L1OpenOrder) {
    static ctrl_loop loop;
    probe = LoopProbe{};
    order = OpenOrder{};
    ctrl_loop_init(&loop);
    ASSERT_TRUE(bind_probe(&loop));
    mbx_host_trace(trace_open, nullptr);
    EXPECT_TRUE(ctrl_loop_open(&loop, 0)) << "L1 ctrl_loop_open brings the mailbox up";
    mbx_host_trace(nullptr, nullptr);
    EXPECT_TRUE(order.own_eid_hi_at > 0 && order.own_eid_hi_at < order.filter_en_at)
        << "L1 OWN_EID is written before any channel opens";
    EXPECT_EQ(order.filter_en, 1u << MBX_CH_ADP) << "L1 only the bound channel opens";
    EXPECT_EQ(order.tick_ctl, 1u) << "L1 the tick starts because a centisecond consumer is bound";
    EXPECT_EQ(model.irq_enable, (1u << MBX_CH_ADP) | (1u << MBX_IRQ_ENABLE_EVT_LSB))
        << "L1 IRQ_ENABLE holds the bound channel and the event ring";
}

TEST_F(Loop, L2PerPassRxBound) {
    std::uint8_t f[82];
    build_frame(f, sizeof f, 0x22F0, 0xFA, 2);
    for (unsigned k = 0; k < 5u; ++k) {
        static_cast<void>(mbx_model_rx(&model, f, sizeof f, 0));
    }
    static_cast<void>(ctrl_loop_service(&loop_));
    EXPECT_EQ(probe.rx, CTRL_LOOP_RX_PER_PASS) << "L2 a pass takes at most CTRL_LOOP_RX_PER_PASS records of a channel";
    EXPECT_EQ(probe.polls, 1u) << "L2 and polls every module once";
    drain(&loop_);
    EXPECT_EQ(probe.rx, 5u) << "L2 the rest follow in later passes";
}

TEST_F(Loop, L3PerPassEventBound) {
    for (unsigned s = 0; s < 12u; ++s) {
        mbx_timer_arm(s, static_cast<std::uint16_t>(s), mbx_now_ms());
    }
    mbx_model_advance_ms(&model, 0);
    static_cast<void>(ctrl_loop_service(&loop_));
    EXPECT_EQ(probe.events, CTRL_LOOP_EVENTS_PER_PASS) << "L3 a pass takes at most CTRL_LOOP_EVENTS_PER_PASS events";
    drain(&loop_);
    EXPECT_EQ(probe.events, 12u) << "L3 the rest follow in the next pass";
}

TEST_F(Loop, L4TickFanOut) {
    fill_event_ring(0x200u);
    mbx_model_advance_ms(&model, 3u * MBX_TICK_MS);
    EXPECT_EQ(model.tick_count, 3u) << "L4 (a late firmware: the ring is full while three ticks pass)";
    drain(&loop_);
    EXPECT_EQ(probe.ticks_a, 3u) << "L4 every centisecond reaches the first consumer";
    EXPECT_EQ(probe.ticks_b, 3u) << "L4 and the second";
    EXPECT_EQ(probe.order, 0x999u) << "L4 in registration order, tick by tick (a b a b a b)";
}

TEST_F(Loop, L5MalformedRecordCounted) {
    std::uint8_t f[82];
    build_frame(f, sizeof f, 0x22F0, 0xFA, 2);
    static_cast<void>(mbx_model_rx(&model, f, sizeof f, 0));
    adp_rx_tail_word() = 0;
    const unsigned rx_before = probe.rx;
    static_cast<void>(ctrl_loop_service(&loop_));
    EXPECT_EQ(loop_.stats.rx_bad, 1u) << "L5 a malformed record is counted, not handed out";
    EXPECT_EQ(probe.rx, rx_before) << "L5 and no handler saw it";
}

TEST_F(Loop, L6OwedOutputKeepsPassing) {
    drain(&loop_);
    probe.owing = true;
    EXPECT_NE(ctrl_loop_service(&loop_), 0u)
        << "L6 a pass after which a module still owes output asks for the next pass at once";
    probe.owing = false;
    EXPECT_EQ(ctrl_loop_service(&loop_), 0u) << "L6 a pass that handled nothing and owes nothing lets the loop sleep";
}

// A late core: the event ring full while 40 centiseconds pass, which the
// fabric coalesces into one TICK record.
TEST_F(Loop, L7TickSlices) {
    fill_event_ring(0x300u);
    mbx_model_advance_ms(&model, 40u * MBX_TICK_MS);
    probe.ticks_a = 0;
    unsigned most = 0;
    bool slept_owing = false;
    for (unsigned passes = 0; passes < 16u; ++passes) {
        const unsigned before = probe.ticks_a;
        const unsigned work = ctrl_loop_service(&loop_);
        const unsigned slice = probe.ticks_a - before;
        most = slice > most ? slice : most;
        if (work == 0u) {
            slept_owing = loop_.ticks_owed != 0u;
            break;
        }
    }
    EXPECT_EQ(probe.ticks_a, 40u) << "L7 every one of 40 coalesced centiseconds reaches the consumer";
    EXPECT_EQ(most, CTRL_LOOP_TICKS_PER_PASS) << "L7 at most CTRL_LOOP_TICKS_PER_PASS of them per pass";
    EXPECT_TRUE(!slept_owing && loop_.ticks_owed == 0u) << "L7 and the loop keeps passing until the last is dispatched";
}

// A TICK record taken while centiseconds are still carried: 40 coalesced
// behind a full ring, then one more centisecond posted as a second record
// once the first is taken and part of its 40 still waits.
TEST_F(Loop, L8TickRecordWhileCarried) {
    fill_event_ring(0x400u);
    mbx_model_advance_ms(&model, 40u * MBX_TICK_MS);
    probe.ticks_a = 0;
    for (unsigned passes = 0; passes < 16u && loop_.ticks_owed == 0u; ++passes) {
        static_cast<void>(ctrl_loop_service(&loop_));
    }
    const std::uint32_t carried = loop_.ticks_owed;
    mbx_model_advance_ms(&model, MBX_TICK_MS);
    EXPECT_TRUE(carried > 0u && probe.ticks_a + carried == 40u &&
                static_cast<std::uint16_t>(model.evt_head - model.evt_tail) == MBX_EV_WORDS)
        << "L8 (centiseconds are carried when the second TICK record is posted, alone in the ring)";
    for (unsigned passes = 0; passes < 16u && ctrl_loop_service(&loop_) != 0u; ++passes) {}
    EXPECT_EQ(probe.ticks_a, 41u)
        << "L8 a TICK record taken while centiseconds are carried adds to them: all 41 reach the consumer";
    EXPECT_EQ(loop_.ticks_owed, 0u) << "L8 and none is left owed";
}

}  // namespace
