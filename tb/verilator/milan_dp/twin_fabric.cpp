// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// twin_fabric.cpp - the two-placement simulation's all-fabric half (#665).
//
// milan_datapath at CTRL_SPLIT_P = 0, the shipping shape, with KL_pp_shadow
// running ADP, ACMP, AECP and SRP and KL_maap running MAAP. It is provisioned
// as milan_baremetal.c's milan_init() provisions it:
//   1. configure_fabric()'s fifteen writes, through ctrl_plat_csr.c, the copy
//      of them the platform trace proves equal to milan_baremetal.c's for every
//      shipped config (sw/firmware/ctrl/plat/README.md, plattrace);
//   2. the AEM image the build ships (avdecc/gen_aemi_image.py, the argument)
//      served from main memory, as load_aem_image() leaves it at
//      PP_DESC_BASE_P;
//   3. nvm_boot()'s restore walk (PP_CTRL[1]) on blank media, to its terminal;
//   4. entity_advertise(): PP_CTRL[0], then ADP_CTRL[0].
// Two settings are simulation-only and stated here (#665 issuecomment-
// 6716584453, item 1): the processor's and KL_maap's millisecond is
// TWIN_MS_CYC datapath cycles (PP_TIM_DIV_US_P = 1, PP_TIM_DIV_MS_P and
// MAAP_CLK_HZ_P, the Makefile's), and the MAAP_CTRL write carries MAAP's
// pinned first range (seed_valid and seed_offset, milan_csr.sv 0x6CC).
//
// Every control frame the MAC sends is captured with its modeled millisecond
// (cycle / TWIN_MS_CYC) into the capture file twin_compare.py reads.
//
//   Vmilan_dp_twin_af <aemi.bin> <capture.json>

#include <cstdint>
#include <cstdio>
#include <deque>
#include <fstream>
#include <iterator>
#include <memory>
#include <stdexcept>
#include <string>
#include <vector>

#include "Vmilan_datapath.h"
#include "verilated.h"

#include "ctrl_plat_csr.h"
#include "ctrl_plat_io.h"
#include "ctrl_plat_policy_gen.h"
#include "twin.hpp"

#ifndef TWIN_MS_CYC
#error "TWIN_MS_CYC, the compressed millisecond in datapath cycles, comes from the Makefile"
#endif

namespace {

constexpr std::uint64_t kMsCyc = TWIN_MS_CYC;
constexpr std::uintptr_t kCsr = 0x90000000u;    // the window's bus base; any, the io calls take it off
constexpr std::uint32_t kDescBase = 0x20000000u; // PP_DESC_BASE_P
constexpr std::uint32_t kRespBase = 0x20100000u; // PP_RESP_BASE_P
constexpr std::uint32_t kRespBytes = 592u;       // 16 + PP_DESC_LINE_BYTES_P
constexpr std::uint16_t kMaapCtrl = 0x6CC;       // milan_csr.sv A_MAAP_CTRL
constexpr std::uint16_t kPpCtrl = 0x920;
constexpr std::uint16_t kPpStat = 0x924;
constexpr std::uint16_t kAdpCtrl = 0x600;
constexpr unsigned kGuard = 4096;

class FabricHalf {
 public:
    FabricHalf(Vmilan_datapath* dut, std::vector<std::uint8_t> image) : dut_(dut), desc_(std::move(image)) {}

    void reset();
    void boot();
    void run(twin::Capture* cap);
    void capture(twin::Capture* cap) { cap_ = cap; }
    void write(std::uint16_t addr, std::uint32_t value);
    std::uint32_t read(std::uint16_t addr);
    std::uint32_t ms() const { return static_cast<std::uint32_t>(cyc_ / kMsCyc); }
    std::uint32_t boot_stat() const { return boot_stat_; }

 private:
    struct Fires {
        bool aw = false;
        bool w = false;
        bool b = false;
        bool ar = false;
        bool r = false;
        std::uint32_t data = 0;
    };

    void tick();
    void memory_drive();
    void memory_edge();
    void rx_drive();
    void tx_edge();

