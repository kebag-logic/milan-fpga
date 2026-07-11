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
 * Both models replicate the RTL's register stages exactly:
 *   slope_engine       : the sequential slope engine (SlopeEngineRef below), a
 *                        serial restoring divider on a fixed 100-cycle cadence
 *                        that samples the config at cnt 0 and atomically
 *                        commits idle_slope_per_cycle_r/send_slope_per_byte_r
 *                        at cnt 99. Mirrored STATE-FOR-STATE: the harness
 *                        compares the DUT slope registers against SlopeEngineRef
 *                        every cycle, including warm-up and reconfiguration
 *                        transitions. Do not change one without the other.
 *   stage1_pipe        : registers send_delta/credit_add_idle and the control
 *                        signals (is_transmitting/queue_has_data/is_granted/
 *                        shaped). send_delta/credit_add_idle are computed from
 *                        the engine-committed slope registers, then registered.
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
// State-for-state mirror of the RTL sequential slope engine (slope_engine in
// credit_based_shaper.sv). Fixed 100-cycle cadence:
//   cnt 0      sample idle_slope_i / is_1g_i
//   cnt 1      load |idle_slope <<< 16| (48-bit wrap), divisor clk_freq_hz*8
//   cnt 2..49  48 restoring-divider iterations (idle_slope_per_cycle)
//   cnt 50     stash signed quotient 1; load |send_slope <<< 16|, divisor link
//   cnt 51..98 48 iterations (send_slope_per_byte)
//   cnt 99     commit BOTH results atomically; wrap to 0
// All updates below read pre-step state first, mirroring nonblocking <=.
// ---------------------------------------------------------------------------
struct SlopeEngineRef {
    static const uint64_t M48 = ((uint64_t)1 << 48) - 1;
    int      cnt = 0;
    int64_t  idle_s = 0;            // sampled idle slope (sign-extended)
    bool     is1g_s = false;        // sampled link select
    bool     sign = false;          // dividend sign of the divide in flight
    uint64_t num = 0;               // dividend magnitude shift register
    uint64_t rem = 0;               // partial remainder (< divisor)
    uint64_t quo = 0;               // quotient shift register
    int64_t  q1 = 0;                // stashed signed quotient of divide 1
    uint64_t den = 1;               // active divisor
    int64_t  isc = 0, ssb = 0;      // committed slope registers (_r in RTL)

    void reset() { *this = SlopeEngineRef(); }

    static int64_t wrap48(int64_t v) {
        uint64_t u = (uint64_t)v & M48;
        return (u & ((uint64_t)1 << 47)) ? (int64_t)(u | ~M48) : (int64_t)u;
    }

