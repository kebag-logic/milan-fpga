// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// The testbench of the REBOOT simulation (#871): the split SoC of
// reboot_soc.py runs the platform image on the split CPU, driven over the
// mailbox's datapath side by a script, with the flash's journal kept from one
// run to the next. A run that ends at the reset's configuration reload writes
// the journal, and the next run boots from it, as the reload boots the same
// flash (docs/design/REBOOT_RESET.md).
//
// The datapath is not built. The testbench stands for its parts the firmware
// reaches: the CSR window as ctrl_split_boot's register file, and the mailbox's
// datapath side, whose frames it gives and takes, and its GSI window, answered
// as a datapath whose stream runs no traffic would: every GET_STREAM_INFO word
// 0 and the SET_STREAM_FORMAT verdict 3, supported. On the reset port's rise it
// runs KL_reboot_ctrl's sequence, as hdl/milan/KL_reboot_ctrl.sv does:
//   DRAIN   until F_NVM says no live writer, or nothing accepted outside a
//           slot. F_NVM is the value the firmware last committed through the
//           face block, as the datapath takes it at the commit. The RTL's
//           deadline is drain_ms; the simulation also stops at drain_cap_ms
//   EGRESS  on a millisecond tick once the mailbox has sent no byte since
//           the previous tick, else at egress_ms
//   HOLD    the PHY hold rises. The run goes on for hold_window_ms of the
//           RTL's hold_ms, then ends at the reload
// Every figure is an observed bus-cycle count.
//
// The script, one step a line ('#' comments):
//   ready            wait for the ready line
//   wait <ms>        wait that many milliseconds
//   send <tag> <hex> give a frame to the mailbox on interface 0
//   erase            wait for the flash's next sector erase
//   program <n>      wait for the n-th page program since the last erase
//   adp <ms>         wait for an ENTITY_AVAILABLE, at most that many milliseconds
//   request <ms>     wait at most that long for the reset port's rise; the run
//                    ends there if it does not rise
//   reset <ms>       wait at most that long for the reset port, then run the
//                    reset sequence to the reload; the run ends there
//   cut              end now, as a power cut at a command boundary
// Output lines, which run.py grades:
//   READY <cycle>                  the ready line's last byte
//   RXS <cycle> <tag>              a frame's first byte taken by the mailbox
//   RXE <cycle> <tag>              its last byte
//   TX <cycle> <if> <ch> <hex>     a frame's last byte sent by the mailbox
//   NVM <cycle> <word>             a face commit's F_NVM
//   FLASH <cycle> <op>             an erase (d8) or page program (02) taken
//   REQ <cycle>                    the reset port rose
//   DRAIN <cycle> <durable|deadline|cap>
//   EGRESS <cycle> <quiet|deadline>
//   HOLD <cycle>                   the PHY hold rose
//   RELOAD <cycle>                 the run ends at the reload
//   CUT <cycle>                    the run ends at a cut
//   NOREQ <cycle>                  the reset port did not rise in time
//   STEP <cycle> <n> <op>          a script step taken
//   SUMMARY sys=<cycles> cpu=<cycles> ...
#include "Vsim.h"
#include "mbx_contract.h"
#include "reboot_config.hpp"
#include "flash.hpp"
#include "verilator_harness.hpp"
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <deque>
#include <fstream>
#include <map>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

namespace {

unsigned long long ull(std::uint64_t value) { return value; }

struct Step {
    std::string op;
    std::vector<std::string> args;
};

struct Frame {
    std::string tag;
    std::vector<std::uint8_t> bytes;
};

std::vector<std::uint8_t> unhex(const std::string& text) {
    if (text.size() % 2) throw std::runtime_error("a frame's hex has an odd length");
    std::vector<std::uint8_t> out;
    for (std::size_t k = 0; k < text.size(); k += 2) out.push_back(std::uint8_t(std::stoul(text.substr(k, 2), nullptr, 16)));
    return out;
}

class Bench {
public:
    Bench(const char* script, const char* transcript)
        : flash_(erase_cycles, program_cycles), out_(transcript) {
        if (!out_) throw std::runtime_error("cannot open the transcript");
        words_[0x000u] = 0x4d494c4eu;   // ID, 'MILN'
        words_[0x004u] = 0x00020060u;   // VERSION, as every image before the flip (D2)
        if (const char* journal = std::getenv("REBOOT_JOURNAL_IN")) flash_.load(journal, journal_offset);
        std::ifstream input(script);
        if (!input) throw std::runtime_error("cannot open the script");
        std::string line;
        while (std::getline(input, line)) {
            if (line.empty() || line[0] == '#') continue;
            std::istringstream words(line);
            Step step;
            words >> step.op;
            for (std::string w; words >> w;) step.args.push_back(w);
            steps_.push_back(step);
        }
    }

