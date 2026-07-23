// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// KL_mmcm_drp_servo auto_repair REPAIR-path unit harness (roadmap 6 tail).
//
// The shared mmcm_servo TB (sim_main.cpp U7/U8) proves the servo's PS lock
// loop end-to-end; THIS harness zeroes in on the one limb that milan_datapath
// still ties OFF (auto_repair_i = 1'b0) - the XAPP888 DRP read-modify-write
// that repairs a mis-programmed CLKOUT0 divider - and pins the EXACT DRP
// transaction sequence so the tie can be blessed against a bench ClkReg
// readback before it is flipped.
//
//  A DRP-slave model (drp_model.h) is planted with a WRONG CLKOUT0 divider
//  (0x08/0x09) plus junk in the XAPP888 "RESERVED - retain previous value"
//  bits (ClkReg1[12], ClkReg2[15]). Cases:
//
//   AR0  auto_repair_i = 0 (the silicon-safe default, NEGATIVE CONTROL):
//        the mismatch is FLAGGED but the servo issues ZERO DRP writes and
//        runs the PS loop on the live config. This is exactly what the
//        tied-off gateware does today - the safety the tie buys.
//   AR1  auto_repair_i = 1 (the REPAIR path): the servo detects the
//        mismatch and emits the documented safe sequence -
//          w0: PowerReg 0x28 <- 0xFFFF   (XAPP888 Table 14, under RST)
//          w1: ClkReg1  0x08 <- RMW      (O=43 HIGH_TIME=22/LOW_TIME=21,
//                                         RESERVED[12] preserved)
//          w2: ClkReg2  0x09 <- RMW      (EDGE=1 odd divide, FRAC_EN=0,
//                                         RESERVED[15] preserved)
//        every write lands while mmcm_rst is high; no PS fires during
//        reconfiguration; RST is released and relock is waited.
//   AR2  auto_repair_i = 1 against a CORRECT live config: the repair NEVER
//        fires (0 writes) - a matching live clock is never disturbed.
//
// Sim-compressed servo -G params (same scale as the shared TB) keep the
// ns/512ms CSR units real; only timing is compressed.

#include "VKL_mmcm_drp_servo.h"
#include "verilated.h"
#include "drp_model.h"
#include <cstdio>
#include <cstdint>

static VKL_mmcm_drp_servo* dut;
static DrpMmcmModel mm;
static long checks = 0, fails = 0;

static void ck(const char* w, long got, long exp) {
    checks++;
    if (got != exp) { fails++; printf("  [FAIL] %-54s got=%ld exp=%ld\n", w, got, exp); }
    else            printf("  [ ok ] %-54s = %ld\n", w, got);
}
static void ckx(const char* w, long got, long exp) {   // hex report
    checks++;
    if (got != exp) { fails++; printf("  [FAIL] %-54s got=0x%04lX exp=0x%04lX\n", w, got, exp); }
    else            printf("  [ ok ] %-54s = 0x%04lX\n", w, got);
}

// ---- expected O=43 CLKOUT0 encoding (servo defaults; banner lines 195-206) -
static const uint16_t CFG_C0R1  = 0x0595, MASK_C0R1 = 0xEFFF;  // RESERVED[12] out
static const uint16_t CFG_C0R2  = 0x0080, MASK_C0R2 = 0x7FFF;  // RESERVED[15] out
static uint16_t rmw(uint16_t cur, uint16_t exp, uint16_t mask) {
    return (uint16_t)((cur & ~mask) | (exp & mask));
}

// ---- clock wheel (femtosecond grid, mirrors sim_main.cpp) -----------------
static double t_fs = 0;
static double next_i = 10000e3, next_p = 2500e3, next_a = 12345e3;
static const double HALF_I = 10000e3;         // clk_i 50 MHz
static const double HALF_P = 2500e3;          // ps_clk 200 MHz
static const double BASE_PPM = -10.64;
static const double HALF_A0 = 0.5 * (1e15 / 24.576e6) * (1.0 - BASE_PPM * 1e-6);
static double base_a = 12345e3;

static void tick_one() {
    if (next_i <= next_p && next_i <= next_a) {
        t_fs = next_i; next_i += HALF_I;
        dut->clk_i ^= 1;
        if (dut->clk_i) dut->ptp_now_i = (uint64_t)(t_fs / 1e6);
        dut->eval();
        if (dut->clk_i) {
            mm.dclk_edge(dut->drp_addr_o, dut->drp_en_o, dut->drp_we_o,
                         dut->drp_di_o, dut->mmcm_rst_o);
            dut->drp_do_i      = mm.dout;
            dut->drp_rdy_i     = mm.drdy;
            dut->mmcm_locked_i = mm.locked;
        }
    } else if (next_p <= next_a) {
        t_fs = next_p; next_p += HALF_P;
        dut->ps_clk_i ^= 1;
        dut->eval();
        if (dut->ps_clk_i) {
            mm.psclk_edge(dut->ps_en_o, dut->ps_incdec_o, dut->mmcm_rst_o);
            dut->ps_done_i = mm.psdone;
        }
    } else {
        t_fs = next_a;
        base_a += HALF_A0;
        next_a = base_a + mm.audio_adj_fs;
        if (next_a <= t_fs) next_a = t_fs + 1e3;
        dut->clk_audio_i ^= 1;
        dut->eval();
    }
}
static void run_ms(double ms) { double te = t_fs + ms * 1e12; while (t_fs < te) tick_one(); }

