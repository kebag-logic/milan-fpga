// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// Behavioral MMCME2_ADV DRP-slave model for the auto_repair REPAIR-path
// harness. Mirrors tb/verilator/mmcm_servo/mmcm_model.h (same DEN/DWE/DRDY
// handshake, same 12-PSCLK PSDONE, same reset/relock physics) and adds a
// per-write TRANSACTION LOG so the harness can assert the EXACT DRP
// read-modify-write sequence the servo emits during a repair.
//
//  DRP side (DCLK = the servo clk): DEN latches {DADDR, DWE, DI}; DRDY
//  pulses drp_lat DCLK cycles later with DO = reg[DADDR] (reads) and the
//  register updated (writes). Each write is appended to wlog[] together
//  with the mmcm_rst level seen AT THE COMMIT edge (XAPP888 requires every
//  divider write to land while the MMCM is held in reset).
//
//  PS side (PSCLK): PSEN for one cycle starts a shift; PSDONE pulses 12
//  PSCLK cycles later. ps_during_drp_rst counts any PSEN asserted while
//  mmcm_rst is high (XAPP888: "Fine-phase shifting is not allowed ...
//  during reconfiguration") - must stay 0.

#pragma once
#include <cstdint>

struct DrpMmcmModel {
    // programmable register file
    uint16_t regs[128] = {0};
    bool     locked = true;

    // DRP handshake
    int      drp_lat = 0;
    bool     drp_pend = false, drp_we_l = false;
    uint8_t  drp_addr_l = 0;
    uint16_t drp_di_l = 0;
    bool     drdy = false;          // output this cycle
    uint16_t dout = 0;
    long     drp_reads = 0, drp_writes = 0;
    long     writes_wo_rst = 0;     // safe-sequencing violation counter

    // per-write transaction log (the repair sequence is <= a handful)
    static const int WLOG_MAX = 32;
    uint8_t  wlog_addr[WLOG_MAX] = {0};
    uint16_t wlog_data[WLOG_MAX] = {0};
    bool     wlog_rst [WLOG_MAX] = {false};
    int      wlog_n = 0;

    // reset / lock
    int      relock_cnt = 0;
    int      relock_lat = 500;

    // PS
    int      ps_busy = 0;
    bool     ps_dir = false;
    bool     psdone = false;        // output this cycle
    long     ps_ops = 0;
    long     ps_viol = 0;           // PSEN while a shift is in flight
    long     ps_during_drp_rst = 0; // PSEN while RST high (XAPP888 rule)
    int64_t  net_steps = 0;
    bool     invert = false;

    // audio-phase accumulator (femtoseconds) - unused by the repair legs
    double   step_fs = 16898.0;     // 1/(56 * 1056.7568 MHz)
    double   audio_adj_fs = 0.0;

    // one DCLK posedge; inputs are the servo DRP outputs sampled after eval
    void dclk_edge(uint8_t daddr, bool den, bool dwe, uint16_t di, bool rst) {
        drdy = false;
        if (rst) {
            locked = false;
            relock_cnt = relock_lat;
        } else if (!locked && relock_cnt > 0 && !drp_pend) {
            if (--relock_cnt == 0) locked = true;
        }
        if (drp_pend) {
            if (--drp_lat == 0) {
                if (drp_we_l) {
                    regs[drp_addr_l & 0x7F] = drp_di_l;
                    drp_writes++;
                    if (!rst) writes_wo_rst++;
                    if (wlog_n < WLOG_MAX) {
                        wlog_addr[wlog_n] = drp_addr_l & 0x7F;
                        wlog_data[wlog_n] = drp_di_l;
                        wlog_rst [wlog_n] = rst;
                        wlog_n++;
                    }
                } else {
                    drp_reads++;
                }
                dout = regs[drp_addr_l & 0x7F];
                drdy = true;
                drp_pend = false;
            }
        } else if (den) {
            drp_addr_l = daddr; drp_we_l = dwe; drp_di_l = di;
            drp_pend = true;
            drp_lat = 4;               // DRDY a few DCLK later (DS181-ish)
        }
    }

    // one PSCLK posedge; inputs sampled after eval
    void psclk_edge(bool psen, bool psincdec, bool mmcm_rst) {
        psdone = false;
        if (ps_busy > 0) {
            if (psen) ps_viol++;
            if (--ps_busy == 0) {
                psdone = true;         // UG472: 12 PSCLK cycles, 1-cycle pulse
                net_steps    += (ps_dir ^ invert) ? +1 : -1;
                audio_adj_fs += (ps_dir ^ invert) ? +step_fs : -step_fs;
                ps_ops++;
            }
        } else if (psen) {
            ps_dir = psincdec;
            ps_busy = 12;
            if (mmcm_rst) ps_during_drp_rst++;
        }
    }
};
