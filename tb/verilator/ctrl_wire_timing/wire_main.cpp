// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// The wire-timing testbench (#665, #868): the CPU half (wire_soc.py, the CPU
// budget harness's split SoC with KL_mbx_wb's host port on pads) and the split
// placement's own top (tb/verilator/milan_dp/tb_split_top.sv: KL_mbx,
// KL_mbx_cdc and the CTRL_SPLIT_P = 1 datapath), run in lockstep on one bus
// clock. The CPU reaches the split top only through KL_mbx_wb's host port and
// the CSR window, and the testbench reaches the datapath only at its MAC
// boundary, so every frame below is stamped where the datapath meets the MAC.
//
// Lockstep: before each rising bus edge the testbench drives its inputs, then
// settles the two models' boundary (the CPU half's host request into the split
// top, the split top's answer back) until neither moves, so each model samples
// the other's settled outputs at the edge. The bus clock and the CPU clock are
// the shape's sys clock, 100 MHz, edge-aligned; the datapath clock is half of
// it, rising on the even bus edges, as tb_split_top's legs clock it.
//
// What the testbench models, besides the two models:
//  - KL_mbx's millisecond: a one-cycle pulse every sys_hz/1000 bus cycles from
//    the reset's release, as milan_soc.CtrlMailbox counts it;
//  - the CSR window: each Wishbone access of the CPU half becomes one AXI4-Lite
//    access on the split top's s_axi port, on the datapath clock, and is
//    acknowledged when that access completes (CSRW and CSRR log its cycles);
//  - the MAC boundary at 1 Gb/s: each received frame's beats are offered no
//    faster than 2.5 bytes a datapath cycle, and the datapath's transmit
//    beats are accepted no faster, with 24 bytes (preamble, start delimiter,
//    FCS and inter-frame gap) between frames, and a frame shorter than 60
//    bytes counted as 60, the MAC's padding;
//  - the flash device, the CPU budget harness's native model, blank;
//  - the UART, read and never written.
//
// Output lines, which wire_grade.py grades:
//   MS <cycle> <now_ms>                    each millisecond pulse
//   RXW <first> <last> <bytes> <tag> <hex> a frame offered at the MAC boundary:
//                                          the cycles its first and last beat
//                                          were taken
//   TXW <first> <last> <bytes> <hex>       a frame the datapath sent: the cycles
//                                          its first and last beat were taken
//   TXC <cycle> <channel> <value>          a TX_HEAD write: a mailbox commit
//   TMR <cycle> <value> <deadline>         a TMR_CMD write, the deadline the
//                                          last TMR_DEADLINE write gave
//   CSRW|CSRR <cycle> <offset> <value> <cycles>  a CSR window access
//   RXSTALL <cycle>                        a received beat the datapath refused
//   UART <cycle> <hex byte>; READY <cycle>; MARK <cycle> <label>
//   SUMMARY sys=<cycles> ...
// and, for diagnosis only, with WIRE_HOST_LOG=<from>:<to> bus cycles set:
//   HOSTREQ <cycle> <we> <word>            a host request
//   HOST <cycle> <r|w> <word> <data>       a host access completed
//   FLASH <cycle> <op>                     a flash operation ended (chip select released)
//   PROGRESS <ms> host=<n> flash_words=<n> csr=<n>   every 10 ms
#include "Vsim.h"
#include "Vtb_split_top.h"
#include "wire_config.hpp"
#include "flash.hpp"
#include "verilator_harness.hpp"
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <deque>
#include <fstream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

