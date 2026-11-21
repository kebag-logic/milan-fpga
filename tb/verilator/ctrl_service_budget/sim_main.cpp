// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// The testbench of the split CPU budget (#665, #397): it drives the
// mailbox's datapath side from a stimulus script and observes, passively,
// the committed PCs, the CPU's fetch bus (cacheless, or its instruction
// cache's refills) and cacheless data bus, the mailbox host port, the
// receive commit and the event-ring writes. Every figure it prints is an
// observed clock count; run.py grades them. It also reports each call of a
// traced function (SPAN: the commit of its entry to the commit of its return
// address) and each entry of a called one (CALL), the saved-state store's
// steps and the owners they reach (#665), and each MRP timer's expiry with the
// participant that owns it, read off the CPU's register file at the timer
// callback's entry and at its participant's creation (note_owner; PR #934).
// BUDGET_JOURNAL_IN, a file of the
// journal's bytes, is loaded over the flash image at the journal; at the end
// the journal's bytes are written to BUDGET_JOURNAL_OUT.
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
#include <map>
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
    bool step = false;   // the saved-state store's step was entered (step_pc)
    bool mbx_seen = false;  // the pass has addressed the mailbox
    bool aged = false;   // the step was entered before the pass addressed the mailbox: an aged step's (THE STEP)
    std::string writes;  // the mailbox writes, "cycle:word:value" each
    std::array<std::uint64_t, n_modules + 1> module_cycles{};
};

struct Step { std::string op; std::vector<std::string> args; };

