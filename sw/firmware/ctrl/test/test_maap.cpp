// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
// Independent Table B.7 expectations and B.2 wire fixtures.
#include <gtest/gtest.h>
#include <array>
#include <cstdint>
#include <cstring>
#include <vector>

#include "fw_gtest.hpp"
#include "maap.h"
#include "maap_csr.h"

FW_TALLY_LABEL("ctrl MAAP Annex B");

namespace {
using Frame = std::array<std::uint8_t, 60>;
constexpr std::uint64_t kMac = 0x020000000080ULL;
constexpr std::uint64_t kPeer = 0x060000000040ULL;
constexpr std::uint64_t kBase = 0x91e0f0000100ULL;

void put(Frame& f, unsigned at, unsigned n, std::uint64_t value) {
    for (unsigned i = 0; i < n; ++i) f.at(at + n - 1 - i) = static_cast<std::uint8_t>(value >> (8 * i));
}

std::uint64_t field(const Frame& f, unsigned at, unsigned n) {
    std::uint64_t value = 0;
    for (unsigned i = 0; i < n; ++i) value = value * 256 + f.at(at + i);
    return value;
}

Frame pdu(unsigned type, std::uint64_t requested = kBase, unsigned count = 8,
          std::uint64_t peer = kPeer, std::uint64_t destination = MAAP_MULTICAST) {
    Frame f{};
    put(f, 0, 6, destination);
    put(f, 6, 6, peer);
    f[12] = 0x22; f[13] = 0xf0; f[14] = 0xfe;
    f[15] = static_cast<std::uint8_t>(type); f[16] = 8; f[17] = 16;
    put(f, 26, 6, requested); put(f, 32, 2, count);
    if (type == 2) { put(f, 34, 6, requested); put(f, 40, 2, count); }
    return f;
}

struct CoreRig {
    maap core{};
    maap_ports ports{};
    std::vector<Frame> frames;
    std::vector<std::uint32_t> delays;
    std::uint32_t clock = 17;
    unsigned stops = 0, published = 0, last_count = 0;
    bool room = true;
    bool valid = false;
    bool recurse = false;