namespace {

unsigned long long ull(std::uint64_t value) { return value; }

std::vector<std::uint8_t> unhex(const std::string& text) {
    if (text.size() % 2) throw std::runtime_error("odd hex length in the script");
    std::vector<std::uint8_t> out;
    for (std::size_t i = 0; i < text.size(); i += 2) out.push_back(std::uint8_t(std::stoul(text.substr(i, 2), nullptr, 16)));
    return out;
}

std::string hexed(const std::vector<std::uint8_t>& bytes) {
    static const char digit[] = "0123456789abcdef";
    std::string out;
    for (auto b : bytes) { out.push_back(digit[b >> 4]); out.push_back(digit[b & 15]); }
    return out;
}

//! A reply rule: when a transmitted frame matches every (offset, byte), the
//! frame is sent back with each (offset, bytes) patch, `turnaround` bus cycles
//! after its last beat left (the peer's own time, stated by the script).
struct Reply {
    std::string tag;
    std::vector<std::pair<std::size_t, std::uint8_t>> match;
    std::vector<std::pair<std::size_t, std::vector<std::uint8_t>>> patch;
    std::uint64_t turnaround = 0;
};

struct Frame {
    std::string tag;
    std::vector<std::uint8_t> bytes;
    std::uint64_t not_before = 0;
};

struct Step { std::string op; std::vector<std::string> args; };

//! The MAC boundary's line rate in half-bytes per datapath cycle (1 Gb/s at 50 MHz is 2.5 bytes), and the
//! half-bytes between two frames: preamble and start delimiter (8), FCS (4) and inter-frame gap (12).
constexpr int rate_half_bytes = 5;
constexpr int gap_half_bytes = 2 * 24;
constexpr int beat_half_bytes = 16;

class Bench {
public:
    Bench(const char* script, const char* transcript) : flash_(0, 0), out_(transcript) {
        if (!out_) throw std::runtime_error("cannot open the transcript");
        std::ifstream input(script);
        if (!input) throw std::runtime_error("cannot open the stimulus script");
        for (std::string line; std::getline(input, line);) {
            if (line.empty() || line[0] == '#') continue;
            std::istringstream words(line);
            Step step;
            words >> step.op;
            for (std::string w; words >> w;) step.args.push_back(w);
            steps_.push_back(step);
        }
        if (steps_.empty() || steps_.back().op != "end") throw std::runtime_error("the script must end with end");
        if (const char* window = std::getenv("WIRE_HOST_LOG")) {
            // diagnosis only: every host access between two bus cycles, "<from>:<to>"
            host_log_ = true;
            host_log_from_ = std::strtoull(window, nullptr, 10);
            const char* colon = std::strchr(window, ':');
            host_log_to_ = colon ? std::strtoull(colon + 1, nullptr, 10) : ~0ULL;
        }
    }

    bool done() const { return done_; }
    std::uint64_t cycle() const { return sys_; }

    // ---- before a rising bus edge: observe both models (their state after the last edge, settled)
    void sample(const Vsim& cpu, const Vtb_split_top& top) {
        ++sys_;
        if (in_reset_) return;
        host_sample(cpu, top);
        csr_sample(cpu);
        uart_sample(cpu);
        if (fired_) {
            rx_fired();
            tx_fired();
            fired_ = false;
        }
        script();
    }

    // ---- with the inputs settled, just before the rising edge: the handshakes this edge makes
    void latch(const Vsim& cpu, const Vtb_split_top& top, bool dp_rising) {
        if (in_reset_) return;
        flash_latch(cpu);
        if (!dp_rising) return;
        fired_ = true;
        rx_fire_ = rx_offered_ && top.rx_tready;
        if (rx_offered_ && !top.rx_tready) { ++rx_stalls_; std::printf("RXSTALL %llu\n", ull(sys_)); }
        tx_fire_ = top.tx_tvalid && top.tx_tready;
        tx_data_ = top.tx_tdata;
        tx_keep_ = top.tx_tkeep;
        tx_last_ = top.tx_tlast;
        rx_credit_ = std::min(rx_credit_ + rate_half_bytes, beat_half_bytes);
        tx_credit_ = std::min(tx_credit_ + rate_half_bytes, beat_half_bytes);
        if (!csr_busy_) return;
        aw_fire_ = axi_aw_ && top.s_axi_awready;
        w_fire_ = axi_w_ && top.s_axi_wready;
        ar_fire_ = axi_ar_ && top.s_axi_arready;
        b_fire_ = axi_b_ && top.s_axi_bvalid;
        r_fire_ = axi_r_ && top.s_axi_rvalid;
        if (r_fire_) csr_rdata_ = top.s_axi_rdata;
        axi_fired_ = true;
    }

