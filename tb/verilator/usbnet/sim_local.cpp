// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
// The separate local receiver must deliver device unicast and group frames,
// retain whole packets under pressure, and leave network control bytes intact.
#include "VKL_usbnet_local_rx.h"
#include "verilated.h"
#include <algorithm>
#include <cstdint>
#include <cstdio>
#include <deque>
#include <vector>

using Bytes = std::vector<uint8_t>;
static int &checks() { static int n = 0; return n; }
static int &fails() { static int n = 0; return n; }
#define CHECK(c, ...) do { ++checks(); if (!(c)) { std::printf("FAIL %s:%d: ", __FILE__, __LINE__); \
    std::printf(__VA_ARGS__); std::puts(""); ++fails(); } } while (0)
static Bytes frame(uint64_t dst, size_t length, uint8_t seed)
{
    Bytes b(length, seed);
    for (int i = 0; i < 6; ++i) b[i] = uint8_t(dst >> (40 - 8 * i));
    b[6] = 0x0A; b[12] = 0x22; b[13] = 0xF0; b[14] = 0xFB;
    return b;
}
struct Bench {
    VKL_usbnet_local_rx d;
    std::deque<Bytes> local;
    std::deque<Bytes> network;
    size_t loff = 0;
    size_t noff = 0;
    std::vector<Bytes> got;
    Bytes current;
    unsigned cycle = 0;
    unsigned active_tail = 0;
    bool stall = false;
    bool hold = false;
    bool previous_hold = false;
    bool only_network = false;
    unsigned previous_data = 0;
    unsigned previous_last = 0;
    Bench() {
        d.clk_i = 0; d.rst_ni = 0; d.station_mac_i = 0x024B4C000101ull;
        tick(); tick(); d.rst_ni = 1;
    }
    void tick() {
        d.clk_i = 0;
        d.s_active_i = !local.empty() || active_tail;
        if (active_tail) --active_tail;
        d.s_valid_i = !local.empty(); d.s_data_i = 0; d.s_keep_i = 0; d.s_last_i = 0;
        if (!local.empty()) {
            const auto &b = local.front();
            for (unsigned j = 0; j < 8 && loff + j < b.size(); ++j) {
                d.s_data_i |= uint64_t(b[loff + j]) << (8 * j); d.s_keep_i |= 1u << j;
            }
            d.s_last_i = loff + 8 >= b.size();
        }
        d.net_valid_i = !network.empty();
        d.net_data_i = network.empty() ? 0 : network.front()[noff];
        d.net_last_i = !network.empty() && noff + 1 == network.front().size();
        d.m_ready_i = !hold && !(stall && (cycle % 5 == 0 || cycle % 7 == 0));
        d.eval();
        if (only_network) CHECK(d.m_valid_o == d.net_valid_i && d.net_ready_o == d.m_ready_i &&
                                (!d.net_valid_i || (d.m_data_o == d.net_data_i && d.m_last_o == d.net_last_i)),
                                "network control path has no added cycle without local traffic");
        if (previous_hold) CHECK(d.m_valid_o && d.m_data_o == previous_data && d.m_last_o == previous_last,
                                 "local receiver output stable under backpressure");
        previous_hold = d.m_valid_o && !d.m_ready_i;
        previous_data = d.m_data_o; previous_last = d.m_last_o;
        if (d.s_valid_i) {
            loff += 8;
            if (d.s_last_i) { local.pop_front(); loff = 0; active_tail = 2; }
        }
        if (d.net_valid_i && d.net_ready_o) { ++noff; if (d.net_last_i) { network.pop_front(); noff = 0; } }
        if (d.m_valid_o && d.m_ready_i) {
            current.push_back(d.m_data_o);
            if (d.m_last_o) { got.push_back(current); current.clear(); }
        }
        d.clk_i = 1; d.eval(); ++cycle;
    }
    void run(unsigned n) { while (n--) tick(); }
};
int main(int argc, char **argv)
{
    Verilated::commandArgs(argc, argv);
    const uint64_t device = 0x024B4C000101ull;
    // Deliver each destination and boundary separately so FIFO pressure cannot
    // conceal a broken length or destination rule.
    for (uint64_t dst : std::vector<uint64_t>{device, 0xFFFFFFFFFFFFull, 0x91E0F0010000ull, 0x001122334455ull}) {
        for (size_t length : {size_t(60), size_t(61), size_t(1514), size_t(1515)}) {
            Bench b; b.stall = true;
            const auto f = frame(dst, length, 17); b.local.push_back(f); b.run(6000);
            const bool accept = dst == device || ((dst >> 40) & 1);
            CHECK(b.got == (accept ? std::vector<Bytes>{f} : std::vector<Bytes>{}),
                  "computer to device receiver: destination %llx length %zu",
                  static_cast<unsigned long long>(dst), length);
        }
    }
    // The same network stream, with or without local copies, must remain whole.
    // In the idle-local control, every accepted byte goes through on that cycle.
    for (bool with_local : {false, true}) {
        Bench b; b.stall = true; b.only_network = !with_local;
        std::vector<Bytes> expected;
        for (int i = 0; i < 12; ++i) {
            auto f = frame(device, 60 + i, uint8_t(90 + i)); b.network.push_back(f); expected.push_back(f);
        }
        if (with_local) {
            b.local.push_back(frame(device, 1515, 44));
            expected.push_back(frame(device, 1515, 44));
        }
        b.run(8000);
        CHECK(b.got == expected, "network control priority and whole local delivery");
    }
    {
        Bench b;
        const auto local = frame(device, 1515, 44);
        const auto net = frame(device, 61, 77);
        b.local.push_back(local); b.run(230);
        b.hold = true; b.run(3);
        b.network.push_back(net); b.run(20);
        b.hold = false; b.run(4000);
        CHECK(b.got == std::vector<Bytes>({local, net}), "network arrival cannot interrupt a local frame");
    }
    // A transmit-domain reset can revoke an injection before its final beat.
    // Keep a completed local frame stalled at the receiver while cancelling
    // the next one, then require a fresh local frame and network traffic intact.
    for (unsigned beats : {1u, 2u, 3u, 4u, 189u}) {
        Bench b; b.hold = true;
        const auto kept = frame(device, 61, 31);
        const auto after = frame(device, 60, 52);
        const auto net = frame(device, 62, 77);
        b.local.push_back(kept); b.run(20);
        b.local.push_back(frame(device, 1515, 99)); b.run(beats);
        b.local.clear(); b.loff = 0;
        b.network.push_back(net); b.run(20);
        b.local.push_back(after); b.run(20);
        b.hold = false; b.run(4000);
        CHECK(b.got == std::vector<Bytes>({kept, net, after}),
              "aborted local copy preserves completed frames and restarts at the next header: %u beats", beats);
        CHECK(b.d.copied_o == 2, "aborted local copy never commits a descriptor");
    }
    Bench b; b.hold = true;
    for (int i = 0; i < 16; ++i) b.local.push_back(frame(device, 1000, uint8_t(i)));
    b.run(4000);
    CHECK(b.d.full_o > 0, "local receive overflow is counted");
    const auto kept = b.d.copied_o;
    b.hold = false; b.run(16000);
    CHECK(b.got.size() == kept, "local receive overflow preserves complete retained frames");
    for (size_t i = 0; i < b.got.size(); ++i)
        CHECK(b.got[i] == frame(device, 1000, uint8_t(i)), "local receive overflow preserves bytes");
    std::printf("%d checks: %d PASS, %d FAIL\n", checks(), checks() - fails(), fails());
    return fails() != 0;
}
