// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// The testbench of the split CPU budget (#665, #397): it drives the
// mailbox's datapath side from a stimulus script and observes, passively,
// the committed PCs, the CPU's fetch bus (cacheless, or its instruction
// cache's refills) and cacheless data bus, the mailbox host port, the
// receive commit and the event-ring writes. Every figure it prints is an
// observed clock count; run.py grades them.
#include "Vsim.h"
#include "budget_config.hpp"
#include "verilator_harness.hpp"
#include "flash.hpp"
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <deque>
#include <fstream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

namespace {
// printf's %llu takes unsigned long long; the widening is implicit, never a cast.
unsigned long long ull(std::uint64_t value) { return value; }

// Address regions of the CPU's view, in the order budget_config.hpp lists them.
enum Region : unsigned { ROM, SRAM, MBX, FLASH, CSR, OTHER, N_REGIONS };
const char* const region_name[N_REGIONS] = {"rom", "sram", "mbx", "flash", "csr", "other"};

Region region_of(std::uint32_t a) {
    if (a >= rom_base && a - rom_base < rom_size) return ROM;
    if (a >= sram_base && a - sram_base < sram_size) return SRAM;
    if (a >= mbx_base && a - mbx_base < mbx_size) return MBX;
    if (a >= flash_base && a - flash_base < flash_size) return FLASH;
    if (a >= csr_base && a - csr_base < csr_size) return CSR;
    return OTHER;
}

// The source module a committed PC belongs to, n_modules when no linked section holds it.
unsigned module_of(std::uint32_t pc) {
    const auto* end = std::end(code_spans);
    const auto* it = std::upper_bound(std::begin(code_spans), end, pc,
                                      [](std::uint32_t v, const CodeSpan& s) { return v < s.start; });
    if (it == std::begin(code_spans)) return n_modules;
    --it;
    return pc < it->end ? it->module : n_modules;
}

struct Stat {
    std::uint64_t count = 0, sum = 0, max = 0, min = ~0ULL;
    void add(std::uint64_t v) { ++count; sum += v; max = std::max(max, v); min = std::min(min, v); }
    std::string text(const char* name) const {
        char buf[160];
        std::snprintf(buf, sizeof buf, " %s=%llu/%llu/%llu/%llu", name, ull(count),
                      ull(sum), ull(count ? min : 0), ull(max));
        return buf;
    }
};

// One loop pass: from one committed entry of the pass function to the next.
struct Pass {
    std::uint64_t start_cpu = 0, start_sys = 0, instr = 0;
    std::array<std::uint64_t, N_REGIONS> fetch{}, fetch_wait{}, load{}, store{}, lsu_wait{};
    unsigned mbx_writes = 0;
    std::string writes;  // the mailbox writes, "cycle:word:value" each
    std::array<std::uint64_t, n_modules + 1> module_cycles{};
};

struct Step { std::string op; std::vector<std::string> args; };

class Bench {
public:
    Bench(const char* script, const char* flash_image) : flash_(0, 0) {
        if (flash_image[0] != '-') flash_.load(flash_image, 0);
        std::ifstream input(script);
        if (!input) throw std::runtime_error("cannot open stimulus script");
        std::string line;
        while (std::getline(input, line)) {
            if (line.empty() || line[0] == '#') continue;
            std::istringstream words(line);
            Step step;
            words >> step.op;
            for (std::string w; words >> w;) step.args.push_back(w);
            steps_.push_back(step);
        }
        if (steps_.empty() || steps_.back().op != "end") throw std::runtime_error("script must end with end");
    }

    void sample(Vsim& dut, bool cpu_rising) {
        ++sys_;
        if (dut.sys_reset) return;
        if (dut.mbx_ms_tick) {
            ++now_ms_;
            std::printf("MS %llu %u %08x %llu\n", ull(sys_), now_ms_, last_pc_,
                        ull(instr_));
        }
        host_sample(dut);
        if (rx_commit(dut)) {
            std::printf("RXC %llu %u\n", ull(sys_), rx_channel(dut));
        }
        if (evt_write(dut)) {
            std::printf("EVW %llu %u %08x\n", ull(sys_), evt_addr(dut), evt_data(dut));
        }
        egress_sample(dut);
        ingress_sample(dut);
        flash_sample(dut);
        if (cpu_rising) cpu_sample(dut);
        run_script();
    }

