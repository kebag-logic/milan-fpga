// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// Self-checking harness for KL_maap — IEEE 1722 Annex B vs the pipewire
// maap.c reference contract: 3 probes @500ms+jitter -> announce @3-5s
// (address valid only announced); RX PROBE conflict: probing->re-address,
// announced->DEFEND with the overlap; RX DEFEND/ANNOUNCE with conflicting
// CONFLICT fields -> re-address (reference quirk: the REQUEST fields of a
// received ANNOUNCE are NOT checked - byte-faithful to maap.c).
// Scaled clock: CLK_FREQ_HZ_P=10000 -> 1 ms = 10 cycles.
#include "VKL_maap.h"
#include "verilated.h"
#if VM_COVERAGE
#include "verilated_cov.h"
#endif
#include <cstdio>
#include <cstdint>
#include <cstring>
#include <vector>

static VKL_maap* dut;
static long checks=0, fails=0;
static void ck(const char* t, long got, long exp){
    checks++; if(got!=exp){ fails++; printf("  [FAIL] %-44s got=%ld exp=%ld\n",t,got,exp);}
    else printf("  [ ok ] %-44s = %ld\n",t,got); }

static std::vector<uint8_t> txf;      // collected TX frame (wire bytes)
static bool tx_done=false;

static void cyc(int n=1){
    for(int i=0;i<n;i++){
        dut->clk_i=0; dut->eval();
        dut->clk_i=1; dut->eval();
        if(dut->m_axis_tvalid && dut->m_axis_tready){
            int nb = (dut->m_axis_tkeep==0xFF)?8:4;
            for(int l=0;l<nb;l++) txf.push_back((dut->m_axis_tdata>>(8*l))&0xFF);
            if(dut->m_axis_tlast) tx_done=true;
        }
    }
}

// run until a full TX frame is captured or budget expires; returns frame.
// txf is NOT cleared on entry: a frame may already be in flight (e.g. a
// DEFEND that starts during inject()) and must not be truncated.
static std::vector<uint8_t> wait_tx(int budget){
    for(int i=0;i<budget && !tx_done;i++) cyc();
    auto f=txf; txf.clear(); tx_done=false;
    return f;
}

// inject a MAAP PDU on the RX tap (untagged, 60B padded)
static void inject(uint8_t msg, uint16_t req_off, uint16_t req_cnt,
                   uint16_t conf_off, uint16_t conf_cnt, bool conf_pool=true){
    uint8_t f[64]; memset(f,0,sizeof f);
    const uint8_t dst[6]={0x91,0xE0,0xF0,0x00,0xFF,0x00};
    const uint8_t src[6]={0x66,0x77,0x88,0x99,0xAA,0xBB};
    memcpy(f,dst,6); memcpy(f+6,src,6);
    f[12]=0x22; f[13]=0xF0; f[14]=0xFE; f[15]=msg;
    f[16]=0x08; f[17]=0x1C;
    f[26]=0x91; f[27]=0xE0; f[28]=0xF0; f[29]=0x00;
    f[30]=req_off>>8; f[31]=req_off;
    f[32]=req_cnt>>8; f[33]=req_cnt;
    if(conf_pool){ f[34]=0x91; f[35]=0xE0; f[36]=0xF0; f[37]=0x00; }
    f[38]=conf_off>>8; f[39]=conf_off;
    f[40]=conf_cnt>>8; f[41]=conf_cnt;
    for(int b=0;b<8;b++){
        uint64_t v=0;
        for(int j=0;j<8;j++) v|=(uint64_t)f[b*8+j]<<(8*j);
        dut->rx_tdata_i=v; dut->rx_tkeep_i=(b==7)?0x0F:0xFF;
        dut->rx_tvalid_i=1; dut->rx_tready_i=1; dut->rx_tlast_i=(b==7);
        cyc();
    }
    dut->rx_tvalid_i=0; dut->rx_tlast_i=0; cyc(3);
}

