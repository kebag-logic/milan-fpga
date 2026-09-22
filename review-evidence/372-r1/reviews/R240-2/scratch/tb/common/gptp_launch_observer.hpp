// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
#pragma once

#include <array>
#include <cstdint>
#include <deque>
#include <map>
#include <utility>
#include <vector>

namespace milan::tb {

//! THE MAC A DATAPATH BENCH STANDS IN FOR, on the gPTP egress timestamp
//! path (issue #360).
//!
//! WHY A BENCH NEEDS ONE. The plane no longer times a frame when the
//! datapath hands it over; it times the frame's LAUNCH, and it learns that
//! launch from a record the MAC's own observer (`KL_gptp_gmii_launch`)
//! sends back. A bench that terminates `m_axis_mac_tx_*` with nothing
//! behind it therefore has to be that observer, or the plane never
//! discharges its boot fence, never unseals, and transmits nothing at all.
//!
//! WHAT IT MODELS, AND WHAT IT DOES NOT. It models the observer's
//! INTERFACE: one ordered record per attributed frame, the echo that
//! re-establishes the observer position after a seal, and the declared
//! latency of the MAC pipeline between the launch and the record. It does
//! NOT model a MAC: there is no preamble, no queue and no wire here, and
//! the frame is attributed from the boundary beat that carried it. The
//! observation point, the register stages and the correction they add up to
//! are MEASURED against the product's own converted transmit chain in
//! `tb/verilator/gptp_txts`; here they are the declared latency of the MAC
//! this bench stands in for, and the harness's own t1 is taken from the
//! same event the plane takes it from, so the two agree by construction
//! rather than by a copied answer.
class GptpLaunchObserver {
 public:
    //! The observer's own record fields, as the plane's ledger reads them.
    static constexpr unsigned kDeltaCyc = 45;   //! reference octet -> tag
    static constexpr unsigned kObsLatCyc = 2;   //! observer register stages
    static constexpr unsigned kCdcLatCyc = 2;   //! record crossing stages

    //! `phc_tick_ns` is the period the PHC actually advances by in this
    //! build, and `eth_tick_ns` the transmit clock's. The plane is
    //! parameterised for the same two, which is what makes this model's t1
    //! and the plane's the same number.
    GptpLaunchObserver(unsigned phc_tick_ns, unsigned eth_tick_ns = 8)
        : corr_ns_((kDeltaCyc + kObsLatCyc) * eth_tick_ns
                   + kCdcLatCyc * phc_tick_ns + phc_tick_ns / 2) {}

    //! The declared latency, in nanoseconds, between a frame's launch and
    //! the cycle this observer reports it.
    uint64_t correction_ns() const { return corr_ns_; }

    //! One frame left the datapath's MAC boundary. Only the gPTP ones are
    //! attributed: the real observer reads the destination address and the
    //! EtherType off the wire and reports nothing for anything else.
    void offer(const std::vector<uint8_t>& frame, uint64_t cyc) {
        if (frame.size() < 46) return;
        static const std::array<uint8_t, 6> da =
            {0x01, 0x80, 0xC2, 0x00, 0x00, 0x0E};
        for (unsigned i = 0; i < da.size(); i++)
            if (frame[i] != da[i]) return;
        if (frame[12] != 0x88 || frame[13] != 0xF7) return;
        Record rec;
        rec.at = cyc + kReportCyc;
        rec.echo = false;
        rec.oidx = oidx_++;
        rec.type = frame[14] & 0xF;
        rec.seq = static_cast<unsigned>((frame[44] << 8) | frame[45]);
        pending_.push_back(rec);
    }