    // Drive the inputs for the next rising edge; true when any of them changed,
    // so the caller evaluates the model again only then.
    bool drive(Vsim& dut) {
        bool changed = false;
        auto put = [&changed](auto& input, auto value) {
            if (input != value) { input = value; changed = true; }
        };
        const bool frame = !frames_.empty() && sys_ >= ingress_at_;
        put(dut.mbx_rx_valid, frame);
        put(dut.mbx_rx_data, std::uint8_t(frame ? frames_.front().bytes.at(offset_) : 0));
        put(dut.mbx_rx_last, frame && offset_ + 1 == frames_.front().bytes.size());
        put(dut.mbx_rx_if, std::uint8_t(frame ? frames_.front().interface : 0));
        put(dut.mbx_tx_ready, tx_ready_);
        put(dut.mbx_link_up, std::uint8_t(link_));
        put(dut.mbx_gm_change, std::uint8_t(gm_pulse_));
        if (gm_dirty_) {
            for (unsigned i = 0; i < n_if; ++i) set_gm(dut, i, gm_id_[i], gm_domain_[i]);
            gm_dirty_ = false;
            changed = true;
        }
        put(dut.flash_tx_ready, bool(!flash_pending_ && dut.flash_cs));
        put(dut.flash_rx_valid, bool(flash_pending_ && sys_ >= flash_at_));
        put(dut.flash_rx_data, flash_response_);
        return changed;
    }

    bool done() const { return finished_; }

    void report() const {
        flush_idle();
        std::string text = "SUMMARY";
        text += " sys=" + std::to_string(sys_) + " cpu=" + std::to_string(cpu_) + " passes=" + std::to_string(passes_);
        text += " instr=" + std::to_string(instr_) + " bus_errors=" + std::to_string(bus_errors_) + " traps=" + std::to_string(traps_);
        text += mbx_read_.text("mbx_read") + mbx_write_.text("mbx_write");
        text += host_.text("host_cycles");
        for (unsigned r = 0; r < N_REGIONS; ++r) {
            text += fetch_lat_[r].text((std::string("fetch_") + region_name[r]).c_str());
            text += load_lat_[r].text((std::string("load_") + region_name[r]).c_str());
            text += store_lat_[r].text((std::string("store_") + region_name[r]).c_str());
        }
        std::printf("%s\n", text.c_str());
        std::string mods = "MODULES";
        for (unsigned m = 0; m <= n_modules; ++m)
            if (module_total_[m])
                mods += " " + std::string(m < n_modules ? module_name[m] : "unmapped") + ":" + std::to_string(module_total_[m]);
        std::printf("%s\n", mods.c_str());
        std::printf("FLASH erases=%u programs=%u bytes=%u\n", flash_.erases, flash_.programs, flash_.programmed_bytes);
        std::uint64_t boot = 0, service = 0, service_only = 0;
        std::array<std::uint64_t, n_modules + 1> by_module{};
        for (std::size_t w = 0; w < code_seen_.size(); ++w) {
            if (code_seen_[w] & 1) ++boot;
            if (code_seen_[w] & 2) { ++service; by_module[module_of(std::uint32_t(w) << 2)] += 4; }
            if (code_seen_[w] == 2) ++service_only;
        }
        std::string code = "CODE boot_bytes=" + std::to_string(4 * boot) + " service_bytes=" + std::to_string(4 * service) +
            " service_only_bytes=" + std::to_string(4 * service_only);
        for (unsigned m = 0; m <= n_modules; ++m)
            if (by_module[m]) code += " " + std::string(m < n_modules ? module_name[m] : "unmapped") + "=" + std::to_string(by_module[m]);
        std::printf("%s\n", code.c_str());
    }

private:
    struct Frame { unsigned interface; std::vector<std::uint8_t> bytes; std::string tag = "-"; };
    struct Sent { unsigned interface; std::vector<std::uint8_t> bytes; };

