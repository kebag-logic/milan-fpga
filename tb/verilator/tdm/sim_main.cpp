// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// Item-4 TDM front-end family harness:
//   [SLOT] KL_tdm_capture TDM16 slot alignment: pulse fsync + data delay 1
//          (cap A) - pair stream {slot, L, R} sample-exact vs the driven
//          TDM frames, slots 0..7 in order, frame counter advances per wrap.
//   [FS2]  the other documented fsync mode: 50%-duty long frame sync +
//          data delay 0 (cap B) - same stimulus, same samples out.
//   [PDU]  TDM16 -> KL_aaf_packetizer(N=2): TCTX chans partitions the pair
//          slots (t0 = 8ch pairs 0..3, t1 = 2ch pair 4, pairs 5..7 unowned)
//          - t0 234-byte 8-channel AAF PDU and t1 90-byte stereo PDU
//          byte-exact vs hand-built references (IEEE 1722-2016 7.3.3/7.3.4/
//          7.3.5 header math), two epochs (seq chain + fresh payload).
#include "Vtdm_wrap.h"
#include "verilated.h"
#include <cstdio>
#include <cstdint>
#include <vector>

static Vtdm_wrap* dut;
static long checks=0, fails=0;
static void ck(const char* t, long got, long exp){
    checks++; if(got!=exp){ fails++; printf("  [FAIL] %-52s got=%ld exp=%ld\n",t,got,exp);}
    else printf("  [ ok ] %-52s = %ld\n",t,got); }

using Frame = std::vector<uint8_t>;
static std::vector<Frame> fr;  Frame cur;
struct Pair { int slot; uint32_t l, r; };
static std::vector<Pair> apairs, bpairs;

static void sample(){
    if(dut->m_tvalid_o && dut->m_tready_i){
        for(int i=0;i<8;i++) if((dut->m_tkeep_o>>i)&1)
            cur.push_back((dut->m_tdata_o>>(8*i))&0xFF);
        if(dut->m_tlast_o){ fr.push_back(cur); cur.clear(); }
    }
    if(dut->a_pv_o) apairs.push_back({(int)dut->a_slot_o, dut->a_l_o, dut->a_r_o});
    if(dut->b_pv_o) bpairs.push_back({(int)dut->b_slot_o, dut->b_l_o, dut->b_r_o});
}
static void step(){
    dut->clk=0; dut->clk_audio=0; dut->eval();
    dut->clk=1; dut->clk_audio=1; dut->eval();
    sample();
}
static void cyc(int n=1){ for(int i=0;i<n;i++) step(); }

// ---- TDM stimulus ----------------------------------------------------------
static const int SLOTS=16, WB=32, FRAME_BITS=SLOTS*WB;

static uint32_t smp(int f,int s){ return ((((uint32_t)s+1)&0x1F)<<16) | (((uint32_t)f+1)&0xFFFF); }

// bit/fsync for absolute bit index n (frame = n / FRAME_BITS)
static int tdm_bit(long n){
    int f=(int)(n/FRAME_BITS); int p=(int)(n%FRAME_BITS);
    int s=p/WB, b=p%WB;
    uint32_t w = smp(f,s)<<8;
    return (w>>(31-b))&1;
}
static int fsync_pulse(long n){ return (n%FRAME_BITS)==FRAME_BITS-1; }
static int fsync_fifty(long n){ return (n%FRAME_BITS)<FRAME_BITS/2; }

// drive both buses for nbits bit clocks (bclk half-period = 2 clk cycles;
// the master updates data/fsync on the FALLING edge, capture samples rising)
static void drive_tdm(long nbits){
    static long na=0;              // absolute bit index (persists across calls)
    for(long i=0;i<nbits;i++){
        // falling edge: present the next bit
        dut->a_bclk_i=0; dut->b_bclk_i=0;
        dut->a_data_i=tdm_bit(na);       dut->b_data_i=tdm_bit(na);
        dut->a_fsync_i=fsync_pulse(na);  dut->b_fsync_i=fsync_fifty(na);
        dut->eval(); cyc(2);
        // rising edge: capture samples the bit
        dut->a_bclk_i=1; dut->b_bclk_i=1; dut->eval(); cyc(2);
        na++;
    }
}