    Vmilan_datapath* dut_;
    std::vector<std::uint8_t> desc_;
    std::vector<std::uint8_t> resp_ = std::vector<std::uint8_t>(kRespBytes, 0);
    std::uint64_t cyc_ = 0;
    Fires fires_{};
    bool dm_busy_ = false;
    std::uint32_t dm_addr_ = 0;
    unsigned dm_left_ = 0;
    unsigned dm_wait_ = 0;
    bool rm_busy_ = false;
    std::uint32_t rm_addr_ = 0;
    unsigned rm_left_ = 0;
    bool rm_done_ = false;
    std::deque<twin::Frame> rx_q_;
    std::size_t rx_off_ = 0;
    twin::Frame tx_cur_;
    twin::Capture* cap_ = nullptr;
    std::uint32_t boot_stat_ = 0;
};

//! The descriptor memory answers from reset, the miss 142 clocks as the
//! reference SoC's (sim_nxn.cpp's measurement); the response memory is the
//! 592-byte buffer the processor assembles AECP answers in.
void FabricHalf::memory_drive() {
    std::uint64_t data = 0;
    for (unsigned i = 0; i < 8; ++i) {
        const std::uint32_t off = rm_addr_ - kRespBase + i;
        data = (data << 8) | (off < resp_.size() ? resp_[off] : 0u);
    }
    dut_->i_resp_mem_req_ready = !rm_busy_;
    dut_->i_resp_mem_rsp_valid = rm_busy_;
    dut_->i_resp_mem_rsp_data = data;
    dut_->i_resp_mem_rsp_last = rm_busy_ && rm_left_ == 1;
    dut_->i_resp_mem_rsp_err = 0;
    dut_->i_resp_mem_wr_ready = !rm_done_;
    dut_->i_resp_mem_wr_done = rm_done_;
    dut_->i_resp_mem_wr_err = 0;
    std::uint64_t desc = 0;
    for (unsigned i = 0; i < 8; ++i) {
        const std::uint32_t off = dm_addr_ - kDescBase + i;
        desc = (desc << 8) | (off < desc_.size() ? desc_[off] : 0u);
    }
    dut_->i_desc_mem_req_ready = !dm_busy_;
    dut_->i_desc_mem_rsp_valid = dm_busy_ && dm_wait_ == 0;
    dut_->i_desc_mem_rsp_data = desc;
    dut_->i_desc_mem_rsp_last = dm_busy_ && dm_left_ == 1;
    dut_->i_desc_mem_rsp_err = 0;
}

void FabricHalf::memory_edge() {
    if (rm_busy_ && dut_->o_resp_mem_rsp_ready) {
        rm_addr_ += 8;
        rm_busy_ = --rm_left_ != 0;
    } else if (!rm_busy_ && dut_->o_resp_mem_req_valid) {
        rm_addr_ = dut_->o_resp_mem_req_addr;
        rm_left_ = dut_->o_resp_mem_req_beats;
        rm_busy_ = rm_left_ != 0;
    }
    if (rm_done_) {
        rm_done_ = false;
    } else if (dut_->o_resp_mem_wr_valid) {
        for (unsigned i = 0; i < 8; ++i) {
            const std::uint32_t off = dut_->o_resp_mem_wr_addr - kRespBase + i;
            if (off < resp_.size() && (dut_->o_resp_mem_wr_strb & (1u << i)))
                resp_[off] = static_cast<std::uint8_t>(dut_->o_resp_mem_wr_data >> (56 - 8 * i));
        }
        rm_done_ = true;
    }
    if (!dm_busy_ && dut_->o_desc_mem_req_valid) {
        dm_addr_ = dut_->o_desc_mem_req_addr;
        dm_left_ = dut_->o_desc_mem_req_beats;
        dm_busy_ = dm_left_ != 0;
        dm_wait_ = 142;
    } else if (dm_busy_ && dm_wait_ != 0) {
        --dm_wait_;
    } else if (dm_busy_ && dut_->o_desc_mem_rsp_ready) {
        dm_addr_ += 8;
        dm_busy_ = --dm_left_ != 0;
    }
}

//! The MAC's receive side: the queue's head frame, eight bytes a beat, lane 0 first.
void FabricHalf::rx_drive() {
    const bool busy = !rx_q_.empty();
    const twin::Frame* f = busy ? &rx_q_.front() : nullptr;
    std::uint64_t data = 0;
    std::uint8_t keep = 0;
    for (std::size_t i = 0; busy && i < 8 && rx_off_ + i < f->size(); ++i) {
        data |= static_cast<std::uint64_t>((*f)[rx_off_ + i]) << (8 * i);
        keep = static_cast<std::uint8_t>(keep | (1u << i));
    }
    dut_->s_axis_mac_rx_tvalid = busy;
    dut_->s_axis_mac_rx_tlast = busy && rx_off_ + 8 >= f->size();
    dut_->s_axis_mac_rx_tdata = data;
    dut_->s_axis_mac_rx_tkeep = keep;
}

void FabricHalf::tx_edge() {
    if (!dut_->m_axis_mac_tx_tvalid || !dut_->m_axis_mac_tx_tready) return;
    for (unsigned i = 0; i < 8; ++i)
        if (dut_->m_axis_mac_tx_tkeep & (1u << i))
            tx_cur_.push_back(static_cast<std::uint8_t>(dut_->m_axis_mac_tx_tdata >> (8 * i)));
    if (!dut_->m_axis_mac_tx_tlast) return;
    if (cap_ != nullptr && twin::is_control(tx_cur_)) {
        cap_->frames.push_back({ms(), tx_cur_});
    } else if (cap_ != nullptr) {
        ++cap_->stream_frames;
    }
    tx_cur_.clear();
}

//! One datapath cycle. Every clock of the datapath is the one clock, as
//! tb_split_top clocks the split half's datapath.
void FabricHalf::tick() {
    rx_drive();
    dut_->axis_clk = 0;
    dut_->gtx_clk = 0;
    dut_->clk_audio_i = 0;
    dut_->clk_tdm_i = 0;
    dut_->i_ps_clk = 0;
    memory_drive();
    dut_->eval();
    const bool rx_fire = dut_->s_axis_mac_rx_tvalid && dut_->s_axis_mac_rx_tready;
    fires_.aw = dut_->s_axi_awvalid && dut_->s_axi_awready;
    fires_.w = dut_->s_axi_wvalid && dut_->s_axi_wready;
    fires_.b = dut_->s_axi_bvalid && dut_->s_axi_bready;
    fires_.ar = dut_->s_axi_arvalid && dut_->s_axi_arready;
    fires_.r = dut_->s_axi_rvalid && dut_->s_axi_rready;
    fires_.data = dut_->s_axi_rdata;
    memory_edge();
    tx_edge();
    dut_->axis_clk = 1;
    dut_->gtx_clk = 1;
    dut_->clk_audio_i = 1;
    dut_->clk_tdm_i = 1;
    dut_->i_ps_clk = 1;
    dut_->eval();
    if (rx_fire) {
        rx_off_ += 8;
        if (rx_off_ >= rx_q_.front().size()) {
            rx_q_.pop_front();
            rx_off_ = 0;
        }
    }
    ++cyc_;
}

void FabricHalf::write(std::uint16_t addr, std::uint32_t value) {
    dut_->s_axi_awaddr = addr;
    dut_->s_axi_awvalid = 1;
    dut_->s_axi_wdata = value;
    dut_->s_axi_wstrb = 0xF;
    dut_->s_axi_wvalid = 1;
    dut_->s_axi_bready = 1;
    for (unsigned g = 0; g < kGuard; ++g) {
        tick();
        if (fires_.aw) dut_->s_axi_awvalid = 0;
        if (fires_.w) dut_->s_axi_wvalid = 0;
        if (fires_.b) {
            dut_->s_axi_bready = 0;
            return;
        }
    }
    throw std::runtime_error("AXI write response timeout");
}

std::uint32_t FabricHalf::read(std::uint16_t addr) {
    dut_->s_axi_araddr = addr;
    dut_->s_axi_arvalid = 1;
    dut_->s_axi_rready = 1;
    for (unsigned g = 0; g < kGuard; ++g) {
        tick();
        if (fires_.ar) dut_->s_axi_arvalid = 0;
        if (fires_.r) {
            dut_->s_axi_rready = 0;
            return fires_.data;
        }
    }
    throw std::runtime_error("AXI read response timeout");
}

//! The half the io calls reach: the one instance main() makes.
FabricHalf*& current() {
    static FabricHalf* half = nullptr;
    return half;
}

void FabricHalf::reset() {
    dut_->axis_resetn = 0;
    dut_->gtx_resetn = 0;
    dut_->s_axi_awvalid = 0;
    dut_->s_axi_wvalid = 0;
    dut_->s_axi_arvalid = 0;
    dut_->m_axis_mac_tx_tready = 1;
    dut_->i_mac_speed = 2;
    dut_->i_link_up = 1;
    dut_->i_full_duplex = 1;
    dut_->i_mmcm_locked = 1;
    for (int i = 0; i < 16; ++i) tick();
    dut_->axis_resetn = 1;
    dut_->gtx_resetn = 1;
    for (int i = 0; i < 64; ++i) tick();
}

//! milan_init()'s order: configure_fabric(), the image (served from reset
//! here), nvm_boot()'s walk to its terminal, then entity_advertise().
void FabricHalf::boot() {
    const ctrl_plat_policy policy = CTRL_PLAT_POLICY_INIT;
    std::uint32_t version = 0;
    if (!ctrl_plat_csr_identity(kCsr, &version)) throw std::runtime_error("the CSR window is not a Milan datapath");
    ctrl_plat_csr_policy(kCsr, &policy);
    constexpr std::uint32_t kDone = 1u << 2;
    constexpr std::uint32_t kClosed = 1u << 16;
    write(kPpCtrl, read(kPpCtrl) | 0x2u);
    for (unsigned r = 0; r < 4000 && !(boot_stat_ & (kDone | kClosed)); ++r) {
        for (int c = 0; c < 64; ++c) tick();
        boot_stat_ = read(kPpStat);
    }
    write(kPpCtrl, read(kPpCtrl) | 1u);
    write(kAdpCtrl, read(kAdpCtrl) | 1u);
}

//! The scenario: each stimulus frame enters the MAC at its millisecond.
void FabricHalf::run(twin::Capture* cap) {
    const std::vector<twin::Stimulus> stim = twin::scenario();
    std::size_t next = 0;
    while (ms() < twin::kRunMs) {
        while (next < stim.size() && stim[next].ms <= ms()) {
            rx_q_.push_back(stim[next].frame);
            cap->applied.push_back({ms(), stim[next].what});
            ++next;
        }
        tick();
    }
}

std::vector<std::uint8_t> slurp(const char* path) {
    std::ifstream in(path, std::ios::binary);
    return {std::istreambuf_iterator<char>(in), std::istreambuf_iterator<char>()};
}

}  // namespace

