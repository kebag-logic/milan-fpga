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
 *   debt_stage1 /       REQ-CBS-07 wire-time debt, state-for-state: the
 *   debt_update        : per-frame byte counter and the registered Q16 debt
 *                        increment (bytes per accepted beat + 24-octet
 *                        overhead + min-frame pad at tlast) in stage 1, the
 *                        accumulator (drain at the port byte rate, clamp at
 *                        0) in stage 2. wire_transmit = (debt != 0), read
 *                        PRE-step by the credit arms exactly like the RTL's
 *                        combinational wire_transmit_w: it suppresses both
 *                        the idleSlope accrual and the queue-empty decay
 *                        (802.1Q-2018 8.6.8.2 (d)/(e)/(f)).
 *   allow_transmit     : COMBINATIONAL (credit >= 0) off the credit register
 *                        (REQ-CBS-05 removed the extra decision flop); output
 *                        is forced high when the (registered) shaped bit is 0.
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
    bool     tlast      = false;           // bytes_sent carries the frame's last beat
    // runtime configuration ports
    bool     shaped     = true;
    int32_t  idle_slope = 500000000;       // bits/s for current link rate
    int32_t  hi_credit  = 761;             // signed bytes
    int32_t  lo_credit  = -761;            // signed bytes
};

// ---------------------------------------------------------------------------
// REQ-CBS-07 wire-time debt constants, mirroring the RTL elaboration math:
//   WIRE_DRAIN_*_Q16_C = round((link_bytes_per_s << 16) / clk_freq_hz)
// via the same ((n << 17) / d + 1) >> 1 rounding expression.
// ---------------------------------------------------------------------------
static inline int64_t cbs_drain_q16(bool is_1g, int64_t clk_freq_hz) {
    int64_t n = is_1g ? 125000000LL : 12500000LL;
    return (((n << 17) / clk_freq_hz) + 1) >> 1;
}
static const int CBS_WIRE_OVERHEAD_BYTES = 24;   // preamble+SFD+FCS+IFG
static const int CBS_MIN_FRAME_BYTES     = 60;   // 64 wire octets less FCS

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
        // REQ-CBS-06: round the magnitude to nearest (ties away from zero)
        // using the finished divide's remainder/divisor, then apply the sign.
        uint64_t quo_r  = (quo + (((rem << 1) >= den) ? 1u : 0u)) & M48;
        int64_t  quo_s  = sign ? -(int64_t)quo_r : (int64_t)quo_r;

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
        wire_debt = 0; debt_add = 0; frame_cnt = 0; is1g_r = false;
    }

    // PURE steady-state slope values (the SystemVerilog '/' results). The
    // engine converges to exactly these once the config has been stable for
    // two passes; the harness asserts that convergence after long runs.
    // REQ-CBS-06: the engine now rounds to nearest (ties away from zero), so
    // the steady-state values are round(numerator/denominator), not the
    // truncating '/' of the pre-2026-07-26 RTL.
    static int64_t div_round(int64_t num, int64_t den) {
        bool neg = (num < 0);
        uint64_t m = (uint64_t)(neg ? -num : num);
        uint64_t d = (uint64_t)den;
        uint64_t q = m / d;
        if ((m % d) * 2 >= d) q++;
        return neg ? -(int64_t)q : (int64_t)q;
    }
    int64_t idle_slope_per_cycle(bool is_1g, int32_t idle_slope) const {
        (void)is_1g;
        int64_t idle = (int64_t)idle_slope;
        return div_round(idle << CbsConfig::FP, cfg.clk_freq_hz * CbsConfig::BYTE_TO_BIT);
    }
    int64_t send_slope_per_byte(bool is_1g, int32_t idle_slope) const {
        int64_t link = is_1g ? 1000000000LL : 100000000LL;
        int64_t send = (int64_t)idle_slope - link;   // negative
        return div_round(send << CbsConfig::FP, link);
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

        // debt_stage1 (REQ-CBS-07): the per-frame byte counter walks the
        // accepted beats; the Q16 debt increment carries the beat's bytes
        // plus, on tlast, the fixed overhead and the MAC min-frame pad.
        int      frame_len   = (int)frame_cnt + (int)in.bytes_sent;
        int      frame_pad   = (frame_len < CBS_MIN_FRAME_BYTES)
                               ? (CBS_MIN_FRAME_BYTES - frame_len) : 0;
        int      add_bytes   = (int)in.bytes_sent +
                               (in.tlast ? (CBS_WIRE_OVERHEAD_BYTES + frame_pad) : 0);
        uint16_t n_frame_cnt = in.is_transmitting
                               ? (in.tlast ? 0 : (uint16_t)frame_len) : frame_cnt;
        int64_t  n_debt_add  = in.is_transmitting
                               ? ((int64_t)(add_bytes & 0xFF) << 16) : 0;
        bool     n_is1g      = in.is_1g;

        // debt_update (stage 2): += this beat's registered increment, -= the
        // port byte rate, clamp at 0, saturate at 48 bits; parked while
        // unshaped (the registered `shaped`, like the credit).
        int64_t n_wire_debt;
        if (!shaped) {
            n_wire_debt = 0;
        } else {
            int64_t t = wire_debt + debt_add - cbs_drain_q16(is1g_r, cfg.clk_freq_hz);
            const int64_t M48 = (((int64_t)1) << 48) - 1;
            n_wire_debt = (t < 0) ? 0 : (t > M48 ? M48 : t);
        }
        // 8.6.8.2 (e) transmit, from the PRE-step debt register (the RTL's
        // wire_transmit_w reads wire_debt_r combinationally this cycle)
        bool wire_tx = (wire_debt != 0);

        // credit_update_logic (uses CURRENT registered pipeline signals;
        // clamps use the CURRENT-cycle hi/lo config ports)
        int64_t n_credit;
        if (!shaped) {
            n_credit = 0;                                   // strict priority: park at 0
        } else if (istx) {
            int64_t t = credit + send_delta;
            n_credit = (t < LOc) ? LOc : t;
        } else if (wire_tx) {
            n_credit = credit;              // wire busy: no accrual, no decay
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

        // ---- commit, honouring synchronous reset ----
        if (!in.resetn) {
            credit = 0; send_delta = 0; credit_add_idle = 0;
            eng.reset();
            istx = false; qhd = false; isg = false; shaped = false;
            wire_debt = 0; debt_add = 0; frame_cnt = 0; is1g_r = false;
        } else {
            credit = n_credit;
            eng.step(in.idle_slope, in.is_1g, cfg.clk_freq_hz);
            send_delta = n_send_delta; credit_add_idle = n_credit_add_idle;
            istx = n_istx; qhd = n_qhd; isg = n_isg; shaped = n_shaped;
            wire_debt = n_wire_debt; debt_add = n_debt_add;
            frame_cnt = n_frame_cnt; is1g_r = n_is1g;
        }
    }

    int64_t credit_q16() const { return credit; }
    double  credit_bytes() const { return (double)credit / (double)(1 << CbsConfig::FP); }
    int64_t wire_debt_q16() const { return wire_debt; }
    // Output allow_transmit: combinational off the CURRENT credit register
    // (REQ-CBS-05); forced high when unshaped (uses registered shaped).
    bool    allow_transmit() const { return shaped ? (credit >= 0) : true; }

    const CbsConfig cfg;
    int64_t credit;
    int64_t send_delta, credit_add_idle;
    SlopeEngineRef eng;     // mirrors the RTL slope_engine state-for-state
    bool istx, qhd, isg, shaped;
    // REQ-CBS-07 wire-time debt state (mirrors debt_stage1/debt_update)
    int64_t  wire_debt;     // Q16 bytes still owed to the wire
    int64_t  debt_add;      // stage-1 registered increment (Q16)
    uint16_t frame_cnt;     // stage-1 per-frame byte counter
    bool     is1g_r;        // stage-1 registered link select
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
        istx = false; qhd = false; isg = false; shaped = false;
        wire_debt = 0.0; debt_add = 0.0; frame_cnt = 0; is1g_r = false;
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

        // REQ-CBS-07 wire-time debt, same register cadence as the RTL but
        // with the EXACT drain rate (link bytes per second / clk).
        int    frame_len   = (int)frame_cnt + (int)in.bytes_sent;
        int    frame_pad   = (frame_len < CBS_MIN_FRAME_BYTES)
                             ? (CBS_MIN_FRAME_BYTES - frame_len) : 0;
        int    add_bytes   = (int)in.bytes_sent +
                             (in.tlast ? (CBS_WIRE_OVERHEAD_BYTES + frame_pad) : 0);
        uint16_t n_frame_cnt = in.is_transmitting
                               ? (in.tlast ? 0 : (uint16_t)frame_len) : frame_cnt;
        double n_debt_add  = in.is_transmitting ? (double)add_bytes : 0.0;
        bool   n_is1g      = in.is_1g;
        double drain       = (is1g_r ? 125000000.0 : 12500000.0)
                             / (double)cfg.clk_freq_hz;
        double n_wire_debt;
        if (!shaped) n_wire_debt = 0.0;
        else {
            double t = wire_debt + debt_add - drain;
            n_wire_debt = (t < 0.0) ? 0.0 : t;
        }
        bool wire_tx = (wire_debt > 0.0);

        double n_credit;
        if (!shaped) {
            n_credit = 0.0;
        } else if (istx) {
            double t = credit + send_delta;
            n_credit = (t < LOc) ? LOc : t;
        } else if (wire_tx) {
            n_credit = credit;              // wire busy: no accrual, no decay
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
        if (!in.resetn) {
            credit = 0.0; send_delta = 0.0; credit_add_idle = 0.0;
            isc_r = 0.0; ssb_r = 0.0;
            cnt = 0; pend_isc = 0.0; pend_ssb = 0.0;
            istx = qhd = isg = shaped = false;
            wire_debt = 0.0; debt_add = 0.0; frame_cnt = 0; is1g_r = false;
        } else {
            credit = n_credit; send_delta = n_send_delta; credit_add_idle = n_credit_add_idle;
            isc_r = n_isc_r; ssb_r = n_ssb_r;
            cnt = n_cnt; pend_isc = n_pend_isc; pend_ssb = n_pend_ssb;
            istx = n_istx; qhd = n_qhd; isg = n_isg; shaped = n_shaped;
            wire_debt = n_wire_debt; debt_add = n_debt_add;
            frame_cnt = n_frame_cnt; is1g_r = n_is1g;
        }
    }

    double credit_bytes() const { return credit; }
    // REQ-CBS-05: combinational off the current credit, no decision flop
    bool   allow_transmit() const { return shaped ? (credit >= 0.0) : true; }

    const CbsConfig cfg;
    double credit, send_delta, credit_add_idle;
    double isc_r, ssb_r;   // committed slope terms (cadence-aligned with the engine)
    int    cnt;            // slope-engine cadence mirror
    double pend_isc, pend_ssb;
    bool istx, qhd, isg, shaped;
    // REQ-CBS-07 wire-time debt state (exact-rate mirror of the RTL's)
    double   wire_debt, debt_add;
    uint16_t frame_cnt;
    bool     is1g_r;
};

#endif // CBS_REF_MODEL_H
