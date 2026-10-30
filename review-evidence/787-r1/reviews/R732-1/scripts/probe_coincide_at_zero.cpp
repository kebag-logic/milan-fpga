// Reviewer probe (R732-1): KL_reboot_ctrl's egress account at a count of 0.
// A frame-end edge with nothing counted (a stray edge) that lands on the same
// clock as the port taking a frame's last beat. The module's banner says the
// count "can only make the wait longer, never shorter". This probe measures
// whether the taken frame is still waited for. Build:
//   verilator --cc --exe --build -Wall --top-module KL_reboot_ctrl \
//     hdl/milan/KL_reboot_ctrl.sv probe_coincide_at_zero.cpp -o probe
#include "VKL_reboot_ctrl.h"
#include "verilated.h"
#include <cstdio>
#include <cstdint>
static const uint64_t kMs = 64;   // compressed millisecond: the harness drives the tick
static VKL_reboot_ctrl* d; static uint64_t cyc = 0;
static void step() { d->ms_tick_i = (cyc % kMs) == 3; d->clk_i = 0; d->eval(); d->clk_i = 1; d->eval(); ++cyc; }
static int scenario(bool coincide) {
    d->rst_n = 0; d->reboot_req_i = 0; d->mac_tx_beat_i = 0; d->mac_tx_frame_i = 0;
    d->mac_flush_i = 0; d->nvm_backed_i = 0; d->nvm_dirty_i = 0; d->nvm_pend_i = 0;
    d->mac_txend_tgl_i = 0;
    for (int i = 0; i < 4; ++i) step();
    d->rst_n = 1; for (int i = 0; i < 8; ++i) step();
    // a stray edge: the toggle flips with nothing counted
    d->mac_txend_tgl_i = 1;
    step(); step();                 // after two clocks the edge is on txend_w
    // the port takes a whole one-beat frame: on the edge's clock, or 10 clocks later
    if (!coincide) for (int i = 0; i < 10; ++i) step();
    d->mac_tx_beat_i = 1; d->mac_tx_frame_i = 1; step();
    d->mac_tx_beat_i = 0; d->mac_tx_frame_i = 0;
    d->reboot_req_i = 1;
    // the frame is never counted out (no further edge): the wait must run to its bound
    uint64_t n = 0; while (!d->phy_hold_o && n < 40 * kMs) { step(); ++n; }
    std::printf("%s: PHY hold after %llu clocks (%.1f ms); the derived bound is 28 ms\n",
                coincide ? "stray edge ON the take's clock" : "stray edge 10 clocks before the take",
                (unsigned long long)n, double(n) / kMs);
    return n > 28 * kMs ? 0 : 1;    // 0 = the frame was waited for to the bound
}
int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    d = new VKL_reboot_ctrl;
    const int apart = scenario(false);
    const int same = scenario(true);
    std::printf("RESULT apart=%s same-clock=%s\n", apart ? "UNDER-COUNT" : "waited to the bound",
                same ? "UNDER-COUNT" : "waited to the bound");
    d->final(); delete d; return 0;
}
