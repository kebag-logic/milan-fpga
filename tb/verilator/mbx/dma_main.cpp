// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// dma_main.cpp - the split placement's record mover, KL_mbx_dma, on its own
// (#665, owner decision 2026-10-29): its host port answered by a model of
// KL_mbx's (one request a cycle, the answer the cycle after, a write with a
// partial strobe refused), its DMA port by an AXI4 memory with seeded random
// stalls on every channel and an address range that answers with an error,
// and the CPU's port driven as KL_mbx_wb drives it (one request, then wait
// for its answer).
//
// THE ONE DECISION THAT MATTERS: the expectations are a driver's word loop,
// written here from the mailbox contract, never read off the RTL. A receive
// transfer must leave memory as that loop's word stores would, and no byte
// past the record's length; a transmit transfer must leave the ring as the
// loop's word writes would, the lanes past the length zero; the CPU's own
// accesses must keep their answers and wait for the transfer. A monitor on
// the DMA port checks every beat against the AXI4 rules the mover claims
// (IHI0022H A3.2.1 stability, INCR bursts of four-byte beats, WLAST on the
// last beat) and against the line rule (no burst crosses 64 bytes).
//
//   D1  a receive transfer writes memory [addr, addr + len) with the ring
//       words' bytes in ring order and no other byte, at every word of a
//       line, every length to 96 bytes and the largest frame, across the
//       ring's wrap;
//   D2  a transmit transfer writes ring words index .. index + ceil(len/4)
//       with memory's bytes and the lanes past len zero, and no other word;
//   D3  every burst is INCR, four bytes a beat, at most sixteen beats, inside
//       one 64-byte line, with WLAST on its last beat only, and its payload
//       holds while VALID waits for READY;
//   D4  a CPU access made while a transfer runs waits for it, completes with
//       its own answer, and no access of the transfer comes after it;
//   D5  a start with a memory address off a word, or while a transfer runs,
//       is refused and sets ERR; the running transfer still completes;
//   D6  an error response ends the transfer at that burst and sets ERR, no
//       ring word is written from an errored beat, and the next accepted
//       start clears ERR;
//   D7  a length of 0 moves nothing and leaves ERR clear;
//   D8  a reset during a transfer leaves the mover idle, ERR clear and the
//       port the CPU's;
//   D9  every request on the host port, the CPU's and the mover's, holds its
//       address, direction and data through the cycle of its answer, as
//       KL_mbx_wb presents one (an observer reads the fields at the answer),
//       and a line's sixteen ring reads still end within 32 cycles.

#include <algorithm>
#include <cstdint>
#include <cstdio>
#include <deque>
#include <string>
#include <vector>

#include "../../common/verilator_harness.hpp"
#include "VKL_mbx_dma.h"
#include "verilated.h"

namespace {

constexpr std::uint32_t kWindowWords = 1u << 13;   // MBX_ADDR_W_C = 13
constexpr std::uint32_t kMemBase = 0x10000000u;
constexpr std::uint32_t kMemBytes = 0x4000u;
constexpr std::uint32_t kErrBase = 0x10003000u;    // a range of memory that answers SLVERR
constexpr std::uint32_t kErrBytes = 0x40u;     // one line

//! A small deterministic generator, so a failure replays exactly.
struct Rng {
    std::uint32_t s;
    std::uint32_t next() {
        s ^= s << 13;
        s ^= s >> 17;
        s ^= s << 5;
        return s;
    }
    bool chance(unsigned percent) { return next() % 100u < percent; }
};

struct Access {
    bool cpu;
    bool we;
    std::uint32_t addr;
    std::uint32_t data;
};

class Bench {
 public:
    Bench(VKL_mbx_dma* dut, milan::tb::Checker& check) : d_(dut), check_(check) {}