    //! Called once per fabric cycle, before the edge. `phc_ns` is the PHC
    //! this cycle - read where the plane reads it, so this model makes no
    //! assumption about the counter's rate.
    template <class Dut>
    void edge(Dut* dut, uint64_t cyc, uint64_t phc_ns) {
        dut->i_gptp_txseal_ack = 0;
        const bool req = dut->o_gptp_txseal_req != 0;
        //! The crossing latches the RISING edge of the offer, so a level
        //! held across a re-offer is delivered once, not twice.
        if (req && !seal_req_prev_) {
            gen_ = dut->o_gptp_txseal_gen;
            dut->i_gptp_txseal_ack = 1;
            Record echo;
            echo.at = cyc + kReportCyc;
            echo.echo = true;
            echo.oidx = oidx_;
            pending_.push_back(echo);
        }
        seal_req_prev_ = req;

        dut->i_gptp_txrec_valid = 0;
        if (pending_.empty() || cyc < pending_.front().at
                || cyc < last_rec_cyc_ + 2)
            return;
        const Record rec = pending_.front();
        pending_.pop_front();
        last_rec_cyc_ = cyc;
        dut->i_gptp_txrec_valid = 1;
        dut->i_gptp_txrec_kind = rec.echo ? 1 : 0;
        dut->i_gptp_txrec_oidx = rec.oidx;
        //! the generation the seal established; before the first seal it is
        //! 0, which the ledger refuses, exactly as it refuses a crossing
        //! whose source was reset
        dut->i_gptp_txrec_gen = gen_;
        dut->i_gptp_txrec_type = rec.echo ? 0 : rec.type;
        dut->i_gptp_txrec_seq = rec.echo ? 0 : rec.seq;
        dut->i_gptp_txrec_delta = rec.echo ? 0 : kDeltaCyc;
        dut->i_gptp_txrec_abort = 0;
        if (!rec.echo)
            t1_ns_[key(rec.type, rec.seq)] = {phc_ns - corr_ns_, cyc};
    }

    //! The launch instant this observer reported for that frame, if it has
    //! reported it yet, and the cycle it reported it on. A harness that
    //! answers a Pdelay_Req before its own observer has reported the request
    //! is answering for a launch that has not happened.
    //!
    //! BOTH are returned because a harness needs two different clocks: the
    //! launch instant is a PHC time, and the PHC restarts whenever the
    //! design is reset, so anything the harness has to SCHEDULE must be
    //! counted in its own cycles instead.
    bool t1_of(unsigned type, unsigned seq, uint64_t* out,
               uint64_t* at_cycle = nullptr) const {
        const auto it = t1_ns_.find(key(type, seq));
        if (it == t1_ns_.end()) return false;
        *out = it->second.first;
        if (at_cycle != nullptr) *at_cycle = it->second.second;
        return true;
    }

    //! Reset the modelled observer with the MAC it stands in for. The real
    //! one takes the MAC's transmit reset: its position, its generation and
    //! anything it had not yet reported go with it.
    void reset() {
        pending_.clear();
        t1_ns_.clear();
        oidx_ = 0;
        gen_ = 0;
        seal_req_prev_ = false;
        last_rec_cyc_ = 0;
    }

    //! Tie the face off, for a phase that drives the plane no records.
    template <class Dut>
    static void tie_off(Dut* dut) {
        dut->i_gptp_txrec_valid = 0;
        dut->i_gptp_txrec_kind = 0;
        dut->i_gptp_txrec_oidx = 0;
        dut->i_gptp_txrec_gen = 0;
        dut->i_gptp_txrec_type = 0;
        dut->i_gptp_txrec_seq = 0;
        dut->i_gptp_txrec_delta = 0;
        dut->i_gptp_txrec_abort = 0;
        dut->i_gptp_txseal_ack = 0;
    }

 private:
    //! fabric cycles from the boundary beat to the record. Any value works
    //! - the plane's ledger is ordered, not timed - and this one is short
    //! enough to keep the ledger shallow.
    static constexpr uint64_t kReportCyc = 4;

    struct Record {
        uint64_t at = 0;
        bool echo = false;
        unsigned oidx = 0;
        unsigned type = 0;
        unsigned seq = 0;
    };

    static uint32_t key(unsigned type, unsigned seq) {
        return (type << 16) | (seq & 0xFFFF);
    }

    const uint64_t corr_ns_;
    std::deque<Record> pending_;
    std::map<uint32_t, std::pair<uint64_t, uint64_t>> t1_ns_;
    unsigned oidx_ = 0;
    unsigned gen_ = 0;
    bool seal_req_prev_ = false;
    uint64_t last_rec_cyc_ = 0;
};

}  // namespace milan::tb