    // ---- the inputs for the next rising edge (the boundary is settled by the caller)
    void drive(Vsim& cpu, Vtb_split_top& top, bool dp_rising) {
        top.ms_tick_p_i = !in_reset_ && ms_count_ == ms_div - 1;
        cpu.milan_csr_ack = csr_ack_;
        cpu.milan_csr_dat_r = csr_rdata_;
        cpu.serial_source_ready = 1;
        cpu.serial_sink_valid = 0;
        cpu.flash_tx_ready = !flash_pending_ && cpu.flash_cs;
        cpu.flash_rx_valid = flash_pending_ && sys_ >= flash_at_;
        cpu.flash_rx_data = flash_response_;
        top.link_up = link_;
        top.s_axi_awaddr = axi_addr_;
        top.s_axi_araddr = axi_addr_;
        top.s_axi_wdata = axi_wdata_;
        top.s_axi_wstrb = axi_wstrb_;
        top.s_axi_awvalid = axi_aw_;
        top.s_axi_wvalid = axi_w_;
        top.s_axi_bready = axi_b_;
        top.s_axi_arvalid = axi_ar_;
        top.s_axi_rready = axi_r_;
        if (dp_rising) {
            rx_drive(top);
            top.tx_tready = tx_credit_ >= beat_half_bytes;
        }
    }

    // ---- after the rising edge
    void advance() {
        if (in_reset_) return;
        if (ms_count_ == ms_div - 1) {
            ms_count_ = 0;
            ++now_ms_;
            std::printf("MS %llu %u\n", ull(sys_), now_ms_);
            if (host_log_ && now_ms_ % 10 == 0)
                std::printf("PROGRESS %u host=%llu flash_words=%u csr=%u\n", now_ms_, ull(host_accesses_), flash_words_,
                            csr_reads_ + csr_writes_);
        } else {
            ++ms_count_;
        }
    }

    void release() { in_reset_ = false; }

    void report() const {
        std::printf("SUMMARY sys=%llu now_ms=%u rx_frames=%u tx_frames=%u rx_stalls=%u csr_reads=%u csr_writes=%u "
                    "host_accesses=%llu flash_selects=%u flash_words=%u uart_bytes=%zu\n",
                    ull(sys_), now_ms_, rx_frames_, tx_frames_, rx_stalls_, csr_reads_, csr_writes_,
                    ull(host_accesses_), flash_ops_, flash_words_, transcript_.size());
    }

private:
    // KL_mbx's host port, seen at the boundary: each access completes on its acknowledgement
    void host_sample(const Vsim& cpu, const Vtb_split_top& top) {
        if (cpu.mbx_host_req) {
            if (host_log_ && sys_ >= host_log_from_ && sys_ < host_log_to_)
                std::printf("HOSTREQ %llu %u %03x\n", ull(sys_), unsigned(cpu.mbx_host_we), unsigned(cpu.mbx_host_addr));
            host_we_ = cpu.mbx_host_we;
            host_word_ = cpu.mbx_host_addr;
            host_wdata_ = cpu.mbx_host_wdata;
        }
        if (!top.host_ack_o) return;
        ++host_accesses_;
        if (host_log_ && sys_ >= host_log_from_ && sys_ < host_log_to_)
            std::printf("HOST %llu %c %03x %08x\n", ull(sys_), host_we_ ? 'w' : 'r', host_word_,
                        host_we_ ? host_wdata_ : std::uint32_t(top.host_rdata_o));
        if (!host_we_) return;
        for (unsigned ch = 0; ch < n_channels; ++ch)
            if (host_word_ == tx_head_word[ch]) std::printf("TXC %llu %u %u\n", ull(sys_), ch, host_wdata_);
        if (host_word_ == tmr_deadline_word) deadline_ = host_wdata_;
        if (host_word_ == tmr_cmd_word) std::printf("TMR %llu %08x %u\n", ull(sys_), host_wdata_, deadline_);
    }