    std::uint32_t word(std::uint32_t offset) const {
        auto it = words_.find(offset);
        return it == words_.end() ? (0x5a000001u | (offset << 8)) : it->second;
    }

    void sample(Vsim& dut, std::uint64_t time_ps) {
        ++sys_;
        tick_ = dut.mbx_ms_tick;
        if (tick_) ++ms_;
        csr_sample(dut, time_ps);
        uart_sample(dut);
        flash_sample(dut);
        host_sample(dut);
        ingress_sample(dut);
        egress_sample(dut);
        reset_sample(dut);
        gsi_sample(dut);
        script();
    }

    void drive(Vsim& dut) {
        dut.milan_csr_ack = csr_ack_;
        dut.milan_csr_dat_r = csr_rdata_;
        dut.serial_source_ready = 1;
        dut.serial_sink_valid = 0;
        const bool frame = !frames_.empty();
        dut.mbx_rx_valid = frame;
        dut.mbx_rx_data = frame ? frames_.front().bytes.at(offset_) : 0;
        dut.mbx_rx_last = frame && offset_ + 1 == frames_.front().bytes.size();
        dut.mbx_rx_if = 0;
        dut.mbx_tx_ready = 1;
        dut.mbx_link_up = 1;
        dut.flash_tx_ready = !flash_pending_ && dut.flash_cs;
        dut.flash_rx_valid = flash_pending_ && sys_ >= flash_at_;
        dut.flash_rx_data = flash_response_;
        dut.gsi_ans_p = gsi_answer_;
        dut.gsi_ans_tag = gsi_tag_;
        dut.gsi_ans_data = gsi_data_;
    }

    bool done() const { return done_; }

    void report() const {
        if (const char* path = std::getenv("REBOOT_JOURNAL_OUT")) {
            std::ofstream journal(path, std::ios::binary);
            for (std::uint32_t a = journal_offset; a < journal_offset + journal_size; ++a)
                journal.put(static_cast<char>(flash_.byte(a)));
            if (!journal) throw std::runtime_error("cannot write the journal");
        }
        std::printf("SUMMARY sys=%llu cpu=%llu erases=%u programs=%u steps=%zu of %zu\n", ull(sys_),
                    ull(sys_ * cpu_hz / sys_hz), flash_.erases, flash_.programs, step_, steps_.size());
    }

    bool completed() const { return step_ == steps_.size(); }

private:
    enum class Phase { IDLE, DRAIN, EGRESS, HOLD };

    void csr_sample(Vsim& dut, std::uint64_t time_ps) {
        if (!(dut.milan_csr_cyc && dut.milan_csr_stb) || csr_ack_) {
            csr_ack_ = false;
            return;
        }
        const std::uint32_t offset = (std::uint32_t(dut.milan_csr_adr) << 2) & (csr_size - 1u);
        if (dut.milan_csr_we) {
            words_[offset] = dut.milan_csr_dat_w;
            if (offset == 0x520u && (dut.milan_csr_dat_w & 0x4u)) {   // PTP_CMD's snapshot strobe
                const std::uint64_t ns = time_ps / 1000u;
                words_[0x530u] = std::uint32_t(ns);
                words_[0x534u] = std::uint32_t(ns >> 32);
            }
        } else {
            csr_rdata_ = word(offset);
        }
        csr_ack_ = true;
    }

    void uart_sample(Vsim& dut) {
        if (!dut.serial_source_valid) return;
        const char ch = char(dut.serial_source_data);
        transcript_.push_back(ch);
        out_.put(ch);
        if (!ready_ && transcript_.size() >= ready_line.size()
            && transcript_.compare(transcript_.size() - ready_line.size(), ready_line.size(), ready_line) == 0) {
            ready_ = true;
            std::printf("READY %llu\n", ull(sys_));
        }
    }