    std::vector<std::uint32_t> ring = std::vector<std::uint32_t>(kWindowWords, 0);
    std::vector<std::uint8_t> mem = std::vector<std::uint8_t>(kMemBytes, 0);
    std::vector<Access> log;       // every host-port access, in order
    unsigned stall = 0;            // percent of cycles each AXI channel stalls
    unsigned refused = 0;          // host writes with a partial strobe
    unsigned bursts = 0;
    std::uint64_t cycles = 0;
    std::vector<std::uint64_t> read_cycles;   // the cycle of each ring read of the mover's
    Rng rng{0x2545F491u};

    void reset() {
        d_->rst_n = 0;
        idle();
        for (int i = 0; i < 4; ++i) step();
        d_->rst_n = 1;
        step();
    }

    //! One clock: drive this cycle's inputs from the models, sample the
    //! outputs (which may depend on them), then rise.
    void step() {
        d_->host_ack_i = ack_next_ ? 1 : 0;
        d_->host_rdata_i = rdata_next_;
        drive_axi();
        d_->clk_i = 0;
        d_->eval();
        cpu_ack_ = d_->cpu_ack_o != 0;
        cpu_rdata_ = d_->cpu_rdata_o;
        sample_host();
        sample_axi();
        d_->clk_i = 1;
        d_->eval();
        d_->start_p_i = 0;
        d_->cpu_req_i = 0;
        ++cycles;
    }

    void idle() {
        d_->start_p_i = 0;
        d_->cpu_req_i = 0;
        d_->cpu_we_i = 0;
        d_->cpu_addr_i = 0;
        d_->cpu_wdata_i = 0;
        d_->cpu_be_i = 0;
        d_->axi_awready_i = 0;
        d_->axi_wready_i = 0;
        d_->axi_bvalid_i = 0;
        d_->axi_arready_i = 0;
        d_->axi_rvalid_i = 0;
        ack_next_ = false;
        aw_q_.clear();
        b_q_.clear();
        r_q_.clear();
    }

    //! Set the operands and pulse START for one cycle.
    void start(std::uint32_t base, std::uint32_t mask, std::uint32_t index, std::uint32_t addr, std::uint32_t len,
               bool to_ring) {
        d_->ring_base_i = base;
        d_->ring_mask_i = mask;
        d_->ring_index_i = index;
        d_->mem_addr_i = addr;
        d_->len_bytes_i = len;
        d_->to_ring_i = to_ring ? 1 : 0;
        d_->start_p_i = 1;
    }

    //! Run until the mover is idle; false on a timeout.
    bool wait_idle(unsigned limit = 20000) {
        step();
        for (unsigned i = 0; i < limit; ++i) {
            if (!d_->busy_o) return true;
            step();
        }
        return false;
    }

    //! A CPU access as KL_mbx_wb makes it: one request, then its answer.
    //! Returns the read data, or ~0 on a timeout.
    std::uint32_t cpu(bool we, std::uint32_t addr, std::uint32_t data, unsigned limit = 20000) {
        d_->cpu_req_i = 1;
        d_->cpu_we_i = we ? 1 : 0;
        d_->cpu_addr_i = addr;
        d_->cpu_wdata_i = data;
        d_->cpu_be_i = 0xF;
        for (unsigned i = 0; i < limit; ++i) {
            step();
            if (cpu_ack_) return cpu_rdata_;
        }
        check_.fail("D4 a CPU access is answered");
        return ~0u;
    }

    bool busy() const { return d_->busy_o != 0; }
    bool err() const { return d_->err_o != 0; }
    VKL_mbx_dma* dut() { return d_; }

 private:
    struct Burst {
        std::uint32_t addr;
        unsigned beats;
        unsigned done = 0;
        bool error = false;
    };

