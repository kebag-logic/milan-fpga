// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// twin_split.cpp - the two-placement simulation's split half (#665).
//
// tb_split_top: KL_mbx on the mailbox clock, KL_mbx_cdc and the two byte
// crossings, and milan_datapath at CTRL_SPLIT_P = 1, the shipping shape. The
// control firmware is the split image's own platform (sw/firmware/ctrl/plat,
// ctrl_plat.c's boot and composition), built for the host by twin_fw.py, as
// tb/verilator/mbx's co-simulation runs the firmware on the RTL mailbox:
//   - mbx_hal.h is KL_mbx's host port, one request a mailbox clock;
//   - ctrl_plat_io.h's CSR window is the datapath's AXI4-Lite port, its UART a
//     sink that is always empty and never full;
//   - F1's flash is the store's host flash model, blank, as test_plat_boot.cpp
//     gives it.
// The modeled millisecond is one KL_mbx millisecond tick: the bench pulses
// ms_tick_p_i, lets the mailbox and the datapath run, and services the loop
// until it reports nothing owed, so the firmware is never late against its
// own clock. MAAP's first range is pinned at twin::kMaapPreferred, compiled
// in by twin_fw.py (CTRL_PLAT_MAAP_PREFERRED, simulation only).
//
// Every control frame the datapath's MAC sends is captured with the
// millisecond it left at into the capture file twin_compare.py reads. With
// --plant NAME the capture is planted before it is written, so the comparison
// must refuse it (twin_compare.py names each plant's words):
//   byte-flip            one byte of the second ADPDU's payload inverted
//   srp-plus-k           the first MSRP Talker vector's FirstValue one higher
//   missing-notification the first unsolicited AECP response after the
//                        STOP_STREAMING response dropped
//
//   Vmilan_dp_twin_sp <capture.json> [--plant NAME]

#include <cstdint>
#include <cstdio>
#include <cstring>
#include <deque>
#include <memory>
#include <stdexcept>
#include <string>
#include <vector>

#include "Vtb_split_top.h"
#include "verilated.h"

#include "srp_entity_gen.h"
#include "ctrl_plat.h"
#include "ctrl_plat_policy_gen.h"
#include "mbx_hal.h"
extern "C" {
#include "nvm_fmodel.h"
}
// the store's headers carry no extern "C", and its shape header asserts in C11's spelling
#define _Static_assert static_assert
extern "C" {
#include "nvm_store.h"
}
#undef _Static_assert
#include "twin.hpp"

namespace {

constexpr std::uintptr_t kCsr = 0x90000000u;
constexpr std::uintptr_t kUart = 0xf0001000u;
constexpr ctrl_plat_uart kUartRegs = {kUart + 0x0u, kUart + 0x4u, kUart + 0x8u, kUart + 0x10u};
constexpr unsigned kGuard = 4096;
//! Mailbox clocks the bench runs after each tick before it services the loop,
//! and the most service passes one millisecond takes.
constexpr unsigned kSettle = 64;
constexpr unsigned kPasses = 400;

class SplitHalf {
 public:
    explicit SplitHalf(Vtb_split_top* d) : d_(d) {}

    void reset();
    std::uint32_t host(std::uint32_t byte_off, bool we, std::uint32_t v);
    void axi_write(std::uint16_t addr, std::uint32_t value);
    std::uint32_t axi_read(std::uint16_t addr);
    void sys(std::uint64_t n);
    void tick_ms();
    void mac_rx(const twin::Frame& f) { rx_q_.push_back(f); }
    bool quiet() const { return rx_q_.empty() && tx_cur_.empty(); }
    std::uint32_t ms() const { return ms_; }
    void capture(twin::Capture* cap) { cap_ = cap; }
    unsigned host_timeouts() const { return host_timeouts_; }
    std::string& console() { return console_; }

 private:
    struct Fires {
        bool aw = false;
        bool w = false;
        bool b = false;
        bool ar = false;
        bool r = false;
        std::uint32_t data = 0;
    };

    void unit();
    void dp_edge();
    void dp_cycles(unsigned n);
    void rx_drive();
    void tx_take();

