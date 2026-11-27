#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include "Vsim.h"
#include <verilated.h>
#include "sim_header.h"

extern "C" void litex_sim_init_runtime(long load_start, long save_start);
#if defined(__GNUC__) || defined(__clang__)
extern "C" void litex_sim_user_init(void *vsim) __attribute__((weak));
static void litex_sim_call_user_init(void *vsim)
{
    if (litex_sim_user_init != nullptr)
        litex_sim_user_init(vsim);
}
#else
static void litex_sim_call_user_init(void *vsim)
{
    (void)vsim;
}
#endif
extern "C" void litex_sim_dump()
{
}

extern "C" void litex_sim_init(void **out)
{
    Vsim *sim;

    sim = new Vsim;

    litex_sim_init_runtime(0, -1);
    sim_trace[0].signal = &sim->sim_trace;
    litex_sim_register_pads(sim_trace, (char*)"sim_trace", 0);

    serial[0].signal = &sim->serial_source_valid;
    serial[1].signal = &sim->serial_source_ready;
    serial[2].signal = &sim->serial_source_data;
    serial[3].signal = &sim->serial_sink_valid;
    serial[4].signal = &sim->serial_sink_ready;
    serial[5].signal = &sim->serial_sink_data;
    litex_sim_register_pads(serial, (char*)"serial", 0);

    sys_clk[0].signal = &sim->sys_clk;
    litex_sim_register_pads(sys_clk, (char*)"sys_clk", 0);

    sys_reset[0].signal = &sim->sys_reset;
    litex_sim_register_pads(sys_reset, (char*)"sys_reset", 0);

    milan_clk[0].signal = &sim->milan_clk;
    litex_sim_register_pads(milan_clk, (char*)"milan_clk", 0);

    audio_clk[0].signal = &sim->audio_clk;
    litex_sim_register_pads(audio_clk, (char*)"audio_clk", 0);

    audio_tdm_clk[0].signal = &sim->audio_tdm_clk;
    litex_sim_register_pads(audio_tdm_clk, (char*)"audio_tdm_clk", 0);

    mbx[0].signal = &sim->mbx_link_up;
    mbx[1].signal = &sim->mbx_gm_change;
    mbx[2].signal = &sim->mbx_gm_id;
    mbx[3].signal = &sim->mbx_domain;
    mbx[4].signal = &sim->mbx_rx_valid;
    mbx[5].signal = &sim->mbx_rx_ready;
    mbx[6].signal = &sim->mbx_rx_data;
    mbx[7].signal = &sim->mbx_rx_last;
    mbx[8].signal = &sim->mbx_rx_if;
    mbx[9].signal = &sim->mbx_tx_valid;
    mbx[10].signal = &sim->mbx_tx_ready;
    mbx[11].signal = &sim->mbx_tx_data;
    mbx[12].signal = &sim->mbx_tx_last;
    mbx[13].signal = &sim->mbx_tx_if;
    mbx[14].signal = &sim->mbx_tx_ch;
    mbx[15].signal = &sim->mbx_host_req;
    mbx[16].signal = &sim->mbx_host_we;
    mbx[17].signal = &sim->mbx_host_addr;
    mbx[18].signal = &sim->mbx_host_wdata;
    mbx[19].signal = &sim->mbx_host_ack;
    mbx[20].signal = &sim->mbx_host_rdata;
    mbx[21].signal = &sim->mbx_ms_tick;
    mbx[22].signal = &sim->mbx_avb_chg;
    mbx[23].signal = &sim->mbx_asp_chg;
    mbx[24].signal = &sim->mbx_amap_wr;
    litex_sim_register_pads(mbx, (char*)"mbx", 0);

    flash[0].signal = &sim->flash_cs;
    flash[1].signal = &sim->flash_tx_valid;
    flash[2].signal = &sim->flash_tx_ready;
    flash[3].signal = &sim->flash_tx_data;
    flash[4].signal = &sim->flash_tx_len;
    flash[5].signal = &sim->flash_tx_width;
    flash[6].signal = &sim->flash_rx_valid;
    flash[7].signal = &sim->flash_rx_ready;
    flash[8].signal = &sim->flash_rx_data;
    litex_sim_register_pads(flash, (char*)"flash", 0);

    litex_sim_call_user_init(sim);

    *out = sim;
}
