// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// KL_usbnet_tap (#1011): the receive copy's classes, the transmit drops, the
// best-effort-only injection with its rate limit, and the frame-end account.
// Each case states the rule it checks; mutants.py plants one defect per rule
// and requires this harness to fail on each.
//
// Clocks: the system clock (the tap's) at 10 time units, the MAC's transmit
// clock at 14. The MAC model takes beats at the core input, holds each frame
// for a fixed pipeline delay and sends it octet by octet on the transmit
// clock, pulsing eth_end_i on its last octet.

#include "VKL_usbnet_tap.h"
#include "verilated.h"

#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <deque>
#include <functional>
#include <map>
#include <memory>
#include <string>
#include <vector>

using Bytes = std::vector<uint8_t>;

static int &fails() { static int n = 0; return n; }
#define CHECK(c, ...) do { if (!(c)) { std::printf("FAIL %s:%d: ", __FILE__, __LINE__); \
    std::printf(__VA_ARGS__); std::printf("\n"); ++fails(); } } while (0)

// ---------------------------------------------------------------------------
//  Frames
// ---------------------------------------------------------------------------
using Mac = uint64_t;
static const Mac HOST   = 0x0A1234567890ull;   // locally administered, individual
static const Mac DEVICE = 0x024B4C000101ull;   // the boards' own prefix
static const Mac PEER   = 0x001B21AABBCCull;
static const Mac BCAST  = 0xFFFFFFFFFFFFull;
static const Mac ADP_MC = 0x91E0F0010000ull;
static const Mac AAF_MC = 0x91E0F000FE01ull;
static const Mac GPTP   = 0x0180C200000Eull;
static const Mac LLDP   = 0x0180C200000Eull;
static const Mac MVRP   = 0x0180C2000021ull;
static const Mac MMRP   = 0x0180C2000020ull;
static const Mac IP_MC  = 0x01005E000001ull;

static void put_mac(Bytes &b, Mac m) { for (int i = 5; i >= 0; --i) b.push_back(uint8_t(m >> (8 * i))); }

struct Tag { int pcp; int vid; uint16_t tpid; };

static Bytes frame(Mac dst, Mac src, uint16_t etype, int len, int subtype = -1,
                   std::vector<Tag> tags = {}, uint8_t seed = 1)
{
    Bytes b;
    put_mac(b, dst);
    put_mac(b, src);
    for (const Tag &t : tags) {
        b.push_back(uint8_t(t.tpid >> 8)); b.push_back(uint8_t(t.tpid));
        uint16_t tci = uint16_t((t.pcp << 13) | (t.vid & 0xFFF));
        b.push_back(uint8_t(tci >> 8)); b.push_back(uint8_t(tci));
    }
    b.push_back(uint8_t(etype >> 8)); b.push_back(uint8_t(etype));
    if (subtype >= 0) b.push_back(uint8_t(subtype));
    uint8_t x = seed;
    while (static_cast<int>(b.size()) < len) { x = uint8_t(x * 13 + 7); b.push_back(x); }
    b.resize(len);
    return b;
}

// ---------------------------------------------------------------------------
//  Reference rules (independent of the RTL's spelling)
// ---------------------------------------------------------------------------
static Mac rd_mac(const Bytes &b, int at) { Mac m = 0; for (int i = 0; i < 6; ++i) m = (m << 8) | b[at + i]; return m; }
static bool reserved(Mac d) { Mac top = d >> 4; return top == 0x0180C200000ull || top == 0x0180C200002ull; }

struct Look { bool shape, stream, tagged; int pcp; };
static Look look(const Bytes &b)
{
    Look l{false, false, false, 0};
    if (b.size() < 14) { l.shape = true; return l; }
    uint16_t et = uint16_t(b[12] << 8 | b[13]);
    if (et == 0x8100 || et == 0x88A8) {
        l.tagged = true;
        if (b.size() < 19) { l.shape = true; return l; }
        l.pcp = b[14] >> 5;
        uint16_t it = uint16_t(b[16] << 8 | b[17]);
        if (it == 0x8100 || it == 0x88A8) { l.shape = true; return l; }
        l.stream = it == 0x22F0 && !(b[18] & 0x80);
    } else if (et == 0x22F0) {
        if (b.size() < 15) { l.shape = true; return l; }
        l.stream = !(b[14] & 0x80);
    }
    return l;
}

static bool want_copy(const Bytes &b, bool host_ok)
{
    if (!host_ok) return false;
    Look l = look(b);
    if (l.shape || l.stream) return false;
    Mac d = rd_mac(b, 0);
    if (!((d >> 40) & 1)) return d == HOST;
    return !reserved(d);
}

