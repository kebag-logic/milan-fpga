/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * Independent reference models for credit_based_shaper.sv (runtime-config rev).
 *
 * Two models are provided:
 *
 *   FixedPointRef - a cycle-accurate, bit-exact re-implementation of the RTL's
 *                   own integer/Q16 arithmetic and pipeline. If the DUT ever
 *                   disagrees with this model, the RTL does not implement the
 *                   arithmetic it was written to implement (a coding bug).
 *
 *   IdealRef      - the same 802.1Qav credit FSM evaluated in floating point
 *                   with the *exact* (non-truncated) idle/send rates. The gap
 *                   between the DUT and this model is the quantization/precision
 *                   error introduced by the chosen fixed-point representation.
 *
 * The shaper's idleSlope / hiCredit / loCredit / shaped-enable are now runtime
 * input ports, so every field is carried per-cycle in CbsInputs (exactly like
 * the RTL, where they are all input ports). The models therefore support live
 * reconfiguration mid-simulation.
 *
 * Both models replicate the RTL's two register stages exactly:
 *   stage1_pipe        : registers send_delta/credit_add_idle and the control
 *                        signals (is_transmitting/queue_has_data/is_granted/
 *                        shaped). send_delta/credit_add_idle are computed from
 *                        the *current* cycle's config, then registered.
 *   credit_update_logic: updates credit from the *registered* control signals
 *                        and send_delta/credit_add_idle, but clamps to the
 *                        *current* cycle's hiCredit/loCredit (the RTL clamp
 *                        terms are combinational from the config ports).
 *   allow_transmit     : registers (credit >= 0); output is forced high when
 *                        the (registered) shaped bit is 0.
 */

#ifndef CBS_REF_MODEL_H
#define CBS_REF_MODEL_H

#include <cstdint>
#include <algorithm>

struct CbsConfig {
    int64_t clk_freq_hz     = 100000000;   // compile-time parameter (constant divisor)
    static const int FP = 16;              // FP_DECIMAL_POINT
    static const int BYTE_TO_BIT = 8;
};

struct CbsInputs {
    bool     resetn;
    bool     queue_has_data;
    bool     is_transmitting;
    bool     is_1g;
    bool     is_granted;
    uint16_t bytes_sent;
    // runtime configuration ports
    bool     shaped     = true;
    int32_t  idle_slope = 500000000;       // bits/s for current link rate
    int32_t  hi_credit  = 761;             // signed bytes
    int32_t  lo_credit  = -761;            // signed bytes
};

// ---------------------------------------------------------------------------
// Bit-exact replica of the RTL integer arithmetic + pipeline.
// ---------------------------------------------------------------------------
class FixedPointRef {
public:
    explicit FixedPointRef(const CbsConfig& c) : cfg(c) { reset(); }

    void reset() {
        credit = 0;
        send_delta = 0; credit_add_idle = 0;
        istx = false; qhd = false; isg = false; shaped = false;
        allow = false;
    }

    // Combinational slope terms, replicating the RTL divides. All divisors are
    // compile-time constants (clk*8, and 1e9/1e8 selected by is_1g).
    int64_t idle_slope_per_cycle(bool is_1g, int32_t idle_slope) const {
        (void)is_1g;
        int64_t idle = (int64_t)idle_slope;
        return ((idle << CbsConfig::FP) / cfg.clk_freq_hz) / CbsConfig::BYTE_TO_BIT;
    }
    int64_t send_slope_per_byte(bool is_1g, int32_t idle_slope) const {
        int64_t link = is_1g ? 1000000000LL : 100000000LL;
        int64_t send = (int64_t)idle_slope - link;   // negative
        return (send << CbsConfig::FP) / link;        // constant divisor per branch
    }