    void host_sample(Vsim& dut) {
        if (dut.mbx_host_req) host_req_at_ = sys_;
        if (!dut.mbx_host_ack) return;
        host_.add(sys_ - host_req_at_);
        const unsigned word = dut.mbx_host_addr;
        if (host_we_) {
            if (word == filter_en_word && host_wdata_) filter_open_ = true;
            for (unsigned ch = 0; ch < n_ch; ++ch)
                if (word == tx_head_word(ch)) { ++tx_commits_[ch]; std::printf("TXC %llu %u %u\n", ull(sys_), ch, host_wdata_); }
            if (word == tmr_cmd_word) ++tmr_writes_.at(host_wdata_ & 0xffu).at(host_wdata_ >> 30);
            char buf[64];
            std::snprintf(buf, sizeof buf, " %llu:%x:%x", ull(sys_), word, host_wdata_);
            pass_.writes += buf;
            ++pass_.mbx_writes;
        }
        (void)dut;
    }

    void egress_sample(Vsim& dut) {
        if (!dut.mbx_tx_valid || !tx_ready_) return;
        egress_.push_back(dut.mbx_tx_data);
        if (!dut.mbx_tx_last) return;
        std::string hex;
        char b[3];
        for (auto byte : egress_) { std::snprintf(b, sizeof b, "%02x", byte); hex += b; }
        std::printf("WIRE %llu %u %u %s\n", ull(sys_), unsigned(dut.mbx_tx_if),
                    unsigned(dut.mbx_tx_ch), hex.c_str());
        auto& kept = last_wire_.at(dut.mbx_tx_ch);
        kept.push_back({unsigned(dut.mbx_tx_if), egress_});
        if (kept.size() > 32) kept.pop_front();
        ++wire_frames_;
        egress_.clear();
    }

    void ingress_sample(Vsim& dut) {
        gm_pulse_ = 0;
        if (frames_.empty() || sys_ < ingress_at_ || !dut.mbx_rx_valid || !dut.mbx_rx_ready) return;
        if (offset_ == 0)
            std::printf("RXS %llu %u %zu %s\n", ull(sys_), frames_.front().interface,
                        frames_.front().bytes.size(), frames_.front().tag.c_str());
        if (++offset_ < frames_.front().bytes.size()) return;
        std::printf("RXE %llu\n", ull(sys_));
        frames_.pop_front();
        offset_ = 0;
        ingress_at_ = sys_ + gap_;
    }

    void flash_sample(Vsim& dut) {
        if (flash_cs_ && !dut.flash_cs) {
            const auto op = flash_.deselect(sys_);
            if (op) std::printf("FLASHOP %llu %u\n", ull(sys_), op);
        }
        flash_cs_ = dut.flash_cs;
        if (dut.flash_rx_valid && dut.flash_rx_ready) flash_pending_ = false;
        if (dut.flash_tx_valid && dut.flash_tx_ready) {
            flash_response_ = flash_.transfer(dut.flash_tx_data, dut.flash_tx_len, dut.flash_tx_width, sys_);
            // fw_service_budget's device timing: 12.5 MHz SCK, one completion cycle.
            flash_at_ = sys_ + dut.flash_tx_len * (sys_hz / 12500000) + 1;
            flash_pending_ = true;
        }
    }