enum TxVerdict { TXV_PASS, TXV_SOURCE, TXV_LINKLOCAL, TXV_STREAM, TXV_PRIORITY, TXV_LENGTH, TXV_SHAPE };
static int want_tx(const Bytes &b, Mac host, bool host_ok)
{
    if (b.size() < 14) return TXV_LENGTH;
    Look l = look(b);
    if (l.shape && !l.tagged) return TXV_LENGTH;
    if (l.tagged && b.size() < 19) return TXV_LENGTH;
    if (b.size() > 1518) return TXV_LENGTH;
    if (!host_ok || rd_mac(b, 6) != host) return TXV_SOURCE;
    if (reserved(rd_mac(b, 0))) return TXV_LINKLOCAL;
    if (l.shape) return TXV_SHAPE;
    if (l.stream) return TXV_STREAM;
    if (l.tagged && l.pcp > 1) return TXV_PRIORITY;
    return TXV_PASS;
}

// ---------------------------------------------------------------------------
//  The bench
// ---------------------------------------------------------------------------
struct Sent { Bytes b; uint64_t first; bool lo; };

struct Bench {
    std::unique_ptr<VKL_usbnet_tap> model;
    VKL_usbnet_tap *d;
    uint64_t tsys = 0;
    uint64_t teth = 0;
    uint64_t ncyc = 0;
    uint64_t necyc = 0;
    // stimulus
    std::deque<Bytes> rx_q;                     // frames the device receives
    size_t rx_off = 0;
    std::deque<std::pair<uint64_t, Bytes>> hi_q; // datapath frames, with their release cycle
    size_t hi_off = 0;
    std::deque<uint16_t> dn_q;                  // bus words from the computer
    bool up_ready = true;
    bool m_stall = false;
    bool m_hold = false;
    unsigned rnd = 12345;
    // observation
    std::vector<uint16_t> up_words;
    std::vector<Sent> out;                      // frames at the MAC core input
    Bytes cur; bool cur_lo = false; uint64_t cur_first = 0;
    std::vector<int> rx_verdicts;
    std::vector<int> tx_verdicts;
    std::vector<uint64_t> hi_release; // per datapath frame
    std::vector<uint64_t> hi_start;
    // the MAC model, transmit clock side
    std::deque<std::pair<uint64_t, int>> mac_q; // (ready eth cycle, octets on the wire)
    int mac_left = 0; bool end_pulse = false;
    uint32_t tgl_flips = 0; uint8_t last_tgl = 0;
    unsigned hi_in_mac_max = 0;
    bool lo_overlap = false;                    // an injected frame shared the MAC with a datapath frame
    int in_mac_hi = 0;
    int in_mac_lo = 0;
    bool prev_inj = false;
    bool prev_hi_valid = false;

    Bench() : model(std::make_unique<VKL_usbnet_tap>()), d(model.get()) {
        d->clk_i = 0; d->eth_clk_i = 0; d->rst_ni = 0; d->eth_rst_ni = 0;
        d->inject_en_i = 1; d->bus_alive_i = 1; d->m_ready_i = 1; d->up_ready_i = 1;
        d->eval();
        for (int i = 0; i < 8; ++i) step();
        d->rst_ni = 1; d->eth_rst_ni = 1;
        for (int i = 0; i < 8; ++i) step();
        last_tgl = d->txend_tgl_o;
    }
    unsigned rand_() { rnd = rnd * 1103515245u + 12345u; return (rnd >> 16) & 0x7FFF; }

    void drive_sys() {
        // receive stream
        d->rx_valid_i = 0; d->rx_last_i = 0;
        if (!rx_q.empty() && (rand_() % 4)) {
            const Bytes &f = rx_q.front();
            uint64_t w = 0; uint8_t k = 0;
            // octets past the frame's end carry garbage, as a MAC may leave them
            for (int i = 0; i < 8; ++i) {
                bool in = rx_off + i < f.size();
                w |= uint64_t(in ? f[rx_off + i] : 0xA5) << (8 * i);
                if (in) k |= uint8_t(1u << i);
            }
            d->rx_valid_i = 1; d->rx_data_i = w; d->rx_keep_i = k;
            d->rx_last_i = rx_off + 8 >= f.size();
        }
        // datapath stream: gapless once released, as the store-and-forward FIFO
        d->hi_valid_i = 0; d->hi_last_i = 0; d->hi_be_i = 0;
        if (!hi_q.empty() && hi_q.front().first <= ncyc) {
            const Bytes &f = hi_q.front().second;
            uint64_t w = 0; int n = 0;
            for (int i = 0; i < 8 && hi_off + i < f.size(); ++i) { w |= uint64_t(f[hi_off + i]) << (8 * i); ++n; }
            d->hi_valid_i = 1; d->hi_data_i = w;
            d->hi_last_i = hi_off + 8 >= f.size();
            d->hi_be_i = d->hi_last_i ? uint8_t(1u << (n - 1)) : 0;
        }
        d->dn_valid_i = !dn_q.empty() && (rand_() % 5);
        d->dn_data_i = dn_q.empty() ? 0 : dn_q.front();
        d->up_ready_i = up_ready && (rand_() % 3);
        d->m_ready_i = !m_hold && !(m_stall && (rand_() % 8 == 0));
    }

