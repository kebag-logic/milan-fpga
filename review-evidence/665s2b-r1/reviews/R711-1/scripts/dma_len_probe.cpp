// Boundary probe of KL_mbx_dma's 12-bit length (len_bytes_i 0..4095): for each length, start a receive
// and a transmit move, answer the host port the cycle after each request and the AXI port at once, and
// report the cycles until BUSY falls (or HANG after 200000 cycles), the words read or written, and ERR.
#include <cstdint>
#include <cstdio>
#include <memory>
#include "VKL_mbx_dma.h"
#include "verilated.h"
int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    auto ctx = std::make_unique<VerilatedContext>();
    auto m = std::make_unique<VKL_mbx_dma>(ctx.get());
    auto tick = [&] { m->clk_i = 0; m->eval(); m->clk_i = 1; m->eval(); };
    const unsigned lens[] = {0, 1, 4, 1514, 2048, 4088, 4089, 4092, 4093, 4094, 4095};
    int hangs = 0;
    for (int to_ring = 0; to_ring < 2; ++to_ring) for (unsigned len : lens) {
        m->rst_n = 0; tick(); tick(); m->rst_n = 1;
        m->cpu_req_i = 0; m->axi_awready_i = 1; m->axi_wready_i = 1; m->axi_bvalid_i = 0; m->axi_bresp_i = 0;
        m->axi_arready_i = 1; m->axi_rvalid_i = 0; m->axi_rresp_i = 0; m->axi_rlast_i = 0; m->host_ack_i = 0;
        m->ring_base_i = 0; m->ring_mask_i = 0xFFFF; m->ring_index_i = 0; m->mem_addr_i = 0x10000000u;
        m->len_bytes_i = len; m->to_ring_i = to_ring; m->start_p_i = 1; tick(); m->start_p_i = 0;
        unsigned cyc = 0, words = 0, beats_left = 0; bool b_pending = false, ack_next = false;
        while (cyc < 200000) {
            m->eval();
            if (!m->busy_o && cyc > 1) break;
            m->host_ack_i = ack_next; ack_next = m->host_req_o; if (m->host_req_o) ++words;
            m->axi_bvalid_i = b_pending;
            if (m->axi_arvalid_o && m->axi_arready_i) beats_left = m->axi_arlen_o + 1;
            m->axi_rvalid_i = beats_left != 0; m->axi_rlast_i = beats_left == 1; m->axi_rdata_i = 0x11223344u;
            bool rtake = m->axi_rvalid_i && m->axi_rready_o;
            bool wlast = m->axi_wvalid_o && m->axi_wready_i && m->axi_wlast_o;
            bool btake = m->axi_bvalid_i && m->axi_bready_o;
            tick(); ++cyc;
            if (rtake) --beats_left;
            if (wlast) b_pending = true;
            if (btake) b_pending = false;
        }
        bool hang = m->busy_o;
        hangs += hang;
        std::printf("%s len %4u: %s after %u cycles, %u host-port requests, err %d\n", to_ring ? "transmit" : "receive ",
                    len, hang ? "HANG (busy, the host port held)" : "idle", cyc, words, int(m->err_o));
    }
    std::printf("length probe: %d of %zu moves hang\n", hangs, 2 * sizeof lens / sizeof lens[0]);
    m->final();
    return 0;
}
