// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// Item-4 TDM front-end family harness.
//
// LEVEL / ORACLE DECLARATION (docs/testing/methodology.md):
//   [SLOT] [FS2] [MCLK] [MBND] [MNEG]  L0 - module in isolation.
//        ORACLE: the module's own clause-derived expectation. For [MCLK]/[MBND]
//        that is the TDM frame's arithmetic - bclk = SLOTS x WORD_BITS x fs and
//        one fsync per frame - not a golden capture of our own output.
//   [MPAIR]                            L0, shape-matched (R4).
//        ORACLE: a per-slot-DISTINCT serial pattern, so a slot->pair mapping
//        error cannot hide behind identical samples; EVERY pair of a frame is
//        checked, not a sample of them. Negative control included: the same
//        data against a reversed map must NOT verify.
//   [PDU] [MPDU]                       L2 - real frames across a boundary port.
//        ORACLE: a hand-built reference PDU from IEEE 1722-2016 7.3.3 / 7.3.4 /
//        7.3.5 and 4.4.4.10 header math, byte for byte - not a re-read of the
//        packetizer's own output.
//   The L1 binding (pads / wrapper parameter names / front-end selection) is
//   NOT observable here and is asserted by sw/builder/test_builder.py gates 24
//   and 24b. The L5 wire claim is the silicon acceptance procedure; RTL green
//   is not silicon fixed (R6).
//
// Coverage:
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
//   [MCLK] KL_tdm_capture_master (TDM32, BCLK_HALF_P=1) - THE BUS IT
//          GENERATES: bclk period, 50% duty, fsync exactly one bclk wide,
//          one fsync per SLOTS_P*WORD_BITS_P bclks, mclk = clk_tdm/2, and
//          all of it under a synchronous reset that must leave the phase
//          clean.  A master exists precisely because nothing external drives
//          the bus, so the generated bus IS the contract.
//   [MPAIR] the same master's pair stream: slot -> pair mapping (pair k =
//          TDM slots {2k, 2k+1}, IEEE 1722-2016 7.3.5 channel order), all 16
//          pairs of a TDM32 frame in order, sample-exact against a known
//          serial pattern, and the pairs_captured liveness counter (the CSR
//          a bench read checks - see the silicon procedure).
//   [MBND] boundary: a SECOND master at SLOTS_P=8 / BCLK_HALF_P=2 off the
//          same clock - proves the divider is a real divider (bclk = clk/4)
//          and that the smallest supported slot count frames correctly.
//   [MNEG] NEGATIVE controls, because a check that cannot fail proves
//          nothing: (1) the pair stream must NOT match a deliberately wrong
//          slot->pair map, (2) a master whose data line is held 0 must still
//          produce pairs - at the right rate and all-zero - which is exactly
//          the pmoda-less AX7101 failure mode (digital silence at the right
//          frame width, not silence of frames).
//   [MPDU] master -> KL_aaf_packetizer(WIRE_CHANS_P=8): the end-to-end claim.
//          A 234-byte EIGHT-channel AAF PDU, byte-exact, sourced from a
//          front-end that nobody drives.  This is the shape the AX7101 8x8
//          talkers advertise (0x0205022002006000) and which the fabric
//          emitted as 2 channels on 2026-07-27.
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
static std::vector<Frame> fr, mfr;  Frame cur, mcur;
struct Pair { int slot; uint32_t l, r; };
static std::vector<Pair> apairs, bpairs, mpairs, m2pairs;

// ---- MASTER-role instrumentation ------------------------------------------
// A master GENERATES the bus, so the bus is part of what must be checked. Every
// measurement below is in clk_tdm cycles (one per step()).
struct BusMon {
    int  prev_bclk = 0, prev_fsync = 0, prev_mclk = 0;
    long lvl_since = 0;                 // cycles the current bclk level has held
    long hi_min = 1e9, hi_max = 0, lo_min = 1e9, lo_max = 0;
    long mhi_min = 1e9, mhi_max = 0, mlo_min = 1e9, mlo_max = 0, mlvl_since = 0;
    long rises = 0;                     // bclk rises seen
    long fs_hi_rises = 0;               // rises with fsync asserted
    long last_fs_rise = -1;             // rise index of the last fsync-high rise
    std::vector<long> fs_gaps;          // rises between consecutive fsync highs
    std::vector<long> fs_widths;        // consecutive fsync-high rises (burst len)
    long fs_run = 0;
    bool armed = false;                 // measurements enabled (post-reset)
};
static BusMon mmon, m2mon;