    void sample_sys() {
        if (d->rx_valid_i) {
            rx_off += 8;
            if (d->rx_last_i) { rx_q.pop_front(); rx_off = 0; }
        }
        if (d->hi_valid_i && d->hi_ready_o) {
            if (hi_off == 0) hi_release.push_back(hi_q.front().first);
            hi_off += 8;
            if (d->hi_last_i) { hi_q.pop_front(); hi_off = 0; }
        }
        if (d->dn_valid_i && d->dn_ready_o) dn_q.pop_front();
        if (d->up_valid_o && d->up_ready_i) up_words.push_back(d->up_data_o);
        if (d->rx_verdict_valid_o) rx_verdicts.push_back(d->rx_verdict_o);
        if (d->tx_verdict_valid_o) tx_verdicts.push_back(d->tx_verdict_o);
        // the core's transmit input takes a frame with no gap inside it
        if (!cur.empty() && d->m_ready_i && !d->m_valid_o) { CHECK(false, "no gap inside a frame"); cur.clear(); }
        // the datapath wins every arbitration: an injection is granted only
        // in a clock where no datapath frame was offered
        if (d->inj_active_o && !prev_inj) CHECK(!prev_hi_valid, "the datapath wins every arbitration");
        prev_inj = d->inj_active_o; prev_hi_valid = d->hi_valid_i;
        if (d->m_valid_o && d->m_ready_i) {
            bool lo = !d->hi_ready_o;   // the datapath was not the one accepted
            if (cur.empty()) { cur_first = ncyc; cur_lo = lo; if (!lo) hi_start.push_back(ncyc); }
            int n = 8;
            if (d->m_last_o) {
                CHECK(d->m_be_o && !(d->m_be_o & (d->m_be_o - 1)), "last beat be is one-hot (%02x)", d->m_be_o);
                n = d->m_be_o ? __builtin_ctz(d->m_be_o) + 1 : 8;
            } else {
                CHECK(d->m_be_o == 0, "be is zero before the last beat");
            }
            for (int i = 0; i < n; ++i) cur.push_back(uint8_t(d->m_data_o >> (8 * i)));
            if (d->m_last_o) {
                out.push_back({cur, cur_first, cur_lo});
                int wire = int(std::max<size_t>(cur.size(), 60) + 24);
                mac_q.push_back({necyc + 30, wire});
                if (cur_lo) { if (in_mac_hi) lo_overlap = true; ++in_mac_lo; }
                else { if (in_mac_lo) lo_overlap = true; ++in_mac_hi; }
                cur.clear();
            }
        }
    }

    void eth_edge() {
        end_pulse = false;
        if (mac_left == 0 && !mac_q.empty() && mac_q.front().first <= necyc) {
            mac_left = mac_q.front().second; mac_q.pop_front();
        }
        if (mac_left > 0 && --mac_left == 0) {
            end_pulse = true;
            // the oldest frame in the MAC ends
            size_t inm = size_t(in_mac_hi + in_mac_lo);
            if (inm > 0 && inm <= out.size()) {
                size_t k = out.size() - inm;
                if (out[k].lo) --in_mac_lo; else --in_mac_hi;
            }
        }
        d->eth_end_i = end_pulse;
    }

    void step() {
        // the next edge of whichever clock comes first
        uint64_t ns = tsys + 5;
        uint64_t ne = teth + 7;
        if (ns <= ne) {
            tsys = ns; d->clk_i = !d->clk_i; d->eval();
            if (d->clk_i) ++ncyc;
            else drive_sys();
        } else {
            teth = ne; d->eth_clk_i = !d->eth_clk_i;
            d->eval();
            if (!d->eth_clk_i) { eth_edge(); ++necyc; }
            if (d->txend_tgl_o != last_tgl) { ++tgl_flips; last_tgl = d->txend_tgl_o; }
        }
        d->eval();
    }