    void sample_host() {
        if (prev_req_) {
            check_.that("D9 a request's address holds through its answer", d_->host_addr_o == prev_addr_);
            check_.that("D9 a request's direction holds through its answer", (d_->host_we_o != 0) == prev_we_);
            if (prev_we_) check_.that("D9 a write's data holds through its answer", d_->host_wdata_o == prev_wdata_);
        }
        prev_req_ = d_->host_req_o != 0;
        prev_addr_ = d_->host_addr_o;
        prev_we_ = d_->host_we_o != 0;
        prev_wdata_ = d_->host_wdata_o;
        ack_next_ = false;
        if (!d_->host_req_o) return;
        const std::uint32_t addr = d_->host_addr_o;
        const bool we = d_->host_we_o != 0;
        // the CPU's requests are the ones the mover passes or holds; a ring access of the mover's is not
        const bool cpu = !d_->busy_o;
        log.push_back({cpu, we, addr, we ? static_cast<std::uint32_t>(d_->host_wdata_o) : 0u});
        if (!cpu && !we) read_cycles.push_back(cycles);
        if (we) {
            if (d_->host_be_o == 0xF) {
                ring[addr] = d_->host_wdata_o;
            } else {
                ++refused;
            }
            rdata_next_ = 0;
        } else {
            rdata_next_ = ring[addr];
        }
        ack_next_ = true;
    }

    bool in_mem(std::uint32_t a) const { return a >= kMemBase && a < kMemBase + kMemBytes; }
    bool in_err(std::uint32_t a) const { return a >= kErrBase && a < kErrBase + kErrBytes; }

    void check_burst(std::uint32_t addr, unsigned len, unsigned size, unsigned burst) {
        ++bursts;
        check_.that("D3 a burst is INCR", burst == 1);
        check_.that("D3 a burst's beats are four bytes", size == 2);
        check_.that("D3 a burst is at most sixteen beats", len <= 15);
        check_.that("D3 a burst starts on a word", (addr & 3u) == 0);
        check_.that("D3 a burst stays inside one 64-byte line", (addr >> 6) == ((addr + 4u * len) >> 6));
    }

    void drive_axi() {
        d_->axi_awready_i = !rng.chance(stall);
        d_->axi_arready_i = !rng.chance(stall);
        d_->axi_wready_i = (!aw_q_.empty() && !rng.chance(stall)) ? 1 : 0;
        d_->axi_bvalid_i = (!b_q_.empty() && !rng.chance(stall)) ? 1 : 0;
        d_->axi_bresp_i = b_q_.empty() ? 0 : (b_q_.front() ? 2 : 0);
        d_->axi_bid_i = 0;
        if (!r_q_.empty() && !rng.chance(stall)) {
            Burst& r = r_q_.front();
            const std::uint32_t a = r.addr + 4u * r.done;
            std::uint32_t word = 0;
            const bool bad = !in_mem(a) || in_err(a);
            if (!bad) {
                for (unsigned k = 0; k < 4; ++k) word |= std::uint32_t(mem[a - kMemBase + k]) << (8 * k);
            }
            d_->axi_rvalid_i = 1;
            d_->axi_rdata_i = word;
            d_->axi_rresp_i = bad ? 2 : 0;
            d_->axi_rlast_i = (r.done + 1 == r.beats) ? 1 : 0;
        } else {
            d_->axi_rvalid_i = 0;
            d_->axi_rlast_i = 0;
        }
        d_->axi_rid_i = 0;
    }

