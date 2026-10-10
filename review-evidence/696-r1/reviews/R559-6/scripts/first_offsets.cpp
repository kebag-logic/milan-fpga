// Reviewer harness: first PROBE requested_start of KL_maap for (mac, clock) pairs
// read from stdin as "mac_hex clock_hex" lines. Each station starts from reset and
// enables on the same cycle (equally timed). Scaled clock CLK_FREQ_HZ_P=10000.
#include "VKL_maap.h"
#include "verilated.h"
#include <cstdio>
#include <cstdint>
int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    VKL_maap* d = new VKL_maap;
    auto tick = [&]{ d->clk_i=0; d->eval(); d->clk_i=1; d->eval(); };
    unsigned long long mac; unsigned clk;
    while (std::scanf("%llx %x", &mac, &clk) == 2) {
        d->rst_n=0; d->enable_i=0; d->station_mac_i=mac; d->realtime_ns_i=clk;
        d->count_i=8; d->seed_valid_i=0; d->seed_offset_i=0; d->port_operational_i=1;
        d->m_axis_tready=1; d->rx_tvalid_i=0; d->rx_tready_i=0; d->rx_tlast_i=0;
        d->rx_tdata_i=0; d->rx_tkeep_i=0;
        for (int i=0;i<6;++i) tick();
        d->rst_n=1; for (int i=0;i<3;++i) tick();
        d->enable_i=1;
        int beat=0; long start=-1;
        for (int c=0;c<200 && start<0;++c) {
            d->clk_i=0; d->eval();
            if (d->m_axis_tvalid && d->m_axis_tready) {
                if (beat==3) start=((d->m_axis_tdata>>48)&0xff)<<8 | ((d->m_axis_tdata>>56)&0xff);
                beat = d->m_axis_tlast ? 0 : beat+1;
            }
            d->clk_i=1; d->eval();
        }
        std::printf("%012llx %08x 0x%04lx\n", mac, clk, start);
    }
    delete d; return 0;
}