    void cycles(uint64_t n) {
        uint64_t end = ncyc + n;
        while (ncyc < end) {
            // sample just before the rising edge, then let it rise
            if (!d->clk_i && tsys + 5 <= teth + 7) sample_sys();
            step();
        }
    }

    // ---- bus records --------------------------------------------------------
    void rec(int type, const Bytes &p) {
        dn_q.push_back(uint16_t((type << 12) | (p.size() & 0xFFF)));
        for (size_t i = 0; i < p.size(); i += 2)
            dn_q.push_back(uint16_t(p[i] | ((i + 1 < p.size() ? p[i + 1] : 0) << 8)));
    }
    void host(Mac m, uint16_t state) {
        Bytes p; put_mac(p, m); p.push_back(uint8_t(state)); p.push_back(uint8_t(state >> 8));
        rec(1, p);
    }
    void raw_hdr(uint16_t w) { dn_q.push_back(w); }
    void drain_dn() { for (int i = 0; i < 200000 && !dn_q.empty(); ++i) cycles(1); cycles(20); }

    // records seen toward the computer, parsed
    std::vector<Bytes> up_frames(bool *ok) {
        std::vector<Bytes> r; size_t i = 0; *ok = true;
        while (i < up_words.size()) {
            uint16_t h = up_words[i++];
            if ((h >> 12) != 0) { *ok = false; break; }
            int len = h & 0xFFF; Bytes f;
            for (int k = 0; k < (len + 1) / 2; ++k) {
                if (i >= up_words.size()) { *ok = false; return r; }
                uint16_t w = up_words[i++];
                f.push_back(uint8_t(w));
                if (static_cast<int>(f.size()) < len) f.push_back(uint8_t(w >> 8));
                else if (w >> 8) *ok = false;   // the pad octet is zero
            }
            r.push_back(f);
        }
        return r;
    }
    ~Bench() { d->final(); }
};

using BenchPtr = std::unique_ptr<Bench>;
static BenchPtr mk() { return std::make_unique<Bench>(); }
static void done(BenchPtr &b) { b.reset(); }

// ---------------------------------------------------------------------------
//  Cases
// ---------------------------------------------------------------------------
static void host_record()
{
    BenchPtr b = mk();
    CHECK(!b->d->host_ok_o && !b->d->usb_ok_o, "no computer at reset");
    b->host(HOST, 0x0003); b->drain_dn();
    CHECK(b->d->host_ok_o && b->d->host_mac_o == HOST, "host record sets the address (%012llx)",
          static_cast<unsigned long long>(b->d->host_mac_o));
    CHECK(b->d->host_state_o == 0x0003, "state word kept");
    CHECK(b->d->usb_ok_o, "LD1 input: SuperSpeed, fresh, bus alive");
    b->d->bus_alive_i = 0; b->cycles(4);
    CHECK(!b->d->usb_ok_o, "LD1 input needs the bus clock");
    b->d->bus_alive_i = 1; b->cycles(4);
    b->host(HOST, 0x0002); b->drain_dn();
    CHECK(!b->d->usb_ok_o, "LD1 input needs SuperSpeed");
    b->host(HOST, 0x0003); b->drain_dn();
    CHECK(b->d->usb_ok_o, "back at SuperSpeed");
    b->cycles(3200);   // HOST_TIMEOUT_MS_P = 3 at 1 MHz
    CHECK(!b->d->usb_ok_o && b->d->host_ok_o, "a stale host record drops LD1, keeps the address");
    b->host(0x0B0000000001ull | (1ull << 40), 0x0003); b->drain_dn();
    CHECK(!b->d->host_ok_o, "a group address is refused");
    b->host(0x001B21000001ull, 0x0003); b->drain_dn();
    CHECK(!b->d->host_ok_o, "a universally administered address is refused");
    b->host(HOST, 0x0003); b->drain_dn();
    CHECK(b->d->host_ok_o, "accepted again");
    b->rec(2, {}); b->drain_dn();
    CHECK(!b->d->host_ok_o && !b->d->usb_ok_o && b->d->host_mac_o == 0, "detach clears the computer");
    CHECK(b->d->tx_skipped_o == 2, "the two refused addresses are counted (%u)", b->d->tx_skipped_o);
    done(b);
}

struct RxCase { const char *name; Bytes f; };