    void flash_sample(Vsim& dut) {
        if (flash_cs_ && !dut.flash_cs) {
            const unsigned op = flash_.deselect(sys_);
            if (op) {
                std::printf("FLASH %llu %02x\n", ull(sys_), op);
                if (op == 0xd8) { ++erases_; programs_ = 0; }
                if (op == 0x02) ++programs_;
            }
        }
        flash_cs_ = dut.flash_cs;
        if (dut.flash_rx_valid && dut.flash_rx_ready) flash_pending_ = false;
        if (dut.flash_tx_valid && dut.flash_tx_ready) {
            flash_response_ = flash_.transfer(dut.flash_tx_data, dut.flash_tx_len, dut.flash_tx_width, sys_);
            flash_at_ = sys_ + dut.flash_tx_len * (sys_hz / 12500000) + 1;   // a 12.5 MHz SCK
            flash_pending_ = true;
        }
    }

    // The face block's F_NVM, as the datapath takes it at the commit's GO.
    void host_sample(Vsim& dut) {
        if (dut.mbx_host_req) {
            host_we_ = dut.mbx_host_we;
            host_addr_ = std::uint32_t(dut.mbx_host_addr) << 2;
            host_wdata_ = dut.mbx_host_wdata;
        }
        if (!dut.mbx_host_ack || !host_we_) return;
        if (host_addr_ == MBX_FACE_BASE + MBX_FACE_REG_F_NVM) nvm_written_ = host_wdata_;
        if (host_addr_ == MBX_FACE_BASE + MBX_FACE_REG_F_COMMIT && ((host_wdata_ >> MBX_F_COMMIT_GO_LSB) & 1u)) {
            nvm_ = nvm_written_;
            std::printf("NVM %llu %08x\n", ull(sys_), nvm_);
        }
    }

    void ingress_sample(Vsim& dut) {
        if (frames_.empty() || !dut.mbx_rx_valid || !dut.mbx_rx_ready) return;
        if (offset_ == 0) std::printf("RXS %llu %s\n", ull(sys_), frames_.front().tag.c_str());
        if (++offset_ < frames_.front().bytes.size()) return;
        std::printf("RXE %llu %s\n", ull(sys_), frames_.front().tag.c_str());
        frames_.pop_front();
        offset_ = 0;
    }

    void egress_sample(Vsim& dut) {
        if (!dut.mbx_tx_valid) return;
        egress_.push_back(dut.mbx_tx_data);
        if (!dut.mbx_tx_last) return;
        std::string hex;
        char b[3];
        for (auto byte : egress_) { std::snprintf(b, sizeof b, "%02x", byte); hex += b; }
        std::printf("TX %llu %u %u %s\n", ull(sys_), unsigned(dut.mbx_tx_if), unsigned(dut.mbx_tx_ch), hex.c_str());
        if (unsigned(dut.mbx_tx_ch) == MBX_CH_ADP && egress_.size() > 15 && (egress_[15] & 0x0fu) == 0u) available_ = true;
        egress_.clear();
    }

    // The GSI window (contract 2.3): each request answered once, four bus cycles on, under its tag
    void gsi_sample(Vsim& dut) {
        gsi_answer_ = false;
        const bool fresh = dut.gsi_req && (!gsi_open_ || unsigned(dut.gsi_tag) != gsi_tag_);
        if (fresh) {
            gsi_open_ = true;
            gsi_tag_ = unsigned(dut.gsi_tag);
            gsi_data_ = (dut.gsi_kind == 0 && dut.gsi_sel == 15) ? 3u : 0u;
            gsi_at_ = sys_ + 4;
            gsi_due_ = true;
        } else if (!dut.gsi_req) {
            gsi_open_ = false;
        }
        if (gsi_due_ && sys_ >= gsi_at_) {
            gsi_answer_ = true;
            gsi_due_ = false;
        }
    }

    bool durable() const {
        const bool backed = (nvm_ >> MBX_F_NVM_BACKED_LSB) & 1u, dirty = (nvm_ >> MBX_F_NVM_DIRTY_LSB) & 1u,
                   pend = (nvm_ >> MBX_F_NVM_PEND_LSB) & 1u;
        return !backed || (!dirty && !pend);
    }

