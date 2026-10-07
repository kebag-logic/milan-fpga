// Reviewer probe: drive KL_mbx_rx alone with a seeded random frame stream and
// print a transaction-level trace (every ring write, every counter after each
// frame). Built once against the round-1 RTL (-DOLD) and once against the
// round-2 RTL; the two traces must be identical. Frames the round-2 row admits
// on purpose (a DEFEND, message_type 2, to the arrival interface's own MAC,
// 16 bytes or longer) are given to the round-1 build with the MAAP multicast
// destination instead, and the first two payload words of their records (the
// destination bytes) are masked in both traces. Cycle counts and mid-frame
// ready-low cycles are printed separately (they are allowed to differ).
#include "VKL_mbx_rx.h"
#include "verilated.h"
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <random>
#include <vector>

static VKL_mbx_rx* d;
static uint64_t cyc = 0;
static void tick() { d->clk_i = 0; d->eval(); d->clk_i = 1; d->eval(); ++cyc; }

static const uint64_t OWN_MAC = 0x020000000001ull, OWN_EID = 0x0011223344556677ull;
static const uint64_t MAAP_MC = 0x91E0F000FF00ull, MAAP_BASE = 0x91E000000100ull;

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    const unsigned seed = argc > 1 ? (unsigned)atoi(argv[1]) : 1u;
    const unsigned frames = argc > 2 ? (unsigned)atoi(argv[2]) : 20000u;
    FILE* trace = fopen(argc > 3 ? argv[3] : "trace.txt", "w");
    FILE* perf = fopen(argc > 4 ? argv[4] : "perf.txt", "w");
    std::mt19937_64 rng(seed);
    auto R = [&](uint64_t n) { return (uint64_t)(rng() % n); };
    d = new VKL_mbx_rx;
    d->rst_n = 0; d->rx_valid_i = 0; d->ms_tick_p_i = 0; d->now_ms_i = 0;
    d->own_eid_i = OWN_EID;
    d->own_mac_i = OWN_MAC;
    d->open_i = 0x1F; d->maap_base_i = MAAP_BASE; d->maap_count_i = 8;
    d->rx_tail_words_i[0] = d->rx_tail_words_i[1] = d->rx_tail_words_i[2] = 0;
    for (int i = 0; i < 4; ++i) tick();
    d->rst_n = 1; tick();
    const uint64_t dsts[] = {0x91E0F0010000ull, 0x91E0F0010001ull, MAAP_MC, OWN_MAC, OWN_MAC ^ 0x010000000000ull,
                             OWN_MAC ^ 1ull, 0x020000000099ull, 0x0180C200000Eull, 0x0180C2000021ull, 0};
    const uint16_t ets[] = {0x22F0, 0x22F0, 0x22F0, 0x22EA, 0x88F5, 0x8100, 0x0800, 0};
    const uint8_t subs[] = {0xFA, 0xFB, 0xFC, 0xFE, 0xFE, 0xFD, 0};
    unsigned special = 0, specials_total = 0;
    for (unsigned f = 0; f < frames; ++f) {
        // the stream's own state changes between frames
        if (R(200) == 0) d->open_i = R(4) == 0 ? (uint32_t)R(32) : 0x1Fu;
        if (R(300) == 0) d->maap_count_i = R(3) == 0 ? 0 : (uint16_t)(1 + R(16));
        unsigned ticks = (unsigned)R(4);
        for (unsigned t = 0; t < ticks; ++t) { d->ms_tick_p_i = 1; tick(); d->ms_tick_p_i = 0; tick(); }
        d->now_ms_i = f;
        // the frame
        uint64_t dst = dsts[R(10)]; if (dst == 0) dst = rng() & 0xFFFFFFFFFFFFull;
        uint16_t et = ets[R(8)]; if (et == 0) et = (uint16_t)rng();
        uint8_t sub = subs[R(7)]; if (sub == 0) sub = (uint8_t)rng();
        unsigned len;
        switch (R(8)) {
        case 0: case 1: len = 1 + (unsigned)R(20); break;           // around the byte 14/15 boundary
        case 2: len = 14 + (unsigned)R(4); break;                   // 14..17 exactly
        case 3: case 4: len = 60 + (unsigned)R(12); break;
        case 5: len = 62 + (unsigned)R(6); break;                   // MAAP max_frame 64 boundary
        case 6: len = 126 + (unsigned)R(6); break;                  // ADP/ACMP 128 boundary
        default: len = R(4) == 0 ? 1510 + (unsigned)R(8) : 16 + (unsigned)R(300); break;
        }
        std::vector<uint8_t> fr(len);
        for (auto& b : fr) b = (uint8_t)rng();
        auto put = [&](unsigned off, uint64_t v, unsigned n) {
            for (unsigned i = 0; i < n; ++i) if (off + i < len) fr[off + i] = (uint8_t)(v >> (8 * (n - 1 - i)));
        };
        put(0, dst, 6); put(12, et, 2); put(14, sub, 1);
        if (len > 15) fr[15] = (uint8_t)((fr[15] & 0xF0u) | (unsigned)R(16));
        for (unsigned off : {18u, 26u, 34u, 42u}) {
            unsigned c = (unsigned)R(4);
            if (c == 0) put(off, OWN_EID, 8);
            else if (c == 1) put(off, 0, 8);
        }
        if (R(2)) {  // a MAAP range near this entity's
            put(26, MAAP_BASE + (uint64_t)(int64_t)((int)R(24) - 12), 6);
            put(32, R(4) == 0 ? 0 : 1 + R(10), 2);
        }
        if (len >= 16 && R(2)) {  // a valid frame of one table row, then maybe one element changed
            unsigned row = (unsigned)R(8);
            uint64_t tdst = 0; uint16_t tet = 0x22F0; int tsub = -1; unsigned tmt = (unsigned)R(16);
            switch (row) {
            case 0: tdst = 0x91E0F0010000ull; tsub = 0xFA; tmt = 2; put(18, R(2) ? OWN_EID : 0, 8); break;
            case 1: tdst = R(2) ? 0x91E0F0010000ull : OWN_MAC; tsub = 0xFC; put(R(2) ? 34 : 42, OWN_EID, 8); break;
            case 2: tdst = OWN_MAC; tsub = 0xFB; put((tmt & 1u) ? 26 : 18, OWN_EID, 8); break;
            case 3: case 4: tdst = (row == 4 && R(2)) ? OWN_MAC : MAAP_MC; tsub = 0xFE;
                    tmt = row == 4 ? 2u : 1u + (unsigned)R(3);
                    put(26, MAAP_BASE + (uint64_t)R(8), 6); put(32, 1 + R(8), 2); break;
            case 5: tdst = 0x0180C200000Eull; tet = 0x22EA; break;
            case 6: tdst = 0x0180C2000021ull; tet = 0x88F5; break;
            default: tdst = MAAP_MC; tsub = 0xFE; tmt = 2; put(26, MAAP_BASE + 3, 6); put(32, 2, 2); break;
            }
            switch (R(6)) {  // one element changed, or none
            case 0: tdst = dsts[R(10)] ? dsts[R(10)] : 0x0A0B0C0D0E0Full; break;
            case 1: tet = ets[R(7)]; break;
            case 2: if (tsub >= 0) tsub = subs[R(6)]; break;
            case 3: tmt = (unsigned)R(16); break;
            default: break;
            }
            dst = tdst; et = tet; if (tsub >= 0) sub = (uint8_t)tsub; else sub = fr[14];
            put(0, dst, 6); put(12, et, 2); put(14, sub, 1);
            if (tsub >= 0) fr[15] = (uint8_t)((fr[15] & 0xF0u) | tmt);
        }
        unsigned ifx = R(5) == 0 ? 1u : 0u;  // index 1: no interface in this build
        const bool sp = ifx == 0 && dst == OWN_MAC && et == 0x22F0 && sub == 0xFE && len >= 16 && (fr[15] & 0x0Fu) == 2u;
#ifdef OLD
        if (sp) put(0, MAAP_MC, 6);
#endif
        specials_total += sp;
        // offer the bytes; random idle gaps between bytes (decided before ready is seen)
        fprintf(trace, "F %u len=%u if=%u sp=%d\n", f, len, ifx, sp ? 1 : 0);
        unsigned writes = 0, ready_low = 0; uint64_t c0 = cyc;
        auto sample = [&]() {
            d->eval();
            if (d->wr_en_o) {
                bool mask = sp && writes < 2;
                fprintf(trace, " W ch=%u a=%u d=%08x\n", d->wr_ch_o, d->wr_addr_o, mask ? 0xDEADDEADu : d->wr_data_o);
                ++writes;
            }
        };
        for (unsigned i = 0; i < len; ++i) {
            while (R(8) == 0) { d->rx_valid_i = 0; sample(); tick(); }
            d->rx_valid_i = 1; d->rx_data_i = fr[i]; d->rx_last_i = i + 1 == len; d->rx_if_i = ifx;
            for (;;) {
                sample();
                bool took = d->rx_ready_o;
                if (!took && i > 0) ++ready_low;
                tick();
                if (took) break;
            }
        }
        d->rx_valid_i = 0; d->rx_last_i = 0;
        for (unsigned k = 0; k < 24; ++k) { sample(); tick(); }
        fprintf(trace, " C mis=%u", d->mismatch_cnt_o);
        for (int c = 0; c < 5; ++c) {
            auto w16 = [&](const VlWide<3>& v, int c) { return (unsigned)((v[(16 * c) / 32] >> ((16 * c) % 32)) & 0xFFFFu); };
            fprintf(trace, " [%d h=%u d=%u r=%u p=%u]", c, w16(d->rx_head_words_o, c), w16(d->rx_drop_cnt_o, c),
                    w16(d->rate_drop_cnt_o, c), w16(d->rx_pass_cnt_o, c));
        }
        fprintf(trace, "\n");
        fprintf(perf, "%u %u %u %llu\n", f, len, ready_low, (unsigned long long)(cyc - c0));
        // the core consumes, most of the time
        if (R(10) < 7) for (int w = 0; w < 3; ++w) d->rx_tail_words_i[w] = d->rx_head_words_o[w];
    }
    fprintf(trace, "END specials=%u\n", specials_total);
    fclose(trace); fclose(perf);
    printf("frames=%u specials=%u cycles=%llu\n", frames, specials_total, (unsigned long long)cyc);
    delete d;
    return 0;
}