static void bus_observe(BusMon& m, int bclk, int fsync, int mclk, bool have_mclk){
    if(m.armed){
        m.lvl_since++;
        if(bclk != m.prev_bclk){
            if(m.prev_bclk){ if(m.lvl_since<m.hi_min)m.hi_min=m.lvl_since;
                             if(m.lvl_since>m.hi_max)m.hi_max=m.lvl_since; }
            else           { if(m.lvl_since<m.lo_min)m.lo_min=m.lvl_since;
                             if(m.lvl_since>m.lo_max)m.lo_max=m.lvl_since; }
            m.lvl_since = 0;
        }
        if(have_mclk){
            m.mlvl_since++;
            if(mclk != m.prev_mclk){
                if(m.prev_mclk){ if(m.mlvl_since<m.mhi_min)m.mhi_min=m.mlvl_since;
                                 if(m.mlvl_since>m.mhi_max)m.mhi_max=m.mlvl_since; }
                else           { if(m.mlvl_since<m.mlo_min)m.mlo_min=m.mlvl_since;
                                 if(m.mlvl_since>m.mlo_max)m.mlo_max=m.mlvl_since; }
                m.mlvl_since = 0;
            }
        }
        if(bclk && !m.prev_bclk){            // bclk RISE: the sampling edge
            m.rises++;
            if(fsync){
                if(m.last_fs_rise>=0 && m.fs_run==0)
                    m.fs_gaps.push_back(m.rises - m.last_fs_rise);
                m.last_fs_rise = m.rises;
                m.fs_hi_rises++; m.fs_run++;
            } else if(m.fs_run){ m.fs_widths.push_back(m.fs_run); m.fs_run = 0; }
        }
    }
    m.prev_bclk = bclk; m.prev_fsync = fsync; m.prev_mclk = mclk;
}

static void sample(){
    if(dut->m_tvalid_o && dut->m_tready_i){
        for(int i=0;i<8;i++) if((dut->m_tkeep_o>>i)&1)
            cur.push_back((dut->m_tdata_o>>(8*i))&0xFF);
        if(dut->m_tlast_o){ fr.push_back(cur); cur.clear(); }
    }
    if(dut->mp_tvalid_o && dut->mp_tready_i){
        for(int i=0;i<8;i++) if((dut->mp_tkeep_o>>i)&1)
            mcur.push_back((dut->mp_tdata_o>>(8*i))&0xFF);
        if(dut->mp_tlast_o){ mfr.push_back(mcur); mcur.clear(); }
    }
    if(dut->a_pv_o) apairs.push_back({(int)dut->a_slot_o, dut->a_l_o, dut->a_r_o});
    if(dut->b_pv_o) bpairs.push_back({(int)dut->b_slot_o, dut->b_l_o, dut->b_r_o});
    if(dut->m_pv_o) mpairs.push_back({(int)dut->m_slot_o, dut->m_l_o, dut->m_r_o});
    if(dut->m2_pv_o) m2pairs.push_back({(int)dut->m2_slot_o, dut->m2_l_o, dut->m2_r_o});
}

// ---- MASTER serial driver --------------------------------------------------
// We are the CODEC here: the fabric owns bclk/fsync, we present a bit on the
// bclk FALLING edge and it samples on the RISING edge (KL_tdm_capture_master's
// documented convention, and the slave's - so a loopback interoperates).
//
// DATA_DELAY_P = 1 (DSP mode B / Philips heritage): fsync is asserted for the
// whole of bclk 0 of the frame, `startp_r` registers on the NEXT rise, and the
// slot-0 MSB is sampled on the rise AFTER that.  So from the rise where fsync
// is seen high we must let ONE falling edge pass before presenting bit 0.
// That is asserted, not assumed - [MPAIR] fails visibly on a one-bit slip.
static const int MSLOTS=32, M2SLOTS=8, WB=32;
static const int MFRAME_BITS = MSLOTS*WB, M2FRAME_BITS = M2SLOTS*WB;
// 6-bit slot tag so slot 31 stays distinguishable (the 5-bit tag the 16-slot
// buses use would alias slot 31 onto 0)
static uint32_t msmp(int f,int s){ return ((((uint32_t)s+1)&0x3F)<<16) | (((uint32_t)f+1)&0xFFFF); }

