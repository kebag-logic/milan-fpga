// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// Digital audio loop: KL_aaf_packetizer (talker, N=1, direct pair injection)
// -> avtp_stream_parser -> KL_avtp_rx_monitor -> KL_aaf_rx_depacketizer
// (listener). Drives a coherent 1 kHz tone (48 kHz, 24-bit, -12 dBFS - the
// bench tone_1k_m12 amplitude) into the talker and proves:
//   (1) every AAF PDU is stream+format matched and ACCEPTED (FRAMES_RX),
//   (2) the recovered S32BE payload is BIT-EXACT to the injected samples
//       (the packetize/depacketize path adds nothing - the pad byte is 0),
//   (3) the THD+N of the recovered tone sits at the 24-bit quantization
//       floor (a bit-exact path contributes 0 dB of its own).
// This closes the talker->listener AUDIO gap the per-block unit TBs never
// covered - offline, no board.
#include "Vaaf_audio_loop_wrap.h"
#include "verilated.h"
#include <cstdio>
#include <cstdint>
#include <vector>
#include <cmath>

static const double PI = 3.14159265358979323846;

static Vaaf_audio_loop_wrap* dut;
static long checks = 0, fails = 0;
static void ck(const char* t, long got, long exp){
    checks++;
    if(got != exp){ fails++; printf("  [FAIL] %-46s got=%ld exp=%ld\n", t, got, exp); }
    else           printf("  [ ok ] %-46s = %ld\n", t, got);
}

// ---- coherent 1 kHz tone: 48000 * 32 / 1536 = 1000 Hz exactly -------------
static const int    M     = 1536;      // analysis window = 32 whole cycles
static const int    KCYC  = 32;        // fundamental bin
static const int    NF    = 300;       // frames to inject (1800 pairs > M + margin)
static const int    AMP   = (1 << 21); // -12.04 dBFS (matches bench tone_1k_m12)

static int32_t tone24(int n){          // signed 24-bit sample of the tone
    double v = AMP * sin(2.0 * PI * KCYC * n / M);
    long q = lround(v);
    if(q >  (1 << 23) - 1) q =  (1 << 23) - 1;
    if(q < -(1 << 23))     q = -(1 << 23);
    return (int32_t)q;
}

// ---- recovered payload capture (S32BE, always full 8-byte beats) ----------
static std::vector<uint8_t> rxcur;
static std::vector<int32_t> rsamp;     // sign-extended 24-bit, interleaved L,R
static long padbad = 0, framebad = 0;

static void capture(){
    if(dut->pcm_tvalid_o && dut->pcm_tready_i){
        uint64_t d = dut->pcm_tdata_o;                 // full word (no partial beats)
        for(int i = 0; i < 8; i++) rxcur.push_back((d >> (8*i)) & 0xFF);
        if(dut->pcm_tlast_o){
            if(rxcur.size() % 4 != 0) framebad++;
            for(size_t o = 0; o + 3 < rxcur.size(); o += 4){
                int32_t s = (rxcur[o] << 16) | (rxcur[o+1] << 8) | rxcur[o+2];
                if(rxcur[o+3] != 0) padbad++;          // 24-in-32, low byte must be 0
                if(s & 0x800000) s -= 0x1000000;       // sign-extend 24-bit
                rsamp.push_back(s);
            }
            rxcur.clear();
        }
    }
}

static void step(){ dut->clk = 0; dut->eval(); dut->clk = 1; dut->eval(); capture(); }
static void cyc(int n){ for(int i = 0; i < n; i++) step(); }

static void inject_pair(int32_t l, int32_t r){
    dut->pair_l_i = (uint32_t)(l & 0xFFFFFF);
    dut->pair_r_i = (uint32_t)(r & 0xFFFFFF);
    dut->pair_valid_i = 1; step();
    dut->pair_valid_i = 0; cyc(23);        // drain cadence (proven in NxN P4)
}