    void step(int32_t idle_slope_i, bool is_1g_i, int64_t clk_freq_hz) {
        // combinational helpers from PRE-step state
        int64_t  link   = is1g_s ? 1000000000LL : 100000000LL;
        int64_t  ldval  = (cnt == 1) ? wrap48(idle_s << CbsConfig::FP)
                                     : wrap48((idle_s - link) << CbsConfig::FP);
        bool     ldsign = ldval < 0;
        uint64_t ldmag  = (uint64_t)(ldsign ? -ldval : ldval) & M48;
        uint64_t trial  = (rem << 1) | ((num >> 47) & 1);
        bool     ge     = (trial >= den);
        int64_t  quo_s  = sign ? -(int64_t)quo : (int64_t)quo;

        if (cnt == 0) {
            idle_s = (int64_t)idle_slope_i;
            is1g_s = is_1g_i;
        } else if (cnt == 1 || cnt == 50) {
            if (cnt == 50) q1 = quo_s;
            sign = ldsign; num = ldmag; rem = 0; quo = 0;
            den = (cnt == 1) ? (uint64_t)(clk_freq_hz * CbsConfig::BYTE_TO_BIT)
                             : (uint64_t)link;
        } else if (cnt == 99) {
            isc = q1; ssb = quo_s;
        } else {
            rem = ge ? (trial - den) : trial;
            quo = (quo << 1) | (ge ? 1 : 0);
            num = (num << 1) & M48;
        }
        cnt = (cnt == 99) ? 0 : cnt + 1;
    }
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
        eng.reset();
        istx = false; qhd = false; isg = false; shaped = false;
        allow = false;
    }

    // PURE steady-state slope values (the SystemVerilog '/' results). The
    // engine converges to exactly these once the config has been stable for
    // two passes; the harness asserts that convergence after long runs.
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

    // Engine-committed slope registers (what the credit datapath consumes).
    int64_t isc_reg() const { return eng.isc; }
    int64_t ssb_reg() const { return eng.ssb; }

    // Advance one posedge. `in` are the input values stable before the edge.
    void step(const CbsInputs& in) {
        const int64_t HIc = (int64_t)in.hi_credit << CbsConfig::FP;
        const int64_t LOc = (int64_t)in.lo_credit << CbsConfig::FP;

        // ---- next-state values (nonblocking: all computed from current) ----

        // stage1_pipe (uses the engine-committed slope registers, PRE-step:
        // on a commit edge the RTL stage1 still reads the old values)
        int64_t n_send_delta      = eng.ssb * (int64_t)(int16_t)in.bytes_sent;
        int64_t n_credit_add_idle = eng.isc;
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
            eng.reset();
            istx = false; qhd = false; isg = false; shaped = false; allow = false;
        } else {
            credit = n_credit;
            eng.step(in.idle_slope, in.is_1g, cfg.clk_freq_hz);
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
    SlopeEngineRef eng;     // mirrors the RTL slope_engine state-for-state
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
        isc_r = 0.0; ssb_r = 0.0;
        cnt = 0; pend_isc = 0.0; pend_ssb = 0.0;
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

        // slope-engine cadence mirror (float): sample the exact rates at cnt 0,
        // commit at cnt 99, exactly aligned with SlopeEngineRef so the DUT-vs-
        // ideal gap stays pure quantization error through warm-up/reconfig.
        double n_isc_r = isc_r, n_ssb_r = ssb_r;
        double n_pend_isc = pend_isc, n_pend_ssb = pend_ssb;
        if (cnt == 0) {
            n_pend_isc = idle_rate_per_cycle(in.is_1g, in.idle_slope);
            n_pend_ssb = send_rate_per_byte(in.is_1g, in.idle_slope);
        } else if (cnt == 99) {
            n_isc_r = pend_isc; n_ssb_r = pend_ssb;
        }
        int n_cnt = (cnt == 99) ? 0 : cnt + 1;
        double n_send_delta      = ssb_r * (double)in.bytes_sent;
        double n_credit_add_idle = isc_r;
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
            isc_r = 0.0; ssb_r = 0.0;
            cnt = 0; pend_isc = 0.0; pend_ssb = 0.0;
            istx = qhd = isg = shaped = allow = false;
        } else {
            credit = n_credit; send_delta = n_send_delta; credit_add_idle = n_credit_add_idle;
            isc_r = n_isc_r; ssb_r = n_ssb_r;
            cnt = n_cnt; pend_isc = n_pend_isc; pend_ssb = n_pend_ssb;
            istx = n_istx; qhd = n_qhd; isg = n_isg; shaped = n_shaped; allow = n_allow;
        }
    }

    double credit_bytes() const { return credit; }
    bool   allow_transmit() const { return shaped ? allow : true; }

    const CbsConfig cfg;
    double credit, send_delta, credit_add_idle;
    double isc_r, ssb_r;   // committed slope terms (cadence-aligned with the engine)
    int    cnt;            // slope-engine cadence mirror
    double pend_isc, pend_ssb;
    bool istx, qhd, isg, shaped, allow;
};

#endif // CBS_REF_MODEL_H