    void sample_axi() {
        // A3.2.1: a VALID that waits holds its payload.
        if (aw_wait_) {
            check_.that("D3 AWVALID holds until AWREADY", d_->axi_awvalid_o);
            check_.that("D3 the write address holds while it waits",
                        d_->axi_awaddr_o == aw_addr_ && d_->axi_awlen_o == aw_len_);
        }
        if (w_wait_) {
            check_.that("D3 WVALID holds until WREADY", d_->axi_wvalid_o);
            check_.that("D3 the write data holds while it waits",
                        d_->axi_wdata_o == w_data_ && d_->axi_wstrb_o == w_strb_ && d_->axi_wlast_o == w_last_);
        }
        if (ar_wait_) {
            check_.that("D3 ARVALID holds until ARREADY", d_->axi_arvalid_o);
            check_.that("D3 the read address holds while it waits",
                        d_->axi_araddr_o == ar_addr_ && d_->axi_arlen_o == ar_len_);
        }
        aw_wait_ = d_->axi_awvalid_o && !d_->axi_awready_i;
        aw_addr_ = d_->axi_awaddr_o;
        aw_len_ = d_->axi_awlen_o;
        w_wait_ = d_->axi_wvalid_o && !d_->axi_wready_i;
        w_data_ = d_->axi_wdata_o;
        w_strb_ = d_->axi_wstrb_o;
        w_last_ = d_->axi_wlast_o;
        ar_wait_ = d_->axi_arvalid_o && !d_->axi_arready_i;
        ar_addr_ = d_->axi_araddr_o;
        ar_len_ = d_->axi_arlen_o;

        if (d_->axi_awvalid_o && d_->axi_awready_i) {
            check_burst(d_->axi_awaddr_o, d_->axi_awlen_o, d_->axi_awsize_o, d_->axi_awburst_o);
            check_.that("D3 one burst in flight", aw_q_.empty() && b_q_.empty() && r_q_.empty());
            aw_q_.push_back({static_cast<std::uint32_t>(d_->axi_awaddr_o), d_->axi_awlen_o + 1u});
        }
        if (d_->axi_wvalid_o && d_->axi_wready_i) {
            Burst& w = aw_q_.front();
            const std::uint32_t a = w.addr + 4u * w.done;
            const bool last = (w.done + 1 == w.beats);
            check_.that("D3 WLAST marks a burst's last beat only", (d_->axi_wlast_o != 0) == last);
            if (!in_mem(a) || in_err(a)) {
                w.error = true;
            } else {
                for (unsigned k = 0; k < 4; ++k) {
                    if (d_->axi_wstrb_o & (1u << k)) mem[a - kMemBase + k] = std::uint8_t(d_->axi_wdata_o >> (8 * k));
                }
            }
            ++w.done;
            if (last) {
                b_q_.push_back(w.error);
                aw_q_.pop_front();
            }
        }
        if (d_->axi_bvalid_i && d_->axi_bready_o) b_q_.pop_front();
        if (d_->axi_arvalid_o && d_->axi_arready_i) {
            check_burst(d_->axi_araddr_o, d_->axi_arlen_o, d_->axi_arsize_o, d_->axi_arburst_o);
            check_.that("D3 one burst in flight", aw_q_.empty() && b_q_.empty() && r_q_.empty());
            r_q_.push_back({static_cast<std::uint32_t>(d_->axi_araddr_o), d_->axi_arlen_o + 1u});
        }
        if (d_->axi_rvalid_i && d_->axi_rready_o) {
            Burst& r = r_q_.front();
            if (++r.done == r.beats) r_q_.pop_front();
        }
    }