static int  state()    { return (int)(dut->status_o & 7); }
static int  mismatch() { return (int)((dut->status_o >> 4) & 1); }
static int  verified() { return (int)((dut->status_o >> 3) & 1); }

// drive the servo back to IDLE, then engage CRF (clock_source == 2)
static void deselect() { dut->clk_src_i = 0; run_ms(2); }
static void engage_until_active() {
    dut->clk_src_i = 2; dut->crf_locked_i = 1;
    long guard = 0;
    while (!(state() == 3 || state() == 4) && guard < 2000) { run_ms(0.05); guard++; }
}

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    dut = new VKL_mmcm_drp_servo;

    dut->rst_n = 0; dut->clk_src_i = 0; dut->crf_locked_i = 0;
    dut->crf_rate_i = 0; dut->auto_repair_i = 0; dut->ps_invert_i = 0;
    dut->mmcm_locked_i = 1;
    run_ms(0.02);
    dut->rst_n = 1;
    run_ms(0.05);

    // corrupt values: WRONG divider fields + junk in the RESERVED bits the
    // RMW must retain (ClkReg1[12]=1, ClkReg2[15]=1; both differ from exp)
    const uint16_t WRONG08 = 0x1234;   // bit12 set (RESERVED junk)
    const uint16_t WRONG09 = 0x8700;   // bit15 set (RESERVED junk)
    const uint16_t EXP08   = rmw(WRONG08, CFG_C0R1, MASK_C0R1);  // 0x1595
    const uint16_t EXP09   = rmw(WRONG09, CFG_C0R2, MASK_C0R2);  // 0x8080

    // ================================================================== //
    // AR0  auto_repair OFF - NEGATIVE CONTROL (today's tied-off gateware) //
    // ================================================================== //
    printf("[AR0] auto_repair_i=0: mismatch flagged, ZERO DRP writes (safe default)\n");
    {
        deselect();
        mm.regs[0x08] = WRONG08; mm.regs[0x09] = WRONG09; mm.regs[0x28] = 0x0000;
        dut->auto_repair_i = 0;
        long r0 = mm.drp_reads, w0 = mm.drp_writes, wl0 = mm.wlog_n;
        engage_until_active();
        ck ("[AR0] mismatch flagged",                 mismatch(), 1);
        ck ("[AR0] verified NOT set",                 verified(), 0);
        ck ("[AR0] read-verify issued 2 reads",       mm.drp_reads - r0, 2);
        ck ("[AR0] ZERO DRP writes (silicon-safe)",   mm.drp_writes - w0, 0);
        ck ("[AR0] ZERO write-log entries",           mm.wlog_n - wl0, 0);
        ck ("[AR0] MMCM never held in reset",         (long)dut->mmcm_rst_o, 0);
        ck ("[AR0] servo runs on live config (ACQUIRE/LOCKED)",
            state() == 3 || state() == 4, 1);
        ck ("[AR0] live registers untouched (0x08)",  mm.regs[0x08], WRONG08);
        ck ("[AR0] live registers untouched (0x09)",  mm.regs[0x09], WRONG09);
    }

    // ================================================================== //
    // AR1  auto_repair ON - the REPAIR path (exact DRP RMW sequence)      //
    // ================================================================== //
    printf("[AR1] auto_repair_i=1: detect + XAPP888 read-modify-write REPAIR\n");
    {
        deselect();
        mm.regs[0x08] = WRONG08; mm.regs[0x09] = WRONG09; mm.regs[0x28] = 0x0000;
        dut->auto_repair_i = 1;
        long r0 = mm.drp_reads, w0 = mm.drp_writes;
        int  wl0 = mm.wlog_n;
        long rst0 = mm.writes_wo_rst, psr0 = mm.ps_during_drp_rst, psv0 = mm.ps_viol;
        engage_until_active();

        // exact write sequence: power, then RMW 0x08, then RMW 0x09
        int nw = mm.wlog_n - wl0;
        ck ("[AR1] mismatch was flagged",             mismatch(), 1);
        ck ("[AR1] exactly 3 DRP writes",             mm.drp_writes - w0, 3);
        ck ("[AR1] write-log has 3 entries",          nw, 3);
        // verify + RMW reads: 2 (verify) + 1 (0x08) + 1 (0x09) = 4
        ck ("[AR1] read count (2 verify + 2 RMW)",    mm.drp_reads - r0, 4);
        if (nw == 3) {
            printf("  seq: w0=(0x%02X<-0x%04X rst=%d) w1=(0x%02X<-0x%04X rst=%d) "
                   "w2=(0x%02X<-0x%04X rst=%d)\n",
                   mm.wlog_addr[wl0+0], mm.wlog_data[wl0+0], mm.wlog_rst[wl0+0],
                   mm.wlog_addr[wl0+1], mm.wlog_data[wl0+1], mm.wlog_rst[wl0+1],
                   mm.wlog_addr[wl0+2], mm.wlog_data[wl0+2], mm.wlog_rst[wl0+2]);
            // w0: PowerReg
            ck ("[AR1] w0 addr = PowerReg 0x28",      mm.wlog_addr[wl0+0], 0x28);
            ckx("[AR1] w0 data = 0xFFFF (XAPP888 T14)",mm.wlog_data[wl0+0], 0xFFFF);
            ck ("[AR1] w0 under MMCM reset",          mm.wlog_rst[wl0+0], 1);
            // w1: ClkReg1 RMW
            ck ("[AR1] w1 addr = ClkReg1 0x08",       mm.wlog_addr[wl0+1], 0x08);
            ckx("[AR1] w1 data = RMW (O=43 HT/LT, RES[12] kept)",
                mm.wlog_data[wl0+1], EXP08);
            ck ("[AR1] w1 under MMCM reset",          mm.wlog_rst[wl0+1], 1);
            // w2: ClkReg2 RMW
            ck ("[AR1] w2 addr = ClkReg2 0x09",       mm.wlog_addr[wl0+2], 0x09);
            ckx("[AR1] w2 data = RMW (EDGE=1, RES[15] kept)",
                mm.wlog_data[wl0+2], EXP09);
            ck ("[AR1] w2 under MMCM reset",          mm.wlog_rst[wl0+2], 1);

            // decode the repaired ClkReg fields against the banner
            uint16_t d1 = mm.wlog_data[wl0+1], d2 = mm.wlog_data[wl0+2];
            ck ("[AR1]   HIGH_TIME[11:6] = 22",       (d1 >> 6) & 0x3F, 22);
            ck ("[AR1]   LOW_TIME [5:0]  = 21",       d1 & 0x3F, 21);
            ck ("[AR1]   ClkReg1 RESERVED[12] preserved",
                (d1 >> 12) & 1, (WRONG08 >> 12) & 1);
            ck ("[AR1]   divider bits set to expected", d1 & MASK_C0R1, CFG_C0R1);
            ck ("[AR1]   EDGE[7] = 1 (odd divide)",   (d2 >> 7) & 1, 1);
            ck ("[AR1]   NO_COUNT[6] = 0",            (d2 >> 6) & 1, 0);
            ck ("[AR1]   ClkReg2 RESERVED[15] preserved",
                (d2 >> 15) & 1, (WRONG09 >> 15) & 1);
            ck ("[AR1]   ClkReg2 non-RESERVED = expected", d2 & MASK_C0R2, CFG_C0R2);
        }

        // safe-sequencing invariants
        ck ("[AR1] no writes outside MMCM reset",     mm.writes_wo_rst - rst0, 0);
        ck ("[AR1] no PS shifts during reconfig",     mm.ps_during_drp_rst - psr0, 0);
        ck ("[AR1] no PSEN protocol violations",      mm.ps_viol - psv0, 0);
        // registers land repaired, RST released, relock reached
        ckx("[AR1] reg 0x08 committed",               mm.regs[0x08], EXP08);
        ckx("[AR1] reg 0x09 committed",               mm.regs[0x09], EXP09);
        ckx("[AR1] reg 0x28 committed",               mm.regs[0x28], 0xFFFF);
        ck ("[AR1] MMCM reset released",              (long)dut->mmcm_rst_o, 0);
        ck ("[AR1] MMCM relocked (status[5])",        (dut->status_o >> 5) & 1, 1);
        ck ("[AR1] verified after repair",            verified(), 1);
        ck ("[AR1] no relock-timeout fault",          (dut->status_o >> 8) & 1, 0);
        ck ("[AR1] resumed servo (ACQUIRE/LOCKED)",   state() == 3 || state() == 4, 1);
    }

    // ================================================================== //
    // AR2  auto_repair ON, CORRECT config - repair must NOT fire          //
    // ================================================================== //
    printf("[AR2] auto_repair_i=1 with a CORRECT config: repair never fires\n");
    {
        deselect();
        mm.regs[0x08] = CFG_C0R1; mm.regs[0x09] = CFG_C0R2; mm.regs[0x28] = 0x0000;
        dut->auto_repair_i = 1;
        long w0 = mm.drp_writes; int wl0 = mm.wlog_n;
        engage_until_active();
        ck ("[AR2] verified set (match)",             verified(), 1);
        ck ("[AR2] no mismatch",                      mismatch(), 0);
        ck ("[AR2] ZERO DRP writes on a live match",  mm.drp_writes - w0, 0);
        ck ("[AR2] ZERO write-log entries",           mm.wlog_n - wl0, 0);
        ck ("[AR2] MMCM never held in reset",         (long)dut->mmcm_rst_o, 0);
        ck ("[AR2] straight to servo (ACQUIRE/LOCKED)",
            state() == 3 || state() == 4, 1);
    }

    printf("======================================================================\n");
    printf("KL_mmcm_drp_servo auto_repair: %ld checks, %ld failures\n", checks, fails);
    delete dut;
    return fails ? 1 : 0;
}