    // KL_reboot_ctrl's phases, on the reset port's level (the SoC's MultiReg is the datapath's)
    void reset_sample(Vsim& dut) {
        if (phase_ == Phase::IDLE) {
            if (dut.reboot && !requested_) {
                requested_ = true;
                phase_ = Phase::DRAIN;
                phase_ms_ = 0;
                std::printf("REQ %llu\n", ull(sys_));
            }
            return;
        }
        if (phase_ == Phase::DRAIN) {
            const bool cap = phase_ms_ >= drain_cap_ms;
            if (durable() || phase_ms_ >= drain_ms || cap) {
                std::printf("DRAIN %llu %s\n", ull(sys_), durable() ? "durable" : cap ? "cap" : "deadline");
                phase_ = Phase::EGRESS;
                phase_ms_ = 0;
                quiet_ = false;
            } else if (tick_) {
                ++phase_ms_;
            }
            return;
        }
        if (phase_ == Phase::EGRESS) {
            const bool idle = egress_.empty() && !dut.mbx_tx_valid;
            if ((tick_ && quiet_ && idle) || phase_ms_ >= egress_ms) {
                std::printf("EGRESS %llu %s\n", ull(sys_), quiet_ ? "quiet" : "deadline");
                std::printf("HOLD %llu\n", ull(sys_));
                phase_ = Phase::HOLD;
                phase_ms_ = 0;
            } else if (tick_) {
                ++phase_ms_;
                quiet_ = idle;
            } else if (!idle) {
                quiet_ = false;
            }
            return;
        }
        if (tick_ && ++phase_ms_ >= hold_window_ms && reset_step_) {
            std::printf("RELOAD %llu\n", ull(sys_));
            finish();
        }
    }

    void finish() {
        ++step_;
        done_ = true;
    }

    void script() {
        if (done_) return;
        if (step_ == steps_.size()) {
            done_ = true;
            return;
        }
        const Step& s = steps_[step_];
        if (!announced_) {
            std::printf("STEP %llu %zu %s\n", ull(sys_), step_, s.op.c_str());
            announced_ = true;
            mark_ms_ = ms_;
            mark_erases_ = erases_;
            if (s.op == "adp") available_ = false;
        }
        if (s.op == "ready") {
            if (ready_) next();
        } else if (s.op == "wait") {
            if (ms_ - mark_ms_ >= std::stoul(s.args.at(0))) next();
        } else if (s.op == "send") {
            frames_.push_back({s.args.at(0), unhex(s.args.at(1))});
            next();
        } else if (s.op == "erase") {
            if (erases_ > mark_erases_) next();
        } else if (s.op == "program") {
            if (programs_ >= std::stoul(s.args.at(0))) next();
        } else if (s.op == "adp") {
            if (available_ || ms_ - mark_ms_ >= std::stoul(s.args.at(0))) {
                if (!available_) std::printf("NOADP %llu\n", ull(sys_));
                next();
            }
        } else if (s.op == "request") {
            if (requested_) {
                next();
            } else if (ms_ - mark_ms_ >= std::stoul(s.args.at(0))) {
                std::printf("NOREQ %llu\n", ull(sys_));
                finish();
            }
        } else if (s.op == "reset") {
            reset_step_ = true;
            if (!requested_ && ms_ - mark_ms_ >= std::stoul(s.args.at(0))) {
                std::printf("NOREQ %llu\n", ull(sys_));
                finish();
            }
        } else if (s.op == "cut") {
            std::printf("CUT %llu\n", ull(sys_));
            finish();
        } else {
            throw std::runtime_error("unknown script step " + s.op);
        }
    }

    void next() {
        ++step_;
        announced_ = false;
    }