struct SerDrv {
    int  slots, frame_bits;
    long n = 0;              // bit index inside the frame
    int  f = -1;             // frame number
    int  pend = 0;           // falling edges to skip after an fsync-high rise
    bool silent = false;     // hold the line at 0 (the digital-silence control)
    int  prev_bclk = 0;
};
static SerDrv mdrv{MSLOTS, MFRAME_BITS}, m2drv{M2SLOTS, M2FRAME_BITS};

static int ser_bit(SerDrv& d){
    if(d.silent || d.f < 0) return 0;
    int s = (int)(d.n / WB), b = (int)(d.n % WB);
    uint32_t w = msmp(d.f, s) << 8;              // 24-bit sample in bits 31..8
    return (w >> (31-b)) & 1;
}
// called every step, BEFORE eval, with the bclk/fsync sampled after the last eval
static int ser_next(SerDrv& d, int bclk, int fsync, int cur_bit){
    int out = cur_bit;
    if(bclk && !d.prev_bclk && fsync) d.pend = 2;   // rise with fsync asserted
    if(!bclk && d.prev_bclk){                        // FALL: present the next bit
        if(d.pend && --d.pend == 0){ d.n = 0; d.f++; }
        out = ser_bit(d);
        d.n++;
        if(d.n >= d.frame_bits) d.n = 0;             // free-run between fsyncs
    }
    d.prev_bclk = bclk;
    return out;
}

static void step(){
    // present the master buses' data for the coming edge (codec-side, falling)
    dut->m_data_i  = ser_next(mdrv,  dut->m_bclk_o,  dut->m_fsync_o,  dut->m_data_i);
    dut->m2_data_i = ser_next(m2drv, dut->m2_bclk_o, dut->m2_fsync_o, dut->m2_data_i);
    dut->clk=0; dut->clk_audio=0; dut->clk_tdm=0; dut->eval();
    dut->clk=1; dut->clk_audio=1; dut->clk_tdm=1; dut->eval();
    bus_observe(mmon,  dut->m_bclk_o,  dut->m_fsync_o,  dut->m_mclk_o,  true);
    bus_observe(m2mon, dut->m2_bclk_o, dut->m2_fsync_o, 0,              false);
    sample();
}
static void cyc(int n=1){ for(int i=0;i<n;i++) step(); }

// ---- TDM stimulus ----------------------------------------------------------
static const int SLOTS=16, FRAME_BITS=SLOTS*WB;

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

// ---- MASTER pair-stream checker -------------------------------------------
// Pair k carries TDM slots {2k, 2k+1} (KL_tdm_capture_master's channel-map
// contract, and what KL_aaf_packetizer's TCTX chans prefix-sum assumes).
// `xslot` deliberately mangles that map: passing it must make the check FAIL,
// which is how we know the check can fail at all.
static bool master_pairs_ok(const std::vector<Pair>& ps, size_t from,
                            int slots, int nframes, int* f0_out, bool xslot=false){
    int pf = slots/2;                          // pairs per TDM frame
    // find the start of a clean frame: slot 0 with a decodable sample
    size_t i0 = from;
    while(i0 + (size_t)pf*nframes <= ps.size() &&
          !(ps[i0].slot==0 && (ps[i0].l & 0xFFFF))) i0++;
    if(i0 + (size_t)pf*nframes > ps.size()) return false;
    int f0 = (int)(ps[i0].l & 0xFFFF) - 1;
    if(f0_out) *f0_out = f0;
    for(int n=0;n<pf*nframes;n++){
        const Pair& p = ps[i0+n];
        int f = f0 + n/pf, k = n%pf;
        int ks = xslot ? (pf-1-k) : k;         // the mangled map for the control
        if(p.slot != ks) return false;
        if(p.l != msmp(f, 2*k) || p.r != msmp(f, 2*k+1)) return false;
    }
    return true;
}

