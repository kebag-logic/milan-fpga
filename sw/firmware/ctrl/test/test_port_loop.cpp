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
//       event type decoded, timers, the coherent grandmaster read, the own
//       MAC the filter matches and the FILTER_MISMATCH it counts (lane FC);
//   L   the event loop: the order ctrl_loop_open brings the mailbox up in,
//       the per-pass bounds, the TICK fan-out to centisecond consumers, and
//       THE STEP: its client last in every pass that takes no input, given
//       the deadline read as the pass starts, and its age limit, counted in
//       the centiseconds a dispatch carries.
//
// One test per labelled step; each assertion carries the check's name from
// the hand-rolled suite it replaces (README.md, "The port").

#include <gtest/gtest.h>

#include <cstddef>
#include <cstdint>
#include <cstring>
#include <cwchar>
#include <functional>
#include <string>

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

// Each interface's own unicast MAC as ctrl_loop_open takes them, one apart,
// so a write into another interface's block shows (#665 lane FC).
struct OwnMacs {
    std::uint64_t mac[MBX_N_IF];
    OwnMacs() {
        for (unsigned i = 0; i < MBX_N_IF; ++i) {
            mac[i] = 0x001B92112200ull + i;
        }
    }
};
const OwnMacs kOwn;

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

// The refusals P0 does not reach: no class, too many classes, a class of
// zero-byte blocks, and no arena at all (#665 FT, coverage).
TEST(Pool, P5ClassTablesAndArenasRefused) {
    ctrl_pool pool;
    const ctrl_pool_class zero_bytes[] = {{0u, 4u}};
    ctrl_pool_class many[CTRL_POOL_MAX_CLASSES + 1u];
    for (unsigned k = 0; k < CTRL_POOL_MAX_CLASSES + 1u; ++k) {
        many[k] = ctrl_pool_class{static_cast<std::uint16_t>(16u * (k + 1u)), 1u};
    }
    EXPECT_FALSE(ctrl_pool_init(&pool, arena, sizeof arena, classes, 0)) << "P5 a pool of no class is refused";
    EXPECT_FALSE(ctrl_pool_init(&pool, arena, sizeof arena, many, CTRL_POOL_MAX_CLASSES + 1u))
        << "P5 more classes than CTRL_POOL_MAX_CLASSES are refused";
    EXPECT_FALSE(ctrl_pool_init(&pool, arena, sizeof arena, zero_bytes, 1)) << "P5 a class of zero-byte blocks is refused";
    EXPECT_FALSE(ctrl_pool_init(&pool, nullptr, sizeof arena, classes, 2)) << "P5 no arena is refused";
    EXPECT_EQ(pool.n_bins, 0u) << "P5 and a refused pool carves nothing";
}

// calloc of nothing is refused as malloc of nothing is, and calloc on an
// exhausted pool returns NULL without touching memory (#665 FT, coverage).
TEST(Pool, P6CallocOfNothingAndOnAnExhaustedPool) {
    FullPool f;
    ASSERT_NO_FATAL_FAILURE(fill(f));
    const std::uint32_t refused = f.pool.refused;
    EXPECT_EQ(ctrl_pool_calloc(&f.pool, 0u, 8u), nullptr) << "P6 calloc of zero members is refused";
    EXPECT_EQ(ctrl_pool_calloc(&f.pool, 1u, 8u), nullptr) << "P6 calloc on an exhausted pool returns NULL";
    EXPECT_EQ(f.pool.refused - refused, 2u) << "P6 and both refusals are counted";
}

// A pointer below every class is no block of the pool's (#665 FT, coverage).
TEST(Pool, P7FreeBelowTheArenaRefused) {
    ctrl_pool pool;
    ASSERT_TRUE(ctrl_pool_init(&pool, arena + 64, sizeof arena - 64u, classes, 2));
    ctrl_pool_free(&pool, arena);
    EXPECT_EQ(pool.bad_frees, 1u) << "P7 a free below the first class is refused and counted";
    EXPECT_EQ(ctrl_pool_in_use(&pool), 0u) << "P7 and no block changes hands";
}

// The port layer before a pool is bound, and what it reports bound
// (#665 FT, coverage).
TEST(Pool, P8PortLayerUnbound) {
    ctrl_pool pool;
    ASSERT_TRUE(ctrl_pool_init(&pool, arena, sizeof arena, classes, 2));
    shlan_port_bind_pool(nullptr);
    EXPECT_EQ(shlan_port_pool(), nullptr) << "P8 no pool is reported before the bind";
    EXPECT_EQ(shlan_calloc(2u, 8u), nullptr) << "P8 shlan_calloc before the pool is bound refuses";
    shlan_free(arena);
    EXPECT_EQ(pool.bad_frees, 0u) << "P8 shlan_free before the bind touches no pool";
    shlan_port_bind_pool(&pool);
    EXPECT_EQ(shlan_port_pool(), &pool) << "P8 the bound pool is the one reported";
    shlan_port_bind_pool(nullptr);
}

// A class whose stride is a power of two finds a block's index by a shift,
// any other by a divide (#665): both take, release and refuse alike, and
// each block's used flag is its own.
TEST(Pool, P9BlockIndexByShiftAndByDivide) {
    for (const ctrl_pool_class c : {ctrl_pool_class{48u, 3u}, ctrl_pool_class{64u, 3u}}) {
        ctrl_pool pool;
        ASSERT_TRUE(ctrl_pool_init(&pool, arena, sizeof arena, &c, 1));
        const ctrl_pool_bin& bin = pool.bins[0];
        void* block[3];
        for (auto& b : block) {
            b = ctrl_pool_alloc(&pool, 40u);
            ASSERT_NE(b, nullptr);
        }
        for (unsigned k = 0; k < 3u; ++k) {
            EXPECT_EQ(bin.used[k], 1u) << "P9 every taken block's flag is set, stride " << bin.stride;
        }
        ctrl_pool_free(&pool, bytes_of(block[1]) + 8);
        EXPECT_EQ(pool.bad_frees, 1u) << "P9 a free into the middle of a block is refused, stride " << bin.stride;
        ctrl_pool_free(&pool, block[1]);
        EXPECT_EQ(bin.used[0] + 2u * bin.used[1] + 4u * bin.used[2], 5u)
            << "P9 a free clears its own block's flag alone, stride " << bin.stride;
        ctrl_pool_free(&pool, block[1]);
        EXPECT_EQ(pool.bad_frees, 2u) << "P9 a double free is refused, stride " << bin.stride;
        EXPECT_EQ(ctrl_pool_alloc(&pool, 40u), block[1]) << "P9 the released block is handed out next, stride " << bin.stride;
        EXPECT_EQ(ctrl_pool_in_use(&pool), 3u) << "P9 every block is in use again, stride " << bin.stride;
    }
}

