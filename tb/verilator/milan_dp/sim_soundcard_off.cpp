// SPDX-License-Identifier: CERN-OHL-W-2.0

#include "VKL_pcm_route.h"
#include "verilated.h"

#include <cstdint>
#include <cstdlib>
#include <cstdio>

static int checks;

static void expect(bool condition, const char *message)
{
    ++checks;
    if (!condition) {
        std::fprintf(stderr, "FAIL: %s\n", message);
        std::exit(1);
    }
}

static void tick(VKL_pcm_route &dut)
{
    dut.clk_i = 0;
    dut.eval();
    dut.clk_i = 1;
    dut.eval();
}

static void write_route(VKL_pcm_route &dut, unsigned index, unsigned value)
{
    dut.route_wr_idx_i = index;
    dut.route_wr_val_i = value;
    dut.route_wr_en_i = 1;
    tick(dut);
    dut.route_wr_en_i = 0;
}

int main(int argc, char **argv)
{
    Verilated::commandArgs(argc, argv);
    VKL_pcm_route dut;

    dut.rst_n = 0;
    dut.s_tvalid_i = 0;
    dut.s_tlast_i = 0;
    dut.s_tdata_i = 0;
    dut.s_tuser_i = 0;
    dut.m_axis_tready = 0;
    dut.route_wr_en_i = 0;
    tick(dut);
    dut.rst_n = 1;
    tick(dut);

    // Reset route 0 is RENDER|DMA. With DMA_ENABLE_P=0 the ring is a
    // structural zero even while back-pressured, but the render tap consumes.
    dut.s_tdata_i = UINT64_C(0x1122334455667788);
    dut.s_tlast_i = 1;
    dut.s_tuser_i = 0;
    dut.s_tvalid_i = 1;
    dut.eval();
    expect(dut.m_axis_tvalid == 0, "default DMA route reached absent ring");
    expect(dut.s_tready_o == 1, "absent ring back-pressured depacketizer");
    expect(dut.render_tvalid_o == 1, "render tap disappeared with sound card");
    expect(dut.render_tdata_o == UINT64_C(0x1122334455667788),
           "render data changed with sound card");

    // A runtime DMA-only route is also swallowed and never stalls. This is
    // mutation-sensitive: deleting the DMA_ENABLE_P term makes this fail.
    dut.s_tvalid_i = 0;
    write_route(dut, 1, 1);
    dut.s_tuser_i = 1;
    dut.s_tvalid_i = 1;
    dut.eval();
    expect(dut.m_axis_tvalid == 0, "written DMA route reached absent ring");
    expect(dut.s_tready_o == 1, "written DMA route stalled without a ring");
    expect(dut.render_tvalid_o == 0, "DMA-only route leaked into render");

    std::printf("sound-card-off route: %d checks, 0 failures\n", checks);
    return 0;
}