    CoreRig() {
        ports.ctx = this;
        ports.send = [](void* ctx, unsigned interface, const std::uint8_t* f, std::size_t len) {
            auto& r = *static_cast<CoreRig*>(ctx);
            EXPECT_EQ(interface, 3u) << "interface identity";
            EXPECT_EQ(len, 60u) << "padded frame size";
            if (r.recurse) {
                maap_rx(&r.core, nullptr, 0);
                maap_timer_expired(&r.core);
                maap_release(&r.core);
                maap_port_operational(&r.core, false);
                EXPECT_FALSE(maap_begin(&r.core, kBase));
                EXPECT_TRUE(maap_poll(&r.core));
            }
            if (!r.room) return false;
            Frame copy{}; std::memcpy(copy.data(), f, len); r.frames.push_back(copy);
            return true;
        };
        ports.timer_start = [](void* ctx, unsigned interface, std::uint32_t ms) {
            auto& r = *static_cast<CoreRig*>(ctx);
            EXPECT_EQ(interface, 3u);
            r.delays.push_back(ms);
        };
        ports.timer_stop = [](void* ctx, unsigned) { ++static_cast<CoreRig*>(ctx)->stops; };
        ports.range = [](void* ctx, unsigned interface, std::uint64_t, std::uint16_t count, bool valid) {
            auto& r = *static_cast<CoreRig*>(ctx);
            EXPECT_EQ(interface, 3u);
            r.valid = valid; r.last_count = count; ++r.published;
        };
        ports.clock = [](void* ctx) { return static_cast<CoreRig*>(ctx)->clock; };
        EXPECT_TRUE(maap_init(&core, &ports, 3, kMac, 8));
    }
    void begin() { ASSERT_TRUE(maap_begin(&core, kBase)); }
    void acquire() {
        begin();
        for (unsigned k = 0; k < 3; ++k) maap_timer_expired(&core);
        ASSERT_EQ(core.state, MAAP_DEFEND);
        ASSERT_TRUE(valid);
    }
    void receive(const Frame& f, std::size_t len = 60) { maap_rx(&core, f.data(), len); }
};

TEST(MaapCore, InitialAndThreeRetransmissions) {
    CoreRig r;
    EXPECT_EQ(r.core.state, MAAP_INITIAL);
    r.begin();
    ASSERT_EQ(r.frames.size(), 1u) << "initial PROBE is immediate";
    EXPECT_EQ(r.core.probe_count, 3u) << "three retransmissions remain";
    EXPECT_FALSE(r.valid) << "tentative range is not allocated";
    EXPECT_EQ(r.frames[0], pdu(1, kBase, 8, kMac)) << "B.2 complete PROBE bytes";
    for (unsigned k = 0; k < 3; ++k) {
        maap_timer_expired(&r.core);
        EXPECT_EQ(r.core.probe_count, 2u - k) << "retransmission decrements once";
        EXPECT_EQ(r.frames[k + 1], pdu(1, kBase, 8, kMac));
        if (k < 2) { EXPECT_FALSE(r.valid); }
    }
    ASSERT_EQ(r.frames.size(), 5u) << "four PROBEs followed by ANNOUNCE";
    EXPECT_EQ(r.frames[4], pdu(3, kBase, 8, kMac)) << "B.2 complete ANNOUNCE bytes";
    EXPECT_TRUE(r.valid);
    maap_timer_expired(&r.core);
    EXPECT_EQ(r.frames.back(), pdu(3, kBase, 8, kMac)) << "periodic ANNOUNCE";
    EXPECT_FALSE(maap_poll(&r.core));
}

TEST(MaapCore, ConstantsStrictTimersAndSeed) {
    EXPECT_EQ(MAAP_PROBE_BASE_MS, 500u); EXPECT_EQ(MAAP_PROBE_VARIATION_MS, 100u);
    EXPECT_EQ(MAAP_ANNOUNCE_BASE_MS, 30000u); EXPECT_EQ(MAAP_ANNOUNCE_VARIATION_MS, 2000u);
    unsigned min_probe = 1000, max_probe = 0, min_announce = 40000, max_announce = 0;
    for (unsigned seed = 0; seed < 5000; ++seed) {
        CoreRig a; CoreRig b; a.clock = seed; b.clock = seed;
        a.acquire(); b.acquire();
        EXPECT_EQ(a.delays, b.delays) << "seeded deterministic schedule";
        for (auto delay : a.delays) {
            if (delay < 1000) { min_probe = std::min(min_probe, delay); max_probe = std::max(max_probe, delay); }
            else { min_announce = std::min(min_announce, delay); max_announce = std::max(max_announce, delay); }
        }
    }
    EXPECT_EQ(min_probe, 511u); EXPECT_EQ(max_probe, 589u);
    EXPECT_EQ(min_announce, 30011u); EXPECT_EQ(max_announce, 31989u);
    CoreRig zero;
    zero.clock = 0u - static_cast<std::uint32_t>(kMac);
    zero.begin(); EXPECT_NE(zero.core.rng, 0u) << "zero sum cannot lock generator";
}

class MaapCell : public ::testing::TestWithParam<int> {};
TEST_P(MaapCell, TableB7) {
    int key = GetParam();
    const unsigned state = key / 6, type = key % 3 + 1;
    const bool local_wins = key % 6 >= 3;
    CoreRig r;
    if (state == 0) { r.begin(); maap_release(&r.core); }
    if (state == 1) r.begin();
    if (state == 2) r.acquire();
    auto before = r.frames.size();
    auto base = r.core.base;
    // Reverse-octet comparison: local 0x80 loses to 0x40, wins over 0xc0.
    auto peer = local_wins ? 0x0200000000c0ULL : kPeer;
    r.receive(pdu(type, kBase, 8, peer, type == 2 ? kMac : MAAP_MULTICAST));
    const bool defend = state == 2 && type == 1;
    const bool restart = state != 0 && !defend &&
                         ((state == 1 && type != 1) || !local_wins);
    EXPECT_EQ(r.core.conflicts, restart ? 1u : 0u) << "Table B.7 conflict decision";
    EXPECT_EQ(r.frames.size(), before + ((defend || restart) ? 1u : 0u)) << "Table B.7 output count";
    if (restart) {
        EXPECT_EQ(r.core.state, MAAP_PROBE); EXPECT_FALSE(r.valid);
        EXPECT_EQ(r.core.probe_count, 3u);
        EXPECT_EQ(r.frames.back()[15], 1u) << "loss restarts with PROBE";
    } else {
        EXPECT_EQ(r.core.state, static_cast<maap_state>(state));
        EXPECT_EQ(r.core.base, base);
    }
    if (defend) { EXPECT_EQ(field(r.frames.back(), 0, 6), peer) << "DEFEND uses PROBE source"; }
}
INSTANTIATE_TEST_SUITE_P(AllStates, MaapCell, ::testing::Range(0, 18));

TEST(MaapCore, ReverseOctetPriority) {
    CoreRig r; r.begin();
    r.receive(pdu(1, kBase, 8, 0x040000000040ULL));
    EXPECT_EQ(r.core.conflicts, 1u) << "least significant octet decides first";
    CoreRig equal; equal.begin(); equal.receive(pdu(1, kBase, 8, kMac));
    EXPECT_EQ(equal.core.conflicts, 1u) << "equal MAC is not lower";
}

// R528-1-F3: each octet must decide after all later octets tie.
TEST(MaapCore, PriorityAfterTiedOctets) {
    constexpr std::uint64_t local = 0x024040404080ULL;
    for (unsigned octet = 0; octet < 6; ++octet) {
        for (bool wins : {false, true}) {
            CoreRig r;
            ASSERT_TRUE(maap_init(&r.core, &r.ports, 3, local, 8));
            r.begin();
            const auto step = std::uint64_t{octet == 0 ? 2u : 1u} << (8 * (5 - octet));
            const auto peer = wins ? local + step : local - step;
            r.receive(pdu(1, kBase, 8, peer));
            EXPECT_EQ(r.core.conflicts, wins ? 0u : 1u)
                << "every reversed octet decides, including first: " << octet;
        }
    }
}

TEST(MaapCore, RestartDrawsNewRange) {
    CoreRig r; r.acquire();
    r.receive(pdu(3));
    EXPECT_EQ(r.core.conflicts, 1u);
    EXPECT_NE(r.core.base, kBase) << "fixed seed Restart draws a new range";
    EXPECT_GE(r.core.base, MAAP_POOL_BASE);
    EXPECT_LE(r.core.base + 8, MAAP_POOL_BASE + MAAP_POOL_SIZE);
    ASSERT_EQ(r.frames.size(), 6u);
    EXPECT_EQ(field(r.frames.back(), 26, 6), r.core.base);
    EXPECT_EQ(r.frames.back()[15], 1u);
}

TEST(MaapCore, UniformDrawRejectsIncompleteBucket) {
    CoreRig r;
    // Inverse xorshift seed: the first word is UINT32_MAX, outside the
    // largest complete multiple of 79. The next word is 0x0003e01f.
    r.clock = 0x5e6cfc67u;
    r.begin();
    EXPECT_EQ(r.core.rng, 0x0003e01fu) << "incomplete random bucket rejected";
    EXPECT_EQ(r.core.last_delay_ms, 587u) << "draw uses the next complete-bucket word";
}

TEST(MaapCore, DefendEchoAndIntersection) {
    CoreRig r; r.acquire();
    for (const auto& range : std::array<std::array<unsigned, 3>, 4>{{
             {0xfc, 8, 4}, {0x104, 8, 4}, {0xf8, 32, 8}, {0x102, 2, 2}}}) {
        auto req = MAAP_POOL_BASE + range[0];
        r.receive(pdu(1, req, range[1]));
        auto expected = pdu(2, req, range[1], kMac, kPeer);
        put(expected, 34, 6, std::max(req, kBase)); put(expected, 40, 2, range[2]);
        EXPECT_EQ(r.frames.back(), expected) << "echo request and exact intersection";
    }
}

TEST(MaapCore, DisjointAdjacentZeroAndDefendRange) {
    CoreRig r; r.acquire(); const auto n = r.frames.size();
    r.receive(pdu(1, kBase + 8, 1)); r.receive(pdu(1, kBase - 8, 8));
    r.receive(pdu(1, kBase + 2, 0)); r.receive(pdu(3, MAAP_POOL_BASE + 1000, 8));
    EXPECT_EQ(r.frames.size(), n) << "half open intervals and zero count do not conflict";
    auto f = pdu(2); put(f, 34, 6, kBase + 8); r.receive(f);
    EXPECT_EQ(r.core.conflicts, 0u) << "DEFEND tests conflict fields";
    put(f, 26, 6, kBase + 1000); put(f, 34, 6, kBase); r.receive(f);
    EXPECT_EQ(r.core.conflicts, 1u) << "DEFEND conflict wins over echoed request";
}

TEST(MaapCore, MalformedAndVersionCompatibility) {
    CoreRig r; r.begin();
    std::vector<Frame> bad;
    for (auto pair : std::array<std::array<unsigned, 2>, 10>{{
             {12, 0x81}, {14, 0xff}, {15, 0x81}, {15, 0}, {15, 4}, {17, 15}, {17, 40},
             {0, 0x92}, {17, 20}, {6, 7}}}) {
        auto f = pdu(1); f[pair[0]] = static_cast<std::uint8_t>(pair[1]); bad.push_back(f);
    }
    bad.push_back(pdu(1, kBase, 8, 0));
    for (unsigned length : {15u, 40u}) {
        auto f = pdu(1); f[16] = 56; f[17] = static_cast<std::uint8_t>(length); bad.push_back(f);
    }
    for (const auto& f : bad) r.receive(f);
    auto own = pdu(1, kBase, 8, kPeer, kMac); r.receive(own);
    auto foreign = pdu(2, kBase, 8, kPeer, kPeer); r.receive(foreign);
    for (unsigned len = 0; len < 42; ++len) r.receive(pdu(1), len);
    EXPECT_EQ(r.core.discarded, bad.size() + 44) << "malformed input is rejected";
    EXPECT_EQ(r.core.conflicts, 0u);
    for (unsigned version : {0u, 1u, 7u, 31u}) {
        CoreRig v; v.begin(); auto f = pdu(3); f[16] = static_cast<std::uint8_t>(version << 3);
        v.receive(f, 42); EXPECT_EQ(v.core.conflicts, 1u) << "B.2.3 recognized future and older messages";
    }
    CoreRig extended; extended.begin(); auto f = pdu(3); f[16] = 56; f[17] = 20;
    extended.receive(f); EXPECT_EQ(extended.core.conflicts, 1u) << "unknown extension ignored";
}

TEST(MaapCore, InitAndPreferredRangeBounds) {
    CoreRig r;
    for (auto mac : {0ULL, 0x1000000000000ULL, 0x010000000001ULL})
        EXPECT_FALSE(maap_init(&r.core, &r.ports, 3, mac, 8)) << "invalid source MAC";
    EXPECT_FALSE(maap_init(&r.core, &r.ports, 256, kMac, 8));
    EXPECT_FALSE(maap_init(&r.core, &r.ports, 3, kMac, 0));
    EXPECT_FALSE(maap_init(&r.core, &r.ports, 3, kMac, 0xfe01));
    ASSERT_TRUE(maap_init(&r.core, &r.ports, 3, kMac, 8));
    EXPECT_FALSE(maap_begin(&r.core, MAAP_POOL_BASE - 1));
    EXPECT_FALSE(maap_begin(&r.core, MAAP_POOL_BASE + 0xfdf9));
    EXPECT_TRUE(maap_begin(&r.core, MAAP_POOL_BASE + 0xfdf8));
    EXPECT_EQ(r.core.base, MAAP_POOL_BASE + 0xfdf8) << "last legal range";
    auto n = r.frames.size(); EXPECT_TRUE(maap_begin(&r.core, kBase));
    EXPECT_EQ(r.frames.size(), n) << "Begin in PROBE ignored";
    CoreRig entire;
    ASSERT_TRUE(maap_init(&entire.core, &entire.ports, 3, kMac, 0xfe00));
    ASSERT_TRUE(maap_begin(&entire.core, 0)); EXPECT_EQ(entire.core.base, MAAP_POOL_BASE);
    CoreRig random; ASSERT_TRUE(maap_begin(&random.core, 0));
    EXPECT_GE(random.core.base, MAAP_POOL_BASE);
    EXPECT_LE(random.core.base + 8, MAAP_POOL_BASE + MAAP_POOL_SIZE);
}

TEST(MaapCore, ReleaseLossAndRetry) {
    CoreRig claimed; claimed.acquire();
    maap_port_operational(&claimed.core, true);
    EXPECT_FALSE(claimed.valid) << "PortOperational invalidates acquired address";
    CoreRig r; maap_release(&r.core); maap_port_operational(&r.core, false);
    r.valid = true;
    r.begin(); EXPECT_EQ(r.core.state, MAAP_INITIAL); EXPECT_TRUE(r.frames.empty());
    EXPECT_FALSE(r.valid) << "starting down withdraws the prior owner";
    maap_port_operational(&r.core, true); EXPECT_EQ(r.core.state, MAAP_PROBE);
    for (unsigned k = 0; k < 3; ++k) maap_timer_expired(&r.core);
    EXPECT_TRUE(r.valid);
    maap_port_operational(&r.core, true); EXPECT_EQ(r.core.state, MAAP_PROBE);
    EXPECT_FALSE(r.valid) << "PortOperational invalidates acquired address";
    maap_port_operational(&r.core, false);
    EXPECT_EQ(r.core.state, MAAP_INITIAL); EXPECT_EQ(r.last_count, 0u);
    maap_port_operational(&r.core, true); EXPECT_EQ(r.core.state, MAAP_PROBE);
    maap_release(&r.core); EXPECT_FALSE(r.core.enabled); EXPECT_EQ(r.last_count, 0u);
    maap_timer_expired(&r.core); EXPECT_EQ(r.core.stale_expiries, 1u);
    auto n = r.frames.size(); maap_port_operational(&r.core, true);
    EXPECT_EQ(r.frames.size(), n) << "released instance stays idle";
}

// R528-1-F1: Table B.7 note a survives the normal link-down boot order.
TEST(MaapCore, BeginBeforePortOperationalRetainsRange) {
    CoreRig r;
    maap_port_operational(&r.core, false);
    r.begin();
    EXPECT_TRUE(r.frames.empty());
    EXPECT_FALSE(maap_begin(&r.core, MAAP_POOL_BASE - 1));
    maap_port_operational(&r.core, true);
    ASSERT_EQ(r.frames.size(), 1u);
    EXPECT_EQ(r.core.base, kBase) << "Begin supplied range survives port down";
    EXPECT_EQ(r.frames[0], pdu(1, kBase, 8, kMac));
    r.receive(pdu(2));
    EXPECT_NE(r.core.base, kBase) << "saved range consumed before conflict Restart";
    maap_release(&r.core);
    maap_port_operational(&r.core, false);
    ASSERT_TRUE(maap_begin(&r.core, 0));
    maap_port_operational(&r.core, true);
    EXPECT_NE(r.core.base, kBase) << "new Begin without preferred range draws";
}

TEST(MaapCore, StalledOutputRetainsOrderAndOriginalExpiry) {
    CoreRig r; r.room = false; r.begin();
    EXPECT_EQ(r.core.queued, 1u);
    maap_timer_expired(&r.core); EXPECT_TRUE(r.core.expiry_owed);
    maap_timer_expired(&r.core); EXPECT_EQ(r.core.stale_expiries, 1u);
    EXPECT_TRUE(maap_poll(&r.core)); EXPECT_TRUE(r.frames.empty());
    r.room = true;
    EXPECT_TRUE(maap_poll(&r.core)) << "original expiry remains owed";
    EXPECT_FALSE(maap_poll(&r.core));
    EXPECT_EQ(r.frames.size(), 2u); EXPECT_EQ(r.core.probe_count, 2u);
    maap_timer_expired(&r.core); r.room = false; maap_timer_expired(&r.core);
    EXPECT_FALSE(r.valid) << "allocation waits for committed ANNOUNCE";
    EXPECT_EQ(r.core.queued, 2u);
    r.room = true; EXPECT_FALSE(maap_poll(&r.core)); EXPECT_TRUE(r.valid);
    ASSERT_EQ(r.frames.size(), 5u);
    EXPECT_EQ(r.frames[3][15], 1u); EXPECT_EQ(r.frames[4][15], 3u) << "last PROBE precedes ANNOUNCE";
}

TEST(MaapCore, QueueBoundAndWithdrawal) {
    CoreRig r; r.acquire(); r.room = false;
    for (unsigned k = 0; k < MAAP_QUEUE_FRAMES + 1; ++k) r.receive(pdu(1));
    EXPECT_EQ(r.core.queued, MAAP_QUEUE_FRAMES);
    EXPECT_EQ(r.core.overflow, 1u) << "overload is counted as failure";
    r.room = true; auto n = r.frames.size(); EXPECT_TRUE(maap_poll(&r.core));
    EXPECT_EQ(r.frames.size(), n + 2) << "poll has bounded work";
    maap_release(&r.core); EXPECT_EQ(r.core.queued, 0u); EXPECT_FALSE(maap_poll(&r.core));
    CoreRig loss; loss.acquire(); loss.room = false; loss.receive(pdu(1)); loss.receive(pdu(3));
    EXPECT_EQ(loss.core.queued, 1u) << "lost range output replaced by new PROBE";
    loss.room = true; maap_poll(&loss.core); EXPECT_EQ(loss.frames.back()[15], 1u);
}

TEST(MaapCore, ReentrantPortsAreCountedAndIgnored) {
    CoreRig r; r.recurse = true; r.begin();
    EXPECT_EQ(r.core.reentries, 6u) << "all input guards fire";
    EXPECT_EQ(r.core.state, MAAP_PROBE); EXPECT_TRUE(r.core.timer_running);
    EXPECT_EQ(r.frames.size(), 1u); EXPECT_TRUE(r.core.enabled);
}

struct CsrRig {
    std::array<std::uint32_t, 1024> regs{};
    std::array<std::uint64_t, 8> streams{};
    std::vector<std::array<std::uint32_t, 3>> writes;
    maap_csr output{};
    maap_csr_port port{};
    CsrRig() {
        port.ctx = this;
        port.read32 = [](void* ctx, unsigned, std::uint32_t offset) { return static_cast<CsrRig*>(ctx)->regs.at(offset / 4); };
        port.write32 = [](void* ctx, unsigned interface, std::uint32_t offset, std::uint32_t value) {
            auto& r = *static_cast<CsrRig*>(ctx);
            r.writes.push_back({interface, offset, value});
            // REGISTER_MAP 0x800: listener DMAC words are read-only.
            if ((offset == 0x81c || offset == 0x820) && !(r.regs[0x800 / 4] & 0x100u)) return;
            r.regs.at(offset / 4) = value;
            auto k = r.regs[0x800 / 4] & 15;
            if (offset == 0x81c) r.streams.at(k) = (r.streams.at(k) & 0xffff00000000ULL) | value;
            if (offset == 0x820) r.streams.at(k) = (static_cast<std::uint64_t>(value) << 32) | (r.streams.at(k) & 0xffffffffULL);
        };
    }
};

TEST(MaapCsr, EveryStreamAddressAndLossGate) {
    CsrRig r; r.regs[0x6cc / 4] = 0x12340803; r.regs[0x800 / 4] = 0x201;
    ASSERT_TRUE(maap_csr_init(&r.output, r.port, 8, true, 0x20001, 3));
    maap_csr_allocation(&r.output, 2, kBase, 9, true);
    EXPECT_EQ(r.regs[0x658 / 4], 0xf0000100u); EXPECT_EQ(r.regs[0x65c / 4], 0x91e0u);
    for (unsigned k = 1; k < 8; ++k) EXPECT_EQ(r.streams[k], kBase + k) << "stream destination base plus index";
    EXPECT_EQ(r.regs[0x75c / 4], 0xf0000108u); EXPECT_EQ(r.regs[0x760 / 4], 0x91e0u);
    EXPECT_EQ(r.regs[0x800 / 4], 0x201u) << "selection restored";
    EXPECT_EQ(r.regs[0x6cc / 4], 0x12340802u) << "fabric MAAP disabled without touching seed";
    ASSERT_GE(r.writes.size(), 4u);
    EXPECT_EQ(r.writes[0][1], 0x654u); EXPECT_EQ(r.writes[0][2], 0x20000u);
    EXPECT_EQ(r.writes[1][1], 0x750u); EXPECT_EQ(r.writes[1][2], 2u);
    EXPECT_EQ(r.regs[0x654 / 4], 0x20001u); EXPECT_EQ(r.regs[0x750 / 4], 3u);
    for (const auto& w : r.writes) EXPECT_EQ(w[0], 2u) << "interface stays attached";
    maap_csr_allocation(&r.output, 2, kBase, 0, false);
    EXPECT_EQ(r.regs[0x654 / 4], 0x20000u); EXPECT_EQ(r.regs[0x750 / 4], 2u) << "loss closes both media gates";
}

TEST(MaapCsr, ShapesAndCountRefusal) {
    CsrRig r;
    EXPECT_FALSE(maap_csr_init(&r.output, r.port, 9, false, 1, 0));
    EXPECT_FALSE(maap_csr_init(&r.output, r.port, 0, false, 0, 0));
    ASSERT_TRUE(maap_csr_init(&r.output, r.port, 1, false, 1, 0));
    maap_csr_allocation(&r.output, 0, kBase, 2, true);
    EXPECT_EQ(r.output.refused, 1u); EXPECT_EQ(r.regs[0x654 / 4], 0u) << "wrong shape stays disabled";
    maap_csr_allocation(&r.output, 0, kBase, 1, true);
    EXPECT_EQ(r.regs[0x654 / 4], 1u); EXPECT_EQ(r.regs[0x75c / 4], 0u);
    ASSERT_TRUE(maap_csr_init(&r.output, r.port, 0, true, 0, 3));
    maap_csr_allocation(&r.output, 0, kBase + 3, 1, true);
    EXPECT_EQ(r.regs[0x75c / 4], 0xf0000103u) << "CRF only shape";
}

// R528-1-F4: inspect the whole trace, not just its final register image.
TEST(MaapCsr, AdmissionAfterEveryDestinationWrite) {
    CsrRig r;
    ASSERT_TRUE(maap_csr_init(&r.output, r.port, 8, true, 1, 1));
    maap_csr_allocation(&r.output, 0, kBase, 9, true);
    unsigned destinations = 0, enables = 0;
    for (unsigned k = 0; k < r.writes.size(); ++k) {
        const auto offset = r.writes[k][1], value = r.writes[k][2];
        if (offset == 0x658 || offset == 0x65c || offset == 0x81c ||
            offset == 0x820 || offset == 0x75c || offset == 0x760) {
            EXPECT_EQ(enables, 0u) << "no destination write after admission opens";
            ++destinations;
        }
        if ((offset == 0x654 || offset == 0x750) && (value & 1u)) {
            EXPECT_EQ(destinations, 18u) << "enables follow every destination word";
            EXPECT_GE(k, r.writes.size() - 2u) << "AAF and CRF enables are last";
            ++enables;
        }
    }
    EXPECT_EQ(destinations, 18u); EXPECT_EQ(enables, 2u);
}
} // namespace