    // the CSR window: one Wishbone access, one AXI4-Lite access on the datapath clock
    void csr_sample(const Vsim& cpu) {
        if (csr_ack_) {
            csr_ack_ = false;
            return;
        }
        if (axi_fired_) {
            axi_fired_ = false;
            if (aw_fire_) axi_aw_ = false;
            if (w_fire_) axi_w_ = false;
            if (ar_fire_) axi_ar_ = false;
            if (b_fire_ || r_fire_) {
                axi_b_ = axi_r_ = false;
                csr_busy_ = false;
                csr_ack_ = true;
                if (csr_we_) ++csr_writes_; else ++csr_reads_;
                std::printf("%s %llu %03x %08x %llu\n", csr_we_ ? "CSRW" : "CSRR", ull(sys_), unsigned(axi_addr_),
                            csr_we_ ? axi_wdata_ : csr_rdata_, ull(sys_ - csr_start_));
            }
            return;
        }
        if (csr_busy_ || !(cpu.milan_csr_cyc && cpu.milan_csr_stb)) return;
        csr_busy_ = true;
        csr_we_ = cpu.milan_csr_we;
        csr_start_ = sys_;
        axi_addr_ = std::uint16_t((std::uint32_t(cpu.milan_csr_adr) << 2) & (csr_size - 1u));
        axi_wdata_ = cpu.milan_csr_dat_w;
        axi_wstrb_ = cpu.milan_csr_sel;
        axi_aw_ = axi_w_ = axi_b_ = csr_we_;
        axi_ar_ = axi_r_ = !csr_we_;
    }

    void uart_sample(const Vsim& cpu) {
        if (!cpu.serial_source_valid) return;
        const char ch = char(cpu.serial_source_data);
        transcript_.push_back(ch);
        out_.put(ch);
        std::printf("UART %llu %02x\n", ull(sys_), unsigned(std::uint8_t(ch)));
    }

    // the flash device: its chip select, and the PHY's handshakes at this edge (CPU budget harness's timing)
    void flash_latch(const Vsim& cpu) {
        if (flash_cs_ && !cpu.flash_cs) {
            const unsigned op = flash_.deselect(sys_);
            ++flash_ops_;
            if (host_log_ && sys_ >= host_log_from_ && sys_ < host_log_to_) std::printf("FLASH %llu %u\n", ull(sys_), op);
        }
        if (cpu.flash_tx_valid && cpu.flash_tx_ready) ++flash_words_;
        flash_cs_ = cpu.flash_cs;
        if (cpu.flash_rx_valid && cpu.flash_rx_ready) flash_pending_ = false;
        if (cpu.flash_tx_valid && cpu.flash_tx_ready) {
            flash_response_ = flash_.transfer(cpu.flash_tx_data, cpu.flash_tx_len, cpu.flash_tx_width, sys_);
            flash_at_ = sys_ + cpu.flash_tx_len * (sys_hz / 12500000u) + 1;   // a 12.5 MHz SCK
            flash_pending_ = true;
        }
    }

    // ---- the receive side of the MAC boundary: the beat the last datapath edge took
    void rx_fired() {
        if (!rx_fire_) return;
        const Frame& f = rx_.front();
        const std::size_t n = std::min<std::size_t>(8, f.bytes.size() - rx_offset_);
        if (rx_offset_ == 0) rx_first_ = sys_ - 1;
        rx_offset_ += n;
        rx_credit_ -= int(2 * n);
        if (rx_offset_ < f.bytes.size()) return;
        ++rx_frames_;
        std::printf("RXW %llu %llu %zu %s %s\n", ull(rx_first_), ull(sys_ - 1), f.bytes.size(), f.tag.c_str(),
                    hexed(f.bytes).c_str());
        rx_credit_ -= gap_half_bytes + 2 * int(std::max<std::size_t>(60, f.bytes.size()) - f.bytes.size());
        rx_.pop_front();
        rx_offset_ = 0;
    }