    VKL_mbx_dma* d_;
    milan::tb::Checker& check_;
    bool cpu_ack_ = false;          // cpu_ack_o in the cycle just stepped
    bool prev_req_ = false;         // a host request in the cycle before, and its fields
    bool prev_we_ = false;
    std::uint32_t prev_addr_ = 0, prev_wdata_ = 0;
    std::uint32_t cpu_rdata_ = 0;
    bool ack_next_ = false;
    std::uint32_t rdata_next_ = 0;
    std::deque<Burst> aw_q_, r_q_;
    std::deque<bool> b_q_;
    bool aw_wait_ = false, w_wait_ = false, ar_wait_ = false;
    std::uint32_t aw_addr_ = 0, w_data_ = 0, ar_addr_ = 0;
    unsigned aw_len_ = 0, w_strb_ = 0, w_last_ = 0, ar_len_ = 0;
};

std::uint8_t pattern(std::uint32_t i) { return static_cast<std::uint8_t>(0x5Au ^ (i * 29u + (i >> 5))); }

//! The ring as a driver's receive loop reads it: byte k of the record in word
//! index + k/4 at bits 8*(k%4).
std::uint8_t ring_byte(const Bench& b, std::uint32_t base, std::uint32_t mask, std::uint32_t index, std::uint32_t k) {
    const std::uint32_t word = b.ring[base + ((index + k / 4u) & mask)];
    return static_cast<std::uint8_t>(word >> (8u * (k % 4u)));
}

constexpr std::uint32_t kBase = 0x400;   // the AECP receive ring: 0x1000 bytes in, 512 words
constexpr std::uint32_t kMask = 511;
constexpr std::uint8_t kGuard = 0xEE;

void receive_case(Bench& b, milan::tb::Checker& check, std::uint32_t addr, std::uint32_t len, std::uint32_t index,
                  const char* tag) {
    for (std::uint32_t w = 0; w <= kMask; ++w) {
        b.ring[kBase + w] = 0;
        for (unsigned k = 0; k < 4; ++k) b.ring[kBase + w] |= std::uint32_t(pattern(w * 4 + k + len)) << (8 * k);
    }
    std::fill(b.mem.begin(), b.mem.end(), kGuard);
    b.start(kBase, kMask, index, addr, len, false);
    if (!check.that((std::string("D1 a receive transfer ends, ") + tag).c_str(), b.wait_idle())) return;
    check.that((std::string("D1 a receive transfer sets no ERR, ") + tag).c_str(), !b.err());
    bool exact = true, outside = true;
    for (std::uint32_t i = 0; i < kMemBytes; ++i) {
        const std::uint32_t a = kMemBase + i;
        if (a >= addr && a < addr + len) {
            exact = exact && b.mem[i] == ring_byte(b, kBase, kMask, index, a - addr);
        } else {
            outside = outside && b.mem[i] == kGuard;
        }
    }
    check.that((std::string("D1 memory holds the record's bytes in ring order, ") + tag).c_str(), exact);
    check.that((std::string("D1 no byte outside [addr, addr + len) is written, ") + tag).c_str(), outside);
}

void transmit_case(Bench& b, milan::tb::Checker& check, std::uint32_t addr, std::uint32_t len, std::uint32_t index,
                   const char* tag) {
    for (std::uint32_t i = 0; i < kMemBytes; ++i) b.mem[i] = pattern(i + len);
    std::vector<std::uint32_t> before = b.ring;
    for (std::uint32_t w = 0; w <= kMask; ++w) b.ring[kBase + w] = 0xDEADBEEFu;
    before = b.ring;
    b.start(kBase, kMask, index, addr, len, true);
    if (!check.that((std::string("D2 a transmit transfer ends, ") + tag).c_str(), b.wait_idle())) return;
    check.that((std::string("D2 a transmit transfer sets no ERR, ") + tag).c_str(), !b.err());
    const std::uint32_t words = (len + 3u) / 4u;
    bool exact = true, others = true;
    for (std::uint32_t w = 0; w <= kMask; ++w) {
        const std::uint32_t k = (w - index) & kMask;   // the record's word k, if k < words
        if (k < words) {
            std::uint32_t want = 0;
            for (unsigned lane = 0; lane < 4; ++lane) {
                const std::uint32_t byte = 4u * k + lane;
                if (byte < len) want |= std::uint32_t(b.mem[addr - kMemBase + byte]) << (8 * lane);
            }
            exact = exact && b.ring[kBase + w] == want;
        } else {
            others = others && b.ring[kBase + w] == before[kBase + w];
        }
    }
    check.that((std::string("D2 the ring holds the record's words, the lanes past len zero, ") + tag).c_str(), exact);
    check.that((std::string("D2 no other ring word is written, ") + tag).c_str(), others);
    check.that("D2 no ring write has a partial strobe", b.refused == 0);
}

void shapes(Bench& b, milan::tb::Checker& check) {
    // every word of a line, every length to 96 bytes, and the largest frame; the index near the wrap
    for (unsigned stall : {0u, 30u}) {
        b.stall = stall;
        for (std::uint32_t off = 0; off < 64; off += 4) {
            for (std::uint32_t len = 1; len <= 96; ++len) {
                const std::uint32_t index = (kMask - 3u + off / 4u + len) & 0xFFFFu;
                char tag[96];
                std::snprintf(tag, sizeof tag, "line word %u, %u bytes, index %u, stall %u%%", off / 4, len, index,
                              stall);
                receive_case(b, check, kMemBase + 0x100 + off, len, index, tag);
                transmit_case(b, check, kMemBase + 0x900 + off, len, index, tag);
            }
        }
        for (std::uint32_t len : {1514u, 1513u, 1512u}) {
            char tag[64];
            std::snprintf(tag, sizeof tag, "%u bytes, stall %u%%", len, stall);
            receive_case(b, check, kMemBase + 0x204, len, 0xFFF0u, tag);
            transmit_case(b, check, kMemBase + 0x1004, len, 0x01F8u, tag);
        }
    }
    b.stall = 0;
}

//! The log's CPU access is its last, and its only one.
bool last_is_cpu(const Bench& b) {
    std::size_t cpu = 0;
    for (const Access& a : b.log) cpu += a.cpu ? 1u : 0u;
    return cpu == 1 && !b.log.empty() && b.log.back().cpu;
}

void cpu_waits(Bench& b, milan::tb::Checker& check) {
    // a CPU read and a CPU write made while a long transfer runs
    for (bool to_ring : {false, true}) {
        b.ring[5] = 0x12345678u;
        b.log.clear();
        b.start(kBase, kMask, 7, kMemBase + 0x200, 400, to_ring);
        b.step();
        b.step();
        check.that("D4 the transfer is running", b.busy());
        const std::uint32_t got = b.cpu(false, 5, 0);
        check.that("D4 a CPU read held for a transfer gets its own word", got == 0x12345678u);
        check.that("D4 a CPU access held for a transfer completes after it", !b.busy());
        check.that("D4 no access of a transfer comes after the CPU's held one", last_is_cpu(b));
        b.log.clear();
        b.start(kBase, kMask, 9, kMemBase + 0x200, 300, to_ring);
        b.step();
        b.cpu(true, 6, 0xCAFEF00Du);
        check.that("D4 a CPU write held for a transfer lands", b.ring[6] == 0xCAFEF00Du);
        check.that("D4 no access of a transfer comes after the CPU's held one", last_is_cpu(b));
    }
    // a CPU access in the cycle a transfer starts goes first
    b.ring[3] = 0x0BADF00Du;
    b.start(kBase, kMask, 0, kMemBase + 0x100, 64, false);
    const std::uint32_t got = b.cpu(false, 3, 0);
    check.that("D4 a CPU read in the cycle a transfer starts gets its own word", got == 0x0BADF00Du);
    check.that("D4 that transfer still ends", b.wait_idle());
}

void refusals(Bench& b, milan::tb::Checker& check) {
    std::fill(b.mem.begin(), b.mem.end(), kGuard);
    b.log.clear();
    for (std::uint32_t mis : {1u, 2u, 3u}) {
        b.start(kBase, kMask, 0, kMemBase + 0x100 + mis, 16, false);
        b.step();
        check.that("D5 a start off a word is refused: no transfer runs", !b.busy());
        check.that("D5 a start off a word sets ERR", b.err());
    }
    check.that("D5 a refused start moves nothing", b.log.empty() && b.mem[0x100] == kGuard);
    // a start while a transfer runs: refused, the running one completes as asked
    for (std::uint32_t w = 0; w <= kMask; ++w) b.ring[kBase + w] = 0x01010101u * (w & 0xFFu);
    b.start(kBase, kMask, 0, kMemBase + 0x400, 200, false);
    b.step();
    b.step();
    b.start(kBase, kMask, 100, kMemBase + 0x800, 40, false);
    check.that("D5 the running transfer ends", b.wait_idle());
    check.that("D5 a start while a transfer runs sets ERR", b.err());
    bool kept = true;
    for (std::uint32_t k = 0; k < 200; ++k) {
        kept = kept && b.mem[0x400 + k] == ring_byte(b, kBase, kMask, 0, k);
    }
    check.that("D5 the running transfer still completes as asked", kept);
    check.that("D5 the refused start moved nothing", b.mem[0x800] == kGuard);
    // D7: a length of 0 moves nothing, ERR clear
    b.log.clear();
    b.start(kBase, kMask, 0, kMemBase + 0x100, 0, false);
    b.step();
    check.that("D7 a length of 0 runs no transfer", !b.busy() && b.log.empty());
    check.that("D7 a length of 0 clears ERR", !b.err());
}

void errors(Bench& b, milan::tb::Checker& check) {
    // receive: the third chunk's line answers SLVERR
    std::fill(b.mem.begin(), b.mem.end(), kGuard);
    b.start(kBase, kMask, 0, kErrBase - 128, 400, false);
    check.that("D6 a receive transfer with an error response ends", b.wait_idle());
    check.that("D6 a write error response sets ERR", b.err());
    check.that("D6 the transfer stops at the errored burst",
               b.mem[kErrBase - kMemBase + 64] == kGuard && b.mem[kErrBase - kMemBase + 128] == kGuard);
    // the next accepted start clears it
    b.start(kBase, kMask, 0, kMemBase + 0x100, 8, false);
    check.that("D6 a later transfer ends", b.wait_idle());
    check.that("D6 the next accepted start clears ERR", !b.err());
    // transmit: an errored read burst writes no ring word from its errored beats, and nothing after
    for (std::uint32_t w = 0; w <= kMask; ++w) b.ring[kBase + w] = 0xDEADBEEFu;
    b.start(kBase, kMask, 0, kErrBase - 64, 300, true);
    check.that("D6 a transmit transfer with an error response ends", b.wait_idle());
    check.that("D6 a read error response sets ERR", b.err());
    bool good = true, none = true;
    for (std::uint32_t k = 0; k < 16; ++k) {
        std::uint32_t want = 0;
        for (unsigned lane = 0; lane < 4; ++lane) want |= std::uint32_t(b.mem[kErrBase - 64 - kMemBase + 4 * k + lane]) << (8 * lane);
        good = good && b.ring[kBase + k] == want;
    }
    for (std::uint32_t k = 16; k < 75; ++k) none = none && b.ring[kBase + k] == 0xDEADBEEFu;
    check.that("D6 the words before the errored burst are written", good);
    check.that("D6 no ring word is written from an errored beat or after it", none);
}

void reset_during(Bench& b, milan::tb::Checker& check) {
    b.ring[2] = 0x77777777u;
    b.start(kBase, kMask, 0, kMemBase + 0x100, 600, true);
    for (int i = 0; i < 20; ++i) b.step();
    check.that("D8 the transfer is running before the reset", b.busy());
    b.reset();
    check.that("D8 a reset leaves the mover idle", !b.busy());
    check.that("D8 a reset clears ERR", !b.err());
    check.that("D8 after a reset the port is the CPU's", b.cpu(false, 2, 0) == 0x77777777u);
}

void back_to_back(Bench& b, milan::tb::Checker& check) {
    b.stall = 0;
    b.read_cycles.clear();
    b.start(kBase, kMask, 0, kMemBase + 0x100, 64, false);
    check.that("D9 the transfer ends", b.wait_idle());
    const bool sixteen = b.read_cycles.size() == 16;
    check.that("D9 a line's sixteen ring reads end within 32 cycles",
               sixteen && b.read_cycles.back() - b.read_cycles.front() < 32);
}

}  // namespace

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    const milan::tb::Model<VKL_mbx_dma> model;
    milan::tb::Checker check{"mbx record mover (KL_mbx_dma)"};
    Bench b(model.get(), check);
    b.reset();
    shapes(b, check);
    cpu_waits(b, check);
    refusals(b, check);
    errors(b, check);
    reset_during(b, check);
    back_to_back(b, check);
    std::printf("bursts %u, cycles %llu\n", b.bursts, static_cast<unsigned long long>(b.cycles));
    return check.report();
}