static void rx_classes()
{
    std::vector<RxCase> cs = {
        {"unicast to the computer",          frame(HOST, PEER, 0x0800, 98)},
        {"unicast to the device",            frame(DEVICE, PEER, 0x0800, 98)},
        {"unicast to another station",       frame(PEER, DEVICE, 0x0800, 98)},
        {"broadcast ARP",                    frame(BCAST, PEER, 0x0806, 60)},
        {"ADP multicast",                    frame(ADP_MC, PEER, 0x22F0, 82, 0xFA)},
        {"ACMP multicast",                   frame(ADP_MC, PEER, 0x22F0, 70, 0xFC)},
        {"MAAP multicast",                   frame(0x91E0F000FF00ull, PEER, 0x22F0, 60, 0xFE)},
        {"AECP unicast to the computer",     frame(HOST, DEVICE, 0x22F0, 100, 0xFB)},
        {"IPv4 multicast",                   frame(IP_MC, PEER, 0x0800, 77)},
        {"tagged IPv4 multicast",            frame(IP_MC, PEER, 0x0800, 81, -1, {{0, 2, 0x8100}})},
        {"tagged ADP",                       frame(ADP_MC, PEER, 0x22F0, 86, 0xFA, {{0, 2, 0x8100}})},
        {"tagged AAF stream",                frame(AAF_MC, PEER, 0x22F0, 300, 0x02, {{3, 2, 0x8100}})},
        {"untagged AAF stream",              frame(AAF_MC, PEER, 0x22F0, 300, 0x02)},
        {"CRF stream",                       frame(AAF_MC, PEER, 0x22F0, 100, 0x04, {{3, 2, 0x8100}})},
        {"CVF stream unicast to the computer", frame(HOST, PEER, 0x22F0, 200, 0x03)},
        {"experimental stream 0x7F",         frame(AAF_MC, PEER, 0x22F0, 90, 0x7F)},
        {"NTSCF control 0x82",               frame(AAF_MC, PEER, 0x22F0, 90, 0x82)},
        {"gPTP link-local",                  frame(GPTP, PEER, 0x88F7, 64)},
        {"LLDP link-local",                  frame(0x0180C2000000ull | 0x0E, PEER, 0x88CC, 64)},
        {"bridge group 01-80-C2-00-00-00",   frame(0x0180C2000000ull, PEER, 0x0027, 64)},
        {"MVRP",                             frame(MVRP, PEER, 0x88F5, 64)},
        {"MMRP",                             frame(MMRP, PEER, 0x88F6, 64)},
        {"01-80-C2-00-00-10 is not link-local", frame(0x0180C2000010ull, PEER, 0x0800, 64)},
        {"double tag",                       frame(BCAST, PEER, 0x0800, 80, -1, {{0, 2, 0x88A8}, {0, 3, 0x8100}})},
        {"odd length broadcast",             frame(BCAST, PEER, 0x0800, 61)},
        {"long broadcast",                   frame(BCAST, PEER, 0x0800, 1514)},
    };
    for (int attached = 0; attached < 2; ++attached) {
        BenchPtr b = mk();
        if (attached) { b->host(HOST, 3); b->drain_dn(); }
        std::vector<Bytes> want;
        for (auto &c : cs) { b->rx_q.push_back(c.f); if (want_copy(c.f, attached)) want.push_back(c.f); }
        for (int i = 0; i < 400000 && (!b->rx_q.empty() || b->up_words.size() < 1); ++i) b->cycles(1);
        b->cycles(20000);
        bool ok; auto got = b->up_frames(&ok);
        CHECK(ok, "records toward the computer are well formed");
        CHECK(got.size() == want.size(), "attached=%d: %zu copied, %zu expected", attached, got.size(), want.size());
        for (size_t i = 0; i < got.size() && i < want.size(); ++i)
            CHECK(got[i] == want[i], "attached=%d: copy %zu is octet-exact", attached, i);
        CHECK(b->rx_verdicts.size() == cs.size(), "one verdict per frame (%zu)", b->rx_verdicts.size());
        // name the class that went wrong
        for (size_t i = 0; i < cs.size() && i < b->rx_verdicts.size(); ++i) {
            bool copied = b->rx_verdicts[i] <= 1;
            CHECK(copied == want_copy(cs[i].f, attached), "attached=%d: %s: copied=%d", attached, cs[i].name, copied);
        }
        CHECK(b->d->rx_copied_o == want.size(), "copied counter");
        done(b);
    }
}

