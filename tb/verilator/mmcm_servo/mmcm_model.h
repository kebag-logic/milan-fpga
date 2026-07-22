// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// Behavioral MMCME2_ADV model for the KL_mmcm_drp_servo harnesses.
//
//  DRP side (DCLK = the servo clk): DEN latches {DADDR, DWE, DI}; DRDY
//  pulses DRDY_LAT DCLK cycles later with DO = reg[DADDR] (reads) and the
//  register updated (writes) - the documented DEN/DWE/DRDY handshake.
//  LOCKED drops while RST is high and returns RELOCK_LAT DCLK cycles after
//  release (XAPP888: reconfiguration under reset, then wait for lock).
//
//  PS side (PSCLK): PSEN for one cycle starts a shift; PSDONE pulses
//  exactly 12 PSCLK cycles later (UG472: "always 12 PSCLK cycles");
//  each completed INCREMENT delays the modeled audio clock by step_fs
//  (UG472: "Each increment adds to the phase shift ... 1/56th of the VCO
//  period"), a DECREMENT advances it - so a sustained step rate is a
//  frequency offset, exactly the physics the servo exploits. PSEN while a
//  shift is in flight is counted as a protocol violation.

#pragma once
#include <cstdint>

struct MmcmModel {
    // programmable state
    uint16_t regs[128] = {0};
    bool     locked = true;

    // DRP handshake
    int      drp_lat = 0;
    bool     drp_pend = false, drp_we_l = false;
    uint8_t  drp_addr_l = 0;
    uint16_t drp_di_l = 0;
    bool     drdy = false;     // output this cycle
    uint16_t dout = 0;
    long     drp_reads = 0, drp_writes = 0;
    long     writes_wo_rst = 0;    // safe-sequencing violation counter

    // reset / lock
    int      relock_cnt = 0;
    int      relock_lat = 500;

    // PS
    int      ps_busy = 0;
    bool     ps_dir = false;
    bool     psdone = false;   // output this cycle
    long     ps_ops = 0;
    long     ps_viol = 0;      // PSEN while busy
    long     ps_during_drp_rst = 0;  // PSEN while RST high (XAPP888 rule)
    int64_t  net_steps = 0;    // +1 per increment (delay), -1 per decrement

    // audio clock phase adjustment accumulator (femtoseconds)
    double   step_fs = 16898.0;    // 1/(56 * 1056.7568 MHz) = 16.898 ps
    double   audio_adj_fs = 0.0;   // cumulative phase moved (+ = delayed)

    // one DCLK posedge; inputs are the servo's DRP outputs sampled after eval
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
                psdone = true;             // UG472: 12 PSCLK cycles, 1-cycle pulse
                net_steps += ps_dir ? +1 : -1;
                audio_adj_fs += ps_dir ? +step_fs : -step_fs;
                ps_ops++;
            }
        } else if (psen) {
            ps_dir = psincdec;
            ps_busy = 12;
            if (mmcm_rst) ps_during_drp_rst++;
        }
    }
};