    // Advance one posedge. `in` are the input values stable before the edge.
    void step(const CbsInputs& in) {
        const int64_t HIc = (int64_t)in.hi_credit << CbsConfig::FP;
        const int64_t LOc = (int64_t)in.lo_credit << CbsConfig::FP;

        // ---- next-state values (nonblocking: all computed from current) ----

        // stage1_pipe (computed from THIS cycle's config, then registered)
        int64_t n_send_delta      = send_slope_per_byte(in.is_1g, in.idle_slope)
                                        * (int64_t)(int16_t)in.bytes_sent;
        int64_t n_credit_add_idle = idle_slope_per_cycle(in.is_1g, in.idle_slope);
        bool    n_istx = in.is_transmitting;
        bool    n_qhd  = in.queue_has_data;
        bool    n_isg  = in.is_granted;
        bool    n_shaped = in.shaped;

        // credit_update_logic (uses CURRENT registered pipeline signals;
        // clamps use the CURRENT-cycle hi/lo config ports)
        int64_t n_credit;
        if (!shaped) {
            n_credit = 0;                                   // strict priority: park at 0
        } else if (istx) {
            int64_t t = credit + send_delta;
            n_credit = (t < LOc) ? LOc : t;
        } else if (!qhd && credit >= 0) {
            n_credit = 0;
        } else if (!qhd) {
            if (credit < 0)
                n_credit = (credit + credit_add_idle >= 0) ? 0 : credit + credit_add_idle;
            else
                n_credit = 0;
        } else {
            // accrue toward hiCredit; also clamps down if a reconfiguration
            // lowered hiCredit below the current credit (REQ-CBS-01).
            n_credit = (credit + credit_add_idle > HIc) ? HIc : credit + credit_add_idle;
        }

        // allow_transmit (registers current credit sign)
        bool n_allow = (credit >= 0);

        // ---- commit, honouring synchronous reset ----
        if (!in.resetn) {
            credit = 0; send_delta = 0; credit_add_idle = 0;
            istx = false; qhd = false; isg = false; shaped = false; allow = false;
        } else {
            credit = n_credit;
            send_delta = n_send_delta; credit_add_idle = n_credit_add_idle;
            istx = n_istx; qhd = n_qhd; isg = n_isg; shaped = n_shaped;
            allow = n_allow;
        }
    }

    int64_t credit_q16() const { return credit; }
    double  credit_bytes() const { return (double)credit / (double)(1 << CbsConfig::FP); }
    // Output allow_transmit: forced high when unshaped (uses registered shaped).
    bool    allow_transmit() const { return shaped ? allow : true; }

    const CbsConfig cfg;
    int64_t credit;
    int64_t send_delta, credit_add_idle;
    bool istx, qhd, isg, shaped, allow;
};

// ---------------------------------------------------------------------------
// Ideal continuous-rate model (same FSM, exact rates, floating point).
// ---------------------------------------------------------------------------
class IdealRef {
public:
    explicit IdealRef(const CbsConfig& c) : cfg(c) { reset(); }

    void reset() {
        credit = 0.0; send_delta = 0.0; credit_add_idle = 0.0;
        istx = false; qhd = false; isg = false; shaped = false; allow = false;
    }

    double idle_rate_per_cycle(bool is_1g, int32_t idle_slope) const {
        (void)is_1g;
        return (double)idle_slope / (double)cfg.clk_freq_hz / (double)CbsConfig::BYTE_TO_BIT;
    }
    double send_rate_per_byte(bool is_1g, int32_t idle_slope) const {
        double link = is_1g ? 1e9 : 1e8;
        return ((double)idle_slope - link) / link;
    }

    void step(const CbsInputs& in) {
        const double HIc = (double)in.hi_credit;
        const double LOc = (double)in.lo_credit;

        double n_send_delta      = send_rate_per_byte(in.is_1g, in.idle_slope) * (double)in.bytes_sent;
        double n_credit_add_idle = idle_rate_per_cycle(in.is_1g, in.idle_slope);
        bool   n_istx = in.is_transmitting, n_qhd = in.queue_has_data, n_isg = in.is_granted;
        bool   n_shaped = in.shaped;

        double n_credit;
        if (!shaped) {
            n_credit = 0.0;
        } else if (istx) {
            double t = credit + send_delta;
            n_credit = (t < LOc) ? LOc : t;
        } else if (!qhd && credit >= 0.0) {
            n_credit = 0.0;
        } else if (!qhd) {
            if (credit < 0.0)
                n_credit = (credit + credit_add_idle >= 0.0) ? 0.0 : credit + credit_add_idle;
            else
                n_credit = 0.0;
        } else {
            n_credit = (credit + credit_add_idle > HIc) ? HIc : credit + credit_add_idle;
        }
        bool n_allow = (credit >= 0.0);

        if (!in.resetn) {
            credit = 0.0; send_delta = 0.0; credit_add_idle = 0.0;
            istx = qhd = isg = shaped = allow = false;
        } else {
            credit = n_credit; send_delta = n_send_delta; credit_add_idle = n_credit_add_idle;
            istx = n_istx; qhd = n_qhd; isg = n_isg; shaped = n_shaped; allow = n_allow;
        }
    }

    double credit_bytes() const { return credit; }
    bool   allow_transmit() const { return shaped ? allow : true; }

    const CbsConfig cfg;
    double credit, send_delta, credit_add_idle;
    bool istx, qhd, isg, shaped, allow;
};

#endif // CBS_REF_MODEL_H