    void rx_drive(Vtb_split_top& top) {
        rx_offered_ = !rx_.empty() && sys_ >= rx_.front().not_before && rx_credit_ >= beat_half_bytes;
        top.rx_tvalid = rx_offered_;
        if (!rx_offered_) { top.rx_tlast = 0; return; }
        const Frame& f = rx_.front();
        const std::size_t n = std::min<std::size_t>(8, f.bytes.size() - rx_offset_);
        std::uint64_t data = 0;
        for (std::size_t i = 0; i < n; ++i) data |= std::uint64_t(f.bytes[rx_offset_ + i]) << (8 * i);
        top.rx_tdata = data;
        top.rx_tkeep = std::uint8_t((1u << n) - 1u);
        top.rx_tlast = rx_offset_ + n == f.bytes.size();
    }

    // ---- the transmit side: the beat the last datapath edge took
    void tx_fired() {
        if (!tx_fire_) return;
        if (tx_bytes_.empty()) tx_first_ = sys_ - 1;
        for (unsigned i = 0; i < 8; ++i)
            if (tx_keep_ & (1u << i)) tx_bytes_.push_back(std::uint8_t(tx_data_ >> (8 * i)));
        tx_credit_ -= 2 * __builtin_popcount(unsigned(tx_keep_));
        if (!tx_last_) return;
        ++tx_frames_;
        std::printf("TXW %llu %llu %zu %s\n", ull(tx_first_), ull(sys_ - 1), tx_bytes_.size(), hexed(tx_bytes_).c_str());
        tx_credit_ -= gap_half_bytes + 2 * int(std::max<std::size_t>(60, tx_bytes_.size()) - tx_bytes_.size());
        replies(tx_bytes_);
        tx_bytes_.clear();
    }

    void replies(const std::vector<std::uint8_t>& sent) {
        for (const Reply& r : replies_) {
            bool hit = true;
            for (const auto& [at, byte] : r.match) hit = hit && at < sent.size() && sent[at] == byte;
            if (!hit) continue;
            Frame f{r.tag, sent, sys_ + r.turnaround};
            for (const auto& [at, bytes] : r.patch)
                for (std::size_t i = 0; i < bytes.size(); ++i) f.bytes.at(at + i) = bytes[i];
            rx_.push_back(f);
        }
    }

    // ---- the stimulus script
    bool seen(const std::string& text) const { return transcript_.find(text) != std::string::npos; }

    std::uint64_t ms_cycles(const std::string& ms) const { return std::stoull(ms) * (sys_hz / 1000u); }

    void script() {
        while (step_ < steps_.size()) {
            const Step& s = steps_[step_];
            if (s.op == "wait") {
                if (s.args.at(0) == "ready") {
                    if (!seen(ready_line)) return;
                    std::printf("READY %llu\n", ull(sys_));
                } else if (s.args.at(0) == "ms") {
                    if (!waiting_) { wait_until_ = sys_ + ms_cycles(s.args.at(1)); waiting_ = true; }
                    if (sys_ < wait_until_) return;
                    waiting_ = false;
                } else if (s.args.at(0) == "cycles") {
                    if (!waiting_) { wait_until_ = sys_ + std::stoull(s.args.at(1)); waiting_ = true; }
                    if (sys_ < wait_until_) return;
                    waiting_ = false;
                } else if (s.args.at(0) == "now") {      // until NOW_MS reaches the value
                    if (now_ms_ < std::stoul(s.args.at(1))) return;
                } else {
                    throw std::runtime_error("unknown wait: " + s.args.at(0));
                }
            } else if (s.op == "link") {
                link_ = s.args.at(0) == "1";
            } else if (s.op == "frame") {
                rx_.push_back(Frame{s.args.at(0), unhex(s.args.at(1)), sys_});
            } else if (s.op == "reply") {
                Reply r;
                r.tag = s.args.at(0);
                r.turnaround = std::stoull(s.args.at(1));
                for (std::size_t i = 2; i < s.args.size(); ++i) {
                    const std::string& a = s.args[i];
                    const auto colon = a.find(':');
                    const auto equal = a.find('=');
                    if (colon != std::string::npos)
                        r.match.emplace_back(std::stoul(a.substr(0, colon)), std::uint8_t(std::stoul(a.substr(colon + 1), nullptr, 16)));
                    else if (equal != std::string::npos)
                        r.patch.emplace_back(std::stoul(a.substr(0, equal)), unhex(a.substr(equal + 1)));
                    else
                        throw std::runtime_error("bad reply term: " + a);
                }
                bool replaced = false;   // a rule of the same tag replaces the one before it
                for (Reply& old : replies_)
                    if (old.tag == r.tag) { old = r; replaced = true; }
                if (!replaced) replies_.push_back(r);
            } else if (s.op == "mark") {
                std::printf("MARK %llu %s\n", ull(sys_), s.args.at(0).c_str());
            } else if (s.op == "end") {
                done_ = true;
                return;
            } else {
                throw std::runtime_error("unknown script step: " + s.op);
            }
            ++step_;
        }
    }

