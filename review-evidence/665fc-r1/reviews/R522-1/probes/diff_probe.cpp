// diff_probe.cpp - reviewer probe for PR #685 (#665 lane FC), round R522-1.
//
// A randomized differential of the full-tuple ingress filter: the same frame
// stream offered to the RTL (KL_mbx behind KL_mbx_wb, tb_mbx_top HOST_P=0) and
// to the firmware's host model (mbx_model.c), each graded against a reference
// written from the owner's table (REQUIREMENTS.md section 1; #664 comment
// 6014311316), not from the generated contract tables. Per frame it compares:
// the channel the frame reached (RX_PASS), its record bytes and IF, RX_DROP,
// and FILTER_MISMATCH. Then three directed probes: FILTER_MISMATCH saturation
// at 0xFFFF, a short frame directly after a mismatch, and a reset during a
// mismatching frame.
//
// Build: see run_diff_probe.sh. Exit 0 = every comparison agreed.

#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <memory>
#include <random>
#include <vector>

#include "../../common/verilator_harness.hpp"
#include "Vtb_mbx_top.h"
#include "bench.hpp"
#include "mbx_contract.h"
#include "mbx_model.h"
#include "verilated.h"

namespace {

constexpr std::uint64_t kEid = 0x0011223344556677ull;
constexpr std::uint64_t kOther = 0x7766554433221100ull;
constexpr std::uint64_t kMac0 = 0x001B92000001ull;   // interface i owns kMac0 + i
constexpr std::uint64_t kMaapBase = 0x91E000000100ull;
constexpr std::uint16_t kMaapCount = 8;

// Requirement table addresses, typed in from REQUIREMENTS.md section 1.
constexpr std::uint64_t kAdpAcmp = 0x91E0F0010000ull;
constexpr std::uint64_t kMaap = 0x91E0F000FF00ull;
constexpr std::uint64_t kMsrp = 0x0180C200000Eull;
constexpr std::uint64_t kMvrp = 0x0180C2000021ull;

const std::uint32_t kRxBase[MBX_N_CH] = MBX_CH_RX_BASE_TBL;
const std::uint32_t kRxWords[MBX_N_CH] = MBX_CH_RX_WORDS_TBL;

std::uint64_t be(const std::vector<std::uint8_t>& f, std::size_t at, unsigned n) {
    std::uint64_t v = 0;
    for (unsigned i = 0; i < n; ++i) v = (v << 8) | f[at + i];
    return v;
}
void put(std::vector<std::uint8_t>& f, std::size_t at, std::uint64_t v, unsigned n) {
    for (unsigned i = 0; i < n; ++i) f[at + i] = static_cast<std::uint8_t>(v >> (8 * (n - 1 - i)));
}

struct Expect {
    int ch = -1;         // channel reached, -1 none
    bool drop = false;   // RX_DROP (passed filter, too long)
    bool mis = false;    // FILTER_MISMATCH moved
};

// The reference, from the requirement text. Frames are kept below every
// channel's ring and rate limits by the driver, so only size can drop.
Expect reference(const std::vector<std::uint8_t>& f, unsigned iface) {
    Expect e;
    const std::size_t len = f.size();
    if (len < 15) return e;                                   // no PDU byte 14
    const std::uint64_t dst = be(f, 0, 6);
    const std::uint64_t et = be(f, 12, 2);
    const unsigned st = f[14];
    const bool own_ok = iface < MBX_N_IF;
    const std::uint64_t own = kMac0 + iface;
    int ch = -1;
    if (dst == kAdpAcmp && et == 0x22F0 && st == 0xFA) ch = 0;
    else if ((dst == kAdpAcmp || (own_ok && dst == own)) && et == 0x22F0 && st == 0xFC) ch = 1;
    else if (own_ok && dst == own && et == 0x22F0 && st == 0xFB) ch = 2;
    else if (dst == kMaap && et == 0x22F0 && st == 0xFE) ch = 3;
    else if ((dst == kMsrp && et == 0x22EA) || (dst == kMvrp && et == 0x88F5)) ch = 4;
    if (ch < 0) {
        e.mis = et == 0x22F0 || et == 0x22EA || et == 0x88F5;
        return e;
    }
    const unsigned msg = len > 15 ? (f[15] & 0x0Fu) : 0u;
    bool id = false;
    switch (ch) {
    case 0:
        id = msg == 2 && len >= 26 && (be(f, 18, 8) == 0 || be(f, 18, 8) == kEid);
        break;
    case 1:
        id = (len >= 42 && be(f, 34, 8) == kEid) || (len >= 50 && be(f, 42, 8) == kEid);
        break;
    case 2:
        id = ((msg & 1u) == 0 && len >= 26 && be(f, 18, 8) == kEid) ||
             ((msg & 1u) == 1 && len >= 34 && be(f, 26, 8) == kEid);
        break;
    case 3: {
        if (msg >= 1 && msg <= 3 && len >= 34) {
            const std::uint64_t start = be(f, 26, 6);
            const std::uint64_t count = be(f, 32, 2);
            id = count != 0 && start <= kMaapBase + kMaapCount - 1 && kMaapBase <= start + count - 1;
        }
        break;
    }
    default:
        id = true;
    }
    if (!id) return e;
    const std::uint32_t maxb[MBX_N_CH] = MBX_CH_MAX_FRAME_BYTES_TBL;   // size limits are not the filter's rule
    if (len > maxb[ch]) {
        e.drop = true;
        e.ch = -1;
        return e;
    }
    e.ch = ch;
    return e;
}

std::uint32_t ch_reg(unsigned c, std::uint32_t r) { return MBX_CH_BASE + MBX_CH_STRIDE * c + r; }
std::uint32_t iff(unsigned i, std::uint32_t r) { return MBX_IFF_BASE + MBX_IFF_STRIDE * i + r; }

// One side: the RTL bench or the model, behind the same register calls.
struct Side {
    virtual ~Side() = default;
    virtual std::uint32_t rd(std::uint32_t off) = 0;
    virtual void wr(std::uint32_t off, std::uint32_t v) = 0;
    virtual void frame(const std::vector<std::uint8_t>& f, unsigned iface) = 0;
    virtual void ms(unsigned n) = 0;
    virtual void reset() = 0;
    void up() {
        wr(MBX_REG_OWN_EID_LO, static_cast<std::uint32_t>(kEid));
        wr(MBX_REG_OWN_EID_HI, static_cast<std::uint32_t>(kEid >> 32));
        for (unsigned i = 0; i < MBX_N_IF; ++i) {
            wr(iff(i, MBX_IFF_REG_OWN_MAC_LO), static_cast<std::uint32_t>(kMac0 + i));
            wr(iff(i, MBX_IFF_REG_OWN_MAC_HI), static_cast<std::uint32_t>((kMac0 + i) >> 32));
        }
        wr(MBX_REG_MAAP_BASE_LO, static_cast<std::uint32_t>(kMaapBase));
        wr(MBX_REG_MAAP_BASE_HI, static_cast<std::uint32_t>(kMaapBase >> 32));
        wr(MBX_REG_MAAP_COUNT, kMaapCount);
        wr(MBX_REG_FILTER_EN, (1u << MBX_N_CH) - 1u);
    }
    std::uint32_t tail[MBX_N_CH] = {};
    // Offer one frame: which channel's RX_PASS moved, its record, and counters.
    struct Got {
        int ch = -1;
        int moved = 0;
        bool drop = false;
        std::uint32_t mis = 0;
        std::vector<std::uint8_t> bytes;
        std::uint32_t rec_if = 0;
    };
    Got offer(const std::vector<std::uint8_t>& f, unsigned iface) {
        std::uint32_t pass[MBX_N_CH], drop[MBX_N_CH];
        for (unsigned c = 0; c < MBX_N_CH; ++c) {
            pass[c] = rd(ch_reg(c, MBX_CH_REG_RX_PASS));
            drop[c] = rd(ch_reg(c, MBX_CH_REG_RX_DROP));
        }
        const std::uint32_t m0 = rd(MBX_REG_FILTER_MISMATCH);
        frame(f, iface);
        Got g;
        g.mis = (rd(MBX_REG_FILTER_MISMATCH) - m0) & 0xFFFFu;
        for (unsigned c = 0; c < MBX_N_CH; ++c) {
            if (rd(ch_reg(c, MBX_CH_REG_RX_PASS)) != pass[c]) {
                g.ch = static_cast<int>(c);
                ++g.moved;
            }
            if (rd(ch_reg(c, MBX_CH_REG_RX_DROP)) != drop[c]) g.drop = true;
        }
        if (g.ch >= 0) {
            const unsigned c = static_cast<unsigned>(g.ch);
            const std::uint32_t mask = kRxWords[c] - 1u;
            const std::uint32_t w0 = rd(kRxBase[c] + 4u * (tail[c] & mask));
            const std::uint32_t len = w0 & 0xFFFFu;
            g.rec_if = (w0 >> MBX_RXREC_W0_IF_LSB) & ((1u << MBX_RXREC_W0_IF_WIDTH) - 1u);
            for (std::uint32_t k = 0; k < len; ++k) {
                const std::uint32_t w = rd(kRxBase[c] + 4u * ((tail[c] + 2u + k / 4u) & mask));
                g.bytes.push_back(static_cast<std::uint8_t>(w >> (8u * (k % 4u))));
            }
            tail[c] = (tail[c] + 2u + (len + 3u) / 4u) & 0xFFFFu;
            wr(ch_reg(c, MBX_CH_REG_RX_TAIL), tail[c]);
        }
        ms(20);   // a token for every bucket: the rate limiter is out of this probe
        return g;
    }
};

struct RtlSide : Side {
    mbx_tb::Bench& b;
    explicit RtlSide(mbx_tb::Bench& bench) : b(bench) {}
    std::uint32_t rd(std::uint32_t off) override { return b.read(off); }
    void wr(std::uint32_t off, std::uint32_t v) override { b.write(off, v); }
    void frame(const std::vector<std::uint8_t>& f, unsigned iface) override {
        b.send_frame(f, iface);
        b.drain_rx(8000);
    }
    void ms(unsigned n) override { b.ms(n); }
    void reset() override {
        b.reset();
        for (auto& t : tail) t = 0;
    }
};

struct ModelSide : Side {
    mbx_model* m;
    explicit ModelSide(mbx_model* model) : m(model) {}
    std::uint32_t rd(std::uint32_t off) override { return mbx_model_read(m, off); }
    void wr(std::uint32_t off, std::uint32_t v) override { mbx_model_write(m, off, v, 0xF); }
    void frame(const std::vector<std::uint8_t>& f, unsigned iface) override {
        (void)mbx_model_rx(m, f.data(), f.size(), iface);
    }
    void ms(unsigned n) override { mbx_model_advance_ms(m, n); }
    void reset() override {
        mbx_model_reset(m);
        for (auto& t : tail) t = 0;
    }
};

// A frame built near the table: a valid row, then each tuple and identity
// element drawn from values on and around the rule.
std::vector<std::uint8_t> draw_free(std::mt19937_64& r, unsigned& iface);

// A valid frame of one table row, then (half the time) one element changed.
std::vector<std::uint8_t> draw(std::mt19937_64& r, unsigned& iface) {
    if (r() % 3 == 0) return draw_free(r, iface);
    const unsigned row = static_cast<unsigned>(r() % 8);
    iface = static_cast<unsigned>(r() % MBX_N_IF);
    std::vector<std::uint8_t> f(row == 6 || row == 7 ? 40 : 70, 0);
    put(f, 6, 0x0011223344A5ull, 6);
    const std::uint64_t own = kMac0 + iface;
    switch (row) {
    case 0: put(f, 0, kAdpAcmp, 6); put(f, 12, 0x22F0, 2); f[14] = 0xFA; f[15] = 2;
            put(f, 18, r() % 2 ? 0 : kEid, 8); break;
    case 1: case 2: put(f, 0, row == 1 ? kAdpAcmp : own, 6); put(f, 12, 0x22F0, 2); f[14] = 0xFC;
            f[15] = static_cast<std::uint8_t>(r() % 16); put(f, 34, r() % 2 ? kEid : kOther, 8);
            put(f, 42, f[34] == 0 ? kEid : (r() % 2 ? kEid : kOther), 8); break;
    case 3: case 4: put(f, 0, own, 6); put(f, 12, 0x22F0, 2); f[14] = 0xFB;
            f[15] = static_cast<std::uint8_t>(2 * (r() % 8) + (row == 4 ? 1 : 0));
            put(f, 18, row == 3 ? kEid : kOther, 8); put(f, 26, row == 4 ? kEid : kOther, 8); break;
    case 5: f.resize(42); put(f, 0, kMaap, 6); put(f, 12, 0x22F0, 2); f[14] = 0xFE;
            f[15] = static_cast<std::uint8_t>(1 + r() % 3); put(f, 26, kMaapBase + 4, 6); put(f, 32, 4, 2); break;
    case 6: put(f, 0, kMsrp, 6); put(f, 12, 0x22EA, 2); f[14] = 0; break;
    default: put(f, 0, kMvrp, 6); put(f, 12, 0x88F5, 2); f[14] = 0; break;
    }
    if (r() % 2) {
        switch (r() % 9) {
        case 0: put(f, 0, std::initializer_list<std::uint64_t>{kAdpAcmp, kAdpAcmp + 1, kMaap, kMsrp, kMvrp, own,
                     own + 1, own ^ 0x800000000000ull, own ^ 1, 0x001B92000099ull}.begin()[r() % 10], 6); break;
        case 1: put(f, 12, std::initializer_list<std::uint64_t>{0x22F0, 0x22EA, 0x88F5, 0x88F7, 0x8100}.begin()[r() % 5], 2); break;
        case 2: f[14] = std::initializer_list<std::uint8_t>{0xFA, 0xFB, 0xFC, 0xFE, 0x02, 0x04, 0xFD}.begin()[r() % 7]; break;
        case 3: f[15] = static_cast<std::uint8_t>(r() % 16); break;
        case 4: { const std::size_t at = 18 + 8 * (r() % 4); if (at + 8 <= f.size()) put(f, at, r() % 2 ? kEid : kOther, 8); break; }
        case 5: f.resize(14 + r() % 40); break;
        case 6: { const std::uint8_t t[] = {0x81, 0x00, 0x60, 0x02}; f.insert(f.begin() + 12, t, t + 4); break; }
        case 7: iface = static_cast<unsigned>(r() % (1u << MBX_IF_W)); break;
        default: f[15] = static_cast<std::uint8_t>((f[15] & 0xF0u) | (r() % 16)); break;
        }
    }
    return f;
}

std::vector<std::uint8_t> draw_free(std::mt19937_64& r, unsigned& iface) {
    auto pick = [&](std::initializer_list<std::uint64_t> xs) {
        std::vector<std::uint64_t> v(xs);
        return v[r() % v.size()];
    };
    const std::uint64_t dsts[] = {kAdpAcmp, kAdpAcmp + 1, kMaap, kMsrp, kMvrp, kMac0, kMac0 + 1, kMac0 + 2,
                                  kMac0 ^ 0x010000000000ull, 0x001B92000099ull, 0xFFFFFFFFFFFFull, 0,
                                  kMac0 ^ 0x000100000000ull};
    const std::uint64_t ets[] = {0x22F0, 0x22F0, 0x22F0, 0x22EA, 0x88F5, 0x8100, 0x88A8, 0x88F7, 0x0800, 0x0000};
    const std::uint8_t sts[] = {0xFA, 0xFB, 0xFC, 0xFE, 0x02, 0x04, 0xFD, 0x00, 0x7F};
    std::size_t len;
    switch (r() % 6) {
    case 0: len = 1 + r() % 20; break;            // around the byte-14 boundary
    case 1: len = 24 + r() % 30; break;           // around the identity fields
    default: len = 50 + r() % 40; break;          // whole PDUs, some past MAAP's 64
    }
    std::vector<std::uint8_t> f(len < 64 ? 64 : len, 0);
    put(f, 0, dsts[r() % (sizeof dsts / sizeof dsts[0])], 6);
    put(f, 6, 0x0011223344A5ull, 6);
    const bool tag = r() % 8 == 0;
    put(f, 12, ets[r() % (sizeof ets / sizeof ets[0])], 2);
    f[14] = sts[r() % sizeof sts];
    f[15] = static_cast<std::uint8_t>(r() % 16);
    put(f, 18, pick({kEid, kOther, 0}), 8);
    put(f, 26, pick({kEid, kOther, 0, kMaapBase + 4, kMaapBase + 8, kMaapBase - 2}), 8);
    if (r() % 2) put(f, 32, pick({0, 1, 2, 4}), 2);
    put(f, 34, pick({kEid, kOther}), 8);
    put(f, 42, pick({kEid, kOther}), 8);
    f.resize(len);
    if (tag && f.size() >= 12) {   // insert an 802.1Q tag after the source address
        const std::uint8_t t[] = {static_cast<std::uint8_t>(r() % 2 ? 0x81 : 0x88), static_cast<std::uint8_t>(r() % 2 ? 0x00 : 0xA8), 0x60, 0x02};
        f.insert(f.begin() + 12, t, t + 4);
    }
    iface = static_cast<unsigned>(r() % (1u << MBX_IF_W));
    return f;
}

}  // namespace

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    const unsigned n = argc > 1 ? static_cast<unsigned>(std::atoi(argv[1])) : 20000u;
    const unsigned seed = argc > 2 ? static_cast<unsigned>(std::atoi(argv[2])) : 522u;
    const milan::tb::Model<Vtb_mbx_top> vm;
    mbx_tb::Bench bench(vm.get(), 0);
    RtlSide rtl(bench);
    auto model = std::make_unique<mbx_model>();
    ModelSide mod(model.get());
    rtl.reset();
    mod.reset();
    rtl.up();
    mod.up();
    std::mt19937_64 r(seed);
    unsigned bad = 0, delivered = 0, mism = 0, drops = 0, tagged = 0;
    unsigned per_ch[MBX_N_CH] = {};
    for (unsigned k = 0; k < n; ++k) {
        unsigned iface = 0;
        const auto f = draw(r, iface);
        const Expect e = reference(f, iface);
        const auto a = rtl.offer(f, iface);
        const auto b = mod.offer(f, iface);
        const bool ok_rtl = a.ch == e.ch && a.moved <= 1 && a.drop == e.drop && a.mis == (e.mis ? 1u : 0u) &&
                            (a.ch < 0 || (a.bytes == f && a.rec_if == iface));
        const bool ok_mod = b.ch == e.ch && b.moved <= 1 && b.drop == e.drop && b.mis == (e.mis ? 1u : 0u) &&
                            (b.ch < 0 || (b.bytes == f && b.rec_if == iface));
        if (f.size() >= 14 && (be(f, 12, 2) == 0x8100 || be(f, 12, 2) == 0x88A8)) {
            ++tagged;
            if (a.ch >= 0 || a.mis || b.ch >= 0 || b.mis) {
                std::printf("[FAIL] tagged frame reached a channel or the counter\n");
                ++bad;
            }
        }
        if (!ok_rtl || !ok_mod) {
            if (bad < 20) {
                std::printf("[FAIL] frame %u len %zu if %u: ref ch %d drop %d mis %d | rtl ch %d drop %d mis %u | "
                            "model ch %d drop %d mis %u\n",
                            k, f.size(), iface, e.ch, e.drop, e.mis, a.ch, a.drop, a.mis, b.ch, b.drop, b.mis);
            }
            ++bad;
        }
        if (e.ch >= 0) {
            ++delivered;
            ++per_ch[e.ch];
        }
        mism += e.mis;
        drops += e.drop;
    }
    std::printf("differential: %u frames, %u delivered (adp %u acmp %u aecp %u maap %u srp %u), %u mismatches, "
                "%u size drops, %u tagged; %u disagreement(s)\n",
                n, delivered, per_ch[0], per_ch[1], per_ch[2], per_ch[3], per_ch[4], mism, drops, tagged, bad);

    // Directed 1: a short frame straight after a mismatch counts nothing.
    {
        std::vector<std::uint8_t> m(40, 0), s(13, 0);
        put(m, 0, kAdpAcmp + 1, 6);
        put(m, 12, 0x22F0, 2);
        m[14] = 0xFA;
        put(s, 0, kAdpAcmp, 6);
        put(s, 12, 0x22F0, 1);
        for (Side* side : {static_cast<Side*>(&rtl), static_cast<Side*>(&mod)}) {
            const std::uint32_t before = side->rd(MBX_REG_FILTER_MISMATCH);
            side->frame(m, 0);
            side->frame(s, 0);
            std::vector<std::uint8_t> s14(14, 0);
            put(s14, 0, kMsrp + 5, 6);
            put(s14, 12, 0x22EA, 2);
            side->frame(s14, 0);
            const std::uint32_t got = (side->rd(MBX_REG_FILTER_MISMATCH) - before) & 0xFFFFu;
            const bool ok = got == 1u;
            std::printf("[%s] %s: a mismatch, then a 13- and a 14-byte control frame, count %u (want 1)\n",
                        ok ? "ok" : "FAIL", side == &rtl ? "rtl" : "model", got);
            bad += !ok;
        }
    }
    // Directed 2: reset in the middle of a mismatching frame clears the
    // counter and the partial frame does not count after reset.
    {
        std::vector<std::uint8_t> m(60, 0);
        put(m, 0, 0x001B92000099ull, 6);
        put(m, 12, 0x22F0, 2);
        m[14] = 0xFB;
        bench.send_frame(m, 0);
        bench.idle(20);   // past byte 14, before the last byte
        rtl.reset();
        bench.drain_rx(8000);   // the remaining bytes of the old frame arrive as a new frame of 40 bytes
        const std::uint32_t got = bench.read(MBX_REG_FILTER_MISMATCH);
        // the tail bytes (from byte 20 on) form a frame whose byte 12/13 are zero: no control EtherType
        const bool ok = got == 0u;
        std::printf("[%s] rtl: reset during a mismatching frame leaves FILTER_MISMATCH %u (want 0)\n",
                    ok ? "ok" : "FAIL", got);
        bad += !ok;
        rtl.up();
    }
    // Directed 3: saturation at 0xFFFF on both.
    {
        std::vector<std::uint8_t> m(15, 0);
        put(m, 0, kAdpAcmp + 1, 6);
        put(m, 12, 0x22F0, 2);
        m[14] = 0xFA;
        rtl.reset();
        mod.reset();
        for (unsigned k = 0; k < 0x10004u; ++k) {
            bench.send_frame(m, 0);
            if ((k & 255u) == 255u) bench.drain_rx(1u << 16);
            (void)mbx_model_rx(model.get(), m.data(), m.size(), 0);
        }
        bench.drain_rx(1u << 16);
        const std::uint32_t a = bench.read(MBX_REG_FILTER_MISMATCH);
        const std::uint32_t b = mbx_model_read(model.get(), MBX_REG_FILTER_MISMATCH);
        const bool ok = a == 0xFFFFu && b == 0xFFFFu;
        std::printf("[%s] 65540 mismatches saturate FILTER_MISMATCH: rtl %#x model %#x (want 0xffff)\n",
                    ok ? "ok" : "FAIL", a, b);
        bad += !ok;
    }
    std::printf("RESULT: %s (%u failure(s))\n", bad ? "FAIL" : "PASS", bad);
    return bad ? 1 : 0;
}