int main(int argc, char** argv){
    Verilated::commandArgs(argc, argv);
    dut = new Vaaf_audio_loop_wrap;

    // talker config (t0 via direct CSR-alias inputs)
    dut->rst_n = 0; dut->stream_en_i = 0; dut->pair_valid_i = 0;
    dut->dest_mac_i    = 0x91E0F000FE01ULL;
    dut->station_mac_i = 0x020000000002ULL;
    dut->vlan_vid_i    = 2;
    dut->transit_ns_i  = 2000000;
    dut->ptp_ns_i      = 0x11223344;
    dut->pcm_tready_i  = 1;
    // listener binding the ACMP/AECP SM would install
    dut->cfg_sid_i     = 0x0200000000020000ULL;   // {station_mac, uid=0}
    dut->bound_i       = 1;
    dut->fmt_i         = 0x0205022002006000ULL;    // AAF/48k/INT32/32/8ch-max
    dut->ptp_now_i     = 0x11223344;
    dut->pres_ofs_i    = 2000000;
    dut->servo_conv_i  = 1;

    cyc(8); dut->rst_n = 1; dut->stream_en_i = 1; cyc(8);

    printf("== AAF talker -> listener digital audio loop ==\n");
    printf("   1 kHz tone, 48 kHz, 24-bit, -12 dBFS, %d frames\n", NF);

    const int total = NF * 6;
    for(int n = 0; n < total; n++) inject_pair(tone24(n), tone24(n));
    cyc(600);                                       // final drain

    // ---- accounting ------------------------------------------------------
    printf("\n[accounting]\n");
    ck("talker emitted >= NF frames", (long)dut->frames_sent_o >= NF, 1);
    ck("listener FRAMES_RX == talker frames", (long)dut->frames_rx_o,
                                              (long)dut->frames_sent_o);
    ck("UNSUPPORTED_FORMAT rejects = 0",   (long)dut->unsupported_fmt_o, 0);
    ck("depacketizer whole-frame drops = 0", (long)dut->pcm_drops_o, 0);
    ck("recovered >= 2*M samples (L+R)", (long)rsamp.size() >= (long)(2*M), 1);
    ck("every payload frame length %%4==0", framebad, 0);
    ck("S32BE pad byte always 0 (24-in-32)", padbad, 0);

    // ---- bit-exact transparency -----------------------------------------
    printf("\n[bit-exact transparency]\n");
    long npairs = (long)rsamp.size() / 2;
    long off = -1;
    for(int cand = 0; cand < 12 && off < 0; cand++){
        bool okc = true;
        for(int k = 0; k < 8; k++)
            if(rsamp[2*k] != tone24(k + cand)){ okc = false; break; }
        if(okc) off = cand;
    }
    ck("recovered stream aligns to source", off >= 0, 1);
    if(off < 0) off = 0;
    long mism = 0, ncmp = 0;
    for(long k = 0; k + off < total && k < npairs; k++){
        int32_t exp = tone24((int)(k + off));
        if(rsamp[2*k]     != exp) mism++;
        if(rsamp[2*k + 1] != exp) mism++;
        ncmp++;
    }
    printf("  [info] compared %ld pairs (L+R), alignment offset %ld\n", ncmp, off);
    ck("BYTE-EXACT: recovered L/R == injected tone", mism, 0);

    // ---- THD+N of the recovered tone ------------------------------------
    printf("\n[audio-domain THD+N of the recovered stream]\n");
    if((long)rsamp.size() >= 2*M){
        std::vector<double> x(M);
        for(int i = 0; i < M; i++) x[i] = (double)rsamp[2*i];   // L channel
        double mean = 0; for(double v : x) mean += v; mean /= M;
        for(double& v : x) v -= mean;
        double re = 0, im = 0;
        for(int n = 0; n < M; n++){
            double a = 2.0 * PI * KCYC * n / M;
            re += x[n] * cos(a); im -= x[n] * sin(a);
        }
        double Efund = 2.0 * (re*re + im*im) / M;
        double Etot  = 0; for(double v : x) Etot += v*v;
        double thdn  = 10.0 * log10((Etot - Efund) / Efund);
        printf("  [info] recovered 1 kHz THD+N = %.1f dB "
               "(24-bit source quant floor; path adds 0)\n", thdn);
        ck("recovered-tone THD+N <= -120 dB", thdn <= -120.0, 1);
    } else {
        ck("recovered-tone THD+N (skipped: too few samples)", 0, 1);
    }

    printf("\n======================================================================\n");
    printf("AAF audio loop: %ld checks, %ld failures\nRESULT: %s\n",
           checks, fails, fails ? "FAIL" : "PASS");
    delete dut;
    return fails ? 1 : 0;
}
