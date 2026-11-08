// Reviewer probe: KL_ctrl_split's rx_drops_o under a full receive FIFO.
// Build: verilator --cc --exe --build --top-module KL_ctrl_split KL_ctrl_split.sv axis_fifo.v this.cpp
// Offers N accepted control frames (ADP, EtherType 0x22F0, subtype 0xFA, 64
// bytes = 8 beats) back to back while the mailbox side is not ready, so the
// 4,096-byte frame FIFO fills; then drains and counts the frames handed out.
// Prints frames offered, frames handed out, rx_drops_o and rx_frames_o.
#include "VKL_ctrl_split.h"
#include "verilated.h"
#include <cstdint>
#include <cstdio>

static VKL_ctrl_split* d;
static void tick() { d->clk_i = 0; d->eval(); d->clk_i = 1; d->eval(); }

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    d = new VKL_ctrl_split;
    d->rst_n = 0; d->rx_tvalid_i = 0; d->rx_tready_i = 1; d->rx_ready_i = 0; d->tx_valid_i = 0;
    d->m_axis_tx_tready = 1;
    for (int i = 0; i < 8; ++i) tick();
    d->rst_n = 1; tick();
    const int N = 100, BEATS = 8;
    for (int f = 0; f < N; ++f) {
        for (int b = 0; b < BEATS; ++b) {
            std::uint8_t by[8];
            for (int k = 0; k < 8; ++k) {
                const int o = 8 * b + k;
                by[k] = static_cast<std::uint8_t>(o);
                if (o < 6) by[k] = (o == 0) ? 0x91 : 0x00;   // a destination
                if (o == 12) by[k] = 0x22;
                if (o == 13) by[k] = 0xF0;
                if (o == 14) by[k] = 0xFA;                   // ADP
            }
            std::uint64_t w = 0;
            for (int k = 0; k < 8; ++k) w |= static_cast<std::uint64_t>(by[k]) << (8 * k);
            d->rx_tdata_i = w; d->rx_tkeep_i = 0xFF; d->rx_tvalid_i = 1; d->rx_tlast_i = (b == BEATS - 1);
            tick();
        }
    }
    d->rx_tvalid_i = 0; d->rx_tlast_i = 0;
    for (int i = 0; i < 10; ++i) tick();
    const unsigned drops_full = d->rx_drops_o;
    d->rx_ready_i = 1;
    int out = 0;
    for (int i = 0; i < 200000; ++i) {
        d->eval();
        if (d->rx_valid_o && d->rx_last_o) ++out;
        tick();
    }
    std::printf("frames offered %d (%d bytes), frames handed out %d, rx_drops_o %u (at full: %u), rx_frames_o %u\n",
                N, N * 8 * BEATS, out, static_cast<unsigned>(d->rx_drops_o), drops_full,
                static_cast<unsigned>(d->rx_frames_o));
    const bool lost = out < N;
    std::printf("%s\n", (lost && d->rx_drops_o == 0) ? "FRAMES LOST AND NOT COUNTED" : "lost frames counted or none lost");
    delete d;
    return 0;
}
