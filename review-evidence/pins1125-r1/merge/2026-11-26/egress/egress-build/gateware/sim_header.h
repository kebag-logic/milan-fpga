#ifndef __SIM_CORE_H_
#define __SIM_CORE_H_
#include "pads.h"

struct pad_s sim_trace[] = {
    { (char*)"sim_trace", 1, NULL },
    { NULL, 0, NULL }
};

struct pad_s serial[] = {
    { (char*)"source_valid", 1, NULL },
    { (char*)"source_ready", 1, NULL },
    { (char*)"source_data", 8, NULL },
    { (char*)"sink_valid", 1, NULL },
    { (char*)"sink_ready", 1, NULL },
    { (char*)"sink_data", 8, NULL },
    { NULL, 0, NULL }
};

struct pad_s sys_clk[] = {
    { (char*)"sys_clk", 1, NULL },
    { NULL, 0, NULL }
};

struct pad_s sys_reset[] = {
    { (char*)"sys_reset", 1, NULL },
    { NULL, 0, NULL }
};

struct pad_s milan_clk[] = {
    { (char*)"milan_clk", 1, NULL },
    { NULL, 0, NULL }
};

struct pad_s audio_clk[] = {
    { (char*)"audio_clk", 1, NULL },
    { NULL, 0, NULL }
};

struct pad_s audio_tdm_clk[] = {
    { (char*)"audio_tdm_clk", 1, NULL },
    { NULL, 0, NULL }
};

struct pad_s mbx[] = {
    { (char*)"link_up", 1, NULL },
    { (char*)"gm_change", 1, NULL },
    { (char*)"gm_id", 64, NULL },
    { (char*)"domain", 8, NULL },
    { (char*)"rx_valid", 1, NULL },
    { (char*)"rx_ready", 1, NULL },
    { (char*)"rx_data", 8, NULL },
    { (char*)"rx_last", 1, NULL },
    { (char*)"rx_if", 1, NULL },
    { (char*)"tx_valid", 1, NULL },
    { (char*)"tx_ready", 1, NULL },
    { (char*)"tx_data", 8, NULL },
    { (char*)"tx_last", 1, NULL },
    { (char*)"tx_if", 1, NULL },
    { (char*)"tx_ch", 3, NULL },
    { (char*)"host_req", 1, NULL },
    { (char*)"host_we", 1, NULL },
    { (char*)"host_addr", 13, NULL },
    { (char*)"host_wdata", 32, NULL },
    { (char*)"host_ack", 1, NULL },
    { (char*)"host_rdata", 32, NULL },
    { (char*)"ms_tick", 1, NULL },
    { (char*)"avb_chg", 1, NULL },
    { (char*)"asp_chg", 1, NULL },
    { (char*)"amap_wr", 1, NULL },
    { NULL, 0, NULL }
};

struct pad_s flash[] = {
    { (char*)"cs", 1, NULL },
    { (char*)"tx_valid", 1, NULL },
    { (char*)"tx_ready", 1, NULL },
    { (char*)"tx_data", 32, NULL },
    { (char*)"tx_len", 6, NULL },
    { (char*)"tx_width", 4, NULL },
    { (char*)"rx_valid", 1, NULL },
    { (char*)"rx_ready", 1, NULL },
    { (char*)"rx_data", 32, NULL },
    { NULL, 0, NULL }
};

#ifndef __cplusplus
void litex_sim_init(void **out);
#endif

#endif /* __SIM_CORE_H_ */
