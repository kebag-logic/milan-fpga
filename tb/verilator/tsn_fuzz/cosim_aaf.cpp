// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// tsn-gen <-> Verilator co-simulation server for the AVTP/AAF RX stack
// (avtp_stream_parser -> KL_avtp_rx_monitor -> KL_aaf_rx_depacketizer, wired
// by the avtp_rxmon TB's wrapper).
//
// AAF is the data plane, so "did it answer?" is the wrong question: the DUT
// answers with COUNTERS. Every fuzzed stream PDU is graded by what moved —
// frames_rx, seq_mismatch, unsupported_fmt, late/early_ts, media_locked — and
// the campaign asserts the accept/reject verdict per field plus the thing
// that actually matters for audio: a malformed PDU must not knock a locked
// stream out of lock.
//
// Built with -GCLK_FREQ_HZ_P=10000 (the avtp_rxmon TB's scaling) so the
// 100 ms unlock timeout is 1000 cycles.
//
// Usage: Vaaf_cosim <socket-path>
#include "Vavtp_rxmon_wrap.h"
#include "verilated.h"
#include "../../common/verilator_harness.hpp"
#include "cosim_axis.h"

//! the bench stream identity + format (mirrors tb/verilator/avtp_rxmon)
constexpr uint64_t SID = 0x020000FFFE010000ULL;
constexpr uint64_t FMT = 0x0205022002006000ULL;   // AAF 48k INT32 depth32 8ch

//! The cycle counts the harness spends waiting for work the DUT does on its
//! own. Every one is the literal that was here before, named where the
//! comment beside it already said what it was waiting for.
constexpr int kDrainCycles = 24;      // verdict + PCM drain after a PDU
constexpr int kResetCycles = 8;       // reset held, then released
constexpr int kIdleBlockCycles = 100; // idle cycles per CTRL_TICK unit
constexpr int kEventCycles = 20;      // settle after a bind / idle event

namespace {

//! The co-simulation server: it owns the Verilated model and every piece of
//! harness state the session handler reads, so what used to be a file-scope
//! `dut` pointer plus a set of free functions is one object whose parts a
//! reader can see at once (Core Guidelines I.2).
class AafCosimServer {
 public:
    //! Serve the campaign on `socket_path`; the value is main's exit status.
    int serve(const char* socket_path) {
        reset_dut();

        int rc = tsn_serve(socket_path, [this](const std::vector<uint8_t>& cmd) -> Frames {
            Frames out;
            if (tsn_is_ctrl(cmd)) {
                switch (cmd[2]) {
                case CTRL_STATE:
                    out.push_back(state_dump());
                    return out;
                case CTRL_RESET:
                    reset_dut();
                    out.push_back(state_dump());
                    return out;
                case CTRL_TICK:                       // idle cycles (unlock timer)
                    for (int t = 0; t < cmd[3]; t++)
                        for (int c = 0; c < kIdleBlockCycles; c++) tick();
                    out.push_back(state_dump());
                    return out;
                case CTRL_EVENT:                      // cmd[3]: bind(0) / idle(1)
                    if (cmd[3] == 0) {
                        dut->bound_i = 0; for (int c = 0; c < kEventCycles; c++) tick();
                        dut->bound_i = 1; for (int c = 0; c < kEventCycles; c++) tick();
                    } else {
                        // MEDIA_RESET IS A WIRE EVENT, not a side-band poke.
                        // Milan Table 5.6 counts the intervals in which "the 'mr'
                        // bit was toggled in any of the received Stream Data
                        // AVTPDUs", so it is driven by sending a PDU with mr
                        // flipped - wire.py already builds that field (b15 bit 3).
                        // This arm used to pulse the LOCAL I2S playback rail,
                        // which no clause names (traceability AVTP-5).
                        for (int c = 0; c < kEventCycles; c++) tick();
                    }
                    out.push_back(state_dump());
                    return out;
                default:
                    return out;
                }
            }
            feed(cmd);
            out.push_back(state_dump());              // the verdict IS the answer
            return out;
        });
        return rc;
    }

