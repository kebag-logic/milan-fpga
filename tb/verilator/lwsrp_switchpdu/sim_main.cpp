// Feed KL_lwsrp_rx the EXACT MSRPDU the certified switch emitted
// (captured at pw0 2026-07-18 21:09) and see what registers for
// lsid = 02:00:00:00:00:01:0000 (the arty's bound stream).
#include "VKL_lwsrp_rx.h"
#include "verilated.h"
#include <cstdio>
#include <vector>
#include <cstdint>
#include "ta_frame.h"

static VKL_lwsrp_rx* dut;
static void step(int n=1){ for(int i=0;i<n;i++){ dut->clk_i=0; dut->eval(); dut->clk_i=1; dut->eval(); } }

static const uint8_t FRAME[] = {
0x01,0x80,0xc2,0x00,0x00,0x0e,0x3c,0xc0,0xc6,0xfe,0x02,0x11,0x22,0xea,0x00,0x02,
0x22,0x00,0x4c,0x20,0x01,0x02,0x00,0x00,0x00,0x00,0x01,0x00,0x00,0x91,0xe0,0xf0,
0x00,0xfe,0x01,0x02,0x7e,0x00,0xe0,0x00,0x01,0x70,0x00,0x02,0x17,0x52,0x80,0x00,
0x3c,0xc0,0xc6,0xfe,0x02,0x10,0x08,0x6c,0x00,0x01,0x02,0x00,0x00,0x00,0x00,0x02,
0x00,0x00,0x91,0xe0,0xf0,0x00,0xfe,0x01,0x02,0x7e,0x00,0xe0,0x00,0x01,0x70,0x00,
0x02,0x17,0x52,0x80,0x00,0x3c,0xc0,0xc6,0xfe,0x02,0x10,0x05,0x6c,0x00,0x00,0x04,
0x04,0x00,0x09,0x20,0x02,0x05,0x02,0x00,0x02,0x7e,0x00,0x00,0x01,0x19,0x00,0x1d,
0x20,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x03,0x08,0x00,
0x0c,0x20,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00
};

int main(int argc, char** argv){
    Verilated::commandArgs(argc, argv);
    dut = new VKL_lwsrp_rx;
    dut->rst_n=0; dut->clk_i=0; dut->enable_i=0; dut->tick_1khz_i=0;
    dut->rx_tvalid_i=0; dut->rx_tlast_i=0;
    step(4); dut->rst_n=1; dut->enable_i=1;
    dut->station_mac_i = 0x020000000002ull;      // the arty
    dut->unique_id_i = 0; dut->vid_i = 0x27E;
    dut->lsid_i = 0x0200000000010000ull;         // bound to AX stream :01
    dut->lsid_en_i = 1;
    step(8);

    size_t n = sizeof(FRAME);
    for (size_t off = 0; off < n; off += 8) {
        uint64_t d = 0; uint8_t k = 0;
        for (int b = 0; b < 8 && off+b < n; b++) {
            d |= (uint64_t)FRAME[off+b] << (8*b);   // little lane
            k |= 1 << b;
        }
        dut->rx_tdata_i = d; dut->rx_tkeep_i = k;
        dut->rx_tvalid_i = 1;
        dut->rx_tlast_i = (off + 8 >= n);
        step();
    }
    dut->rx_tvalid_i = 0; dut->rx_tlast_i = 0;
    step(4000);
    printf("after TF pdu: ta_reg=%d ta_failed=%d code=0x%02x domain_ok=%d\n",
           dut->ta_registered_o, dut->ta_failed_o, dut->ta_fail_code_o, dut->domain_ok_o);

    // now the TalkerAdvertise variant
    size_t n2 = sizeof(FRAME2);
    for (size_t off = 0; off < n2; off += 8) {
        uint64_t d = 0; uint8_t k = 0;
        for (int b = 0; b < 8 && off+b < n2; b++) { d |= (uint64_t)FRAME2[off+b] << (8*b); k |= 1 << b; }
        dut->rx_tdata_i = d; dut->rx_tkeep_i = k;
        dut->rx_tvalid_i = 1; dut->rx_tlast_i = (off + 8 >= n2);
        step();
    }
    dut->rx_tvalid_i = 0; dut->rx_tlast_i = 0;
    step(4000);
    printf("after TA pdu: ta_reg=%d ta_failed=%d code=0x%02x\n",
           dut->ta_registered_o, dut->ta_failed_o, dut->ta_fail_code_o);

    printf("rx_pdus=%u pdu_cnt=%u drops=%u\n", dut->rx_pdus_o, dut->pdu_cnt_o, dut->rx_drops_o);
    printf("ta_registered=%d ta_failed=%d ta_fail_code=0x%02x\n",
           dut->ta_registered_o, dut->ta_failed_o, dut->ta_fail_code_o);
    printf("domain_ok=%d listener_ready=%d leaveall_seen(n/a)\n",
           dut->domain_ok_o, dut->listener_ready_o);
    return 0;
}