int main(int argc,char**argv){
    Verilated::commandArgs(argc,argv);
    dut=new VKL_maap;

    const uint64_t MAC=0x020000000001ULL;   // 02:00:00:00:00:01
    dut->station_mac_i=MAC;
    dut->enable_i=0; dut->count_i=8;
    dut->seed_offset_i=0; dut->seed_valid_i=0;
    dut->m_axis_tready=1; dut->rx_tvalid_i=0;
    dut->rst_n=0; cyc(6); dut->rst_n=1; cyc(3);

    printf("== KL_maap harness (10 kHz scaled: 1 ms = 10 cyc) ==\n");

    printf("\n[1] reset/idle\n");
    ck("state IDLE", dut->state_o, 0);
    ck("addr not valid", dut->addr_valid_o, 0);

    printf("\n[2] enable -> PROBE, three golden probes, then ANNOUNCE\n");
    dut->enable_i=1; cyc(3);
    ck("state PROBE", dut->state_o, 1);
    uint16_t off0 = dut->offset_o;
    ck("offset inside pool", off0 <= 0xFDF8, 1);
    for(int p=0;p<3;p++){
        auto f=wait_tx(9000);          // 500-627ms = 5000-6270 cyc
        char nm[64]; snprintf(nm,sizeof nm,"probe %d emitted (60B)",p+1);
        ck(nm, (long)f.size(), 60);
        if(f.size()==60){
            ck("dst 91:E0:F0:00:FF:00", memcmp(f.data(),
               (const uint8_t[]){0x91,0xE0,0xF0,0x00,0xFF,0x00},6)==0, 1);
            ck("src station mac", f[6]==0x02&&f[11]==0x01, 1);
            ck("ethertype/subtype", f[12]==0x22&&f[13]==0xF0&&f[14]==0xFE, 1);
            ck("msg PROBE", f[15]&0x0F, 1);
            ck("version/len bytes", f[16]==0x08&&f[17]==0x1C, 1);
            ck("request_start pool+off",
               f[26]==0x91&&f[27]==0xE0&&f[28]==0xF0&&f[29]==0x00&&
               f[30]==(off0>>8)&&f[31]==(off0&0xFF), 1);
            ck("request_count 8", (f[32]<<8)|f[33], 8);
            ck("conflict fields zero",
               f[34]|f[35]|f[36]|f[37]|f[38]|f[39]|f[40]|f[41], 0);
        }
    }
    ck("state ANNOUNCE after 3 probes", dut->state_o, 2);
    ck("addr valid", dut->addr_valid_o, 1);
    ck("addr = pool base + offset",
       (long)((dut->addr_o>>16)&0xFFFFFFFF)==0x91E0F000UL &&
       (dut->addr_o&0xFFFF)==off0, 1);

    printf("\n[3] first ANNOUNCE frame (msg 3, same request fields)\n");
    { auto f=wait_tx(55000);           // 3000-5047ms
      ck("announce emitted", (long)f.size(), 60);
      if(f.size()==60){
          ck("msg ANNOUNCE", f[15]&0x0F, 3);
          ck("announce offset unchanged", f[30]==(off0>>8)&&f[31]==(off0&0xFF), 1);
      } }

    printf("\n[4] announced + conflicting PROBE -> DEFEND with the overlap\n");
    inject(1, off0+4, 8, 0, 0);        // overlaps [off0+4, off0+12)
    { auto f=wait_tx(200);
      ck("DEFEND emitted promptly", (long)f.size(), 60);
      if(f.size()==60){
          ck("msg DEFEND", f[15]&0x0F, 2);
          uint16_t cs=(f[38]<<8)|f[39], cc=(f[40]<<8)|f[41];
          ck("conflict start = overlap start", cs, off0+4);
          ck("conflict count = overlap size", cc, 4);
      } }
    ck("still ANNOUNCE", dut->state_o, 2);
    ck("defends counted", dut->defends_o, 1);   // 4b makes it 2 later

    printf("\n[4b] DEFEND overlap branch 2: prober's range starts below ours\n");
    inject(1, off0-4, 8, 0, 0);        // our_start inside [off0-4, off0+4]
    { auto f=wait_tx(200);
      ck("DEFEND emitted (branch 2)", (long)f.size(), 60);
      if(f.size()==60){
          uint16_t cs=(f[38]<<8)|f[39], cc=(f[40]<<8)|f[41];
          ck("conflict start = our start", cs, off0);
          ck("conflict count = overlap", cc, 4);
      } }

    printf("\n[4c] unknown message type ignored\n");
    inject(5, off0, 8, off0, 8);
    cyc(50);
    ck("unknown msg: still ANNOUNCE", dut->state_o, 2);

    printf("\n[5] reference quirk: ANNOUNCE with covering REQUEST is ignored\n");
    inject(3, off0, 8, 0, 0);
    cyc(50);
    ck("no re-address (state ANNOUNCE)", dut->state_o, 2);
    ck("offset unchanged", dut->offset_o, off0);

    printf("\n[6] DEFEND with conflicting CONFLICT fields -> re-address\n");
    inject(2, 0, 0, off0, 8);
    cyc(50);
    ck("back to PROBE", dut->state_o, 1);
    ck("addr dropped", dut->addr_valid_o, 0);
    ck("offset changed", dut->offset_o != off0, 1);
    ck("conflicts counted", dut->conflicts_o, 1);

    printf("\n[7] probing + conflicting PROBE -> silent re-address\n");
    uint16_t off1 = dut->offset_o;
    inject(1, off1, 8, 0, 0);
    cyc(50);
    ck("still PROBE", dut->state_o, 1);
    ck("offset changed again", dut->offset_o != off1, 1);
    ck("conflicts = 2", dut->conflicts_o, 2);

    printf("\n[8] non-conflicting + non-pool PDUs ignored\n");
    uint16_t off2 = dut->offset_o;
    inject(1, (uint16_t)(off2+1000), 8, 0, 0);        // disjoint range
    inject(2, 0, 0, off2, 8, /*conf_pool=*/false);    // wrong pool prefix
    cyc(50);
    ck("offset stable", dut->offset_o, off2);
    ck("conflicts still 2", dut->conflicts_o, 2);

    printf("\n[9] disable -> IDLE; seeded re-enable claims the seed\n");
    dut->enable_i=0; cyc(5);
    ck("IDLE on disable", dut->state_o, 0);
    dut->seed_offset_i=0x1234; dut->seed_valid_i=1;
    dut->enable_i=1; cyc(3);
    ck("seeded offset", dut->offset_o, 0x1234);
    ck("PROBE with seed", dut->state_o, 1);

    printf("\n======================================================================\n");
    printf("KL_maap: %ld checks, %ld failures\n", checks, fails);
#if VM_COVERAGE
    Verilated::threadContextp()->coveragep()->write("coverage.dat");
#endif
    delete dut;
    return fails ? 1 : 0;
}