 private:
    void tick() {
        dut->clk = 0; dut->eval();
        dut->clk = 1; dut->eval();
    }

    void feed(const std::vector<uint8_t>& f) {
        int n = static_cast<int>(f.size());
        for (int off = 0; off < n; off += 8) {
            uint64_t d = 0; uint8_t keep = 0;
            for (int l = 0; l < 8; l++)
                if (off + l < n) { d |= static_cast<uint64_t>(f[off + l]) << (8 * l); keep |= (1 << l); }
            dut->s_tdata_i = d; dut->s_tkeep_i = keep;
            dut->s_tvalid_i = 1; dut->s_tlast_i = (off + 8 >= n);
            tick();
        }
        dut->s_tvalid_i = 0; dut->s_tlast_i = 0; dut->s_tkeep_i = 0;
        for (int c = 0; c < kDrainCycles; c++) tick();      // let the verdict + PCM drain
    }

    //! Every observable the campaign grades a PDU by. Order is the contract with
    //! fuzz_aaf.py's COUNTERS tuple — append only, never reorder.
    std::vector<uint8_t> state_dump() {
        return tsn_state_frame({
            static_cast<uint32_t>(dut->cnt_frames_rx_o),
            static_cast<uint32_t>(dut->cnt_media_locked_o),
            static_cast<uint32_t>(dut->cnt_media_unlocked_o),
            static_cast<uint32_t>(dut->cnt_stream_interrupted_o),
            static_cast<uint32_t>(dut->cnt_seq_mismatch_o),
            static_cast<uint32_t>(dut->cnt_ts_uncertain_o),
            static_cast<uint32_t>(dut->cnt_unsupported_fmt_o),
            static_cast<uint32_t>(dut->cnt_media_reset_o),
            static_cast<uint32_t>(dut->cnt_late_ts_o),
            static_cast<uint32_t>(dut->cnt_early_ts_o),
            static_cast<uint32_t>(dut->media_locked_o),
            static_cast<uint32_t>(dut->pcm_pdus_o),
            static_cast<uint32_t>(dut->pcm_drops_o),
            static_cast<uint32_t>(dut->match_o),
            static_cast<uint32_t>(dut->last_ts_o),
            // the PRE-match view (the 0x8B4 APRB group's sources): every word
            // above it exists only because a frame already matched, so they can
            // never tell an accept-nothing listener why. `match_o` is a
            // one-cycle pulse and reads 0 in any snapshot; these two are
            // free-running counters and are what the accept-verdict campaign
            // grades.
            static_cast<uint32_t>(dut->par_parsed_o),
            static_cast<uint32_t>(dut->par_matched_o),
        });
    }

    void reset_dut() {
        dut->resetn = 0;
        dut->s_tvalid_i = 0; dut->s_tlast_i = 0; dut->s_tkeep_i = 0;
        dut->pcm_tready_i = 1;
        dut->cfg_sid_i = SID;
        dut->bound_i = 1;                 // bound listener: the interesting case
        dut->fmt_i = FMT;
        dut->ptp_now_i = 0xA55AC33C;      // matches the TB's fixed avtp_timestamp
        dut->pres_ofs_i = 0;
        dut->clk_src_i = 0;
        dut->servo_conv_i = 1;
        for (int i = 0; i < kResetCycles; i++) tick();
        dut->resetn = 1;
        for (int i = 0; i < kResetCycles; i++) tick();
    }

    const milan::tb::Model<Vavtp_rxmon_wrap> model;
    Vavtp_rxmon_wrap* dut = model.get();  // the harness's observing pointer
};

}  // namespace

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    if (argc < 2) { fprintf(stderr, "usage: %s <socket-path>\n", argv[0]); return 1; }
    AafCosimServer server;
    return server.serve(argv[1]);     // ~Model runs final() and frees the DUT
}
