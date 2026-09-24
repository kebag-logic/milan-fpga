// Reviewer probe (not part of the tree): drive KL_crf_rx the way
// sim_talker_step.cpp drives it (frame_p_i raised with the rising edge and
// held until the next rising edge) and read rate_valid_o after the accepting
// edge. The registered rate_valid_r stays high; the combinational port reads
// low because w_acc is still asserted against the just-updated references.
#include "VKL_crf_rx.h"
#include "VKL_crf_rx___024root.h"
#include "verilated.h"
#include <cstdint>
#include <cstdio>
int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    VKL_crf_rx d;
    uint64_t ts = 10'000'000'000ULL; uint8_t seq = 0;
    auto edge = [&](bool pdu) {
        d.clk_i = 0; d.eval();
        d.frame_p_i = pdu;
        if (pdu) {
            ts += 2'000'000; ++seq;
            d.seq_i = seq;
            d.fsh_i = (uint64_t{8} << 48) | (uint64_t{96} << 32) | (ts >> 32);
            d.fsh2_i = ts << 32; d.ptp_now_i = ts - 1'000'000;
        }
        d.clk_i = 1; d.eval();
    };
    d.rst_n = 0; d.en_i = 0; d.stop_i = 0; d.subtype_i = 4; d.type_i = 1;
    d.sid_i = 1; d.sid_frame_i = 1; d.pullbase_i = 48000; d.mr_i = 0; d.tu_i = 0;
    edge(false); edge(false); d.rst_n = 1; d.en_i = 1; edge(false);
    int port_low = 0, reg_low = 0, pdus = 0;
    for (int n = 0; n < 600; ++n) {
        edge(true);                       // accepting edge, pulse still high
        if (n >= 300) {
            ++pdus;
            port_low += !d.rate_valid_o;
            reg_low += !d.rootp->KL_crf_rx__DOT__rate_valid_r;
        }
        for (int k = 0; k < 4; ++k) edge(false);
    }
    std::printf("after-edge reads over %d clean PDUs: port low %d, register low %d\n",
                pdus, port_low, reg_low);
    return (port_low == pdus && reg_low == 0) ? 0 : 1;
}