// A free block's first bytes hold the free list, so a client that writes
// into a block after freeing it can leave a class counting free blocks
// behind a list that has ended. That class is exhausted, not followed: the
// next class that fits serves, and with none left the allocation is refused
// and counted (#665 FT, R506-1-F1).
TEST(Pool, P9AFreeListShorterThanItsCountIsExhausted) {
    ctrl_pool pool;
    ASSERT_TRUE(ctrl_pool_init(&pool, arena, sizeof arena, classes, 2));
    void* a = ctrl_pool_alloc(&pool, 24u);
    void* b = ctrl_pool_alloc(&pool, 24u);
    ASSERT_TRUE(in_bin(pool, 0, a) && in_bin(pool, 0, b));
    ctrl_pool_free(&pool, a);
    ctrl_pool_free(&pool, b);
    void* const end = nullptr;
    std::memcpy(b, &end, sizeof end);  // the client's write into b, which heads the list
    EXPECT_EQ(ctrl_pool_alloc(&pool, 24u), b) << "P9 the head of the cut list is still handed out";
    EXPECT_EQ(pool.bins[0].free_count, 3u) << "P9 leaving the small class counting three free blocks and no list";
    const std::uint32_t refused = pool.refused;
    void* spill = ctrl_pool_alloc(&pool, 24u);
    void* last = ctrl_pool_alloc(&pool, 24u);
    EXPECT_TRUE(in_bin(pool, 1, spill) && in_bin(pool, 1, last))
        << "P9 a class whose list ends before its count is exhausted, not followed: the next class serves";
    EXPECT_EQ(ctrl_pool_alloc(&pool, 24u), nullptr) << "P9 then with no fitting class left the allocation is refused";
    EXPECT_EQ(pool.refused - refused, 1u) << "P9 and counted";
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

// A print the formatter cannot encode (a wide character the C locale has no
// byte for) reaches no sink and is counted as discarded (#665 FT, coverage).
TEST(DebugSink, S3UnencodablePrintDiscarded) {
    SinkCapture cap{};
    const std::uint32_t before = ctrl_debug_discarded();
    ctrl_debug_bind(capture_sink, &cap);
    const int n = shlan_printf("%lc", static_cast<wint_t>(0x10FFFFu));
    EXPECT_LT(n, 0) << "S3 an encoding failure is returned as the formatter's negative value";
    EXPECT_EQ(cap.calls, 0u) << "S3 and the sink receives nothing";
    EXPECT_EQ(ctrl_debug_discarded() - before, 1u) << "S3 the discard is counted";
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

// The own MAC the driver writes is the destination the model's AECP tuple
// takes on that interface, and FILTER_MISMATCH reads what the model counted
// (#665 lane FC).
TEST_F(Driver, D12OwnMacAndMismatchOnTheModel) {
    static mbx_frame got;
    std::uint8_t f[64];
    build_frame(f, sizeof f, 0x22F0, 0xFB, 0);
    wire_put_be(f, kOwn.mac[0], 6);
    wire_put_be(f + 18, 0x1122334455667788ull, 8);
    ASSERT_TRUE(mbx_open());
    mbx_filter_set_own_eid(0x1122334455667788ull);
    EXPECT_TRUE(mbx_filter_set_own_mac(0, kOwn.mac[0])) << "D12 interface 0's own MAC is written";
    mbx_filter_open(1u << MBX_CH_AECP);
    EXPECT_TRUE(mbx_model_rx(&model, f, sizeof f, 0)) << "D12 an AEM_COMMAND to it on interface 0 passes";
    EXPECT_EQ(mbx_rx_take(MBX_CH_AECP, &got), MBX_STATUS_OK) << "D12 and is taken";
    EXPECT_EQ(mbx_filter_mismatch(), 0u) << "D12 a frame that passes is no mismatch";
    wire_put_be(f, kOwn.mac[0] ^ 0x010000000000ull, 6);
    EXPECT_FALSE(mbx_model_rx(&model, f, sizeof f, 0)) << "D12 to another unicast MAC it does not";
    EXPECT_EQ(mbx_filter_mismatch(), 1u) << "D12 FILTER_MISMATCH reads the one tuple failure";
}

// ---- L: the event loop -----------------------------------------------------

struct LoopProbe {
    unsigned rx;
    unsigned rx_acmp;          // the records of ACMP's channel, where a test binds it
    unsigned events;
    unsigned polls;
    unsigned ticks_a;
    unsigned ticks_b;
    std::uint32_t order;  // the tick consumers' call order, two bits per call
    unsigned calls;
    bool owing;  // what the probe's poll reports
    std::uint32_t now;       // the step's clock, in microseconds
    std::uint32_t now_step;  // what each read of it advances it by
    unsigned clock_reads;
    std::uint32_t poll_us;   // the time each poll takes on that clock
    unsigned steps;
    unsigned polls_at_step;  // the polls run when the step was last called
    std::uint32_t deadline;  // the deadline the step was last given
    bool step_owing;         // what the probe's step reports
    unsigned retries;          // THE RETRY's client calls
    unsigned round_left;       // what the last round was given of its pass, in microseconds
    unsigned polls_at_retry;   // the polls run when the retry was last called
    unsigned steps_at_retry;   // the steps run when the retry was last called
    bool retry_owing;          // what the probe's retry reports
    bool retry_aged;           // what the probe's retry age reports
    unsigned aged_reads;       // THE RETRY's age reads
    unsigned rx_at_aged;       // the records taken when the age was last read
    unsigned transmits;        // THE TRANSMIT's client calls
    unsigned polls_at_transmit;  // the polls run when the transmit was last called
    bool transmit_aged;        // what the probe's transmit age reports
    unsigned transmit_aged_reads;  // THE TRANSMIT's age reads
    unsigned rx_at_transmit_aged;  // the records taken when its age was last read
    std::string order_of;      // the deferrable clients in call order: T transmit, R retry, S step
    std::function<void()> on_event;   // what the next event's sink does besides counting it
};

LoopProbe probe;

void probe_rx(void*, const mbx_frame*) {
    probe.rx++;
}
void probe_event(void*, const mbx_event*) {
    probe.events++;
    if (probe.on_event) {
        probe.on_event();
    }
}

bool probe_poll(void*) {
    probe.polls++;
    probe.now += probe.poll_us;
    return probe.owing;
}

std::uint32_t probe_clock(void*) {
    probe.clock_reads++;
    probe.now += probe.now_step;
    return probe.now;
}

bool probe_step(void*, std::uint32_t deadline) {
    probe.steps++;
    probe.polls_at_step = probe.polls;
    probe.deadline = deadline;
    probe.order_of += 'S';
    return probe.step_owing;
}

void probe_rx_acmp(void*, const mbx_frame*) {
    probe.rx_acmp++;
}

bool probe_retry(void*, unsigned left_us) {
    probe.round_left = left_us;
    probe.retries++;
    probe.polls_at_retry = probe.polls;
    probe.steps_at_retry = probe.steps;
    probe.now += probe.poll_us;
    probe.order_of += 'R';
    return probe.retry_owing;
}

bool probe_retry_aged(void*) {
    probe.aged_reads++;
    probe.rx_at_aged = probe.rx;
    return probe.retry_aged;
}

void probe_transmit(void*) {
    probe.transmits++;
    probe.polls_at_transmit = probe.polls;
    probe.now += probe.poll_us;
    probe.order_of += 'T';
}

bool probe_transmit_aged(void*) {
    probe.transmit_aged_reads++;
    probe.rx_at_transmit_aged = probe.rx;
    return probe.transmit_aged;
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
    int own_mac_at;     // the last OWN_MAC_LO/HI write of any interface
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
    } else if (off >= MBX_IFF_BASE && off < MBX_IFF_BASE + MBX_IFF_STRIDE * MBX_N_IF) {
        order.own_mac_at = order.n;
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
        ASSERT_TRUE(ctrl_loop_open(&loop_, 0, kOwn.mac));
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
    EXPECT_TRUE(ctrl_loop_open(&loop, 0, kOwn.mac)) << "L1 ctrl_loop_open brings the mailbox up";
    mbx_host_trace(nullptr, nullptr);
    EXPECT_TRUE(order.own_eid_hi_at > 0 && order.own_eid_hi_at < order.filter_en_at)
        << "L1 OWN_EID is written before any channel opens";
    EXPECT_TRUE(order.own_mac_at > 0 && order.own_mac_at < order.filter_en_at)
        << "L1 every interface's OWN_MAC is written before any channel opens";
    bool macs = true;
    for (unsigned i = 0; i < MBX_N_IF; ++i) {
        macs = macs && model.own_mac[i] == kOwn.mac[i];
    }
    EXPECT_TRUE(macs) << "L1 each interface's OWN_MAC holds the MAC given for it";
    EXPECT_EQ(order.filter_en, 1u << MBX_CH_ADP) << "L1 only the bound channel opens";
    EXPECT_EQ(order.tick_ctl, 1u) << "L1 the tick starts because a centisecond consumer is bound";
    EXPECT_EQ(model.irq_enable, (1u << MBX_CH_ADP) | (1u << MBX_IRQ_ENABLE_EVT_LSB))
        << "L1 IRQ_ENABLE holds the bound channel and the event ring";
}

// Every table of the loop refuses a binding with no function and one past
// its size, and keeps what it had (#665 FT, coverage).
TEST_F(LoopBring, L9TablesRefuseNullAndOverflow) {
    static ctrl_loop loop;
    ctrl_loop_init(&loop);
    EXPECT_FALSE(ctrl_loop_bind_rx(&loop, MBX_CH_ADP, nullptr, nullptr)) << "L9 a channel bound to no function is refused";
    EXPECT_FALSE(ctrl_loop_add_sink(&loop, nullptr, nullptr)) << "L9 a sink with no function is refused";
    EXPECT_FALSE(ctrl_loop_add_tick(&loop, nullptr)) << "L9 a centisecond consumer with no function is refused";
    EXPECT_FALSE(ctrl_loop_add_poll(&loop, nullptr, nullptr)) << "L9 a poll with no function is refused";
    for (unsigned k = 0; k < CTRL_LOOP_MAX_SINKS; ++k) {
        ASSERT_TRUE(ctrl_loop_add_sink(&loop, probe_event, nullptr));
    }
    for (unsigned k = 0; k < CTRL_LOOP_MAX_TICKS; ++k) {
        ASSERT_TRUE(ctrl_loop_add_tick(&loop, tick_a));
    }
    for (unsigned k = 0; k < CTRL_LOOP_MAX_POLLS; ++k) {
        ASSERT_TRUE(ctrl_loop_add_poll(&loop, probe_poll, nullptr));
    }
    EXPECT_FALSE(ctrl_loop_add_sink(&loop, probe_event, nullptr)) << "L9 a sink past CTRL_LOOP_MAX_SINKS is refused";
    EXPECT_FALSE(ctrl_loop_add_tick(&loop, tick_a)) << "L9 a consumer past CTRL_LOOP_MAX_TICKS is refused";
    EXPECT_FALSE(ctrl_loop_add_poll(&loop, probe_poll, nullptr)) << "L9 a poll past CTRL_LOOP_MAX_POLLS is refused";
    EXPECT_TRUE(loop.n_sinks == CTRL_LOOP_MAX_SINKS && loop.n_ticks == CTRL_LOOP_MAX_TICKS &&
                loop.n_polls == CTRL_LOOP_MAX_POLLS)
        << "L9 and the tables keep what they had";
}

// THE STEP's binding: a client or a clock missing is refused, and a second
// client is refused, keeping the first (#665).
TEST_F(LoopBring, L10StepBindingRefusals) {
    static ctrl_loop loop;
    ctrl_loop_init(&loop);
    EXPECT_FALSE(ctrl_loop_set_step(&loop, nullptr, nullptr, probe_clock, nullptr))
        << "L10 a step with no function is refused";
    EXPECT_FALSE(ctrl_loop_set_step(&loop, probe_step, nullptr, nullptr, nullptr))
        << "L10 a step with no clock is refused";
    EXPECT_TRUE(ctrl_loop_set_step(&loop, probe_step, nullptr, probe_clock, nullptr)) << "L10 a step binds";
    EXPECT_FALSE(ctrl_loop_set_step(&loop, probe_step, &loop, probe_clock, nullptr))
        << "L10 a second step is refused";
    EXPECT_TRUE(loop.step == probe_step && loop.step_ctx == nullptr && loop.clock == probe_clock)
        << "L10 and the first stays bound";
}

// THE RETRY's binding: a client with no function or no age is refused, and a
// second client is refused, keeping the first (#665).
TEST_F(LoopBring, L15RetryBindingRefusals) {
    static ctrl_loop loop;
    ctrl_loop_init(&loop);
    EXPECT_FALSE(ctrl_loop_set_retry(&loop, nullptr, probe_retry_aged, nullptr))
        << "L15 a retry client with no function is refused";
    EXPECT_FALSE(ctrl_loop_set_retry(&loop, probe_retry, nullptr, nullptr))
        << "L15 a retry client with no age is refused";
    EXPECT_TRUE(ctrl_loop_set_retry(&loop, probe_retry, probe_retry_aged, nullptr)) << "L15 a retry client binds";
    EXPECT_FALSE(ctrl_loop_set_retry(&loop, probe_retry, probe_retry_aged, &loop))
        << "L15 a second retry client is refused";
    EXPECT_TRUE(loop.retry == probe_retry && loop.retry_aged == probe_retry_aged && loop.retry_ctx == nullptr)
        << "L15 and the first stays bound";
}

// THE TRANSMIT's binding: a client with no function or no age is refused, and
// a second client is refused, keeping the first (#665).
TEST_F(LoopBring, L18TransmitBindingRefusals) {
    static ctrl_loop loop;
    ctrl_loop_init(&loop);
    EXPECT_FALSE(ctrl_loop_set_transmit(&loop, nullptr, probe_transmit_aged, nullptr))
        << "L18 a transmit client with no function is refused";
    EXPECT_FALSE(ctrl_loop_set_transmit(&loop, probe_transmit, nullptr, nullptr))
        << "L18 a transmit client with no age is refused";
    EXPECT_TRUE(ctrl_loop_set_transmit(&loop, probe_transmit, probe_transmit_aged, nullptr))
        << "L18 a transmit client binds";
    EXPECT_FALSE(ctrl_loop_set_transmit(&loop, probe_transmit, probe_transmit_aged, &loop))
        << "L18 a second transmit client is refused";
    EXPECT_TRUE(loop.transmit == probe_transmit && loop.transmit_aged == probe_transmit_aged &&
                loop.transmit_ctx == nullptr)
        << "L18 and the first stays bound";
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

// THE STEP (#665): the client is called once a pass, after every poll, with
// the clock's value at which the pass has spent CTRL_LOOP_SHARE_US, read once
// as the pass starts; a step still owed keeps the loop passing.
TEST_F(Loop, L11StepLastWithTheDeadlineReadAtTheStart) {
    drain(&loop_);
    ASSERT_TRUE(ctrl_loop_set_step(&loop_, probe_step, nullptr, probe_clock, nullptr));
    probe.now = 1000u;
    probe.poll_us = 1500u;
    probe.clock_reads = 0;
    const unsigned polls = probe.polls;
    EXPECT_EQ(ctrl_loop_service(&loop_), 0u) << "L11 a step that owes nothing lets the loop sleep";
    EXPECT_EQ(probe.steps, 1u) << "L11 the step is called once a pass";
    EXPECT_EQ(probe.polls_at_step, polls + 1u) << "L11 after every poll";
    EXPECT_EQ(probe.clock_reads, 1u) << "L11 the clock is read once a pass";
    EXPECT_EQ(probe.deadline, 1000u + CTRL_LOOP_SHARE_US)
        << "L11 the deadline is the share past the clock read as the pass starts";
    probe.step_owing = true;
    EXPECT_NE(ctrl_loop_service(&loop_), 0u) << "L11 a step still owed asks for the next pass at once";
    EXPECT_EQ(probe.deadline, 2500u + CTRL_LOOP_SHARE_US) << "L11 each pass reads its own deadline";
    probe.now = 0xfffffc00u;
    probe.step_owing = false;
    EXPECT_EQ(ctrl_loop_service(&loop_), 0u);
    EXPECT_EQ(probe.deadline, 0xfffffc00u + CTRL_LOOP_SHARE_US) << "L11 the deadline wraps with the clock";
}

// THE STEP waits out a pass that takes an input, a record or an event, and
// the next pass that takes nothing takes it (#665).
TEST_F(Loop, L12StepOnlyInAPassThatTakesNoInput) {
    drain(&loop_);
    ASSERT_TRUE(ctrl_loop_set_step(&loop_, probe_step, nullptr, probe_clock, nullptr));
    std::uint8_t f[82];
    build_frame(f, sizeof f, 0x22F0, 0xFA, 2);
    ASSERT_TRUE(mbx_model_rx(&model, f, sizeof f, 0));
    static_cast<void>(ctrl_loop_service(&loop_));
    EXPECT_EQ(probe.steps, 0u) << "L12 a pass that takes a record does not take the step";
    mbx_timer_arm(0, 0x500u, mbx_now_ms());
    mbx_model_advance_ms(&model, 0);
    static_cast<void>(ctrl_loop_service(&loop_));
    EXPECT_EQ(probe.steps, 0u) << "L12 nor one that takes an event";
    static_cast<void>(ctrl_loop_service(&loop_));
    EXPECT_EQ(probe.steps, 1u) << "L12 the next pass that takes nothing takes it";
}

// THE STEP's age limit (#665): input that leaves no pass empty holds the step
// off until more than CTRL_LOOP_STEP_AGE centiseconds have been dispatched
// since it last ran or owed nothing; the next pass is then the step's alone,
// before any input, and the input it held off is taken by the pass after it.
TEST_F(Loop, L13AnAgedStepIsAPassOfItsOwn) {
    drain(&loop_);
    ASSERT_TRUE(ctrl_loop_set_step(&loop_, probe_step, nullptr, probe_clock, nullptr));
    std::uint8_t f[82];
    build_frame(f, sizeof f, 0x22F0, 0xFA, 2);
    // a centisecond and a record before every pass: no pass takes nothing
    const auto busy_pass = [&]() {
        mbx_model_advance_ms(&model, MBX_TICK_MS);
        EXPECT_TRUE(mbx_model_rx(&model, f, sizeof f, 0));
        static_cast<void>(ctrl_loop_service(&loop_));
    };
    for (unsigned k = 0; k < CTRL_LOOP_STEP_AGE; ++k) {
        busy_pass();
    }
    EXPECT_EQ(probe.steps, 0u) << "L13 a step held off for CTRL_LOOP_STEP_AGE centiseconds still waits";
    busy_pass();
    EXPECT_EQ(probe.steps, 0u) << "L13 the pass that dispatches one more takes its input, not the step";
    ASSERT_TRUE(mbx_model_rx(&model, f, sizeof f, 0));
    mbx_timer_arm(0, 0x600u, mbx_now_ms());
    mbx_model_advance_ms(&model, 0);
    const unsigned rx = probe.rx;
    const unsigned events = probe.events;
    const unsigned polls = probe.polls;
    probe.now = 7000u;
    EXPECT_NE(ctrl_loop_service(&loop_), 0u) << "L13 the step's pass asks for the next pass at once";
    EXPECT_EQ(probe.steps, 1u) << "L13 the next pass takes the step though input waits";
    EXPECT_TRUE(probe.rx == rx && probe.events == events && probe.polls == polls)
        << "L13 and takes nothing else: no event, no record, no poll";
    EXPECT_EQ(probe.deadline, 7000u + CTRL_LOOP_SHARE_US) << "L13 with the deadline read as it starts";
    EXPECT_EQ(loop_.stats.aged_passes, 1u) << "L13 the pass is counted as an aged step's";
    static_cast<void>(ctrl_loop_service(&loop_));
    EXPECT_TRUE(probe.rx == rx + 1u && probe.events == events + 1u)
        << "L13 the next pass takes the input it held off";
    EXPECT_EQ(probe.steps, 1u) << "L13 and the step's age starts again";
    drain(&loop_);
    EXPECT_EQ(probe.steps, 2u) << "L13 (a pass that takes nothing runs the step)";
    for (unsigned k = 0; k < CTRL_LOOP_STEP_AGE; ++k) {
        busy_pass();
    }
    drain(&loop_);
    EXPECT_EQ(probe.steps, 3u) << "L13 (and again, after CTRL_LOOP_STEP_AGE more centiseconds)";
    for (unsigned k = 0; k < CTRL_LOOP_STEP_AGE; ++k) {
        busy_pass();
    }
    EXPECT_EQ(probe.steps, 3u) << "L13 a step run in a pass that takes nothing starts its age again";
    probe.step_owing = true;
    probe.poll_us = CTRL_LOOP_SHARE_US;
    static_cast<void>(ctrl_loop_service(&loop_));
    EXPECT_EQ(probe.steps, 4u) << "L13 (a pass that takes nothing offers the step, which has no room)";
    probe.step_owing = false;
    probe.poll_us = 0u;
    busy_pass();
    EXPECT_EQ(probe.steps, 4u) << "L13 (its input taken)";
    ASSERT_TRUE(mbx_model_rx(&model, f, sizeof f, 0));
    static_cast<void>(ctrl_loop_service(&loop_));
    EXPECT_EQ(probe.steps, 5u) << "L13 a step it had no room for keeps its age";
    EXPECT_EQ(loop_.stats.aged_passes, 2u) << "L13 and is the next pass's alone";
}

// THE STEP's age counts centiseconds, not dispatches (#665): one TICK record
// carries every centisecond the fabric counted while the event ring was held
// (MAILBOX_SPLIT.md), so the pass that dispatches a record of
// CTRL_LOOP_STEP_AGE + 1 centiseconds ages the step past its limit on its own,
// and one of CTRL_LOOP_STEP_AGE does not.
TEST_F(Loop, L14TheAgeCountsCentisecondsNotDispatches) {
    drain(&loop_);
    ASSERT_TRUE(ctrl_loop_set_step(&loop_, probe_step, nullptr, probe_clock, nullptr));
    std::uint8_t f[82];
    build_frame(f, sizeof f, 0x22F0, 0xFA, 2);
    // centiseconds counted while the event ring is held, posted as one TICK record, and a record beside it: one
    // pass takes both, so it takes no step
    const auto coalesced = [&](unsigned centiseconds) {
        mbx_model_evt_pause(&model, true);
        mbx_model_advance_ms(&model, centiseconds * MBX_TICK_MS);
        EXPECT_TRUE(mbx_model_rx(&model, f, sizeof f, 0));
        mbx_model_evt_pause(&model, false);
        const unsigned ticks = loop_.stats.ticks;
        const unsigned events = loop_.stats.events;
        static_cast<void>(ctrl_loop_service(&loop_));
        EXPECT_TRUE(loop_.stats.ticks == ticks + centiseconds && loop_.stats.events == events + 1u)
            << "L14 (one record carries them, and one pass dispatches them)";
    };
    coalesced(CTRL_LOOP_STEP_AGE);
    ASSERT_TRUE(mbx_model_rx(&model, f, sizeof f, 0));
    static_cast<void>(ctrl_loop_service(&loop_));
    EXPECT_EQ(probe.steps, 0u) << "L14 a dispatch of CTRL_LOOP_STEP_AGE centiseconds leaves the next pass its input";
    drain(&loop_);
    const unsigned steps = probe.steps;  // a pass that took nothing ran the step: its age starts again
    coalesced(CTRL_LOOP_STEP_AGE + 1u);
    ASSERT_TRUE(mbx_model_rx(&model, f, sizeof f, 0));
    const unsigned rx = probe.rx;
    static_cast<void>(ctrl_loop_service(&loop_));
    EXPECT_TRUE(probe.steps == steps + 1u && probe.rx == rx)
        << "L14 one dispatch of CTRL_LOOP_STEP_AGE + 1 centiseconds makes the next pass the step's alone";
    EXPECT_EQ(loop_.stats.aged_passes, 1u) << "L14 counted as an aged step's";
}

// THE RETRY (#665): the client is called only in a pass that took no input,
// no event and no record, and dispatched no centisecond, after its polls and
// before THE STEP, or after the step in the pass given whole to an aged step;
// a retry still owed keeps the loop passing.
TEST_F(Loop, L16TheRetryOnlyInAPassThatTakesNothing) {
    drain(&loop_);
    ASSERT_TRUE(ctrl_loop_set_retry(&loop_, probe_retry, probe_retry_aged, nullptr));
    std::uint8_t f[82];
    build_frame(f, sizeof f, 0x22F0, 0xFA, 2);
    ASSERT_TRUE(mbx_model_rx(&model, f, sizeof f, 0));
    static_cast<void>(ctrl_loop_service(&loop_));
    EXPECT_EQ(probe.retries, 0u) << "L16 a pass that takes a record does not call the retry";
    mbx_timer_arm(0, 0x700u, mbx_now_ms());
    mbx_model_advance_ms(&model, 0);
    static_cast<void>(ctrl_loop_service(&loop_));
    EXPECT_EQ(probe.retries, 0u) << "L16 nor one that takes an event";
    // centiseconds counted while the event ring is held, more than one pass dispatches: the pass after the one
    // that takes their record dispatches the last and takes no input
    mbx_model_evt_pause(&model, true);
    mbx_model_advance_ms(&model, (CTRL_LOOP_TICKS_PER_PASS + 1u) * MBX_TICK_MS);
    mbx_model_evt_pause(&model, false);
    static_cast<void>(ctrl_loop_service(&loop_));
    ASSERT_EQ(loop_.ticks_owed, 1u);
    const unsigned events = loop_.stats.events;
    const unsigned rx = loop_.stats.rx_records;
    const unsigned ticks = loop_.stats.ticks;
    static_cast<void>(ctrl_loop_service(&loop_));
    ASSERT_TRUE(loop_.stats.events == events && loop_.stats.rx_records == rx && loop_.stats.ticks == ticks + 1u);
    EXPECT_EQ(probe.retries, 0u) << "L16 nor one that dispatches a centisecond, though it takes no input";
    const unsigned polls = probe.polls;
    const unsigned passes = loop_.stats.retry_passes;
    probe.retry_owing = true;
    EXPECT_NE(ctrl_loop_service(&loop_), 0u) << "L16 a retry still owed asks for the next pass at once";
    EXPECT_EQ(probe.retries, 1u) << "L16 the next pass that takes nothing calls it";
    EXPECT_EQ(probe.polls_at_retry, polls + 1u) << "L16 after its polls";
    EXPECT_EQ(loop_.stats.retry_passes, passes + 1u) << "L16 the pass is counted as one that called the retry";
    probe.retry_owing = false;
    EXPECT_EQ(ctrl_loop_service(&loop_), 0u) << "L16 a retry that owes nothing lets the loop sleep";
    // with THE STEP bound, the retry comes before it, so the step's deadline counts the retry's time
    ASSERT_TRUE(ctrl_loop_set_step(&loop_, probe_step, nullptr, probe_clock, nullptr));
    drain(&loop_);
    const unsigned steps = probe.steps;
    const unsigned retries = probe.retries;
    EXPECT_EQ(ctrl_loop_service(&loop_), 0u);
    EXPECT_TRUE(probe.retries == retries + 1u && probe.steps_at_retry == steps && probe.steps == steps + 1u)
        << "L16 and before THE STEP";
    // a centisecond and a record before every pass: no pass takes nothing, and the aged step's pass calls it
    const auto busy_pass = [&]() {
        mbx_model_advance_ms(&model, MBX_TICK_MS);
        EXPECT_TRUE(mbx_model_rx(&model, f, sizeof f, 0));
        static_cast<void>(ctrl_loop_service(&loop_));
    };
    for (unsigned k = 0; k <= CTRL_LOOP_STEP_AGE; ++k) {
        busy_pass();
    }
    EXPECT_EQ(probe.retries, retries + 1u) << "L16 input that leaves no pass empty holds it off";
    const unsigned aged_steps = probe.steps;
    const unsigned aged = loop_.stats.aged_passes;
    ASSERT_TRUE(mbx_model_rx(&model, f, sizeof f, 0));
    const unsigned aged_polls = probe.polls;
    probe.retry_aged = true;
    EXPECT_NE(ctrl_loop_service(&loop_), 0u);
    probe.retry_aged = false;
    ASSERT_EQ(loop_.stats.aged_passes, aged + 1u);
    EXPECT_TRUE(probe.retries == retries + 2u && probe.steps_at_retry == aged_steps + 1u && probe.polls == aged_polls)
        << "L16 the pass given whole to an aged step calls it after the step, once it is aged";
    for (unsigned k = 0; k <= CTRL_LOOP_STEP_AGE; ++k) {
        busy_pass();
    }
    ASSERT_TRUE(mbx_model_rx(&model, f, sizeof f, 0));
    EXPECT_NE(ctrl_loop_service(&loop_), 0u);
    ASSERT_EQ(loop_.stats.aged_passes, aged + 2u);
    EXPECT_EQ(probe.retries, retries + 2u) << "L16 and not before: a retry not aged waits its pace";
}

// THE RETRY's age limit (#665): once the client reports a retry aged, the next
// pass calls it before it takes any input, takes nothing else and asks for the
// next pass at once, which takes the input it held off; the age is read as
// each pass starts, after THE STEP's age, whose pass takes the round instead.
TEST_F(Loop, L17AnAgedRetryIsAPassOfItsOwn) {
    drain(&loop_);
    ASSERT_TRUE(ctrl_loop_set_retry(&loop_, probe_retry, probe_retry_aged, nullptr));
    std::uint8_t f[82];
    build_frame(f, sizeof f, 0x22F0, 0xFA, 2);
    ASSERT_TRUE(mbx_model_rx(&model, f, sizeof f, 0));
    const unsigned reads = probe.aged_reads;
    static_cast<void>(ctrl_loop_service(&loop_));
    EXPECT_EQ(probe.retries, 0u) << "L17 a retry not aged waits beside input";
    EXPECT_TRUE(probe.aged_reads == reads + 1u && probe.rx_at_aged == 0u)
        << "L17 the age is read once as the pass starts, before it takes any input";
    ASSERT_TRUE(mbx_model_rx(&model, f, sizeof f, 0));
    mbx_timer_arm(0, 0x710u, mbx_now_ms());
    mbx_model_advance_ms(&model, MBX_TICK_MS);
    const unsigned rx = probe.rx;
    const unsigned events = probe.events;
    const unsigned polls = probe.polls;
    const unsigned ticks = loop_.stats.ticks;
    const unsigned passes = loop_.stats.retry_passes;
    probe.retry_aged = true;
    EXPECT_NE(ctrl_loop_service(&loop_), 0u) << "L17 the aged retry's pass asks for the next pass at once";
    EXPECT_EQ(probe.retries, 1u) << "L17 the next pass calls the retry though input waits";
    EXPECT_TRUE(probe.rx == rx && probe.events == events && probe.polls == polls && loop_.stats.ticks == ticks)
        << "L17 and takes nothing else: no event, no record, no poll, no centisecond";
    EXPECT_EQ(loop_.stats.retry_passes, passes + 1u) << "L17 the pass is counted as one that called the retry";
    EXPECT_EQ(probe.round_left, CTRL_LOOP_SHARE_US - CTRL_LOOP_SHARE_MARGIN_US)
        << "L17 a round in a pass of its own has all of it under the margin, with no clock";
    probe.retry_aged = false;
    static_cast<void>(ctrl_loop_service(&loop_));
    EXPECT_TRUE(probe.rx == rx + 1u && probe.events > events && loop_.stats.ticks == ticks + 1u)
        << "L17 the next pass takes the input it held off";
    EXPECT_EQ(probe.retries, 1u) << "L17 and calls no retry beside it";
    drain(&loop_);
    // with THE STEP aged too, the step's pass takes the round after the step, and no pass of its own follows
    ASSERT_TRUE(ctrl_loop_set_step(&loop_, probe_step, nullptr, probe_clock, nullptr));
    drain(&loop_);
    const auto busy_pass = [&]() {
        mbx_model_advance_ms(&model, MBX_TICK_MS);
        EXPECT_TRUE(mbx_model_rx(&model, f, sizeof f, 0));
        static_cast<void>(ctrl_loop_service(&loop_));
    };
    for (unsigned k = 0; k <= CTRL_LOOP_STEP_AGE; ++k) {
        busy_pass();
    }
    ASSERT_TRUE(mbx_model_rx(&model, f, sizeof f, 0));
    const unsigned steps = probe.steps;
    const unsigned retries = probe.retries;
    const unsigned aged_reads = probe.aged_reads;
    probe.retry_aged = true;
    probe.now_step = 100u;
    EXPECT_NE(ctrl_loop_service(&loop_), 0u);
    probe.now_step = 0u;
    EXPECT_TRUE(probe.steps == steps + 1u && probe.retries == retries + 1u && probe.steps_at_retry == steps + 1u)
        << "L17 an aged step's pass takes the round after the step";
    EXPECT_EQ(probe.aged_reads, aged_reads + 1u) << "L17 the age is read once, as the pass starts";
    EXPECT_LT(probe.round_left, CTRL_LOOP_SHARE_US - CTRL_LOOP_SHARE_MARGIN_US)
        << "L17 a round beside a step has what the step left of the pass";
    probe.retry_aged = false;
    drain(&loop_);
}

// THE TRANSMIT (#665): the client is called only in a pass given whole to it, once it reports a build owed: before
// any input, taking nothing else, the first read of a pass that may be given whole, with an aged round after it; the
// next pass takes the input it held off, and the owed build does not take it.
TEST_F(Loop, L20AnOwedBuildIsAPassOfItsOwn) {
    drain(&loop_);
    ASSERT_TRUE(ctrl_loop_set_transmit(&loop_, probe_transmit, probe_transmit_aged, nullptr));
    ASSERT_TRUE(ctrl_loop_set_retry(&loop_, probe_retry, probe_retry_aged, nullptr));
    drain(&loop_);
    std::uint8_t f[82];
    build_frame(f, sizeof f, 0x22F0, 0xFA, 2);
    ASSERT_TRUE(mbx_model_rx(&model, f, sizeof f, 0));
    const unsigned reads = probe.transmit_aged_reads;
    const unsigned before = probe.transmits;
    const unsigned rx0 = probe.rx;
    static_cast<void>(ctrl_loop_service(&loop_));
    EXPECT_EQ(probe.transmits, before) << "L20 no build owed, no call, whatever the pass takes";
    EXPECT_TRUE(probe.transmit_aged_reads == reads + 1u && probe.rx_at_transmit_aged == rx0)
        << "L20 the build is read once as the pass starts, before it takes any input";
    ASSERT_TRUE(mbx_model_rx(&model, f, sizeof f, 0));
    mbx_timer_arm(0, 0x730u, mbx_now_ms());
    mbx_model_advance_ms(&model, MBX_TICK_MS);
    const unsigned rx = probe.rx;
    const unsigned events = probe.events;
    const unsigned polls = probe.polls;
    const unsigned ticks = loop_.stats.ticks;
    const unsigned passes = loop_.stats.transmit_passes;
    probe.transmit_aged = true;
    probe.retry_aged = true;
    probe.order_of.clear();
    EXPECT_NE(ctrl_loop_service(&loop_), 0u) << "L20 the build's pass asks for the next pass at once";
    probe.retry_aged = false;
    EXPECT_EQ(probe.order_of, "TR") << "L20 the next pass calls the transmit though input waits, then an aged round";
    EXPECT_EQ(probe.round_left, CTRL_LOOP_SHARE_US - CTRL_LOOP_SHARE_MARGIN_US)
        << "L20 a round beside a build has what it left, all with no clock";
    EXPECT_TRUE(probe.rx == rx && probe.events == events && probe.polls == polls && loop_.stats.ticks == ticks)
        << "L20 and takes nothing else: no event, no record, no poll, no centisecond";
    EXPECT_EQ(loop_.stats.transmit_passes, passes + 1u) << "L20 the pass is counted as the transmit's";
    probe.transmit_aged = false;
    probe.order_of.clear();
    static_cast<void>(ctrl_loop_service(&loop_));
    EXPECT_TRUE(probe.rx == rx + 1u && probe.events > events && loop_.stats.ticks == ticks + 1u)
        << "L20 the next pass takes the input it held off";
    EXPECT_EQ(probe.order_of, "") << "L20 and calls no transmit beside its record";
    drain(&loop_);
    // with THE STEP aged too, the build's pass comes first, and the step's next
    ASSERT_TRUE(ctrl_loop_set_step(&loop_, probe_step, nullptr, probe_clock, nullptr));
    drain(&loop_);
    const auto busy_pass = [&]() {
        mbx_model_advance_ms(&model, MBX_TICK_MS);
        EXPECT_TRUE(mbx_model_rx(&model, f, sizeof f, 0));
        static_cast<void>(ctrl_loop_service(&loop_));
    };
    for (unsigned k = 0; k <= CTRL_LOOP_STEP_AGE; ++k) {
        busy_pass();
    }
    ASSERT_TRUE(mbx_model_rx(&model, f, sizeof f, 0));
    probe.transmit_aged = true;
    probe.order_of.clear();
    loop_.retry_firm = true;
    EXPECT_NE(ctrl_loop_service(&loop_), 0u);
    EXPECT_EQ(probe.order_of, "T") << "L20 a build owed comes before an aged step";
    probe.transmit_aged = false;
    EXPECT_NE(ctrl_loop_service(&loop_), 0u);
    EXPECT_EQ(probe.order_of, "TS") << "L20 the aged step's pass may follow it, the second in a row";
    loop_.retry_firm = false;
    drain(&loop_);
}

// THE TICK's cap (#665): a pass that dispatches a centisecond takes
// CTRL_LOOP_RX_PER_TICK_PASS records of a channel, and the next pass, which
// dispatches none, CTRL_LOOP_RX_PER_PASS.
TEST_F(Loop, L21APassThatDispatchesACentisecondTakesOneRecordOfAChannel) {
    drain(&loop_);
    std::uint8_t f[82];
    build_frame(f, sizeof f, 0x22F0, 0xFA, 2);
    for (unsigned k = 0; k < CTRL_LOOP_RX_PER_PASS + 1u; ++k) {
        ASSERT_TRUE(mbx_model_rx(&model, f, sizeof f, 0));
    }
    mbx_model_advance_ms(&model, MBX_TICK_MS);
    const unsigned rx = probe.rx;
    const unsigned ticks = loop_.stats.ticks;
    static_cast<void>(ctrl_loop_service(&loop_));
    ASSERT_EQ(loop_.stats.ticks, ticks + 1u);
    EXPECT_EQ(probe.rx, rx + CTRL_LOOP_RX_PER_TICK_PASS)
        << "L21 a pass that dispatches a centisecond takes CTRL_LOOP_RX_PER_TICK_PASS records of a channel";
    static_cast<void>(ctrl_loop_service(&loop_));
    EXPECT_EQ(probe.rx, rx + CTRL_LOOP_RX_PER_TICK_PASS + CTRL_LOOP_RX_PER_PASS)
        << "L21 the next pass, which dispatches none, takes CTRL_LOOP_RX_PER_PASS";
    drain(&loop_);
}

// A pass given whole (#665): at most CTRL_LOOP_WHOLE_RUN in a row, and one at most while records wait and the client
// yields, or while THE DRAIN's channel holds records it could not take.
TEST_F(Loop, L22PassesGivenWholeStandApartAsInputWaits) {
    drain(&loop_);
    ASSERT_TRUE(ctrl_loop_set_retry(&loop_, probe_retry, probe_retry_aged, nullptr));
    drain(&loop_);
    std::uint8_t f[82];
    build_frame(f, sizeof f, 0x22F0, 0xFA, 2);
    const auto whole = [&]() {   // whether the next pass is given whole to the round
        const unsigned retries = probe.retries;
        const unsigned passes = loop_.stats.passes;
        const unsigned polls = probe.polls;
        static_cast<void>(ctrl_loop_service(&loop_));
        EXPECT_EQ(loop_.stats.passes, passes + 1u);
        return probe.retries == retries + 1u && probe.polls == polls;
    };
    probe.retry_aged = true;
    loop_.retry_firm = true;
    EXPECT_TRUE(whole()) << "L22 the first after an ordinary pass";
    static_assert(CTRL_LOOP_WHOLE_RUN == 3u, "the test runs a full row of passes given whole");
    EXPECT_TRUE(whole()) << "L22 a second may follow it";
    EXPECT_TRUE(whole()) << "L22 and a third";
    EXPECT_FALSE(whole()) << "L22 a fourth may not";
    EXPECT_TRUE(whole()) << "L22 the next after an ordinary pass";
    loop_.events_left = true;
    EXPECT_FALSE(whole()) << "L22 none follows another while events wait";
    EXPECT_TRUE(whole()) << "L22 the next after an ordinary pass";
    loop_.drain_ch = MBX_CH_ADP + 1u;
    ASSERT_TRUE(mbx_model_rx(&model, f, sizeof f, 0));
    EXPECT_FALSE(whole()) << "L22 and none follows another while a record of THE DRAIN's channel waits";
    loop_.drain_ch = 0u;
    probe.retry_aged = false;
    drain(&loop_);
    // records left in a ring, the client yielding: the pass after one given whole is ordinary
    for (unsigned k = 0; k < CTRL_LOOP_RX_PER_PASS + 1u; ++k) {
        ASSERT_TRUE(mbx_model_rx(&model, f, sizeof f, 0));
    }
    loop_.retry_firm = false;
    static_cast<void>(ctrl_loop_service(&loop_));
    EXPECT_TRUE(loop_.backlog) << "L22 a pass that leaves a record marks the backlog";
    probe.retry_aged = true;
    EXPECT_TRUE(whole()) << "L22 a round after that pass";
    EXPECT_FALSE(whole()) << "L22 and no second while records wait and the client yields";
    EXPECT_FALSE(loop_.backlog) << "L22 the ring taken, the backlog is gone";
    probe.retry_aged = false;
    loop_.retry_firm = true;
    drain(&loop_);
}

// THE DRAIN (#665): its channel's records go first, past CTRL_LOOP_RX_PER_PASS while the pass has spent less than
// CTRL_LOOP_DRAIN_US, CTRL_LOOP_DRAIN_RECORDS at most, and a pass that took more than CTRL_LOOP_RX_PER_PASS of them
// takes no other channel's. With no clock bound it is any channel.
TEST_F(Loop, L23TheDrainTakesItsChannelFirstWhileThePassHasRoom) {
    drain(&loop_);
    std::uint8_t f[82];
    build_frame(f, sizeof f, 0x22F0, 0xFA, 2);
    loop_.drain_ch = MBX_CH_ADP + 1u;
    const auto fill = [&]() {
        for (unsigned k = 0; k < MBX_CH_ADP_RATE_BURST; ++k) {
            ASSERT_TRUE(mbx_model_rx(&model, f, sizeof f, 0));
        }
    };
    static_assert(MBX_CH_ADP_RATE_BURST > CTRL_LOOP_RX_PER_PASS, "the test takes more than a pass's records of a channel");
    fill();
    static_cast<void>(ctrl_loop_service(&loop_));   // reads the ring's mark, which the next pass's order is
    unsigned rx = probe.rx;
    static_cast<void>(ctrl_loop_service(&loop_));
    EXPECT_EQ(probe.rx, rx + CTRL_LOOP_RX_PER_PASS) << "L23 with no clock bound it takes as any channel";
    EXPECT_TRUE(loop_.backlog) << "L23 a channel that took all it may marks the backlog";
    drain(&loop_);
    EXPECT_FALSE(loop_.backlog) << "L23 until one takes less";
    ASSERT_TRUE(ctrl_loop_set_step(&loop_, probe_step, nullptr, probe_clock, nullptr));
    drain(&loop_);
    mbx_model_advance_ms(&model, MBX_CH_ADP_RATE_REFILL_MS * MBX_CH_ADP_RATE_BURST);
    drain(&loop_);
    fill();
    rx = probe.rx;
    static_cast<void>(ctrl_loop_service(&loop_));
    EXPECT_GT(probe.rx, rx + CTRL_LOOP_RX_PER_PASS) << "L23 with a clock it goes past CTRL_LOOP_RX_PER_PASS";
    drain(&loop_);
    mbx_model_advance_ms(&model, MBX_CH_ADP_RATE_REFILL_MS * MBX_CH_ADP_RATE_BURST);
    drain(&loop_);
    fill();
    rx = probe.rx;
    probe.now_step = CTRL_LOOP_DRAIN_US + 1u;   // the first read past the pass's own finds it past its time
    static_cast<void>(ctrl_loop_service(&loop_));
    probe.now_step = 0u;
    EXPECT_EQ(probe.rx, rx + CTRL_LOOP_RX_PER_PASS) << "L23 and stops once the pass has spent CTRL_LOOP_DRAIN_US";
    drain(&loop_);
    // a burst longer than the limit: ACMP's, bound past the open, which opens the filter of what was bound by then
    static_assert(MBX_CH_ACMP_RATE_BURST > CTRL_LOOP_DRAIN_RECORDS + CTRL_LOOP_RX_PER_PASS, "the test passes the limit");
    ASSERT_TRUE(ctrl_loop_bind_rx(&loop_, MBX_CH_ACMP, probe_rx_acmp, nullptr));
    model.filter_en |= 1u << MBX_CH_ACMP;
    std::uint8_t a[48];   // short enough that the ring holds the whole burst
    build_frame(a, sizeof a, 0x22F0, 0xFC, 2);
    std::memset(a + 16, 0, sizeof a - 16u);   // the entity the loop opened as, which the filter's terms name
    unsigned message = 0;
    while (message < 16u && !mbx_model_rx(&model, a, sizeof a, 0)) {
        a[15] = static_cast<std::uint8_t>(++message);
    }
    ASSERT_LT(message, 16u) << "(a message the channel takes)";
    for (unsigned k = 1; k < MBX_CH_ACMP_RATE_BURST; ++k) {
        ASSERT_TRUE(mbx_model_rx(&model, a, sizeof a, 0));
    }
    loop_.drain_ch = MBX_CH_ACMP + 1u;
    const unsigned acmp = probe.rx_acmp;
    static_cast<void>(ctrl_loop_service(&loop_));
    EXPECT_EQ(probe.rx_acmp, acmp + CTRL_LOOP_DRAIN_RECORDS) << "L23 and stops at CTRL_LOOP_DRAIN_RECORDS";
    drain(&loop_);
    loop_.drain_ch = 0u;
}

// What a pass has left (#665): once every channel has had its due, a record of each in turn while the pass has spent less
// than CTRL_LOOP_DRAIN_US, in a pass that dispatches a centisecond too, whose cost that time counts.
TEST_F(Loop, L25WhatAPassHasLeftGoesToTheRecordsStillWaiting) {
    drain(&loop_);
    ASSERT_TRUE(ctrl_loop_set_step(&loop_, probe_step, nullptr, probe_clock, nullptr));
    drain(&loop_);
    std::uint8_t f[82];
    build_frame(f, sizeof f, 0x22F0, 0xFA, 2);
    const auto fill = [&]() {
        mbx_model_advance_ms(&model, MBX_CH_ADP_RATE_REFILL_MS * MBX_CH_ADP_RATE_BURST);
        drain(&loop_);
        for (unsigned k = 0; k < MBX_CH_ADP_RATE_BURST; ++k) {
            ASSERT_TRUE(mbx_model_rx(&model, f, sizeof f, 0));
        }
    };
    fill();
    unsigned rx = probe.rx;
    static_cast<void>(ctrl_loop_service(&loop_));
    EXPECT_EQ(probe.rx, rx + MBX_CH_ADP_RATE_BURST) << "L23 what a pass has left goes to the records still waiting";
    fill();
    rx = probe.rx;
    mbx_model_advance_ms(&model, MBX_TICK_MS);
    static_cast<void>(ctrl_loop_service(&loop_));
    EXPECT_GT(probe.rx, rx + CTRL_LOOP_RX_PER_TICK_PASS) << "L23 a pass that dispatches a centisecond takes them too";
    fill();
    rx = probe.rx;
    mbx_model_advance_ms(&model, MBX_TICK_MS);
    probe.now_step = CTRL_LOOP_DRAIN_US + 1u;
    static_cast<void>(ctrl_loop_service(&loop_));
    probe.now_step = 0u;
    EXPECT_EQ(probe.rx, rx + CTRL_LOOP_RX_PER_TICK_PASS) << "L23 until the pass has spent its time, at its cap";
    drain(&loop_);
    // two channels with records: each has its due, then a record of each in turn until the pass has spent its time
    ASSERT_TRUE(ctrl_loop_bind_rx(&loop_, MBX_CH_ACMP, probe_rx_acmp, nullptr));
    model.filter_en |= 1u << MBX_CH_ACMP;   // bound past the open, which opens the filter of what was bound by then
    std::uint8_t a[82];
    build_frame(a, sizeof a, 0x22F0, 0xFC, 2);
    std::memset(a + 16, 0, sizeof a - 16u);   // the entity the loop opened as, which the filter's terms name
    fill();
    unsigned message = 0;
    while (message < 16u && !mbx_model_rx(&model, a, sizeof a, 0)) {
        a[15] = static_cast<std::uint8_t>(++message);
    }
    ASSERT_LT(message, 16u) << "(a message the channel takes)";
    for (unsigned k = 1; k < MBX_CH_ADP_RATE_BURST; ++k) {
        ASSERT_TRUE(mbx_model_rx(&model, a, sizeof a, 0));
    }
    rx = probe.rx;
    const unsigned acmp = probe.rx_acmp;
    probe.now_step = CTRL_LOOP_DRAIN_US / 3u + 1u;   // the spare records' fourth read of the clock finds it spent
    static_cast<void>(ctrl_loop_service(&loop_));
    probe.now_step = 0u;
    EXPECT_TRUE(probe.rx == rx + CTRL_LOOP_RX_PER_PASS + 1u && probe.rx_acmp == acmp + CTRL_LOOP_RX_PER_PASS + 1u)
        << "L23 one a channel in turn";
    drain(&loop_);
}

// THE DRAIN's order (#665): a record follows only the events posted before it, by ring position: a pass that emptied
// the event ring has taken every event posted before the ring's mark it read as it started, so an event posted after
// a record holds it back no more, and one posted before it does until it is taken.
TEST_F(Loop, L24ARecordFollowsOnlyTheEventsPostedBeforeIt) {
    drain(&loop_);
    std::uint8_t f[82];
    build_frame(f, sizeof f, 0x22F0, 0xFA, 2);
    loop_.drain_ch = MBX_CH_ADP + 1u;
    const std::uint16_t before = loop_.rx_order;
    ASSERT_TRUE(mbx_model_rx(&model, f, sizeof f, 0));
    static_cast<void>(ctrl_loop_service(&loop_));
    EXPECT_NE(loop_.rx_order, before) << "L24 a pass that empties the event ring moves the order to the mark it read";
    drain(&loop_);
    const std::uint16_t held = loop_.rx_order;
    fill_event_ring(0x740u);
    mbx_model_advance_ms(&model, 0);
    ASSERT_TRUE(mbx_model_rx(&model, f, sizeof f, 0));
    static_cast<void>(ctrl_loop_service(&loop_));
    EXPECT_EQ(loop_.rx_order, held) << "L24 a pass that leaves events keeps the order where it was";
    drain(&loop_);
    // a record posted as the pass takes its events follows them in no order that pass read
    mbx_model_advance_ms(&model, MBX_CH_ADP_RATE_REFILL_MS * MBX_CH_ADP_RATE_BURST);
    drain(&loop_);
    const std::uint16_t mark = mbx_rx_mark(MBX_CH_ADP);
    probe.on_event = [&]() {
        probe.on_event = nullptr;
        EXPECT_TRUE(mbx_model_rx(&model, f, sizeof f, 0));
    };
    mbx_model_advance_ms(&model, MBX_TICK_MS);
    static_cast<void>(ctrl_loop_service(&loop_));
    EXPECT_EQ(loop_.rx_order, mark) << "L24 the mark is read before the events";
    drain(&loop_);
    loop_.drain_ch = 0u;
}

}  // namespace