static void rx_full()
{
    BenchPtr b = mk();
    b->host(HOST, 3); b->drain_dn();
    b->up_ready = false;
    int n = 12;
    for (int i = 0; i < n; ++i) b->rx_q.push_back(frame(BCAST, PEER, 0x0800, 1000, -1, {}, uint8_t(i + 1)));
    for (int i = 0; i < 200000 && !b->rx_q.empty(); ++i) b->cycles(1);
    b->cycles(10);   // the last frame's verdict, past the copy's input register
    unsigned full = b->d->rx_full_o;
    CHECK(full > 0 && full < unsigned(n), "a full buffer drops whole frames (%u of %d)", full, n);
    b->up_ready = true;
    b->cycles(60000);
    bool ok; auto got = b->up_frames(&ok);
    CHECK(ok && got.size() == size_t(n) - full, "the frames kept come out whole (%zu)", got.size());
    // the kept frames are the first ones, octet-exact
    for (size_t i = 0; i < got.size(); ++i)
        CHECK(got[i] == frame(BCAST, PEER, 0x0800, 1000, -1, {}, uint8_t(i + 1)), "kept frame %zu exact", i);
    done(b);
}

struct TxCase { const char *name; Bytes f; };

static void tx_drops()
{
    BenchPtr b = mk();
    b->host(HOST, 3); b->drain_dn();
    std::vector<TxCase> cs = {
        {"unicast IPv4",                frame(PEER, HOST, 0x0800, 98)},
        {"AECP to the device",          frame(DEVICE, HOST, 0x22F0, 100, 0xFB)},
        {"ADP discover multicast",      frame(ADP_MC, HOST, 0x22F0, 82, 0xFA)},
        {"tagged best effort",          frame(PEER, HOST, 0x0800, 90, -1, {{0, 2, 0x8100}})},
        {"tagged background",           frame(PEER, HOST, 0x0800, 90, -1, {{1, 2, 0x8100}})},
        {"foreign source",              frame(PEER, PEER, 0x0800, 98)},
        {"the device's source",         frame(PEER, DEVICE, 0x0800, 98)},
        {"gPTP",                        frame(GPTP, HOST, 0x88F7, 64)},
        {"MSRP",                        frame(0x0180C200000Eull, HOST, 0x22EA, 64)},
        {"MVRP",                        frame(MVRP, HOST, 0x88F5, 64)},
        {"untagged AAF",                frame(AAF_MC, HOST, 0x22F0, 200, 0x02)},
        {"tagged AAF",                  frame(AAF_MC, HOST, 0x22F0, 200, 0x02, {{3, 2, 0x8100}})},
        {"CRF",                         frame(AAF_MC, HOST, 0x22F0, 100, 0x04)},
        {"tagged priority 3",           frame(PEER, HOST, 0x0800, 90, -1, {{3, 2, 0x8100}})},
        {"tagged priority 2",           frame(PEER, HOST, 0x0800, 90, -1, {{2, 2, 0x8100}})},
        {"tagged priority 7",           frame(PEER, HOST, 0x0800, 90, -1, {{7, 2, 0x8100}})},
        {"double tag",                  frame(PEER, HOST, 0x0800, 90, -1, {{0, 2, 0x88A8}, {0, 3, 0x8100}})},
        {"too long",                    frame(PEER, HOST, 0x0800, 1519)},
        {"longest",                     frame(PEER, HOST, 0x0800, 1518)},
        {"too short",                   frame(PEER, HOST, 0x0800, 13)},
        {"odd length",                  frame(PEER, HOST, 0x0800, 61)},
    };
    std::vector<Bytes> want; std::vector<int> wantv;
    for (auto &c : cs) {
        b->rec(0, c.f);
        int v = want_tx(c.f, HOST, true); wantv.push_back(v);
        if (v == TXV_PASS) want.push_back(c.f);
    }
    // an unknown record between frames keeps the parser in step
    b->rec(7, Bytes(33, 0xEE));
    Bytes after = frame(PEER, HOST, 0x0800, 70, -1, {}, 99);
    b->rec(0, after); wantv.push_back(TXV_PASS); want.push_back(after);
    b->drain_dn();
    b->cycles(200000);
    CHECK(b->tx_verdicts.size() == wantv.size(), "one verdict per frame record (%zu of %zu)",
          b->tx_verdicts.size(), wantv.size());
    for (size_t i = 0; i < wantv.size() && i < b->tx_verdicts.size(); ++i)
        CHECK(b->tx_verdicts[i] == wantv[i], "%s: verdict %d, expected %d",
              i < cs.size() ? cs[i].name : "after the unknown record", b->tx_verdicts[i], wantv[i]);
    std::vector<Bytes> got;
    for (auto &s : b->out) { CHECK(s.lo, "only injected frames here"); got.push_back(s.b); }
    CHECK(got.size() == want.size(), "%zu injected, %zu expected", got.size(), want.size());
    for (size_t i = 0; i < got.size() && i < want.size(); ++i) CHECK(got[i] == want[i], "injected frame %zu exact", i);
    CHECK(b->d->tx_skipped_o == 1, "the unknown record is counted");
    // no computer: nothing passes
    b->rec(2, {}); b->drain_dn();
    size_t before = b->out.size();
    b->rec(0, frame(PEER, HOST, 0x0800, 98)); b->drain_dn(); b->cycles(30000);
    CHECK(b->out.size() == before && b->tx_verdicts.back() == TXV_SOURCE, "after detach the source check refuses");
    // injection disabled: the frame waits, and leaves once enabled
    b->host(HOST, 3); b->drain_dn();
    b->d->inject_en_i = 0;
    b->rec(0, frame(PEER, HOST, 0x0800, 98)); b->drain_dn(); b->cycles(30000);
    CHECK(b->out.size() == before, "inject_en_i low holds the computer's frames");
    b->d->inject_en_i = 1; b->cycles(30000);
    CHECK(b->out.size() == before + 1, "and they leave once it rises");
    done(b);
}