// ---- TCTX window write -----------------------------------------------------
static void tctx_wr(int t,int w,uint32_t v){
    dut->tctx_wr_en_i=1; dut->tctx_wr_addr_i=(uint8_t)((t<<4)|w);
    dut->tctx_wr_data_i=v;
    for(int i=0;i<32;i++){ dut->clk=0; dut->clk_audio=0; dut->eval();
        bool rdy=dut->tctx_wr_rdy_o;
        dut->clk=1; dut->clk_audio=1; dut->eval(); sample();
        if(rdy){ dut->tctx_wr_en_i=0; cyc(); return; } }
    dut->tctx_wr_en_i=0; printf("  [FAIL] tctx_wr timeout\n"); fails++; checks++;
}

// ---- hand-built AAF PDU reference (1722-2016 Fig 26 + 7.3.3/7.3.4/7.3.5) --
static Frame build_ref(int C, uint8_t seq, uint64_t dmac, uint64_t smac,
                       uint16_t uid, uint16_t vid, uint32_t ts,
                       const std::vector<std::vector<uint32_t>>& s6xC){
    Frame f(42 + 6*C*4, 0);
    for(int i=0;i<6;i++) f[i]   =(dmac>>(8*(5-i)))&0xFF;
    for(int i=0;i<6;i++) f[6+i] =(smac>>(8*(5-i)))&0xFF;
    f[12]=0x81; f[13]=0x00;
    f[14]=(3<<5)|((vid>>8)&0xF); f[15]=vid&0xFF;
    f[16]=0x22; f[17]=0xF0;
    f[18]=0x02; f[19]=0x81; f[20]=seq; f[21]=0x00;
    uint64_t sid=(smac<<16)|uid;
    for(int i=0;i<8;i++) f[22+i]=(sid>>(8*(7-i)))&0xFF;
    for(int i=0;i<4;i++) f[30+i]=(ts>>(8*(3-i)))&0xFF;
    f[34]=0x02;                       // format INT_32BIT
    f[35]=0x50 | ((C>>8)&3);          // nsr=48k, cpf[9:8] (7.3.3: 10-bit field)
    f[36]=C&0xFF;                     // channels_per_frame
    f[37]=0x20;                       // bit_depth = 32 (7.3.4)
    uint16_t sdl=6*C*4;               // stream_data_length (4.4.4.10)
    f[38]=sdl>>8; f[39]=sdl&0xFF;
    f[40]=0; f[41]=0;
    for(int i=0;i<6;i++) for(int c=0;c<C;c++){    // 7.3.5 interleave, NBO
        uint32_t v=s6xC[i][c];
        int o=42+(i*C+c)*4;
        f[o]=(v>>16)&0xFF; f[o+1]=(v>>8)&0xFF; f[o+2]=v&0xFF; f[o+3]=0;
    }
    return f;
}

static void cmp_frame(const char* t, const Frame& got, const Frame& exp){
    bool eq = (got==exp);
    if(!eq){
        printf("    %s: size got=%zu exp=%zu\n", t, got.size(), exp.size());
        for(size_t i=0;i<got.size() && i<exp.size(); i++)
            if(got[i]!=exp[i]) printf("      byte %zu: got=%02x exp=%02x\n",
                                      i, got[i], exp[i]);
    }
    ck(t, eq, 1);
}

// check a captured pair stream against the generator from its first frame
static int check_pairs(const char* tag, const std::vector<Pair>& ps, int npairs){
    if((int)ps.size() < npairs){ ck("enough pairs captured", ps.size(), npairs); return -1; }
    ck("first pair is slot 0", ps[0].slot, 0);
    int f0 = (int)(ps[0].l & 0xFFFF) - 1;      // frame encoded in the sample
    bool ok=1;
    for(int i=0;i<npairs;i++){
        int f=f0 + i/8, p=i%8;
        if(ps[i].slot != p) ok=0;
        if(ps[i].l != smp(f,2*p) || ps[i].r != smp(f,2*p+1)) ok=0;
    }
    char buf[96]; snprintf(buf,sizeof buf,"%s: %d pairs slot/L/R exact (f0=%d)",tag,npairs,f0);
    ck(buf, ok, 1);
    return f0;
}