// ctrl_plat_io.h on the datapath's CSR window; the MAAP_CTRL write carries
// the pinned first range (the simulation-only setting named above)
extern "C" std::uint32_t ctrl_plat_io_read32(std::uintptr_t address) {
    return current()->read(static_cast<std::uint16_t>(address - kCsr));
}

extern "C" void ctrl_plat_io_write32(std::uintptr_t address, std::uint32_t value) {
    const auto off = static_cast<std::uint16_t>(address - kCsr);
    if (off == kMaapCtrl) value |= 1u << 1 | static_cast<std::uint32_t>(twin::kMaapOffset) << 16;
    current()->write(off, value);
}

int main(int argc, char** argv) {
    if (argc != 3) {
        std::fprintf(stderr, "usage: %s <aemi.bin> <capture.json>\n", argv[0]);
        return 2;
    }
    auto ctx = std::make_unique<VerilatedContext>();
    const auto dut = std::make_unique<Vmilan_datapath>(ctx.get());
    std::vector<std::uint8_t> image = slurp(argv[1]);
    if (image.size() < 4 || image[0] != 'A' || image[1] != 'E' || image[2] != 'M' || image[3] != 'I') {
        std::fprintf(stderr, "FAIL the AEM image %s is not an AEMI image\n", argv[1]);
        return 2;
    }
    FabricHalf half(dut.get(), std::move(image));
    current() = &half;
    twin::Capture cap;
    cap.placement = "all-fabric";
    cap.ms_unit = "processor millisecond, " + std::to_string(kMsCyc) + " datapath cycles";
    // the capture starts at reset: MAAP and SRP send while the boot provisions
    half.capture(&cap);
    half.reset();
    half.boot();
    cap.notes.push_back({"boot_pp_stat", std::to_string(half.boot_stat())});
    cap.notes.push_back({"boot_ms", std::to_string(half.ms())});
    half.run(&cap);
    half.capture(nullptr);
    dut->final();
    if (!cap.write(argv[2])) {
        std::fprintf(stderr, "FAIL the capture %s was not written\n", argv[2]);
        return 2;
    }
    std::printf("all-fabric half: %zu control frames, %llu stream frames, boot PP_STAT 0x%x, %u ms\n",
                cap.frames.size(), static_cast<unsigned long long>(cap.stream_frames), half.boot_stat(),
                twin::kRunMs);
    return 0;
}