    void cpu_sample(Vsim& dut) {
        ++cpu_;
        ++pass_.module_cycles[module_];
        ++module_total_[module_];
        if (commit_valid(dut)) {
            ++instr_;
            ++pass_.instr;
            last_pc_ = commit_pc(dut);
            module_ = module_of(last_pc_);
            if (trace_left_ && (tracing_ || (trace_from && last_pc_ == trace_from) || (trace_after_ && sys_ >= trace_after_))) {
                tracing_ = true;
                --trace_left_;
                std::printf("PC %llu %08x\n", ull(cpu_), last_pc_);
            }
            if (last_pc_ == pass_pc) pass_boundary();
            // A function entry a probe starts at (a test-only entry's call), by its symbol.
            for (unsigned e = 0; e < n_entries; ++e)
                if (last_pc_ == entry_pc[e]) std::printf("ENTRY %llu %s\n", ull(sys_), entry_name[e]);
        }
        if (trap_valid(dut)) {
            ++traps_;
            std::printf("TRAP %llu %u %u %08x\n", ull(cpu_), unsigned(trap_interrupt(dut)),
                        trap_cause(dut), last_pc_);
        }
        // A fetch command carries fetch_beats words: one without a cache, a whole line on the
        // instruction cache's refill bus. Its wait runs to its last beat (or its error).
        if (fetch_cmd_valid(dut) && fetch_cmd_ready(dut)) {
            const auto r = region_of(fetch_address(dut));
            ++pass_.fetch[r];
            fetch_at_[fetch_cmd_id(dut)] = {cpu_, r, fetch_address(dut), 0};
            if (tracing_ && trace_left_) std::printf("FETCH %llu %08x\n", ull(cpu_), fetch_address(dut));
            if (r == ROM || r == FLASH)
                for (unsigned k = 0; k < fetch_beats; ++k) note_code(fetch_address(dut) + 4u * k);
        }
        if (fetch_rsp_valid(dut)) {
            auto& at = fetch_at_[fetch_rsp_id(dut)];
            const bool error = fetch_rsp_error(dut);
            if (error) {
                ++bus_errors_;
                std::printf("BUSERR %llu fetch %08x\n", ull(cpu_), at.address);
            }
            if (at.beats < fetch_beats && (++at.beats == fetch_beats || error)) {
                at.beats = fetch_beats;
                fetch_lat_[at.region].add(cpu_ - at.start);
                pass_.fetch_wait[at.region] += cpu_ - at.start;
            }
        }
        if (lsu_cmd_valid(dut) && lsu_cmd_ready(dut)) {
            const auto r = region_of(lsu_address(dut));
            const bool write = lsu_write(dut);
            (write ? pass_.store : pass_.load)[r] += 1;
            lsu_at_[lsu_cmd_id(dut)] = {cpu_, r, write, lsu_address(dut)};
        }
        if (lsu_rsp_valid(dut)) {
            const auto& at = lsu_at_[lsu_rsp_id(dut)];
            const auto wait = cpu_ - at.start;
            if (lsu_rsp_error(dut)) {
                ++bus_errors_;
                std::printf("BUSERR %llu %s %08x\n", ull(cpu_), at.write ? "store" : "load", at.address);
            }
            (at.write ? store_lat_ : load_lat_)[at.region].add(wait);
            if (at.region == MBX) (at.write ? mbx_write_ : mbx_read_).add(wait);
            pass_.lsu_wait[at.region] += wait;
        }
    }

    // The code words fetched before the mailbox opened (boot) and after it (service).
    void note_code(std::uint32_t address) {
        const auto word = address >> 2;
        if (word >= code_seen_.size()) code_seen_.resize(word + 1, 0);
        const std::uint8_t bit = filter_open_ ? 2 : 1;
        if (!code_seen_[word]) ++code_words_;
        code_seen_[word] |= bit;
    }

    void pass_boundary() {
        if (passes_ > 0) finish_pass();
        ++passes_;
        pass_ = Pass{};
        pass_.start_cpu = cpu_;
        pass_.start_sys = sys_;
        pass_.instr = 1;
        pass_open_ = true;
    }

    void finish_pass() {
        const auto cycles = cpu_ - pass_.start_cpu;
        if (pass_.mbx_writes == 0) {
            ++idle_count_;
            idle_max_ = std::max(idle_max_, cycles);
            idle_min_ = std::min(idle_min_, cycles);
            ++quiet_run_;
            return;
        }
        quiet_run_ = 0;
        flush_idle();
        std::string text = "PASS " + std::to_string(passes_) + " " + std::to_string(pass_.start_sys) + " " +
            std::to_string(pass_.start_cpu) + " " + std::to_string(cycles) + " instr=" + std::to_string(pass_.instr);
        for (unsigned r = 0; r < N_REGIONS; ++r) {
            if (pass_.fetch[r]) text += " fetch_" + std::string(region_name[r]) + "=" + std::to_string(pass_.fetch[r]) + "/" + std::to_string(pass_.fetch_wait[r]);
            if (pass_.load[r]) text += " load_" + std::string(region_name[r]) + "=" + std::to_string(pass_.load[r]);
            if (pass_.store[r]) text += " store_" + std::string(region_name[r]) + "=" + std::to_string(pass_.store[r]);
            if (pass_.lsu_wait[r]) text += " wait_" + std::string(region_name[r]) + "=" + std::to_string(pass_.lsu_wait[r]);
        }
        text += " code_words=" + std::to_string(code_words_) + " mods=";
        for (unsigned m = 0; m <= n_modules; ++m)
            if (pass_.module_cycles[m])
                text += std::string(m < n_modules ? module_name[m] : "unmapped") + ":" + std::to_string(pass_.module_cycles[m]) + ",";
        std::printf("%s W%s\n", text.c_str(), pass_.writes.c_str());
    }