    Vtb_split_top* d_;
    std::uint64_t u_ = 0;
    std::uint64_t dp_ = 0;
    std::uint32_t ms_ = 0;
    Fires fires_{};
    bool rx_fire_ = false;
    std::deque<twin::Frame> rx_q_;
    std::size_t rx_off_ = 0;
    twin::Frame tx_cur_;
    twin::Capture* cap_ = nullptr;
    unsigned host_timeouts_ = 0;
    std::string console_;
};

//! One time unit: the mailbox clock toggles every second unit (period 4),
//! the datapath's every fourth, offset by one (period 8), as sim_split.cpp.
void SplitHalf::unit() {
    ++u_;
    if (u_ % 2 == 0) {
        const bool rising = !d_->sys_clk;
        d_->sys_clk = rising;
        d_->eval();
        if (rising) d_->ms_tick_p_i = 0;
    } else if (u_ % 4 == 1) {
        const bool rising = !d_->dp_clk;
        if (rising) dp_edge();
        d_->dp_clk = rising;
        d_->eval();
        if (rising) {
            ++dp_;
            if (rx_fire_) {
                rx_off_ += 8;
                if (rx_off_ >= rx_q_.front().size()) {
                    rx_q_.pop_front();
                    rx_off_ = 0;
                }
            }
            rx_drive();
            d_->eval();
        }
    }
}

//! What the datapath clock's rising edge takes: every handshake as it stands before it.
void SplitHalf::dp_edge() {
    rx_fire_ = d_->rx_tvalid && d_->rx_tready;
    fires_.aw = d_->s_axi_awvalid && d_->s_axi_awready;
    fires_.w = d_->s_axi_wvalid && d_->s_axi_wready;
    fires_.b = d_->s_axi_bvalid && d_->s_axi_bready;
    fires_.ar = d_->s_axi_arvalid && d_->s_axi_arready;
    fires_.r = d_->s_axi_rvalid && d_->s_axi_rready;
    fires_.data = d_->s_axi_rdata;
    tx_take();
}

void SplitHalf::rx_drive() {
    const bool busy = !rx_q_.empty();
    const twin::Frame* f = busy ? &rx_q_.front() : nullptr;
    std::uint64_t data = 0;
    std::uint32_t keep = 0;
    for (std::size_t i = 0; busy && i < 8 && rx_off_ + i < f->size(); ++i) {
        data |= static_cast<std::uint64_t>((*f)[rx_off_ + i]) << (8 * i);
        keep |= 1u << i;
    }
    d_->rx_tvalid = busy;
    d_->rx_tlast = busy && rx_off_ + 8 >= f->size();
    d_->rx_tdata = data;
    d_->rx_tkeep = keep;
}

void SplitHalf::tx_take() {
    if (!d_->tx_tvalid || !d_->tx_tready) return;
    for (unsigned i = 0; i < 8; ++i)
        if (d_->tx_tkeep & (1u << i)) tx_cur_.push_back(static_cast<std::uint8_t>(d_->tx_tdata >> (8 * i)));
    if (!d_->tx_tlast) return;
    twin::Frame answer;
    const char* who = nullptr;
    if (cap_ != nullptr && twin::is_control(tx_cur_)) {
        cap_->frames.push_back({ms_, tx_cur_});
        if (twin::controller_available_answer(tx_cur_, &answer, &who)) {
            rx_q_.push_back(answer);
            cap_->applied.push_back({ms_, who, answer});
        }
    } else if (cap_ != nullptr) {
        cap_->stream_frame(ms_);
    }
    tx_cur_.clear();
}

void SplitHalf::dp_cycles(unsigned n) {
    const std::uint64_t until = dp_ + n;
    while (dp_ < until) unit();
}

void SplitHalf::sys(std::uint64_t n) {
    // a mailbox clock is two units, so n of them are 4n units
    for (std::uint64_t k = 0; k < 4 * n; ++k) unit();
}

void SplitHalf::reset() {
    d_->sys_rst_n = 0;
    d_->dp_rst_n = 0;
    d_->host_req_i = 0;
    d_->rx_tvalid = 0;
    d_->tx_tready = 1;
    d_->link_up = 1;
    d_->s_axi_awvalid = 0;
    d_->s_axi_wvalid = 0;
    d_->s_axi_arvalid = 0;
    d_->s_axi_bready = 0;
    d_->s_axi_rready = 0;
    // tb_split_top's second KL_ctrl_split, the split leg's tap, idle here
    d_->tap_tvalid = 0;
    d_->tap_ready = 1;
    sys(20);
    d_->sys_rst_n = 1;
    d_->dp_rst_n = 1;
    sys(20);
}

//! One KL_mbx host access: the request for one mailbox clock, then the clock its ack arrives.
std::uint32_t SplitHalf::host(std::uint32_t byte_off, bool we, std::uint32_t v) {
    d_->host_req_i = 1;
    d_->host_we_i = we;
    d_->host_addr_i = byte_off / 4u;
    d_->host_wdata_i = v;
    d_->host_be_i = 0xF;
    sys(1);
    d_->host_req_i = 0;
    d_->host_we_i = 0;
    for (int i = 0; i < 8; ++i) {
        if (d_->host_ack_o) {
            const std::uint32_t r = d_->host_rdata_o;
            sys(1);
            return r;
        }
        sys(1);
    }
    ++host_timeouts_;
    return 0;
}

void SplitHalf::axi_write(std::uint16_t addr, std::uint32_t value) {
    d_->s_axi_awaddr = addr;
    d_->s_axi_awvalid = 1;
    d_->s_axi_wdata = value;
    d_->s_axi_wstrb = 0xF;
    d_->s_axi_wvalid = 1;
    d_->s_axi_bready = 1;
    for (unsigned g = 0; g < kGuard; ++g) {
        dp_cycles(1);
        if (fires_.aw) d_->s_axi_awvalid = 0;
        if (fires_.w) d_->s_axi_wvalid = 0;
        if (fires_.b) {
            d_->s_axi_bready = 0;
            return;
        }
    }
    throw std::runtime_error("AXI write response timeout");
}

std::uint32_t SplitHalf::axi_read(std::uint16_t addr) {
    d_->s_axi_araddr = addr;
    d_->s_axi_arvalid = 1;
    d_->s_axi_rready = 1;
    for (unsigned g = 0; g < kGuard; ++g) {
        dp_cycles(1);
        if (fires_.ar) d_->s_axi_arvalid = 0;
        if (fires_.r) {
            d_->s_axi_rready = 0;
            return fires_.data;
        }
    }
    throw std::runtime_error("AXI read response timeout");
}

void SplitHalf::tick_ms() {
    d_->ms_tick_p_i = 1;
    sys(1);
    ++ms_;
    nvm_fmodel_advance_us(1000);
}

//! The half the HAL calls reach: the one instance main() makes.
SplitHalf*& current() {
    static SplitHalf* half = nullptr;
    return half;
}

//! The platform's environment, as test_plat_boot.cpp's SetUp() builds it.
struct Env {
    ctrl_plat_policy policy = CTRL_PLAT_POLICY_INIT;
    ctrl_plat_stream streams[CTRL_SRP_SOURCES] = CTRL_PLAT_STREAMS_INIT;
    nvm_flash flash{};
    ctrl_plat_env env{};