int main(int argc,char**argv){
    Verilated::commandArgs(argc,argv);
    dut=new Vtdm_wrap;

    const uint64_t DMAC0=0x91E0F000FE01ULL, SMAC=0x020000000002ULL;
    const uint64_t DMAC1=0x91E0F000FE02ULL;
    dut->rst_n=0; dut->en_i=0; dut->m_tready_i=1;
    dut->a_bclk_i=0; dut->a_fsync_i=0; dut->a_data_i=0;
    dut->b_bclk_i=0; dut->b_fsync_i=0; dut->b_data_i=0;
    dut->dest_mac_i=DMAC0; dut->station_mac_i=SMAC;
    dut->vlan_vid_i=2; dut->ptp_ns_i=0x11223344; dut->transit_ns_i=2000000;
    dut->tctx_wr_en_i=0;
    cyc(8); dut->rst_n=1; cyc(4);

    printf("== TDM front-end family harness (item-4) ==\n");

    // partition BEFORE any pair arrives: t0 = 8ch (pairs 0..3), t1 = 2ch
    // (pair 4, TDM slots 8/9); pairs 5..7 unowned -> dropped
    tctx_wr(0, 0, (8u<<1));                       // t0 chans=8 (en/vid legacy)
    tctx_wr(1, 1, (uint32_t)(DMAC1&0xFFFFFFFF));  // t1 DMAC_LO
    tctx_wr(1, 2, (1u<<16) | (uint32_t)(DMAC1>>32)); // {UID=1, DMAC_HI}
    tctx_wr(1, 0, (2u<<5) | (2u<<1) | 1u);        // t1 CTRL {vid=2, chans=2, en}
    dut->en_i=3; cyc(4);

    // 16 TDM frames on both buses (cap A skips frame 0: its pulse fsync
    // first rises at the END of frame 0; cap B locks at frame 0)
    drive_tdm(16L*FRAME_BITS);
    cyc(2000);                                    // drain CDC + emission

    printf("\n[SLOT] cap A: pulse fsync, data delay 1 (TDM16, 32-bit slots)\n");
    int f0a = check_pairs("capA", apairs, 32);
    ck("capA locks at frame 1 (pulse rises at frame end)", f0a, 1);
    ck("capA pairs_captured liveness counter", dut->a_pairs_o >= 32, 1);

    printf("\n[FS2] cap B: 50%%-duty fsync, data delay 0\n");
    int f0b = check_pairs("capB", bpairs, 32);
    // the long fsync is HIGH at reset release; the armed edge detector must
    // ignore that level and lock on the first true rise (frame 1, pos 0)
    ck("capB locks at frame 1 (armed: level != edge)", f0b, 1);

    printf("\n[PDU] packetizer: chans-partitioned multi-channel PDUs\n");
    // expected: 2 epochs each for t0 (8ch) and t1 (2ch) = 4 frames
    ck("four AAF PDUs emitted", (long)fr.size(), 4);
    std::vector<Frame> t0f, t1f;
    for(auto& f: fr){
        if(f.size()<30) continue;
        uint16_t uid=(f[28]<<8)|f[29];
        (uid==0 ? t0f : t1f).push_back(f);
    }
    ck("two t0 (uid 0) frames", (long)t0f.size(), 2);
    ck("two t1 (uid 1) frames", (long)t1f.size(), 2);
    uint32_t ts=0x11223344u+2000000u;
    if(t0f.size()==2 && t1f.size()==2 && f0a>=0){
        for(int e=0;e<2;e++){
            std::vector<std::vector<uint32_t>> s0(6), s1(6);
            for(int i=0;i<6;i++){
                int f=f0a+e*6+i;
                for(int c=0;c<8;c++) s0[i].push_back(smp(f,c));
                s1[i]={smp(f,8), smp(f,9)};
            }
            char nm[64];
            snprintf(nm,sizeof nm,"t0 epoch %d: 234-byte 8-ch PDU byte-exact",e);
            cmp_frame(nm, t0f[e], build_ref(8,(uint8_t)e,DMAC0,SMAC,0,2,ts,s0));
            snprintf(nm,sizeof nm,"t1 epoch %d: 90-byte 2-ch PDU byte-exact",e);
            cmp_frame(nm, t1f[e], build_ref(2,(uint8_t)e,DMAC1,SMAC,1,2,ts,s1));
        }
    } else for(int k=0;k<4;k++) ck("PDU content (skipped: shape wrong)",0,1);

    printf("\n======================================================================\n");
    printf("TDM front-end family: %ld checks, %ld failures\nRESULT: %s\n",
           checks, fails, fails?"FAIL":"PASS");
    delete dut;
    return fails ? 1 : 0;
}