    void flush_idle() const {
        if (!idle_count_) return;
        std::printf("IDLE %llu %llu %llu\n", ull(idle_count_),
                    ull(idle_min_), ull(idle_max_));
        idle_count_ = 0;
        idle_max_ = 0;
        idle_min_ = ~0ULL;
    }

    bool satisfied(const Step& s) {
        if (s.op == "ready") return filter_open_ && passes_ > 0;
        if (s.op == "cycles") return sys_ - wait_from_ >= std::stoull(s.args.at(0));
        if (s.op == "ms") return now_ms_ >= std::stoul(s.args.at(0));
        if (s.op == "tx") return tx_commits_.at(std::stoul(s.args.at(0))) - tx_mark_.at(std::stoul(s.args.at(0))) >= std::stoul(s.args.at(1));
        if (s.op == "wire") return wire_frames_ - wire_mark_ >= std::stoul(s.args.at(0));
        if (s.op == "tmr") {  // tmr <slot> <op>: a TMR_CMD write of that slot and op (1 arm, 2 cancel)
            const unsigned slot = std::stoul(s.args.at(0)), op = std::stoul(s.args.at(1));
            return tmr_writes_.at(slot).at(op) > tmr_mark_.at(slot).at(op);
        }
        if (s.op == "quiet") return frames_.empty() && quiet_run_ >= std::stoul(s.args.at(0));
        if (s.op == "drained") return frames_.empty();
        throw std::runtime_error("unknown wait " + s.op);
    }