int main(int argc,char**argv){
    Verilated::commandArgs(argc,argv);
    dut=new Vtdm_wrap;

    const uint64_t DMAC0=0x91E0F000FE01ULL, SMAC=0x020000000002ULL;
    const uint64_t DMAC1=0x91E0F000FE02ULL, DMACM=0x91E0F000FE03ULL;
    dut->rst_n=0; dut->en_i=0; dut->m_tready_i=1;
    dut->a_bclk_i=0; dut->a_fsync_i=0; dut->a_data_i=0;
    dut->b_bclk_i=0; dut->b_fsync_i=0; dut->b_data_i=0;
    dut->m_data_i=0; dut->m2_data_i=0;
    dut->mp_en_i=0; dut->mp_dest_mac_i=DMACM; dut->mp_tready_i=1;
    dut->dest_mac_i=DMAC0; dut->station_mac_i=SMAC;
    dut->vlan_vid_i=2; dut->ptp_ns_i=0x11223344; dut->transit_ns_i=2000000;
    dut->tctx_wr_en_i=0;
    // NEGATIVE control #2, armed from the start: bus M2's data line is HELD 0.
    // That is the pmoda-less AX7101 exactly (i_i2s_sdout_i = 0) - and the point
    // is that it must still produce PAIRS, at the right rate, of digital
    // silence. Silence of SAMPLES is a pads problem; silence of FRAMES is what
    // a tied-off slave bus produces, and the two are not the same defect.
    m2drv.silent = true;
    cyc(8); dut->rst_n=1; cyc(4);
    mmon.armed = m2mon.armed = true;      // measure only post-reset
    dut->mp_en_i=1;                       // master-fed talker on from the start

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

    // =======================================================================
    //  THE MASTER ROLE (2026-07-28). Everything above is driven by the
    //  harness; everything below is driven by the FABRIC, which is the whole
    //  point: on every SoC in this tree the slave's bclk/fsync are tied to 0,
    //  so a slave TDM build yields no pairs and its talkers emit no frame.
    // =======================================================================
    printf("\n[MCLK] master TDM32 (BCLK_HALF_P=1): the bus it GENERATES\n");
    // bclk = clk_tdm / (2*BCLK_HALF_P) -> one clk_tdm cycle per half period
    ck("M bclk high width = 1 clk_tdm cycle (min)", mmon.hi_min, 1);
    ck("M bclk high width = 1 clk_tdm cycle (max)", mmon.hi_max, 1);
    ck("M bclk low  width = 1 clk_tdm cycle (min)", mmon.lo_min, 1);
    ck("M bclk low  width = 1 clk_tdm cycle (max)", mmon.lo_max, 1);
    // tdm_mclk_o is the convenience codec MCLK: clk_tdm/2, same as the slave's
    ck("M mclk high width = 1 clk_tdm cycle", mmon.mhi_max, 1);
    ck("M mclk low  width = 1 clk_tdm cycle", mmon.mlo_max, 1);
    // fsync: a ONE-BCLK pulse (TI/McASP shape), one per SLOTS_P*WORD_BITS_P
    // bclks. KL_tdm_capture accepts both this and the 50%-duty long frame, so
    // our own master loops back into our own slave.
    {   bool w1 = !mmon.fs_widths.empty();
        for(long w : mmon.fs_widths) if(w != 1) w1 = false;
        ck("M fsync is exactly ONE bclk wide, every frame", w1, 1);
        bool g = !mmon.fs_gaps.empty();
        for(long v : mmon.fs_gaps) if(v != MFRAME_BITS) g = false;
        ck("M fsync cadence = SLOTS_P*WORD_BITS_P = 1024 bclks", g, 1);
        char b[96];
        snprintf(b,sizeof b,"M frames observed (fsync gaps measured)");
        ck(b, (long)mmon.fs_gaps.size() >= 8, 1);
    }
    printf("\n[MBND] master TDM8 (BCLK_HALF_P=2): the divider is a real divider\n");
    ck("M2 bclk high width = 2 clk_tdm cycles (min)", m2mon.hi_min, 2);
    ck("M2 bclk high width = 2 clk_tdm cycles (max)", m2mon.hi_max, 2);
    ck("M2 bclk low  width = 2 clk_tdm cycles (max)", m2mon.lo_max, 2);
    {   bool g = !m2mon.fs_gaps.empty();
        for(long v : m2mon.fs_gaps) if(v != M2FRAME_BITS) g = false;
        ck("M2 fsync cadence = 8*32 = 256 bclks", g, 1);
    }

    printf("\n[MNEG] negative control: data line held 0 must still frame\n");
    // The pmoda-less AX7101 failure mode, isolated: an unfed line is DIGITAL
    // SILENCE at the correct frame width, NOT an absence of frames. If this
    // ever reports zero pairs the master has stopped being a master.
    ck("M2 (silent line) still produced pairs", (long)(m2pairs.size() > 0), 1);
    {   bool zero = true, slots_ok = true;
        for(size_t i=0;i<m2pairs.size();i++){
            if(m2pairs[i].l || m2pairs[i].r) zero = false;
            if(m2pairs[i].slot != (int)(i % 4)) slots_ok = false;
        }
        ck("M2 silent pairs are all-zero samples", zero, 1);
        ck("M2 silent pairs still cycle slots 0..3 in order", slots_ok, 1);
    }
    size_t m2_mark = m2pairs.size();
    m2drv.silent = false;                     // now feed the real pattern
    cyc(8L*M2FRAME_BITS*4);                   // 8 TDM8 frames at bclk = clk/4
    cyc(400);                                 // drain the CDC

    printf("\n[MPAIR] master pair stream: slot -> pair map and sample values\n");
    int mf0 = -1, m2f0 = -1;
    ck("M produced >= 6 TDM32 frames of pairs", (long)(mpairs.size() >= 16*6), 1);
    ck("M 6 frames x 16 pairs slot/L/R exact (pair k = slots {2k,2k+1})",
       master_pairs_ok(mpairs, 0, MSLOTS, 6, &mf0), 1);
    ck("M pairs_captured liveness counter advanced", (long)(dut->m_pairs_o >= 16*6), 1);
    ck("M2 4 frames x 4 pairs slot/L/R exact after the line came up",
       master_pairs_ok(m2pairs, m2_mark, M2SLOTS, 4, &m2f0), 1);
    // NEGATIVE control #1: the SAME data against a deliberately reversed
    // slot->pair map must NOT verify. Without this, "the map is right" and
    // "the checker ignores the map" look identical.
    ck("M pair map check REJECTS a reversed map (proves it can fail)",
       master_pairs_ok(mpairs, 0, MSLOTS, 6, nullptr, /*xslot=*/true), 0);

    printf("\n[MPDU] master -> packetizer: an EIGHT-channel AAF PDU off a\n"
           "       front-end nobody drives (IEEE 1722-2016 7.3.3/7.3.4/7.3.5)\n");
    // THE LANE'S CLAIM. The AX7101 8x8 talkers advertise 0x0205022002006000 =
    // AAF PCM32 48 kHz EIGHT channels; on 2026-07-27 the fabric emitted 2 and
    // a Milan-validated listener discarded 296,294 of 296,294 frames as
    // UNSUPPORTED_FORMAT. channels_per_frame is IEEE 1722-2016 7.3.3 (a
    // 10-bit field spanning bytes 35..36 of the frame), bit_depth 7.3.4,
    // the interleaved payload 7.3.5.
    {   std::vector<Frame> good;
        for(auto& f : mfr)
            if(f.size() >= 46 && (f[42]||f[43]||f[44])) good.push_back(f);
        ck("master-fed talker emitted >= 2 AAF PDUs", (long)(good.size() >= 2), 1);
        if(good.size() >= 2){
            ck("PDU length = 42 + 6 x 8ch x 4B = 234 bytes", (long)good[0].size(), 234);
            ck("7.3.3 channels_per_frame = 8", (long)good[0][36], 8);
            ck("7.3.3 cpf[9:8] = 0 (10-bit field)", (long)(good[0][35] & 0x03), 0);
            ck("7.3.3 nsr = 48 kHz (0x5)", (long)((good[0][35]>>4)&0xF), 5);
            ck("7.3.4 bit_depth = 32", (long)good[0][37], 32);
            ck("4.4.4.10 stream_data_length = 192",
               (long)((good[0][38]<<8)|good[0][39]), 192);
            uint32_t s0 = ((uint32_t)good[0][42]<<16)|((uint32_t)good[0][43]<<8)
                          |(uint32_t)good[0][44];
            int f0 = (int)(s0 & 0xFFFF) - 1;
            uint8_t seq = good[0][20];
            ck("PDU seq chain is contiguous", (long)good[1][20],
               (long)(uint8_t)(seq+1));
            uint32_t ts = 0x11223344u + 2000000u;
            for(int e=0;e<2;e++){
                std::vector<std::vector<uint32_t>> s(6);
                for(int i=0;i<6;i++)
                    for(int c=0;c<8;c++) s[i].push_back(msmp(f0+e*6+i, c));
                char nm[80];
                snprintf(nm,sizeof nm,
                         "master epoch %d: 234-byte 8-channel PDU byte-exact",e);
                cmp_frame(nm, good[e],
                          build_ref(8,(uint8_t)(seq+e),DMACM,SMAC,0,2,ts,s));
            }
        } else for(int k=0;k<10;k++) ck("MPDU content (skipped: no PDUs)",0,1);
    }

    printf("\n======================================================================\n");
    printf("TDM front-end family: %ld checks, %ld failures\nRESULT: %s\n",
           checks, fails, fails?"FAIL":"PASS");
    delete dut;
    return fails ? 1 : 0;
}
