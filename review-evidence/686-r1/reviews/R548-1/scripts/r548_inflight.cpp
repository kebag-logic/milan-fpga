// Reviewer directed probe (R548-1, #686): a conflicting PROBE parsed while an
// ANNOUNCE is part-way out on the wire under backpressure. The documented
// contract (MAAP_FABRIC.md conflict cells; KL_maap.sv:213-215, :262) is that
// the in-flight frame is not rewritten and the PROBE goes unanswered.
// Prints the frame captured after the stall and exits 1 if it differs from
// the ANNOUNCE Figure B.1 layout (zero conflict_*), 0 otherwise.
// Build: verilator --cc --exe --build -GCLK_FREQ_HZ_P=10000 KL_maap.sv this.cpp
#include "VKL_maap.h"
#include "verilated.h"
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <vector>

static VKL_maap* d;
static std::vector<uint8_t> cur;
static std::vector<std::vector<uint8_t>> frames;

static void cyc(int n = 1) {
    for (int i = 0; i < n; i++) {
        d->clk_i = 0; d->eval();
        if (d->m_axis_tvalid && d->m_axis_tready) {
            int nb = d->m_axis_tkeep == 0xFF ? 8 : 4;
            for (int l = 0; l < nb; l++) cur.push_back((d->m_axis_tdata >> (8 * l)) & 0xFF);
            if (d->m_axis_tlast) { frames.push_back(cur); cur.clear(); }
        }
        d->clk_i = 1; d->eval();
    }
}

static void inject_probe(uint64_t src, uint16_t off, uint16_t cnt) {
    uint8_t f[64]; memset(f, 0, sizeof f);
    const uint64_t dst = 0x91E0F000FF00ULL;
    for (int k = 0; k < 6; k++) { f[k] = dst >> (40 - 8 * k); f[6 + k] = src >> (40 - 8 * k); }
    f[12] = 0x22; f[13] = 0xF0; f[14] = 0xFE; f[15] = 1; f[16] = 0x08; f[17] = 16;
    f[26] = 0x91; f[27] = 0xE0; f[28] = 0xF0; f[29] = 0x00;
    f[30] = off >> 8; f[31] = off; f[32] = cnt >> 8; f[33] = cnt;
    for (int b = 0; b < 8; b++) {
        uint64_t v = 0;
        for (int j = 0; j < 8; j++) v |= static_cast<uint64_t>(f[b * 8 + j]) << (8 * j);
        d->rx_tdata_i = v; d->rx_tkeep_i = b == 7 ? 0x0F : 0xFF;
        d->rx_tvalid_i = 1; d->rx_tready_i = 1; d->rx_tlast_i = b == 7;
        cyc();
    }
    d->rx_tvalid_i = 0; d->rx_tlast_i = 0; cyc(3);
}

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    d = new VKL_maap;
    d->station_mac_i = 0x020000000001ULL; d->count_i = 8; d->enable_i = 0;
    d->seed_valid_i = 0; d->m_axis_tready = 1; d->rx_tvalid_i = 0;
    d->rst_n = 0; cyc(6); d->rst_n = 1; cyc(3);
    d->enable_i = 1;
    for (long i = 0; i < 100000 && !(d->state_o == 2 && frames.size() >= 5); i++) cyc();
    if (d->state_o != 2) { puts("did not reach ANNOUNCE"); return 2; }
    const uint16_t off = d->offset_o;
    // wait for the next ANNOUNCE request, let two beats go, then stall
    const size_t base = frames.size();
    d->m_axis_tready = 0;
    for (long i = 0; i < 400000 && !d->m_axis_tvalid; i++) cyc();
    d->m_axis_tready = 1; cyc(2); d->m_axis_tready = 0;
    inject_probe(0x0A0B0C0D0E0FULL, off, 8);      // conflicting PROBE
    cyc(50);
    d->m_axis_tready = 1; cyc(50);
    if (frames.size() <= base) { puts("no frame"); return 2; }
    const auto& f = frames[base];
    printf("frames after stall: %zu\n", frames.size() - base);
    printf("frame bytes:");
    for (size_t k = 0; k < f.size(); k++) printf("%s%02X", k % 8 ? " " : "\n  ", f[k]);
    printf("\n");
    bool conf_zero = true;
    for (int k = 34; k < 42; k++) conf_zero = conf_zero && f[k] == 0;
    const bool ok = f.size() == 60 && (f[15] & 0x0F) == 3 && conf_zero &&
                    ((f[30] << 8) | f[31]) == off && frames.size() - base == 1;
    printf("in-flight ANNOUNCE intact and PROBE unanswered: %s\n", ok ? "YES" : "NO");
    delete d;
    return ok ? 0 : 1;
}