    Env() {
        nvm_fmodel_blank();
        nvm_fmodel_power_on();
        nvm_fmodel_window(NVM_SLOT_A, NVM_SLOT_B + NVM_SLOT_BYTES);
        nvm_fmodel_times(1000, 100);
        flash = nvm_fmodel_port;
        env.flash = &flash;
        env.csr = kCsr;
        env.uart = kUartRegs;
        env.policy = &policy;
        env.streams = streams;
        env.aaf_outputs = CTRL_PLAT_AAF_OUTPUTS;
        env.crf_output = CTRL_PLAT_CRF_OUTPUT;
        env.link_rate_bps = CTRL_PLAT_LINK_BPS;
        ctrl_plat_generated_image(&env);
    }
};

//! One modeled millisecond: the stimulus due, the tick, the settle, then the
//! loop serviced until nothing is owed and the MAC has gone quiet.
void millisecond(SplitHalf& half, const std::vector<twin::Stimulus>& stim, std::size_t* next,
                 twin::Capture* cap) {
    while (*next < stim.size() && stim[*next].ms <= half.ms()) {
        half.mac_rx(stim[*next].frame);
        cap->applied.push_back({half.ms(), stim[*next].what, stim[*next].frame});
        ++*next;
    }
    half.tick_ms();
    half.sys(kSettle);
    for (unsigned pass = 0; pass < kPasses; ++pass) {
        const unsigned owed = ctrl_loop_service(&ctrl_plat.app.loop);
        if (owed == 0 && half.quiet()) break;
        half.sys(kSettle);
    }
}

//! The first Talker message's first vector (IEEE 802.1Q-2018 10.8.1.2: each
//! MSRP message is AttributeType, AttributeLength, AttributeListLength, then
//! its vectors; a vector's two-byte header precedes FirstValue, whose
//! stream_id is its first eight bytes, Table 35-2): its stream_id's last byte
//! one higher, so every FirstValue + k it declares is off by one.
bool bump_talker(twin::Frame* f, std::size_t at) {
    std::size_t m = at + 1;
    while (m + 4 + 2 + 8 <= f->size() && !((*f)[m] == 0 && (*f)[m + 1] == 0)) {
        const std::uint8_t kind = (*f)[m];
        if (kind == 1 || kind == 2) {
            ++(*f)[m + 4 + 2 + 7];
            return true;
        }
        m += 4 + static_cast<std::size_t>((*f)[m + 2] << 8 | (*f)[m + 3]);
    }
    return false;
}

//! The planted difference --plant names, applied to the capture.
bool plant(const std::string& name, twin::Capture* cap) {
    unsigned adp = 0;
    bool stopped = false;
    for (auto it = cap->frames.begin(); it != cap->frames.end(); ++it) {
        twin::Frame& f = it->bytes;
        std::uint16_t t = 0;
        std::size_t at = 0;
        if (!twin::ethertype(f, &t, &at)) continue;
        const bool avtp = t == twin::kEtherAvtp && at + 24 < f.size();
        if (name == "byte-flip" && avtp && f[at] == twin::kSubAdp && ++adp == 2) {
            f[at + 20] = static_cast<std::uint8_t>(~f[at + 20]);
            return true;
        }
        // the STOP_STREAMING response (command_type 0x0023), then the first
        // unsolicited response after it (IEEE 1722.1-2021 7.5.2)
        const bool aem = avtp && f[at] == twin::kSubAecp;
        stopped = stopped || (aem && f[at + 22] == 0x00 && f[at + 23] == 0x23);
        if (name == "missing-notification" && stopped && aem && (f[at + 22] & 0x80u)) {
            cap->frames.erase(it);
            return true;
        }
        if (name == "srp-plus-k" && t == twin::kEtherMsrp && bump_talker(&f, at)) return true;
    }
    return false;
}

}  // namespace