    Flash flash_;
    std::ofstream out_;
    std::map<std::uint32_t, std::uint32_t> words_;
    std::string transcript_;
    std::vector<Step> steps_;
    std::deque<Frame> frames_;
    std::vector<std::uint8_t> egress_;
    std::size_t offset_ = 0;
    std::size_t step_ = 0;
    std::uint64_t sys_ = 0;
    std::uint64_t ms_ = 0;
    std::uint64_t mark_ms_ = 0;
    std::uint64_t flash_at_ = 0;
    std::uint64_t gsi_at_ = 0;
    std::uint64_t gsi_data_ = 0;
    unsigned gsi_tag_ = 0;
    bool gsi_open_ = false;
    bool gsi_due_ = false;
    bool gsi_answer_ = false;
    std::uint32_t csr_rdata_ = 0;
    std::uint32_t flash_response_ = 0;
    std::uint32_t host_addr_ = 0;
    std::uint32_t host_wdata_ = 0;
    std::uint32_t nvm_written_ = 0;
    std::uint32_t nvm_ = 0;
    unsigned erases_ = 0;
    unsigned mark_erases_ = 0;
    unsigned programs_ = 0;
    unsigned phase_ms_ = 0;
    Phase phase_ = Phase::IDLE;
    bool tick_ = false;
    bool host_we_ = false;
    bool csr_ack_ = false;
    bool flash_cs_ = false;
    bool flash_pending_ = false;
    bool ready_ = false;
    bool requested_ = false;
    bool reset_step_ = false;
    bool quiet_ = false;
    bool available_ = false;
    bool announced_ = false;
    bool done_ = false;
};

void initialize(Vsim& dut) {
    dut.sys_reset = 1;
    dut.sys_clk = 0;
    dut.milan_clk = 0;
    dut.audio_clk = 0;
    dut.audio_tdm_clk = 0;
    dut.serial_sink_valid = 0;
    dut.serial_source_ready = 1;
    dut.mbx_rx_valid = 0;
    dut.mbx_tx_ready = 1;
    dut.mbx_link_up = 0;
    dut.mbx_gm_change = 0;
    dut.flash_tx_ready = 0;
    dut.flash_rx_valid = 0;
    dut.milan_csr_ack = 0;
    dut.gsi_ans_p = 0;
    dut.gsi_ans_tag = 0;
    dut.gsi_ans_data = 0;
    dut.eval();
}

// The CPU budget harness's clocking: aligned rising edges, the CPU at cpu_hz.
void simulate(Vsim& dut, Bench& bench) {
    const std::array<std::uint64_t, 2> frequency = {sys_hz, cpu_hz};
    std::array<std::uint64_t, 2> edge = {1, 1};
    std::array<std::uint64_t, 2> next{};
    const std::array<std::uint64_t, 2> offset = {0, (500000000000ULL / cpu_hz - 500000000000ULL / sys_hz)};
    for (unsigned i = 0; i < next.size(); ++i) next[i] = 500000000000ULL / frequency[i] + offset[i];
    while (!Verilated::gotFinish() && !bench.done()) {
        const auto time_ps = *std::min_element(next.begin(), next.end());
        if (time_ps > sim_limit_ps) throw std::runtime_error("simulation exceeded its time limit");
        Verilated::threadContextp()->time(time_ps);
        if (next[0] == time_ps && !dut.sys_clk) bench.sample(dut, time_ps);
        for (unsigned i = 0; i < next.size(); ++i) {
            if (next[i] != time_ps) continue;
            if (i == 0) dut.sys_clk = !dut.sys_clk;
            if (i == 1) dut.milan_clk = !dut.milan_clk;
            ++edge[i];
            next[i] = edge[i] * (500000000000ULL / frequency[i])
                + edge[i] * (500000000000ULL % frequency[i]) / frequency[i] + offset[i];
        }
        if (edge[0] > 128) dut.sys_reset = 0;
        dut.eval();
        if (!dut.sys_clk) {
            bench.drive(dut);
            dut.eval();
        }
    }
}

}  // namespace

int main(int argc, char** argv) {
    std::setvbuf(stdout, nullptr, _IOFBF, 1 << 20);
    Verilated::commandArgs(argc, argv);
    milan::tb::Checker check{"ctrl_reboot"};
    try {
        if (argc != 3) throw std::runtime_error("expected the script and the transcript paths");
        const milan::tb::Model<Vsim> model;
        auto& dut = *model.get();
        initialize(dut);
        Bench bench(argv[1], argv[2]);
        simulate(dut, bench);
        check.that("the script ran to its end", bench.completed());
        bench.report();
    } catch (const std::exception& error) {
        std::fflush(stdout);
        std::fprintf(stderr, "FAIL: %s\n", error.what());
        check.that("simulation completed without boundary failures", false);
    }
    std::fflush(stdout);
    return check.report();
}