    void run_script() {
        while (step_ < steps_.size()) {
            const Step& s = steps_[step_];
            if (s.op == "wait") {
                if (!armed_) {
                    armed_ = true;
                    wait_from_ = sys_;
                    tx_mark_ = tx_commits_;
                    wire_mark_ = wire_frames_;
                    quiet_run_ = 0;
                }
                std::vector<std::string> args(s.args.begin() + 1, s.args.end());
                std::uint64_t within = 0;
                if (args.size() >= 2 && args[args.size() - 2] == "within") {
                    within = std::stoull(args.back());
                    args.resize(args.size() - 2);
                }
                Step condition{s.args.at(0), args};
                const bool met = satisfied(condition);
                if (!met && !(within && sys_ - wait_from_ >= within)) return;
                armed_ = false;
                std::printf("STEP %llu %zu wait %s%s\n", ull(sys_), step_, s.args.at(0).c_str(),
                            met ? "" : " TIMEOUT");
            } else if (s.op == "frame") {
                // frame <if> <hex> [tag]
                Frame f{unsigned(std::stoul(s.args.at(0))), {}};
                const auto& hex = s.args.at(1);
                for (std::size_t i = 0; i + 1 < hex.size(); i += 2) f.bytes.push_back(std::stoul(hex.substr(i, 2), nullptr, 16));
                if (s.args.size() > 2) f.tag = s.args[2];
                frames_.push_back(f);
            } else if (s.op == "reply") {
                // reply <if> <ch> <offset>:<hex> [on=<n>] <offset>=<hex> ...: the newest frame the
                // channel sent (on interface n, if given) whose bytes at offset match, patched
                const unsigned ch = std::stoul(s.args.at(1));
                const auto& sel = s.args.at(2);
                const auto colon = sel.find(':');
                const std::size_t sel_at = std::stoul(sel.substr(0, colon));
                const auto sel_hex = sel.substr(colon + 1);
                int on = -1;
                for (std::size_t a = 3; a < s.args.size(); ++a)
                    if (s.args[a].rfind("on=", 0) == 0) on = std::stoi(s.args[a].substr(3));
                const std::vector<std::uint8_t>* chosen = nullptr;
                for (auto it = last_wire_.at(ch).rbegin(); it != last_wire_.at(ch).rend() && !chosen; ++it) {
                    const auto& bytes = it->bytes;
                    bool match = (on < 0 || int(it->interface) == on) && bytes.size() >= sel_at + sel_hex.size() / 2;
                    for (std::size_t i = 0; match && i + 1 < sel_hex.size(); i += 2)
                        match = bytes[sel_at + i / 2] == std::stoul(sel_hex.substr(i, 2), nullptr, 16);
                    if (match) chosen = &bytes;
                }
                if (!chosen) throw std::runtime_error("reply: no frame the channel sent matches " + sel);
                Frame f{unsigned(std::stoul(s.args.at(0))), *chosen};
                for (std::size_t a = 3; a < s.args.size(); ++a) {
                    if (s.args[a].rfind("tag=", 0) == 0) { f.tag = s.args[a].substr(4); continue; }
                    if (s.args[a].rfind("on=", 0) == 0) continue;
                    const auto eq = s.args[a].find('=');
                    std::size_t at = std::stoul(s.args[a].substr(0, eq));
                    const auto hex = s.args[a].substr(eq + 1);
                    for (std::size_t i = 0; i + 1 < hex.size(); i += 2) f.bytes.at(at++) = std::stoul(hex.substr(i, 2), nullptr, 16);
                }
                std::string text;
                char b[3];
                for (auto byte : f.bytes) { std::snprintf(b, sizeof b, "%02x", byte); text += b; }
                std::printf("REPLY %llu %u %s\n", ull(sys_), f.interface, text.c_str());
                frames_.push_back(f);
            } else if (s.op == "gap") {
                gap_ = std::stoull(s.args.at(0));
            } else if (s.op == "link") {
                const unsigned i = std::stoul(s.args.at(0));
                link_ = std::stoul(s.args.at(1)) ? (link_ | (1u << i)) : (link_ & ~(1u << i));
                std::printf("LINK %llu %u %u\n", ull(sys_), i, (link_ >> i) & 1u);
            } else if (s.op == "gm") {
                const unsigned i = std::stoul(s.args.at(0));
                gm_id_.at(i) = std::stoull(s.args.at(1), nullptr, 16);
                gm_domain_.at(i) = std::stoul(s.args.at(2));
                gm_pulse_ |= 1u << i;
                gm_dirty_ = true;
                std::printf("GM %llu %u\n", ull(sys_), i);
            } else if (s.op == "txready") {
                tx_ready_ = std::stoul(s.args.at(0)) != 0;
                std::printf("TXREADY %llu %u\n", ull(sys_), unsigned(tx_ready_));
            } else if (s.op == "mark") {
                // A timer wait counts the slot's writes since the latest mark, so probes run
                // together, one per interface, each see their own arm.
                tmr_mark_ = tmr_writes_;
                std::printf("MARK %llu %s\n", ull(sys_), s.args.at(0).c_str());
            } else if (s.op == "end") {
                if (pass_open_) finish_pass();
                finished_ = true;
                ++step_;
                return;
            } else {
                throw std::runtime_error("unknown step " + s.op);
            }
            ++step_;
        }
    }

    struct FetchAt { std::uint64_t start = 0; Region region = OTHER; std::uint32_t address = 0; unsigned beats = 0; };
    struct LsuAt { std::uint64_t start = 0; Region region = OTHER; bool write = false; std::uint32_t address = 0; };