// RATE: 800 kb/s at a 1 MHz clock: 0.1 octet per clock; burst 3200 octets.
static void tx_rate()
{
    BenchPtr b = mk();
    b->host(HOST, 3); b->drain_dn();
    const int n = 24;
    const int len = 1000;   // cost 1024 octets each
    for (int i = 0; i < n; ++i) b->rec(0, frame(PEER, HOST, 0x0800, len, -1, {}, uint8_t(i)));
    uint64_t t0 = b->ncyc;
    for (int i = 0; i < 600000 && b->out.size() < size_t(n); ++i) b->cycles(1);
    CHECK(b->out.size() == size_t(n), "every frame left (%zu)", b->out.size());
    if (b->out.size() < size_t(n)) { done(b); return; }
    // the burst (3 frames) leaves at once; the rest at the rate
    uint64_t span = b->out.back().first - b->out[3].first;
    double rate = double(n - 4) * 1024 * 8 / (double(span) / 1e6);   // bits per second
    std::printf("  rate: %d frames, steady %.0f b/s over %llu clocks (limit 800000)\n", n, rate,
                static_cast<unsigned long long>(span));
    CHECK(rate <= 800000 * 1.01, "the steady rate stays at the limit (%.0f)", rate);
    CHECK(rate >= 800000 * 0.95, "the limiter does not throttle below it (%.0f)", rate);
    uint64_t burst = b->out[2].first - t0;
    CHECK(b->out[3].first - b->out[2].first > 5000, "the fourth frame waits for tokens");
    (void)burst;
    done(b);
}