class Bench {
public:
    Bench(const char* script, const char* flash_image) : flash_(0, 0) {
        // The store's journal is the flash map's (budget_config.hpp), the KLJ3 journal at the split placement
        // (#823): the device refuses a write outside it, and its reads are the FLASHRD runs below.
        flash_.journal(journal_offset, journal_size);
        if (flash_image[0] != '-') flash_.load(flash_image, 0);
        if (const char* journal = std::getenv("BUDGET_JOURNAL_IN")) flash_.load(journal, journal_offset);
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

    void sample(Vsim& dut) {
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
        // A record its channel's bucket had no token for is held (#917): its hold, in its commit's place, and
        // its commit at the channel's next refill, which grade.py credits to the frame that channel holds.
        if (rx_hold(dut)) {
            std::printf("RXH %llu %u\n", ull(sys_), rx_channel(dut));
        }
        if (const unsigned released = rx_release(dut)) {
            for (unsigned c = 0; c < n_ch; ++c) {
                if ((released >> c) & 1u) std::printf("RXR %llu %u\n", ull(sys_), c);
            }
        }
        if (evt_write(dut)) {
            std::printf("EVW %llu %u %08x\n", ull(sys_), evt_addr(dut), evt_data(dut));
            event_word(evt_addr(dut) % ev_words, evt_data(dut));
        }
        egress_sample(dut);
        ingress_sample(dut);
        if constexpr (has_ts) {
            for (unsigned i = 0; i < n_if; ++i) {
                if (ts_take(dut, i) && !ts_q_[i].empty()) {
                    ts_q_[i].pop_front();
                    ts_shown_n_[i] = ~std::size_t{0};   // show the next head
                }
            }
            peer_tick();
        }
        flash_sample(dut);
        cpu_sample(dut);
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
        put(dut.mbx_avb_chg, std::uint8_t(dp_pulse_[0]));
        put(dut.mbx_asp_chg, std::uint8_t(dp_pulse_[1]));
        put(dut.mbx_amap_wr, std::uint8_t(dp_pulse_[2]));
        if (gm_dirty_) {
            for (unsigned i = 0; i < n_if; ++i) set_gm(dut, i, gm_id_[i], gm_domain_[i]);
            gm_dirty_ = false;
            changed = true;
        }
        if constexpr (has_ts) {
            for (unsigned i = 0; i < n_if; ++i) {
                const bool valid = !ts_q_[i].empty();
                if (valid != ts_shown_[i] || (valid && ts_q_[i].size() != ts_shown_n_[i])) {
                    const TsRec r = valid ? ts_q_[i].front() : TsRec{};
                    set_ts(dut, i, valid, r.egress, r.ok, r.type, r.seq, r.ns);
                    ts_shown_[i] = valid;
                    ts_shown_n_[i] = ts_q_[i].size();
                    changed = true;
                }
            }
        }
        put(dut.flash_tx_ready, bool(!flash_pending_ && dut.flash_cs));
        put(dut.flash_rx_valid, bool(flash_pending_ && sys_ >= flash_at_));
        put(dut.flash_rx_data, flash_response_);
        return changed;
    }

    bool done() const { return finished_; }

    void report() const {
        flush_idle();
        flush_reads();
        if (const char* path = std::getenv("BUDGET_JOURNAL_OUT")) {
            std::ofstream out(path, std::ios::binary);
            for (std::uint32_t a = journal_offset; a < journal_offset + journal_size; ++a)
                out.put(static_cast<char>(flash_.byte(a)));
            if (!out) throw std::runtime_error("cannot write the journal");
        }
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
    struct Frame { unsigned interface; std::vector<std::uint8_t> bytes; std::string tag = "-";
                   std::uint64_t ts_ns = 0; };   // contract 2.5: the stamp the timestamp unit gives it, 0: its arrival
    struct Sent { unsigned interface; std::vector<std::uint8_t> bytes; };

    void host_sample(Vsim& dut) {
        if (dut.mbx_host_req) host_req_at_ = sys_;
        if (!dut.mbx_host_ack) return;
        host_.add(sys_ - host_req_at_);
        const unsigned word = dut.mbx_host_addr;
        if (host_we_) {
            if (word == filter_en_word) {
                // the channel gate the image writes, each bit named by the contract's channel table (grade.py)
                std::printf("OPEN %llu %x\n", ull(sys_), host_wdata_);
                if (host_wdata_) filter_open_ = true;
            }
            for (unsigned ch = 0; ch < n_ch; ++ch)
                if (word == tx_head_word(ch)) { ++tx_commits_[ch]; std::printf("TXC %llu %u %u\n", ull(sys_), ch, host_wdata_); }
            if (word == tmr_cmd_word) ++tmr_writes_.at(host_wdata_ & 0xffu).at(host_wdata_ >> 30);
            if (word == evt_tail_word) {
                evt_released_ += std::uint16_t(host_wdata_ - evt_tail_);
                evt_tail_ = host_wdata_;
            }
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
        if (dut.mbx_tx_ch == gptp_ch) {
            // the launch: the frame's first byte, len cycles of this byte stream ago
            const std::uint64_t t = ns_now() - (egress_.size() - 1) * (1000000000ull / sys_hz);
            ts_note(unsigned(dut.mbx_tx_if), true, egress_, t);
            peer_react(unsigned(dut.mbx_tx_if), egress_, t);
        }
        auto& kept = last_wire_.at(dut.mbx_tx_ch);
        kept.push_back({unsigned(dut.mbx_tx_if), egress_});
        if (kept.size() > 32) kept.pop_front();
        ++wire_frames_;
        egress_.clear();
    }

    // One word of an event record: a whole record is posted, and a TICK record's centiseconds counted.
    void event_word(unsigned word, std::uint32_t data) {
        if (word == 0) evt_type_ = data & 0xffu;
        if (word == 1) evt_count_ = (data >> ev_tick_count_lsb) & ev_tick_count_mask;
        if (word != ev_words - 1) return;
        ++evt_posted_;
        if (evt_type_ == ev_tick_type) centiseconds_ += evt_count_;
    }

    void ingress_sample(Vsim& dut) {
        gm_pulse_ = 0;
        dp_pulse_[0] = dp_pulse_[1] = dp_pulse_[2] = 0;
        if (frames_.empty() || sys_ < ingress_at_ || !dut.mbx_rx_valid || !dut.mbx_rx_ready) return;
        if (offset_ == 0) {
            std::printf("RXS %llu %u %zu %s\n", ull(sys_), frames_.front().interface,
                        frames_.front().bytes.size(), frames_.front().tag.c_str());
            const Frame& fr = frames_.front();
            ts_note(fr.interface, false, fr.bytes, fr.ts_ns ? fr.ts_ns : ns_now());
        }
        if (++offset_ < frames_.front().bytes.size()) return;
        std::printf("RXE %llu\n", ull(sys_));
        frames_.pop_front();
        offset_ = 0;
        ingress_at_ = sys_ + gap_;
    }

    // The saved-state store's flash steps, each closed command as its chip select falls: an erase or a page
    // program (FLASHOP, with its address and bytes), a busy poll (FLASHPOLL), and the journal's reads, one
    // FLASHRD line for each run of reads, each starting inside the span the run has read and within read_gap
    // cycles of its last (the uncached window reads a word for each byte load): a read-back step's 128 bytes,
    // a boot judgement's slot. A save's read-backs are so seen though their passes write nothing to the
    // mailbox (save_window.py).
    void flash_closed() {
        const auto command = flash_.command();
        const auto address = flash_.address();
        if (command == 0x05) std::printf("FLASHPOLL %llu\n", ull(sys_));
        if ((command != 0x03 && command != 0x0b) || address < journal_offset || address >= journal_offset + journal_size)
            return;
        if (address < read_start_ || address > read_next_ || sys_ - read_last_ > read_gap) {
            flush_reads();
            read_first_ = sys_;
            read_start_ = read_next_ = address;
        }
        read_next_ = std::max(read_next_, flash_.cursor());
        read_last_ = sys_;
    }

    void flush_reads() const {
        if (read_next_ == read_start_) return;
        std::printf("FLASHRD %llu %llu %06x %u\n", ull(read_first_), ull(read_last_), read_start_,
                    read_next_ - read_start_);
        read_start_ = read_next_;
    }

    void flash_sample(Vsim& dut) {
        if (flash_cs_ && !dut.flash_cs) {
            flash_closed();
            const auto address = flash_.address();
            const auto programmed = flash_.programmed_bytes;
            const auto op = flash_.deselect(sys_);
            if (op) {
                const auto bytes = flash_.programmed_bytes - programmed;
                std::printf("FLASHOP %llu %u %06x %u\n", ull(sys_), op, address, bytes);
                flash_write_at_ = sys_;
                // the bytes a page program left in the device, so a save's container is read off the log (#920,
                // save_burst.py)
                if (op == 0x02) {
                    std::string text;
                    char b[3];
                    for (std::uint32_t a = address; a < address + bytes; ++a) {
                        std::snprintf(b, sizeof b, "%02x", flash_.byte(a));
                        text += b;
                    }
                    std::printf("FLASHDATA %llu %06x %s\n", ull(sys_), address, text.c_str());
                }
            }
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
            const std::uint32_t prev_pc = last_pc_;
            last_pc_ = commit_pc(dut);
            module_ = module_of(last_pc_);
            trace_commit(prev_pc);
            if (trace_left_ && (tracing_ || (trace_from && last_pc_ == trace_from) || (trace_after_ && sys_ >= trace_after_))) {
                tracing_ = true;
                --trace_left_;
                std::printf("PC %llu %08x\n", ull(cpu_), last_pc_);
            }
            if (last_pc_ == pass_pc) pass_boundary();
            if (last_pc_ == step_pc) {
                pass_.step = true;
                pass_.aged = pass_.aged || !pass_.mbx_seen;
            }
            // A function entry a probe starts at (a test-only entry's call), by its symbol; an MRP timer's
            // expiry with its owner, read off its own argument at the entry (owner_of); an MRPDU's build with its
            // participant, read off its slot at the entry (builder_of).
            for (unsigned e = 0; e < n_entries; ++e)
                if (last_pc_ == entry_pc[e]) {
                    if (entry_owned[e])
                        std::printf("ENTRY %llu %s %s\n", ull(sys_), entry_name[e], owner_of(dut).c_str());
                    else if (entry_pc[e] == build_pc)
                        std::printf("ENTRY %llu %s %s\n", ull(sys_), entry_name[e], builder_of(dut).c_str());
                    else
                        std::printf("ENTRY %llu %s\n", ull(sys_), entry_name[e]);
                }
            note_owner(dut);
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
            pass_.mbx_seen = pass_.mbx_seen || r == MBX;
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

    // A traced call ends at the first commit of its return address, the instruction after the
    // call (prev_pc + 4: the commit before an entry is the call that reached it); its SPAN line
    // names the call's pc, so the grader can hold it to a linking call. CALL lines give each
    // entry of a called function.
    void trace_commit(std::uint32_t prev_pc) {
        for (unsigned s = 0; s < n_spans; ++s) {
            auto& open = spans_[s];
            if (open.active && last_pc_ == open.ret) {
                std::printf("SPAN %llu %llu %llu %08x %s\n", ull(open.sys), ull(open.cpu), ull(cpu_ - open.cpu),
                            open.ret - 4u, span_name[s]);
                open.active = false;
            }
            if (last_pc_ == span_pc[s]) open = {true, prev_pc + 4u, sys_, cpu_};
        }
        for (unsigned c = 0; c < n_calls; ++c)
            if (last_pc_ == call_pc[c]) std::printf("CALL %llu %llu %s\n", ull(sys_), ull(cpu_), call_name[c]);
    }

    // The MRP participants' registry (#665, PR #934): lwSRP's three timers of a participant share one argument,
    // its port's timer_arg, which mrp_app_create registers with shlan_timer_init (the LeaveAll timer's, cb
    // on_la_timer) inside msrp_app_create or mvrp_app_create; srp_mbx.c's create_participants creates an
    // interface's MSRP, then its MVRP, then publishes that interface's Domain, mbx_pub_domain(index, false, ...).
    // Each argument is bound there, at its participant's creation, to its interface and application, so a timer's
    // expiry names its owner by its own argument (a0 at the callback's entry), never by an output after it. A
    // creation that does not end in that publication of exactly one MSRP and one MVRP binds nothing (unbound).
    void note_owner(const Vsim& dut) {
        if (last_pc_ == msrp_create_pc) {
            creating_ = 1;
        } else if (last_pc_ == mvrp_create_pc) {
            creating_ = 2;
        } else if (last_pc_ == timer_init_pc && reg(dut, 11) == la_timer_pc && creating_) {
            pending_.push_back({reg(dut, 12), creating_});
        } else if (last_pc_ == pub_domain_pc && reg(dut, 11) == 0u && !pending_.empty()) {
            const std::uint32_t index = reg(dut, 10);
            const bool pair = pending_.size() == 2 && pending_[0].app != pending_[1].app && index < n_if;
            for (const auto& p : pending_) {
                std::string who = pair ? "if" + std::to_string(index) + (p.app == 1 ? " MSRP" : " MVRP") : "unbound";
                if (pair) owners_[p.arg] = who;
                else owners_.erase(p.arg);
                std::printf("PARTICIPANT %llu %08x %s\n", ull(sys_), p.arg, who.c_str());
            }
            pending_.clear();
            creating_ = 0;
        }
    }

    // A timer callback's owner, by its argument (a0): the participant the registry bound it to, or unresolved.
    std::string owner_of(const Vsim& dut) const {
        const std::uint32_t arg = reg(dut, 10);
        const auto at = owners_.find(arg);
        if (at != owners_.end()) return at->second;
        char buf[32];
        std::snprintf(buf, sizeof buf, "unresolved %08x", arg);
        return buf;
    }

    // A build's participant (#665, PR #934): srp_mbx.c's build_mrpdu(m, i, slot) builds exactly one participant's
    // MRPDU, slot 2n interface n's MSRP and 2n + 1 its MVRP (participant), its slot a2 at the entry; a slot past the
    // point's interfaces is unresolved.
    std::string builder_of(const Vsim& dut) const {
        const std::uint32_t slot = reg(dut, 12);
        if (slot / 2u < n_if) return "if" + std::to_string(slot / 2u) + (slot % 2u ? " MVRP" : " MSRP");
        char buf[32];
        std::snprintf(buf, sizeof buf, "unresolved %08x", slot);
        return buf;
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
        if (flood_gm_) flood_gm();
    }

    // flood gm 1: a grandmaster change as every pass starts, the interfaces in turn, each a new identity, so no
    // pass is without input: the event sources' contract coalesces them but sets no rate (mailbox.yaml).
    void flood_gm() {
        const unsigned i = flood_count_ % n_if;
        gm_id_.at(i) = 0x0a0b0c0dfffd0000ULL + (flood_count_ & 0xffffu);
        gm_pulse_ |= 1u << i;
        gm_dirty_ = true;
        ++flood_count_;
    }

    // The store's own cycles in the pass: its modules' (store_module).
    std::uint64_t store_cycles() const {
        std::uint64_t n = 0;
        for (unsigned m = 0; m < n_modules; ++m)
            if (store_module[m]) n += pass_.module_cycles[m];
        return n;
    }

    void finish_pass() {
        const auto cycles = cpu_ - pass_.start_cpu;
        if (pass_.step) ++step_passes_;
        if (pass_.mbx_writes == 0) {
            ++idle_count_;
            idle_max_ = std::max(idle_max_, cycles);
            idle_min_ = std::min(idle_min_, cycles);
            ++quiet_run_;
            // A pass that carries the store's step though it writes nothing to the mailbox (THE STEP, ctrl_loop.h),
            // aged=1 when the step came before the pass addressed the mailbox, as an aged step's pass takes it.
            if (pass_.step)
                std::printf("STEPPASS %llu %llu %llu %llu store=%llu aged=%u\n", ull(passes_), ull(pass_.start_sys),
                            ull(pass_.start_cpu), ull(cycles), ull(store_cycles()), unsigned(pass_.aged));
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
        // aged=1 as on a STEPPASS line: an aged step's pass writes to the mailbox once THE RETRY's round after
        // the step re-arms AECP's timer (ctrl_loop.h)
        if (pass_.step)
            text += " step=1 store=" + std::to_string(store_cycles()) + " aged=" + std::to_string(unsigned(pass_.aged));
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
        // steps <n>: n passes that carried the store's step have ended; ticks <n>: TICK records carrying n
        // centiseconds have been posted (an aged window's opening age, save_window.py).
        if (s.op == "steps") return step_passes_ - steps_mark_ >= std::stoull(s.args.at(0));
        if (s.op == "ticks") return centiseconds_ - ticks_mark_ >= std::stoull(s.args.at(0));
        if (s.op == "drained") return frames_.empty();
        // events <n>: the event ring holds at most n records the core has not released.
        if (s.op == "events") return evt_posted_ - evt_released_ / ev_words <= std::stoull(s.args.at(0));
        // flash erase|program <n>: the device has taken n of them since power on; flash idle <cycles>: a page
        // was programmed and nothing written since for that long. A save's phases start at these (save_window.py).
        if (s.op == "flash") {
            const auto& kind = s.args.at(0);
            const auto n = std::stoull(s.args.at(1));
            if (kind == "erase") return flash_.erases >= n;
            if (kind == "program") return flash_.programs >= n;
            if (kind == "idle") return flash_.programs > 0 && sys_ - flash_write_at_ >= n;
            throw std::runtime_error("unknown flash wait " + kind);
        }
        throw std::runtime_error("unknown wait " + s.op);
    }

    // reply <if> <ch> <offset>:<hex> [on=<n>] <offset>=<hex> ...: the newest frame the channel sent (on interface
    // n, if given) whose bytes at offset match, patched, queued as a received frame.
    void queue_reply(const Step& s) {
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
                    steps_mark_ = step_passes_;
                    ticks_mark_ = centiseconds_;
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
            } else if (s.op == "gptp") {
                // gptp <gm|slave> <interface>: the gPTP peer on that interface (#884), a grandmaster that
                // syncs this entity or a slave this entity syncs; both answer and send Pdelay_Req
                peer_.on = true;
                peer_.gm = s.args.at(0) == "gm";
                peer_.iface = std::stoul(s.args.at(1));
                peer_.next_sync = peer_.next_ann = peer_.next_preq = ns_now();
            } else if (s.op == "frame") {
                // frame <if> <hex> [tag]
                Frame f{unsigned(std::stoul(s.args.at(0))), {}};
                const auto& hex = s.args.at(1);
                for (std::size_t i = 0; i + 1 < hex.size(); i += 2) f.bytes.push_back(std::stoul(hex.substr(i, 2), nullptr, 16));
                if (s.args.size() > 2) f.tag = s.args[2];
                frames_.push_back(f);
            } else if (s.op == "reply") {
                queue_reply(s);
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
            } else if (s.op == "datapath") {
                // datapath <avb|asp|amap> <if>: a one-cycle pulse of the face block's change input (#894), which the
                // mailbox posts as AVB_INFO_CHANGED, AS_PATH_CHANGED or AMAP_LIVE_WRITE
                static constexpr std::array<const char*, 3> kinds = {"avb", "asp", "amap"};
                unsigned kind = 3;
                for (unsigned k = 0; k < 3; ++k) if (s.args.at(0) == kinds[k]) kind = k;
                if (kind == 3) throw std::runtime_error("unknown datapath change " + s.args.at(0));
                const unsigned i = std::stoul(s.args.at(1));
                dp_pulse_[kind] |= 1u << i;
                std::printf("DATAPATH %llu %s %u\n", ull(sys_), kinds[kind], i);
            } else if (s.op == "flood") {
                // flood gm <0|1>: a grandmaster change as every pass starts while on (flood_gm)
                if (s.args.at(0) != "gm") throw std::runtime_error("unknown flood " + s.args.at(0));
                flood_gm_ = std::stoul(s.args.at(1)) != 0;
                std::printf("FLOOD %llu gm %u %llu\n", ull(sys_), unsigned(flood_gm_), ull(flood_count_));
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
    std::uint64_t flash_write_at_ = 0;  // the last program or erase the device took
    // The journal's run of reads in progress (flash_closed): its first and last read, its first byte and the
    // byte after its last.
    static constexpr std::uint64_t read_gap = sys_hz / 1000;
    mutable std::uint64_t read_first_ = 0, read_last_ = 0;
    mutable std::uint32_t read_start_ = 0, read_next_ = 0;
    bool flood_gm_ = false;
    std::uint64_t flood_count_ = 0;
    std::uint64_t sys_ = 0, cpu_ = 0, instr_ = 0, passes_ = 0, wait_from_ = 0;
    unsigned now_ms_ = 0;
    std::uint32_t last_pc_ = 0;
    // The participants' registry (note_owner): the application being created (1 MSRP, 2 MVRP), the LeaveAll
    // timers' arguments it registered, and each bound argument's owner (`if0 MSRP`).
    struct Pending { std::uint32_t arg; unsigned app; };
    unsigned creating_ = 0;
    std::vector<Pending> pending_;
    std::map<std::uint32_t, std::string> owners_;
    struct OpenSpan { bool active; std::uint32_t ret; std::uint64_t sys, cpu; };
    std::array<OpenSpan, n_spans> spans_{};
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
    std::uint64_t evt_posted_ = 0, evt_released_ = 0;  // event records posted, words released
    std::uint32_t evt_type_ = 0, evt_count_ = 0;          // the record being posted: its type, a TICK's count
    std::uint64_t centiseconds_ = 0, ticks_mark_ = 0;      // centiseconds the TICK records posted carried
    std::uint64_t step_passes_ = 0, steps_mark_ = 0;       // passes that carried the store's step
    std::uint32_t evt_tail_ = 0;
    unsigned wire_frames_ = 0, wire_mark_ = 0;
    std::vector<std::uint8_t> egress_;
    std::array<std::deque<Sent>, n_ch> last_wire_;  // the newest frames each channel sent, with their interface
    std::deque<Frame> frames_;
    // ---- contract 2.5: the timestamp unit's model and a gPTP peer (#884, #665 F6) ----
    // The unit stamps every IEEE 802.1AS event message (messageType 0 to 3) on the gptp channel's ingress and
    // egress with this bench's time, ns; a peer frame carries the stamp the peer's link would give it.
    struct TsRec { bool egress = false, ok = true; unsigned type = 0, seq = 0; std::uint64_t ns = 0; };
    std::array<std::deque<TsRec>, n_if> ts_q_;
    std::array<bool, n_if> ts_shown_{};
    std::array<std::size_t, n_if> ts_shown_n_{};
    std::uint64_t ns_now() const { return sys_ * (1000000000ull / sys_hz); }
    void ts_note(unsigned iface, bool egress, const std::vector<std::uint8_t>& f, std::uint64_t ns) {
        if (!has_ts || iface >= n_if || f.size() < 46 || f[12] != 0x88 || f[13] != 0xF7 || (f[14] & 0x0F) > 3) return;
        ts_q_[iface].push_back({egress, true, unsigned(f[14] & 0x0F), unsigned(f[44] << 8 | f[45]), ns});
    }
    struct Peer {
        bool on = false;
        bool gm = true;
        unsigned iface = 0;
        std::uint64_t next_sync = 0, next_ann = 0, next_preq = 0;
        unsigned sync_seq = 0, ann_seq = 0, preq_seq = 0;
    } peer_;
    static constexpr std::uint64_t peer_clock = 0x02AABBFFFE000001ull;
    static constexpr std::uint64_t peer_delay_ns = 500, peer_turn_ns = 20000;
    static void be(std::vector<std::uint8_t>& f, std::size_t at, std::uint64_t v, unsigned n) {
        for (unsigned k = 0; k < n; ++k) f[at + k] = std::uint8_t(v >> (8 * (n - 1 - k)));
    }
    static void ts10(std::vector<std::uint8_t>& f, std::size_t at, std::uint64_t ns) {
        be(f, at, ns / 1000000000ull, 6);
        be(f, at + 6, ns % 1000000000ull, 4);
    }
    // a peer message: majorSdoId 1, versionPTP 2, the peer's port identity (IEEE 802.1AS-2020 10.6.2)
    static std::vector<std::uint8_t> peer_msg(unsigned type, unsigned ptp_len, unsigned seq, unsigned control,
                                              int logi) {
        std::vector<std::uint8_t> f(14 + ptp_len, 0);
        be(f, 0, 0x0180C200000Eull, 6);
        be(f, 6, 0x02AABB000001ull, 6);
        be(f, 12, 0x88F7, 2);
        f[14] = std::uint8_t(0x10 | type);
        f[15] = 0x12;
        be(f, 16, ptp_len, 2);
        be(f, 34, peer_clock, 8);
        be(f, 42, 1, 2);
        be(f, 44, seq, 2);
        f[46] = std::uint8_t(control);
        f[47] = std::uint8_t(logi);
        return f;
    }
    void peer_send(std::vector<std::uint8_t> f, std::uint64_t ts_ns) {
        frames_.push_back(Frame{peer_.iface, std::move(f), "gptp", ts_ns});
    }
    // the image launched a gPTP frame: a Pdelay_Req is answered as from a 500 ns link and a 20 us turnaround
    void peer_react(unsigned iface, const std::vector<std::uint8_t>& f, std::uint64_t t1) {
        if (!peer_.on || iface != peer_.iface || f.size() < 54 || (f[14] & 0x0F) != 0x2) return;
        const unsigned seq = unsigned(f[44] << 8 | f[45]);
        const std::uint64_t t2 = t1 + peer_delay_ns, t3 = t2 + peer_turn_ns;
        auto resp = peer_msg(0x3, 54, seq, 5, 0x7F);
        resp[20] = 0x02;   // twoStepFlag
        ts10(resp, 48, t2);
        std::copy(f.begin() + 34, f.begin() + 44, resp.begin() + 58);   // requestingPortIdentity
        peer_send(resp, t3 + peer_delay_ns);
        auto fu = peer_msg(0xA, 54, seq, 5, 0x7F);
        ts10(fu, 48, t3);
        std::copy(f.begin() + 34, f.begin() + 44, fu.begin() + 58);
        peer_send(fu, 0);
    }
    // the peer's own messages, each at its Milan v1.2 Table 4.1 interval
    void peer_tick() {
        if (!peer_.on) return;
        const std::uint64_t now = ns_now();
        if (now >= peer_.next_preq) {
            peer_.next_preq += 1000000000ull;
            peer_send(peer_msg(0x2, 54, ++peer_.preq_seq, 5, 0), now + peer_delay_ns);
        }
        if (now >= peer_.next_ann) {
            peer_.next_ann += 1000000000ull;
            auto a = peer_msg(0xB, 64 + 12, ++peer_.ann_seq, 5, 0);
            a[48 + 13] = peer_.gm ? 100 : 250;   // grandmasterPriority1: better, or worse, than the image's 248
            a[48 + 14] = 248;
            a[48 + 15] = 0x22;
            be(a, 48 + 16, 0x436A, 2);
            a[48 + 18] = 248;
            be(a, 48 + 19, peer_clock, 8);
            a[48 + 29] = 0xA0;
            be(a, 14 + 64, 0x0008, 2);
            be(a, 14 + 66, 8, 2);
            be(a, 14 + 68, peer_clock, 8);
            peer_send(a, 0);
        }
        if (peer_.gm && now >= peer_.next_sync) {
            peer_.next_sync += 125000000ull;
            auto sy = peer_msg(0x0, 44, ++peer_.sync_seq, 0, -3);
            sy[20] = 0x02;
            peer_send(sy, now + peer_delay_ns);
            auto fu = peer_msg(0x8, 76, peer_.sync_seq, 2, -3);
            ts10(fu, 48, now);
            be(fu, 58, 0x0003, 2);
            be(fu, 60, 28, 2);
            fu[62] = 0x00;
            fu[63] = 0x80;
            fu[64] = 0xC2;
            fu[67] = 1;
            peer_send(fu, 0);
        }
    }
    std::size_t offset_ = 0;
    std::uint64_t ingress_at_ = 0, gap_ = 20;
    bool tx_ready_ = true;
    unsigned link_ = 0, gm_pulse_ = 0;
    unsigned dp_pulse_[3] = {0, 0, 0};   // the datapath change pads' pulses: AVB_INFO, AS_PATH, the live map
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
    dut.mbx_avb_chg = 0;
    dut.mbx_asp_chg = 0;
    dut.mbx_amap_wr = 0;
    for (unsigned i = 0; i < n_if; ++i) set_ts(dut, i, false, false, false, 0, 0, 0);
    dut.flash_tx_ready = 0;
    dut.flash_rx_valid = 0;
    dut.eval();
}

// The split CPU runs on the bus clock (#665, owner decision 2026-10-30), so every rising edge
// of sys is a CPU edge. The test SoC has no datapath: its Milan clock pad stays low.
static_assert(cpu_hz == sys_hz, "the split CPU runs on the bus clock");

void simulate(Vsim& dut, Bench& bench) {
    std::uint64_t edge = 1;
    std::uint64_t next = 500000000000ULL / sys_hz;
    while (!Verilated::gotFinish() && !bench.done()) {
        const auto time_ps = next;
        if (time_ps > sim_limit_ps) throw std::runtime_error("simulation exceeded its time limit");
        if (time_ps <= Verilated::threadContextp()->time()) throw std::runtime_error("nonmonotonic clock");
        Verilated::threadContextp()->time(time_ps);
        if (!dut.sys_clk) {
            bench.latch_host(dut);
            bench.sample(dut);
        }
        dut.sys_clk = !dut.sys_clk;
        ++edge;
        next = edge * (500000000000ULL / sys_hz) + edge * (500000000000ULL % sys_hz) / sys_hz;
        if (edge > 128) dut.sys_reset = 0;
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
