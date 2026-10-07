// Reviewer cross-check (R548-1, #686), written after this round's verdict to
// test two claims raised by the parallel round on the same head.
//  A: station MAC whose low 32 bits satisfy mac[15:0] ^ mac[31:16] == 0xACE1
//     seeds the LFSR (KL_maap.sv:278-279) with 0; are the B.3.4 timer draws
//     still random? Compares against an ordinary MAC.
//  B: a supplied seed offset beyond POOL_SIZE - count (KL_maap.sv:268); does
//     the claimed block stay inside the 0xFE00 dynamic pool (Table B.9)?
// Prints the measurements; exit 0 always (the report states the reading).
// Build: verilator --cc --exe --build -GCLK_FREQ_HZ_P=10000 KL_maap.sv this.cpp
#include "VKL_maap.h"
#include "verilated.h"
#include <cstdint>
#include <cstdio>
#include <set>
#include <vector>

static VKL_maap* d;
static long now;
static std::vector<long> starts;   // first-beat cycle of each frame
static std::vector<int> types;
static bool in_frame;

static void cyc(long n = 1) {
    for (long i = 0; i < n; i++) {
        d->clk_i = 0; d->eval();
        if (d->m_axis_tvalid && d->m_axis_tready) {
            if (!in_frame) { starts.push_back(now); in_frame = true; }
            if (d->m_axis_tlast) in_frame = false;
        }
        if (d->m_axis_tvalid && d->m_axis_tready && !d->m_axis_tlast && starts.size() > types.size()
            && ((d->m_axis_tdata >> 56) & 0xFF) != 0 && false) {}
        d->clk_i = 1; d->eval(); now++;
    }
}

static void reset(uint64_t mac, bool seed, uint16_t off) {
    d->station_mac_i = mac; d->count_i = 8; d->enable_i = 0;
    d->seed_valid_i = seed; d->seed_offset_i = off;
    d->m_axis_tready = 1; d->rx_tvalid_i = 0;
    d->rst_n = 0; cyc(6); d->rst_n = 1; cyc(3);
    starts.clear(); types.clear(); in_frame = false;
}

static void announce_case(const char* tag, uint64_t mac) {
    reset(mac, true, 0x4000);
    d->enable_i = 1;
    cyc(4 * 6000 + 26 * 320000);           // walk plus ~26 announcements
    std::set<long> probe_iv, ann_iv;
    for (size_t k = 1; k < starts.size(); k++) {
        long iv = starts[k] - starts[k - 1];
        if (k <= 3) probe_iv.insert(iv);
        else if (k >= 6) ann_iv.insert(iv);  // skip the PROBE->ANNOUNCE gap and the first announce
    }
    printf("%s mac=%012llx frames=%zu distinct probe intervals=%zu distinct announce intervals=%zu",
           tag, static_cast<unsigned long long>(mac), starts.size(), probe_iv.size(), ann_iv.size());
    if (!ann_iv.empty()) printf(" announce min=%ld max=%ld", *ann_iv.begin(), *ann_iv.rbegin());
    printf("\n");
}

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    d = new VKL_maap;
    announce_case("A-ordinary", 0x020000000001ULL);
    announce_case("A-zero-seed", 0x02000000ACE1ULL);
    reset(0x020000000001ULL, true, 0xFEFF);
    d->enable_i = 1;
    cyc(4 * 6000 + 100);
    printf("B seed=0xFEFF count=8 state=%u addr_valid=%u offset=0x%04X block_end=0x%05X pool_size=0xFE00\n",
           d->state_o, d->addr_valid_o, d->offset_o, d->offset_o + 8);
    delete d;
    return 0;
}