// BEST EFFORT ONLY. A class A-like datapath stream (a 100-octet frame every
// 1250 clocks: 125 us at 10 MHz scaled) with the computer saturating its
// rate limit. Checks: the datapath wins every arbitration, no injected frame
// shares the MAC with a datapath frame, a datapath frame waits at most one
// injected frame, the datapath frames leave in order and intact, and the
// frame-end toggle counts the datapath frames only.
static void tx_priority(bool stall)
{
    BenchPtr b = mk();
    b->m_stall = stall;
    b->host(HOST, 3); b->drain_dn();
    std::vector<Bytes> hi;
    const int n_hi = 120;
    for (int i = 0; i < n_hi; ++i) {
        hi.push_back(frame(AAF_MC, DEVICE, 0x22F0, 100 + (i % 7), 0x02, {{3, 2, 0x8100}}, uint8_t(i)));
        b->hi_q.push_back({uint64_t(2000 + 1250 * i), hi.back()});
    }
    for (int i = 0; i < 60; ++i) b->rec(0, frame(PEER, HOST, 0x0800, 1518, -1, {}, uint8_t(i)));
    for (int i = 0; i < 400000 && (!b->hi_q.empty() || !b->dn_q.empty()); ++i) b->cycles(1);
    b->cycles(20000);
    std::vector<Bytes> got_hi; size_t n_lo = 0;
    for (auto &s : b->out) { if (s.lo) ++n_lo; else got_hi.push_back(s.b); }
    CHECK(got_hi == hi, "the datapath frames leave in order and intact (%zu)", got_hi.size());
    CHECK(n_lo > 0, "the computer's frames were injected meanwhile (%zu)", n_lo);
    CHECK(!b->lo_overlap, "no injected frame shared the MAC with a datapath frame");
    // the longest wait of a datapath frame: one injected 1518-octet frame on
    // the wire (1542 transmit clocks of 14 units = 2159 system clocks) plus
    // the MAC model's pipeline and the crossings
    uint64_t worst = 0;
    for (size_t i = 0; i < b->hi_start.size() && i < b->hi_release.size(); ++i)
        worst = std::max(worst, b->hi_start[i] - b->hi_release[i]);
    std::printf("  priority (stall=%d): %zu datapath, %zu injected, worst datapath wait %llu clocks\n",
                stall, got_hi.size(), n_lo, static_cast<unsigned long long>(worst));
    // the injected frame's 190 beats into the core (more under stalls), the
    // model's 30-clock pipeline (42 system clocks), its 1542 octets on the
    // wire (2159 system clocks) and the crossings
    const uint64_t bound = (stall ? 220 : 190) + 42 + 2159 + 30;
    CHECK(worst <= bound, "a datapath frame waits at most one injected frame (%llu > %llu)",
          static_cast<unsigned long long>(worst), static_cast<unsigned long long>(bound));
    CHECK(b->tgl_flips == uint32_t(n_hi), "the frame-end toggle counts the datapath frames only (%u of %d)",
          b->tgl_flips, n_hi);
    CHECK(b->d->tx_injected_o == n_lo, "injected counter");
    done(b);
}

// CONTENTION, directed: the MAC input is stalled while a datapath frame
// waits there, and an injected frame becomes ready behind it. When the input
// frees, the datapath frame goes first. (An injection granted while no
// datapath frame waited keeps its grant: the decision is made at the grant.)
static void tx_contention()
{
    BenchPtr b = mk();
    b->host(HOST, 3); b->drain_dn();
    b->m_hold = true;
    Bytes dp = frame(AAF_MC, DEVICE, 0x22F0, 120, 0x02, {{3, 2, 0x8100}});
    b->hi_q.push_back({b->ncyc + 5, dp});
    b->cycles(20);
    b->rec(0, frame(PEER, HOST, 0x0800, 200)); b->drain_dn(); b->cycles(200);
    b->m_hold = false;
    b->cycles(5000);
    CHECK(b->out.size() == 2, "both frames left (%zu)", b->out.size());
    if (b->out.size() == 2) {
        CHECK(!b->out[0].lo && b->out[0].b == dp, "the datapath wins every arbitration: it leaves first");
        CHECK(b->out[1].lo, "the injected frame after it");
    }
    done(b);
}

// Without the computer the datapath passes with no added clock.
static void tx_transparent()
{
    BenchPtr b = mk();
    for (int i = 0; i < 20; ++i) b->hi_q.push_back({uint64_t(100 + 300 * i), frame(PEER, DEVICE, 0x0800, 64 + i)});
    for (int i = 0; i < 20000 && !b->hi_q.empty(); ++i) b->cycles(1);
    b->cycles(5000);
    uint64_t worst = 0;
    for (size_t i = 0; i < b->hi_start.size(); ++i) worst = std::max(worst, b->hi_start[i] - b->hi_release[i]);
    CHECK(b->hi_start.size() == 20 && worst <= 1, "no added clock (%llu)", static_cast<unsigned long long>(worst));
    CHECK(b->tgl_flips == 20u, "every datapath frame end counts (%u)", b->tgl_flips);
    done(b);
}

int main(int argc, char **argv)
{
    std::setvbuf(stdout, nullptr, _IOLBF, 0);   // a crash keeps every line printed so far
    Verilated::commandArgs(argc, argv);
    struct { const char *n; std::function<void()> f; } cases[] = {
        {"host_record", host_record}, {"rx_classes", rx_classes}, {"rx_full", rx_full},
        {"tx_drops", tx_drops}, {"tx_rate", tx_rate},
        {"tx_priority", [] { tx_priority(false); }}, {"tx_priority_stall", [] { tx_priority(true); }},
        {"tx_contention", tx_contention}, {"tx_transparent", tx_transparent},
    };
    for (auto &c : cases) {
        int before = fails();
        c.f();
        std::printf("%s %s\n", fails() == before ? "PASS" : "FAIL", c.n);
    }
    std::printf("%s: %d failure(s)\n", fails() ? "FAIL" : "PASS", fails());
    return fails() ? 1 : 0;
}