    Flash flash_;
    std::ofstream out_;
    std::vector<Step> steps_;
    std::vector<Reply> replies_;
    std::deque<Frame> rx_;
    std::vector<std::uint8_t> tx_bytes_;
    std::string transcript_;
    std::uint64_t sys_ = 0;
    std::uint64_t wait_until_ = 0;
    std::uint64_t flash_at_ = 0;
    std::uint64_t csr_start_ = 0;
    std::uint64_t rx_first_ = 0;
    std::uint64_t tx_first_ = 0;
    std::uint64_t host_accesses_ = 0;
    std::uint64_t tx_data_ = 0;
    std::uint64_t host_log_from_ = 0;
    std::uint64_t host_log_to_ = 0;
    std::uint32_t ms_count_ = 0;
    std::uint32_t now_ms_ = 0;
    std::uint32_t deadline_ = 0;
    std::uint32_t host_word_ = 0;
    std::uint32_t host_wdata_ = 0;
    std::uint32_t flash_response_ = 0;
    std::uint32_t csr_rdata_ = 0;
    std::uint32_t axi_wdata_ = 0;
    std::uint16_t axi_addr_ = 0;
    std::uint8_t axi_wstrb_ = 0;
    std::size_t step_ = 0;
    std::size_t rx_offset_ = 0;
    int rx_credit_ = beat_half_bytes;
    int tx_credit_ = beat_half_bytes;
    unsigned flash_ops_ = 0;
    unsigned flash_words_ = 0;
    unsigned rx_frames_ = 0;
    unsigned tx_frames_ = 0;
    unsigned rx_stalls_ = 0;
    unsigned csr_reads_ = 0;
    unsigned csr_writes_ = 0;
    bool host_log_ = false;
    bool in_reset_ = true;
    bool waiting_ = false;
    bool done_ = false;
    bool link_ = false;
    bool host_we_ = false;
    bool csr_ack_ = false;
    bool csr_busy_ = false;
    bool csr_we_ = false;
    bool flash_cs_ = false;
    bool flash_pending_ = false;
    bool axi_aw_ = false;
    bool axi_w_ = false;
    bool axi_b_ = false;
    bool axi_ar_ = false;
    bool axi_r_ = false;
    bool rx_offered_ = false;
    bool fired_ = false;
    bool rx_fire_ = false;
    bool tx_fire_ = false;
    bool tx_last_ = false;
    bool axi_fired_ = false;
    bool aw_fire_ = false;
    bool w_fire_ = false;
    bool ar_fire_ = false;
    bool b_fire_ = false;
    bool r_fire_ = false;
    std::uint8_t tx_keep_ = 0;
};

void initialize(Vsim& cpu, Vtb_split_top& top) {
    cpu.sys_reset = 1;
    cpu.sys_clk = cpu.milan_clk = cpu.audio_clk = cpu.audio_tdm_clk = 0;
    cpu.serial_sink_valid = 0;
    cpu.serial_source_ready = 1;
    cpu.flash_tx_ready = cpu.flash_rx_valid = 0;
    cpu.milan_csr_ack = 0;
    cpu.mbx_host_ack = 0;
    cpu.mbx_host_rdata = 0;
    top.sys_clk = top.dp_clk = 0;
    top.sys_rst_n = top.dp_rst_n = 0;
    top.host_req_i = top.host_we_i = 0;
    top.ms_tick_p_i = 0;
    top.rx_tvalid = 0;
    top.tx_tready = 0;
    top.link_up = 0;
    top.tap_tvalid = 0;
    top.tap_ready = 1;
    cpu.eval();
    top.eval();
}

//! The boundary between the two models, settled: the split top's answer into the CPU half, the CPU half's request
//! into the split top, until neither moves.
void settle(Vsim& cpu, Vtb_split_top& top) {
    for (unsigned pass = 0; pass < 8; ++pass) {
        cpu.mbx_host_ack = top.host_ack_o;
        cpu.mbx_host_rdata = top.host_rdata_o;
        cpu.eval();
        const bool moved = top.host_req_i != cpu.mbx_host_req || top.host_we_i != cpu.mbx_host_we ||
                           top.host_addr_i != cpu.mbx_host_addr || top.host_wdata_i != cpu.mbx_host_wdata ||
                           top.host_be_i != cpu.mbx_host_be;
        top.host_req_i = cpu.mbx_host_req;
        top.host_we_i = cpu.mbx_host_we;
        top.host_addr_i = cpu.mbx_host_addr;
        top.host_wdata_i = cpu.mbx_host_wdata;
        top.host_be_i = cpu.mbx_host_be;
        top.eval();
        if (!moved && cpu.mbx_host_ack == top.host_ack_o && cpu.mbx_host_rdata == top.host_rdata_o) return;
    }
    throw std::runtime_error("the host port boundary does not settle");
}

void simulate(Vsim& cpu, Vtb_split_top& top, Bench& bench, std::uint64_t limit_cycles) {
    const std::uint64_t half_ps = 500000000000ULL / sys_hz;
    std::uint64_t edge = 0;
    while (!Verilated::gotFinish() && !bench.done()) {
        if (bench.cycle() > limit_cycles) throw std::runtime_error("simulation exceeded its time limit");
        const bool dp_rising = (edge % 2) == 0;
        bench.sample(cpu, top);
        bench.drive(cpu, top, dp_rising);
        settle(cpu, top);
        bench.latch(cpu, top, dp_rising);
        Verilated::threadContextp()->time((2 * edge + 1) * half_ps);
        cpu.sys_clk = cpu.milan_clk = 1;
        top.sys_clk = 1;
        top.dp_clk = dp_rising;
        cpu.eval();
        top.eval();
        bench.advance();
        Verilated::threadContextp()->time((2 * edge + 2) * half_ps);
        cpu.sys_clk = cpu.milan_clk = 0;
        top.sys_clk = 0;
        cpu.eval();
        top.eval();
        ++edge;
        if (edge == 128) {
            cpu.sys_reset = 0;
            top.sys_rst_n = top.dp_rst_n = 1;
            bench.release();
        }
    }
}

}  // namespace

int main(int argc, char** argv) {
    std::setvbuf(stdout, nullptr, _IOFBF, 1 << 20);
    Verilated::commandArgs(argc, argv);
    milan::tb::Checker check{"ctrl_wire_timing"};
    try {
        if (argc != 4) throw std::runtime_error("expected the stimulus script, the transcript path and the limit in ms");
        const milan::tb::Model<Vsim> cpu_model;
        const milan::tb::Model<Vtb_split_top> top_model;
        auto& cpu = *cpu_model.get();
        auto& top = *top_model.get();
        initialize(cpu, top);
        Bench bench(argv[1], argv[2]);
        simulate(cpu, top, bench, std::stoull(argv[3]) * (sys_hz / 1000u));
        check.that("the script ran to its end", bench.done());
        bench.report();
    } catch (const std::exception& error) {
        std::fflush(stdout);
        std::fprintf(stderr, "FAIL: %s\n", error.what());
        check.that("simulation completed without boundary failures", false);
    }
    std::fflush(stdout);
    return check.report();
}