    Flash flash_;
    std::vector<Step> steps_;
    std::size_t step_ = 0;
    bool armed_ = false;
    bool finished_ = false;
    bool filter_open_ = false;
    bool pass_open_ = false;
    std::uint64_t sys_ = 0, cpu_ = 0, instr_ = 0, passes_ = 0, wait_from_ = 0;
    unsigned now_ms_ = 0;
    std::uint32_t last_pc_ = 0;
    unsigned module_ = n_modules;
    std::array<std::uint64_t, n_modules + 1> module_total_{};
    // An optional trace of committed PCs from the first commit at trace_from (a debugging aid).
    std::uint64_t trace_left_ = std::getenv("BUDGET_TRACE_PCS") ? std::stoull(std::getenv("BUDGET_TRACE_PCS")) : 0;
    std::uint32_t trace_from = std::getenv("BUDGET_TRACE_FROM") ? std::stoul(std::getenv("BUDGET_TRACE_FROM"), nullptr, 16) : 0;
    std::uint64_t trace_after_ = std::getenv("BUDGET_TRACE_AFTER") ? std::stoull(std::getenv("BUDGET_TRACE_AFTER")) : 0;
    bool tracing_ = false;
    std::uint64_t host_req_at_ = 0;
    bool host_we_ = false;
    std::uint32_t host_wdata_ = 0;
    std::array<unsigned, n_ch> tx_commits_{}, tx_mark_{};
    std::array<std::array<unsigned, 4>, 256> tmr_writes_{}, tmr_mark_{};  // per slot and op
    unsigned wire_frames_ = 0, wire_mark_ = 0;
    std::vector<std::uint8_t> egress_;
    std::array<std::deque<Sent>, n_ch> last_wire_;  // the newest frames each channel sent, with their interface
    std::deque<Frame> frames_;
    std::size_t offset_ = 0;
    std::uint64_t ingress_at_ = 0, gap_ = 20;
    bool tx_ready_ = true;
    unsigned link_ = 0, gm_pulse_ = 0;
    bool gm_dirty_ = true;
    std::array<std::uint64_t, n_if> gm_id_{};
    std::array<unsigned, n_if> gm_domain_{};
    bool flash_cs_ = false;
    bool flash_pending_ = false;
    std::uint64_t flash_at_ = 0;
    std::uint32_t flash_response_ = 0;
    std::array<FetchAt, 2> fetch_at_{};
    unsigned bus_errors_ = 0, traps_ = 0;
    std::array<LsuAt, 2> lsu_at_{};
    Pass pass_;
    mutable std::uint64_t idle_count_ = 0, idle_max_ = 0, idle_min_ = ~0ULL;
    std::uint64_t quiet_run_ = 0;
    std::vector<std::uint8_t> code_seen_;
    std::uint64_t code_words_ = 0;
    Stat mbx_read_, mbx_write_, host_;
    std::array<Stat, N_REGIONS> fetch_lat_, load_lat_, store_lat_;

public:
    // The host port's request fields, latched the cycle they are presented.
    void latch_host(const Vsim& dut) {
        if (dut.mbx_host_req) { host_we_ = dut.mbx_host_we; host_wdata_ = dut.mbx_host_wdata; }
    }
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
    dut.eval();
}

// fw_service_budget's clocking: aligned rising edges, the CPU at cpu_hz.
void simulate(Vsim& dut, Bench& bench) {
    const std::array<std::uint64_t, 2> frequency = {sys_hz, cpu_hz};
    std::array<std::uint64_t, 2> edge = {1, 1};
    std::array<std::uint64_t, 2> next{};
    const std::array<std::uint64_t, 2> offset = {0, (500000000000ULL / cpu_hz - 500000000000ULL / sys_hz)};
    for (unsigned i = 0; i < next.size(); ++i) next[i] = 500000000000ULL / frequency[i] + offset[i];
    while (!Verilated::gotFinish() && !bench.done()) {
        const auto time_ps = *std::min_element(next.begin(), next.end());
        if (time_ps > sim_limit_ps) throw std::runtime_error("simulation exceeded its time limit");
        if (time_ps <= Verilated::threadContextp()->time()) throw std::runtime_error("nonmonotonic clock");
        Verilated::threadContextp()->time(time_ps);
        if (next[0] == time_ps && !dut.sys_clk) {
            bench.latch_host(dut);
            bench.sample(dut, next[1] == time_ps && !dut.milan_clk);
        }
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
        if (!dut.sys_clk && bench.drive(dut)) dut.eval();
    }
}
} // namespace

int main(int argc, char** argv) {
    std::setvbuf(stdout, nullptr, _IOFBF, 1 << 20);
    Verilated::commandArgs(argc, argv);
    milan::tb::Checker check{"ctrl_service_budget"};
    try {
        if (argc != 3) throw std::runtime_error("expected the stimulus script and the flash image (or -)");
        const milan::tb::Model<Vsim> model;
        auto& dut = *model.get();
        initialize(dut);
        Bench bench(argv[1], argv[2]);
        simulate(dut, bench);
        check.that("every stimulus step completed", bench.done());
        bench.report();
    } catch (const std::exception& error) {
        std::fflush(stdout);
        std::fprintf(stderr, "FAIL: %s\n", error.what());
        check.that("simulation completed without boundary failures", false);
    }
    std::fflush(stdout);
    return check.report();
}