// mbx_hal.h on KL_mbx's host port
extern "C" std::uint32_t mbx_hal_read32(std::uint32_t byte_offset) {
    return current()->host(byte_offset, false, 0);
}

extern "C" void mbx_hal_write32(std::uint32_t byte_offset, std::uint32_t value) {
    (void)current()->host(byte_offset, true, value);
}

extern "C" void mbx_hal_wait(void) {}

// ctrl_plat_io.h: the datapath's CSR window, and a UART that never holds a byte
extern "C" std::uint32_t ctrl_plat_io_read32(std::uintptr_t address) {
    if (address >= kCsr && address < kCsr + 0x10000u) {
        return current()->axi_read(static_cast<std::uint16_t>(address - kCsr));
    }
    return address == kUartRegs.rxempty ? 1u : 0u;
}

extern "C" void ctrl_plat_io_write32(std::uintptr_t address, std::uint32_t value) {
    if (address >= kCsr && address < kCsr + 0x10000u) {
        current()->axi_write(static_cast<std::uint16_t>(address - kCsr), value);
    } else if (address == kUartRegs.rxtx) {
        current()->console().push_back(static_cast<char>(value));
    }
}

int main(int argc, char** argv) {
    const std::string planted = argc == 4 && std::strcmp(argv[2], "--plant") == 0 ? argv[3] : "";
    if (argc != 2 && planted.empty()) {
        std::fprintf(stderr, "usage: %s <capture.json> [--plant NAME]\n", argv[0]);
        return 2;
    }
    auto ctx = std::make_unique<VerilatedContext>();
    const auto dut = std::make_unique<Vtb_split_top>(ctx.get());
    SplitHalf half(dut.get());
    current() = &half;
    twin::Capture cap;
    cap.placement = "split";
    cap.ms_unit = "KL_mbx millisecond tick";
    half.reset();
    half.capture(&cap);
    static Env env;
    const ctrl_plat_stage stage = ctrl_plat_boot(&env.env);
    cap.notes.push_back({"boot_stage", std::to_string(static_cast<int>(stage))});
    cap.notes.push_back({"boot_ms", std::to_string(half.ms())});
    if (stage != CTRL_PLAT_READY) {
        std::fprintf(stderr, "FAIL the platform stopped its boot at stage %d: %s\n", static_cast<int>(stage),
                     half.console().c_str());
        return 2;
    }
    const std::vector<twin::Stimulus> stim = twin::scenario();
    std::size_t next = 0;
    while (half.ms() < twin::kRunMs) millisecond(half, stim, &next, &cap);
    half.capture(nullptr);
    if (!planted.empty() && !plant(planted, &cap)) {
        std::fprintf(stderr, "FAIL the plant %s found nothing to plant\n", planted.c_str());
        return 2;
    }
    if (!planted.empty()) cap.notes.push_back({"plant", planted});
    dut->final();
    if (!cap.write(argv[1])) {
        std::fprintf(stderr, "FAIL the capture %s was not written\n", argv[1]);
        return 2;
    }
    std::printf("split half: %zu control frames, %llu stream frames, %u host timeouts, %u ms%s%s\n",
                cap.frames.size(), static_cast<unsigned long long>(cap.stream_frames), half.host_timeouts(),
                twin::kRunMs, planted.empty() ? "" : ", planted ", planted.c_str());
    return half.host_timeouts() == 0 ? 0 : 1;
}
