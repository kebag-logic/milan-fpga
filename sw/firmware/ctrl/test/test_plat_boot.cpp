// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// test_plat_boot.cpp - the split platform's boot and composition (#665;
// plat/ctrl_plat.c) on the host: the mailbox model behind mbx_hal.h, F1's
// flash model behind the flash port, and the CSR window and UART of
// plat_bus.hpp behind ctrl_plat_io.h, at the generated shape it is built for.
// Every mailbox access records the CSR and UART accesses before it, and every
// flash access the mailbox accesses before it, so a test reads the boot's
// steps in the order the buses carry them (docs/ARCHITECTURE_HW_SW_SPLIT.md
// section 2, Milan v1.2 5.6.1):
//
//   B1  the boot reaches READY in step order: the identity read first, the
//       policy's fifteen writes, MAAP's invalid report taking the stream
//       window from the fabric allocator, the saved state read from the
//       flash, then the mailbox; the face commit before ADP's first timer;
//       the banner first and the ready line last
//   B2  a window that is not a Milan datapath stops the boot at IDENTITY,
//       before any write and any mailbox access
//   B3  a refused AEM image stops it at IMAGE, after the policy and before the
//       mailbox, and the console reports AEM=disabled
//   B4  a stream count MAAP's port refuses stops it after the policy
//   B5  a bitstream with another mailbox contract stops it at MAILBOX, ADP
//       never started
//   B6  a face the datapath never acknowledges stops it at AECP, ADP never
//       started
//   B7  a stopped boot keeps the console and never services the loop; a ready
//       one services the loop, the console among its polls
//   B8  the platform's ports: MAAP's allocation reaches the window and then
//       ACMP's source port, the other ports answer as documented
//   B9  SRP's sources carry the generated streams on every interface
//   B10 a controller's bind after READY is written back to the flash by the
//       store's service on the loop's centisecond tick (Milan v1.2 5.5.2.4,
//       acmp_nvm.h's boot order)
//   B11 the PHY poll (#919, ctrl_plat_phy.h) is armed past the identity check:
//       a foreign window's MDIO pins are never touched; a stage refused past
//       it keeps publishing the PHY's link on its console's turns (#70)
//   B12 THE STEP's client: a call whose store takes a step of its save carries
//       no PHY frame, and one whose store step is an idle one, or that has no
//       store step, carries one; the client owes a step while the PHY owes a
//       frame
//   L1  the ready loop publishes the PHY's link to milan_mac_link_status
//   L2  the datapath's effective link (milan_datapath.sv eff_link_w, the
//       published link_up through the SoC's synchroniser), modelled as a level
//       that stands between two turns: a 3 s loss, and a loss that recovered
//       between two polls, each move LINK_DOWN and LINK_UP by one
//   L3  each edge's counter change reaches AECP, which sends a registered
//       controller one unsolicited GET_COUNTERS for the AVB_INTERFACE, LINK_DOWN
//       then LINK_UP moved by one
//   L4  the link's return is published by the first poll after it, so the
//       gPTP plane's port enable rises then and its Pdelay_Req cease ends
//       (Milan v1.2 4.2.6.2.5), within CTRL_PLAT_PHY_POLL_US of the return

#include <gtest/gtest.h>

#include <algorithm>
#include <cstdint>
#include <cstring>
#include <string>
#include <vector>

#include "acmp_fake.hpp"
#include "fw_gtest.hpp"
#include "plat_bus.hpp"

#include "ctrl_plat.h"
#include "ctrl_plat_policy_gen.h"
extern "C" {
#include "host/nvm_fmodel.h"
}
#include "mbx_hal.h"
#include "mbx_model.h"
// the store's headers carry no extern "C", and its shape header asserts in C11's spelling
#define _Static_assert static_assert
extern "C" {
#include "nvm_store.h"
}
#undef _Static_assert

FW_TALLY_LABEL("ctrl split platform boot (host model, " PLAT_TEST_SHAPE ")");

namespace {

using plat_bus::bus;
using plat_bus::kCsr;

// One mailbox access, with the CSR and UART accesses before it.
struct Mbx {
    std::size_t plat;   // bus().log.size() when it was made
    bool write;
    std::uint32_t offset;
    std::uint32_t value;
};

mbx_model fabric;
std::vector<Mbx> mailbox;
bool other_contract = false;
// mailbox.size() at each flash read, program and erase
std::vector<std::size_t> media;

// F1's flash port on the model, each media access stamped with the mailbox's
int flash_read(void* ctx, std::uint32_t addr, std::uint8_t* dst, std::uint32_t len) {
    media.push_back(mailbox.size());
    return nvm_fmodel_port.read(ctx, addr, dst, len);
}

int flash_program(void* ctx, std::uint32_t addr, const std::uint8_t* src, std::uint32_t len) {
    media.push_back(mailbox.size());
    return nvm_fmodel_port.program(ctx, addr, src, len);
}

int flash_erase(void* ctx, std::uint32_t addr) {
    media.push_back(mailbox.size());
    return nvm_fmodel_port.erase(ctx, addr);
}

// The AVB_INTERFACE's link counters as the datapath counts them (milan_datapath.sv ctr_linkup_r and ctr_linkdn_r,
// IEEE 1722.1-2021 Table 7-158: LINK_UP quadlet 0, LINK_DOWN quadlet 1; CTR_VALID_AVB_C), answered through the
// face's CTR window
struct LinkCounters {
    bool served = false;
    std::uint32_t up = 0, down = 0;
};
LinkCounters counters;

struct Far {
    bool ack = true;
    std::vector<std::size_t> commits;   // the mailbox access count at each F_COMMIT
    static mbx_model_reply answer(void*, unsigned, unsigned window, const std::uint32_t* request, std::uint64_t* data) {
        *data = 0;
        if (!counters.served || window != MBX_WIN_CTR ||
            (request[0] >> MBX_CTR_REQ_TYPE_LSB & 0xffffu) != MBX_CTRCHG_AVB_INTERFACE_TYPE) {
            return MBX_MODEL_SILENT;
        }
        const std::uint32_t word = request[1] >> MBX_CTR_WORD_WORD_LSB & 0x3fu;
        *data = word == 0u ? counters.up : word == 1u ? counters.down : word == 32u ? 0x23u : 0u;
        return MBX_MODEL_ANSWER;
    }
    static bool commit(void* p, unsigned, const std::uint32_t*) {
        auto& f = *static_cast<Far*>(p);
        f.commits.push_back(mailbox.size());
        return f.ack;
    }
};

const ctrl_plat_policy kPolicy = CTRL_PLAT_POLICY_INIT;
const ctrl_plat_stream kStreams[CTRL_SRP_SOURCES] = CTRL_PLAT_STREAMS_INIT;

}  // namespace

// mbx_hal.h on the model, every access in the shared order; another
// contract's bitstream answers ID without this contract's magic
extern "C" std::uint32_t mbx_hal_read32(std::uint32_t offset) {
    std::uint32_t value = mbx_model_read(&fabric, offset);
    if (other_contract && offset == MBX_REG_ID) value = 0u;
    mailbox.push_back({bus().log.size(), false, offset, value});
    return value;
}

extern "C" void mbx_hal_write32(std::uint32_t offset, std::uint32_t value) {
    mailbox.push_back({bus().log.size(), true, offset, value});
    mbx_model_write(&fabric, offset, value, 0xFu);
}

extern "C" void mbx_hal_wait(void) {}

namespace {

struct Boot : ::testing::Test {
    Far far{};
    mbx_model_far side{&far, Far::answer, Far::commit};
    ctrl_plat_env env{};
    nvm_flash flash{};
    std::vector<std::uint8_t> image;

    void SetUp() override {
        bus().reset();
        mailbox.clear();
        media.clear();
        other_contract = false;
        counters = LinkCounters{};
        mbx_model_reset(&fabric);
        mbx_model_far_bind(&fabric, &side);
        for (unsigned i = 0; i < MBX_N_IF; ++i) mbx_model_set_link(&fabric, i, true);
        nvm_fmodel_blank();
        nvm_fmodel_power_on();
        nvm_fmodel_window(NVM_SLOT_A, NVM_SLOT_B + NVM_SLOT_BYTES);
        nvm_fmodel_times(1000, 100);
        flash = {flash_read, flash_program, flash_erase, nvm_fmodel_port.busy, nvm_fmodel_port.now_us,
                 nvm_fmodel_port.ctx};
        env.flash = &flash;
        env.csr = kCsr;
        env.uart = plat_bus::kUartRegs;
        env.policy = &kPolicy;
        env.streams = kStreams;
        env.aaf_outputs = CTRL_PLAT_AAF_OUTPUTS;
        env.crf_output = CTRL_PLAT_CRF_OUTPUT;
        env.link_rate_bps = CTRL_PLAT_LINK_BPS;
        ctrl_plat_generated_image(&env);
    }
    // SRP keeps its one instance as its timer's owner (srp_mbx.h): the image
    // boots once per reset, a test once per case, so each case destroys it
    void TearDown() override {
        srp_mbx_destroy(&ctrl_plat.srp);
        mbx_model_far_bind(&fabric, nullptr);
    }
    void steps(unsigned n) {
        for (unsigned k = 0; k < n; ++k) ctrl_plat_step();
    }
    // The mailbox writes to TMR_CMD arming interface 0's ADP slot.
    std::vector<std::size_t> adp_arms() const {
        std::vector<std::size_t> out;
        for (std::size_t k = 0; k < mailbox.size(); ++k) {
            const auto& a = mailbox[k];
            const std::uint32_t slot = (a.value >> MBX_TMR_CMD_SLOT_LSB) & ((1u << MBX_TMR_CMD_SLOT_WIDTH) - 1u);
            const std::uint32_t op = (a.value >> MBX_TMR_CMD_OP_LSB) & ((1u << MBX_TMR_CMD_OP_WIDTH) - 1u);
            if (a.write && a.offset == MBX_REG_TMR_CMD && slot == CTRL_APP_ADP_FIRST_SLOT && op == MBX_TMR_OP_ARM) {
                out.push_back(k);
            }
        }
        return out;
    }
    // The policy's writes as configure_fabric() makes them on the seeded window.
    std::vector<std::pair<std::uint32_t, std::uint32_t>> policy_writes() const {
        using plat_bus::seed;
        return {{0x600u, seed(0x600u) & ~1u}, {0x920u, seed(0x920u) & ~1u}, {0x604u, kPolicy.entity_id_lo},
                {0x608u, kPolicy.entity_id_hi}, {0x60cu, kPolicy.model_id_lo}, {0x610u, kPolicy.model_id_hi},
                {0x108u, kPolicy.station_mac_lo}, {0x10cu, kPolicy.station_mac_hi},
                {0x100u, seed(0x100u) | kPolicy.mac_ctrl_set}, {0x700u, kPolicy.tcam_ctrl},
                {0x654u, kPolicy.aaf_ctrl}, {0x684u, kPolicy.sr_vid},
                {0x680u, kPolicy.lwsrp_ctrl_reset | CTRL_PLAT_LWSRP_LIVE}, {0x6ccu, kPolicy.maap_ctrl},
                {0x750u, kPolicy.crf_tx_ctrl}};
    }
    std::string ask(const std::string& line, unsigned turns = 200) {
        bus().tx.clear();
        bus().type(line);
        steps(turns);
        return bus().tx;
    }
};

TEST_F(Boot, B1ReachesReadyInStepOrder) {
    ASSERT_EQ(ctrl_plat_boot(&env), CTRL_PLAT_READY) << "B1 the boot reaches its ready state";
    // steps 6-7 before the open: the bindings are restored before any ACMP command can arrive
    ASSERT_FALSE(media.empty()) << "B1 the saved state is read from the flash";
    EXPECT_EQ(*std::max_element(media.begin(), media.end()), 0u)
        << "B1 the saved state is read before the mailbox's first access";
    EXPECT_EQ(nvm_store_status()->terminal, NVM_T_BLANK) << "B1 a blank flash restores nothing";
    ASSERT_FALSE(bus().log.empty()) << "B1 the identity is read before anything";
    EXPECT_TRUE(!bus().log[0].write && bus().log[0].address == kCsr + CTRL_PLAT_CSR_ID)
        << "B1 the identity is read before anything";
    auto writes = bus().writes();
    auto want = policy_writes();
    // MAAP's invalid report on interface 0's window: admission and the fabric allocator off
    want.push_back({0x654u, kPolicy.aaf_ctrl & ~1u});
    want.push_back({0x750u, kPolicy.crf_tx_ctrl & ~1u});
    want.push_back({0x6ccu, kPolicy.maap_ctrl & ~1u});
    ASSERT_GE(writes.size(), want.size()) << "B1 the policy's fifteen writes, then the one MAAP owner";
    const std::vector<std::pair<std::uint32_t, std::uint32_t>> first(writes.begin(), writes.begin() + 18);
    EXPECT_EQ(first, want) << "B1 the policy's fifteen writes, then the one MAAP owner";
    ASSERT_FALSE(mailbox.empty()) << "B1 the mailbox only after the policy";
    std::size_t policy_end = 0;
    for (std::size_t k = 0, seen = 0; k < bus().log.size() && seen < 18; ++k) {
        if (bus().log[k].write) {
            ++seen;
            policy_end = k + 1;
        }
    }
    EXPECT_GE(mailbox.front().plat, policy_end) << "B1 the mailbox only after the policy and the one MAAP owner";
    ASSERT_FALSE(far.commits.empty()) << "B1 the face is committed before AECP opens";
    auto arms = adp_arms();
    ASSERT_FALSE(arms.empty()) << "B1 ADP starts";
    EXPECT_GT(arms.front(), far.commits.front()) << "B1 ADP's first timer after the face commit";
    steps(100);
    const std::string banner = CTRL_PLAT_BANNER, ready = CTRL_PLAT_READY_LINE;
    EXPECT_EQ(bus().tx.find(banner), 0u) << "B1 the banner first";
    EXPECT_EQ(bus().tx.find(banner, 1), std::string::npos) << "B1 one banner per boot";
    EXPECT_EQ(bus().tx.size() >= ready.size() ? bus().tx.substr(bus().tx.size() - ready.size()) : "", ready)
        << "B1 the ready line last";
}

TEST_F(Boot, B2ForeignWindowStopsAtIdentity) {
    bus().csr[CTRL_PLAT_CSR_ID] = 0x12345678u;
    EXPECT_EQ(ctrl_plat_boot(&env), CTRL_PLAT_IDENTITY) << "B2 a foreign window stops the boot";
    EXPECT_TRUE(bus().writes().empty()) << "B2 nothing is written to a foreign window";
    EXPECT_TRUE(mailbox.empty()) << "B2 nor to the mailbox";
}

TEST_F(Boot, B3RefusedImageStopsAtImage) {
    image.assign(env.aem, env.aem + env.aem_bytes);
    image[image.size() / 2] ^= 0x01u;
    env.aem = image.data();
    EXPECT_EQ(ctrl_plat_boot(&env), CTRL_PLAT_IMAGE) << "B3 a refused image stops the boot";
    EXPECT_EQ(bus().writes().size(), 18u) << "B3 after the policy and the one MAAP owner";
    EXPECT_TRUE(mailbox.empty()) << "B3 before the mailbox";
    EXPECT_NE(ask("milan_status\r").find(" AEM=disabled\r\n"), std::string::npos)
        << "B3 the console reports AEM=disabled";
}

TEST_F(Boot, B4RefusedStreamCountStopsAfterThePolicy) {
    env.aaf_outputs = 9;
    EXPECT_EQ(ctrl_plat_boot(&env), CTRL_PLAT_COMPOSE) << "B4 MAAP's port refuses nine AAF outputs";
    EXPECT_EQ(bus().writes().size(), 15u) << "B4 after the policy, before any stream window write";
    EXPECT_TRUE(mailbox.empty()) << "B4 before the mailbox";
}

TEST_F(Boot, B5OtherContractStopsAtMailbox) {
    other_contract = true;
    EXPECT_EQ(ctrl_plat_boot(&env), CTRL_PLAT_MAILBOX) << "B5 another contract stops the boot";
    EXPECT_TRUE(adp_arms().empty()) << "B5 ADP never starts";
    EXPECT_TRUE(far.commits.empty()) << "B5 AECP's face is never committed";
}

TEST_F(Boot, B6UnacknowledgedFaceStopsAtAecp) {
    far.ack = false;
    EXPECT_EQ(ctrl_plat_boot(&env), CTRL_PLAT_AECP) << "B6 no acknowledgement, no AECP";
    EXPECT_FALSE(far.commits.empty()) << "B6 the face was offered";
    EXPECT_TRUE(adp_arms().empty()) << "B6 ADP never starts";
}

TEST_F(Boot, B7OnlyAReadyBootServicesTheLoop) {
    far.ack = false;
    ASSERT_EQ(ctrl_plat_boot(&env), CTRL_PLAT_AECP);
    const std::size_t accesses = mailbox.size();
    EXPECT_NE(ask("milan_gettime\r").find("TAI_NS=0x"), std::string::npos) << "B7 a stopped boot keeps the console";
    EXPECT_EQ(mailbox.size(), accesses) << "B7 and never services the loop";
    TearDown();
    SetUp();
    far.ack = true;
    ASSERT_EQ(ctrl_plat_boot(&env), CTRL_PLAT_READY);
    const std::uint32_t passes = ctrl_plat.app.loop.stats.passes;
    EXPECT_NE(ask("milan_gettime\r").find("TAI_NS=0x"), std::string::npos) << "B7 the console is a loop poll";
    EXPECT_GT(ctrl_plat.app.loop.stats.passes, passes) << "B7 a ready boot services the loop";
}

TEST_F(Boot, B8PlatformPortsAnswerAsDocumented) {
    ASSERT_EQ(ctrl_plat_boot(&env), CTRL_PLAT_READY);
    acmp_source_state s{};
    ctrl_plat.acmp_env.source(ctrl_plat.acmp_env.ctx, 0, &s);
    EXPECT_FALSE(s.dest_mac_valid) << "B8 no destination before MAAP holds a range";
    const std::size_t before = bus().writes().size();
    const std::uint64_t base = 0x91e0f000fe00ull;
    ctrl_plat.config.maap_allocation(ctrl_plat.config.maap_ctx, 0, base, CTRL_SRP_SOURCES, true);
    auto writes = bus().writes();
    ASSERT_GT(writes.size(), before);
    EXPECT_EQ(writes.back(), (std::pair<std::uint32_t, std::uint32_t>{0x750u, kPolicy.crf_tx_ctrl}))
        << "B8 the allocation reaches the window, admission restored last";
    for (unsigned n = 0; n < CTRL_SRP_SOURCES; ++n) {
        ctrl_plat.acmp_env.source(ctrl_plat.acmp_env.ctx, n, &s);
        EXPECT_EQ(s.dest_mac_valid, ctrl_plat.acmp.source_interface[n] == 0u)
            << "B8 each source's destination valid once MAAP holds its interface's range";
        if (ctrl_plat.acmp.source_interface[n] != 0u) continue;
        EXPECT_EQ(s.stream.dest_mac, base + n) << "B8 source n holds base + n";
        EXPECT_EQ(s.stream.stream_id, ctrl_plat.config.entity->mac << 16 | kStreams[n].unique_id)
            << "B8 the stream_id is the MAC and the unique ID";
        EXPECT_EQ(s.stream.vlan_id, kPolicy.sr_vid) << "B8 on the SR class VID";
        EXPECT_FALSE(s.asking_failed) << "B8 no asking-failed source";
    }
    // a report shorter than the sources (maap_csr refuses its count): a source past it holds no address
    ctrl_plat.config.maap_allocation(ctrl_plat.config.maap_ctx, 0, base, 1, true);
    for (unsigned n = 1; n < CTRL_SRP_SOURCES; ++n) {
        if (ctrl_plat.acmp.source_interface[n] != 0u) continue;
        ctrl_plat.acmp_env.source(ctrl_plat.acmp_env.ctx, n, &s);
        EXPECT_FALSE(s.dest_mac_valid) << "B8 a source past the reported count has no destination";
    }
    std::uint64_t owner = 1;
    EXPECT_FALSE(ctrl_plat.acmp_env.locked(ctrl_plat.acmp_env.ctx, &owner)) << "B8 the platform holds no lock";
    EXPECT_EQ(owner, 0u) << "B8 the platform holds no lock";
    ctrl_plat.acmp_env.srp(ctrl_plat.acmp_env.ctx, 0, nullptr);
    ctrl_plat.acmp_env.persist(ctrl_plat.acmp_env.ctx, 0);
    ctrl_plat.acmp_env.changed(ctrl_plat.acmp_env.ctx, 0);
    EXPECT_EQ(ctrl_plat.aecp_platform.random(nullptr), mbx_now_ms()) << "B8 random is the loop's clock";
    std::uint64_t path[4];
    std::size_t count = 9;
    EXPECT_FALSE(ctrl_plat.aecp_platform.path(nullptr, 0, 0, path, 4, &count)) << "B8 GET_AS_PATH unavailable";
    ctrl_plat.srp_config.licence(ctrl_plat.srp_config.ctx, 0, 1, true);
    EXPECT_EQ(ctrl_plat.licences[0], 2u) << "B8 a licence sets its source's bit";
    ctrl_plat.srp_config.licence(ctrl_plat.srp_config.ctx, 0, 1, false);
    EXPECT_EQ(ctrl_plat.licences[0], 0u) << "B8 a revocation clears it";
#if MBX_N_IF > 1
    const std::size_t dropped = ctrl_plat.csr_dropped;
    const std::size_t at = bus().log.size();
    ctrl_plat.config.maap_allocation(ctrl_plat.config.maap_ctx, 1, base + 0x100u, CTRL_SRP_SOURCES, true);
    EXPECT_GT(ctrl_plat.csr_dropped, dropped) << "B8 interface 1 has no window: its writes are dropped";
    EXPECT_EQ(bus().log.size(), at) << "B8 and nothing reaches interface 0's";
    ctrl_plat.acmp_env.source(ctrl_plat.acmp_env.ctx, 1, &s);
    EXPECT_TRUE(s.dest_mac_valid && s.stream.dest_mac == base + 0x100u + 1u)
        << "B8 source 1, on interface 1, holds its interface's range";
#endif
}

TEST_F(Boot, B9SrpSourcesCarryTheGeneratedStreams) {
    ASSERT_EQ(ctrl_plat_boot(&env), CTRL_PLAT_READY);
    const std::uint64_t mac = ctrl_plat.config.entity->mac;
    for (unsigned i = 0; i < MBX_N_IF; ++i) {
        for (unsigned n = 0; n < CTRL_SRP_SOURCES; ++n) {
            const msrp_talker_adv& v = ctrl_plat.sources[i][n].value;
            std::uint64_t id = 0;
            for (unsigned b = 0; b < 8; ++b) id = id << 8 | v.stream_id.bytes[b];
            EXPECT_EQ(id, mac << 16 | kStreams[n].unique_id) << "B9 the stream_id is the MAC and the unique ID";
            EXPECT_EQ(v.vlan_id, kPolicy.sr_vid) << "B9 on the SR class VID";
            EXPECT_EQ(v.max_frame_size, kStreams[n].max_frame_size) << "B9 the generated TSpec";
            EXPECT_EQ(v.max_interval_frames, kStreams[n].max_interval_frames) << "B9 the generated TSpec";
            EXPECT_EQ(v.priority_and_rank, kStreams[n].priority_and_rank) << "B9 the generated class";
            EXPECT_FALSE(ctrl_plat.sources[i][n].allocated) << "B9 unallocated at boot";
        }
        EXPECT_EQ(ctrl_plat.srp_config.mac[i], mac) << "B9 the entity MAC on every interface";
    }
    EXPECT_EQ(ctrl_plat.srp_config.link_rate_bps, CTRL_PLAT_LINK_BPS) << "B9 the generated link rate";
}

TEST_F(Boot, B10ABindAfterReadyIsWrittenBackThroughTheLoop) {
    ASSERT_EQ(ctrl_plat_boot(&env), CTRL_PLAT_READY);
    const unsigned commits = nvm_store_status()->commits_ok;
    const unsigned programs = nvm_fmodel_count()->programs;
    // a controller binds sink 0 through the mailbox, as the datapath delivers it
    acmp_test::Pdu bind;
    bind.msg = spec::MSG_BIND_RX_COMMAND;
    bind.controller = acmp_test::kCtl1;
    bind.talker = acmp_test::kTkA;
    bind.listener = ctrl_plat.config.entity->entity_id;
    const auto frame = acmp_test::acmpdu(bind);
    ASSERT_TRUE(mbx_model_rx(&fabric, frame.data(), frame.size(), 0)) << "B10 the bind reaches the mailbox";
    // the loop's passes, 10 ms of both clocks apart, so each carries one centisecond; the store's step
    // is taken by the pass after it, which takes nothing (THE STEP, ctrl_loop.h)
    for (unsigned k = 0; k < 2000u && nvm_store_status()->commits_ok == commits; ++k) {
        mbx_model_advance_ms(&fabric, 10u);
        nvm_fmodel_advance_us(10000u);
        ctrl_plat_step();
        ctrl_plat_step();
    }
    acmp_sink_view sink{};
    ASSERT_TRUE(acmp_view(&ctrl_plat.app.acmp.acmp, 0, &sink));
    EXPECT_TRUE(sink.bound) << "B10 the bind is taken";
    EXPECT_EQ(nvm_store_status()->commits_ok, commits + 1u)
        << "B10 the bind is written back by the store's service on the loop's tick";
    EXPECT_GT(nvm_fmodel_count()->programs, programs) << "B10 the bind reaches the flash";
}


// ---- the PHY poll (#919) ---------------------------------------------------

constexpr ctrl_plat_phy_bus kPhyBus = {0xf0002004u, 0xf0002008u, 0xf000201cu, 100000000u};
constexpr std::uint32_t kGigFull = 13u;
constexpr unsigned kPollMs = CTRL_PLAT_PHY_POLL_US / 1000u;

// The boot with a 1000BASE-T PHY behind the bus at address 0, and the datapath's effective link as the RTL
// builds it from the published word (L2): a level that stands between two turns, its edges counted, posted to the
// mailbox as the LINK level and to the face as the AVB_INTERFACE's counter change, and kept as the gPTP plane's
// port enable
struct Phy : Boot {
    phy_peer::Peer peer;
    bool level = true;                                  // link_status resets link up
    std::size_t seen = 0;
    std::vector<std::pair<std::uint64_t, bool>> edges;  // the port enable's edges, (us, level)
    std::uint32_t scanned = 0;                          // the mailbox's frames read for notices
    std::vector<std::pair<std::uint32_t, std::uint32_t>> notices;   // the AVB_INTERFACE's (LINK_UP, LINK_DOWN)
    void SetUp() override {
        Boot::SetUp();
        peer = phy_peer::Peer{};
        level = true;
        seen = 0;
        edges.clear();
        scanned = 0;
        notices.clear();
        peer.w = kPhyBus.mdio_w;
        peer.r = kPhyBus.mdio_r;
        peer.status = kPhyBus.link_status;
        peer.gigabit(0u);
        bus().phy = &peer;
        env.phy = kPhyBus;
        counters.served = true;
    }
    // Each unsolicited GET_COUNTERS (IEEE 1722.1-2021 7.4.42) of the AVB_INTERFACE the mailbox sent: an AEM_RESPONSE
    // (message_type 1) with the u bit, its block's quadlets 0 and 1
    void scan() {
        for (; scanned < fabric.tx_sent; ++scanned) {
            const mbx_model_tx* f = mbx_model_tx_frame(&fabric, scanned);
            ASSERT_NE(f, nullptr) << "a frame the capture dropped before it was read";
            const auto quad = [f](unsigned at) {
                return std::uint32_t(f->bytes[at]) << 24 | std::uint32_t(f->bytes[at + 1]) << 16 |
                       std::uint32_t(f->bytes[at + 2]) << 8 | f->bytes[at + 3];
            };
            if (f->len >= 54u && f->bytes[12] == 0x22u && f->bytes[13] == 0xf0u && f->bytes[14] == 0xfbu &&
                (f->bytes[15] & 0x0fu) == 1u && (f->bytes[36] & 0x80u) != 0u &&
                ((f->bytes[36] & 0x7fu) << 8 | f->bytes[37]) == 0x0029u && (f->bytes[38] << 8 | f->bytes[39]) == 9) {
                notices.push_back({quad(46), quad(50)});
            }
        }
    }
    void turn() {
        ctrl_plat_step();
        scan();
        if (peer.published.size() == seen) return;
        seen = peer.published.size();
        const bool up = (peer.word & 1u) != 0u;
        if (up == level) return;
        level = up;
        ++(up ? counters.up : counters.down);
        edges.push_back({nvm_fmodel_now_us(), up});
        mbx_model_set_link(&fabric, 0, up);
        mbx_model_face_event(&fabric, 0, MBX_MODEL_EV_COUNTERS, MBX_CTRCHG_AVB_INTERFACE_TYPE, 0);
    }
    // `ms` milliseconds of both clocks, one at a time, `turns` turns in each
    void run(unsigned ms, unsigned turns = 4) {
        for (unsigned k = 0; k < ms; ++k) {
            mbx_model_advance_ms(&fabric, 1u);
            nvm_fmodel_advance_us(1000u);
            for (unsigned n = 0; n < turns; ++n) turn();
        }
    }
    // A loss of `ms`, then the link back, its loss latched in BMSR as a PHY latches it
    void flap(unsigned ms) {
        peer.link(false);
        run(ms);
        peer.link(true);
        peer.latched_down = true;
    }
    unsigned pin_accesses() const {
        return bus().count(0, kPhyBus.mdio_w, true) + bus().count(0, kPhyBus.mdio_r, false) +
               bus().count(0, kPhyBus.link_status, true);
    }
};

TEST_F(Phy, B11ArmedPastTheIdentityCheck) {
    bus().csr[CTRL_PLAT_CSR_ID] = 0x12345678u;
    ASSERT_EQ(ctrl_plat_boot(&env), CTRL_PLAT_IDENTITY);
    run(2u * kPollMs);
    EXPECT_EQ(pin_accesses(), 0u) << "B11 a foreign window's MDIO pins are never touched";
    TearDown();
    SetUp();
    image.assign(env.aem, env.aem + env.aem_bytes);
    image[image.size() / 2] ^= 0x01u;
    env.aem = image.data();
    ASSERT_EQ(ctrl_plat_boot(&env), CTRL_PLAT_IMAGE);
    run(5);
    EXPECT_FALSE(peer.published.empty()) << "B11 a stage refused past the identity check keeps publishing the link";
    EXPECT_EQ(peer.word, kGigFull) << "B11 a stage refused past the identity check keeps publishing the link";
    EXPECT_TRUE(peer.fault.empty()) << peer.fault;
}

TEST_F(Phy, B12StepCarriesTheStoresSaveOrAPhyFrame) {
    ASSERT_EQ(ctrl_plat_boot(&env), CTRL_PLAT_READY);
    run(5);
    ASSERT_EQ(peer.word, kGigFull);
    ASSERT_EQ(nvm_store_status()->phase, NVM_P_IDLE) << "a blank flash's store is idle";
    nvm_fmodel_advance_us(CTRL_PLAT_PHY_POLL_US);
    // the store's idle step: no flash, no record, so the PHY's frame follows it
    nvm_store_tick();
    std::uint32_t steps = nvm_store_status()->steps;
    std::size_t frames = peer.frames.size();
    EXPECT_TRUE(ctrl_plat_phy_store_step(&ctrl_plat.phy, nvm_store_clock(nullptr) + CTRL_LOOP_SHARE_US))
        << "B12 the client owes a step while the PHY owes a frame";
    EXPECT_EQ(nvm_store_status()->steps, steps + 1u) << "B12 the store's owed step is taken first";
    EXPECT_EQ(peer.frames.size(), frames + 1u) << "B12 a call whose store step is an idle one carries one PHY frame";
    // a save in flight: its step leaves the PHY no room in that call
    ASSERT_EQ(nvm_store_commit_now(), 1);
    nvm_store_tick();
    steps = nvm_store_status()->steps;
    frames = peer.frames.size();
    EXPECT_TRUE(ctrl_plat_phy_store_step(&ctrl_plat.phy, nvm_store_clock(nullptr) + CTRL_LOOP_SHARE_US))
        << "B12 the client owes a step while the PHY owes a frame";
    EXPECT_EQ(nvm_store_status()->steps, steps + 1u) << "B12 the store's step of its save is taken";
    EXPECT_EQ(peer.frames.size(), frames) << "B12 a call whose store takes a step of its save carries no PHY frame";
    // no store step owed: the PHY's frame
    EXPECT_TRUE(ctrl_plat_phy_store_step(&ctrl_plat.phy, nvm_store_clock(nullptr) + CTRL_LOOP_SHARE_US))
        << "B12 the client owes a step while the PHY owes a frame";
    EXPECT_EQ(peer.frames.size(), frames + 1u) << "B12 a call with no store step carries the PHY's frame";
}

TEST_F(Phy, L1ReadyLoopPublishesTheLink) {
    ASSERT_EQ(ctrl_plat_boot(&env), CTRL_PLAT_READY);
    run(5);
    EXPECT_FALSE(peer.published.empty()) << "L1 the ready loop publishes the PHY's link";
    EXPECT_EQ(peer.word, kGigFull) << "L1 the ready loop publishes the PHY's link";
    const std::size_t pubs = peer.published.size();
    run(3u * kPollMs);
    EXPECT_GE(peer.published.size(), pubs + 2u) << "L1 a poll a period, each publishing the link";
    EXPECT_LE(peer.published.size(), pubs + 3u) << "L1 a poll a period, each publishing the link";
    EXPECT_TRUE(peer.fault.empty()) << peer.fault;
}

TEST_F(Phy, L2EveryEdgeIsCounted) {
    ASSERT_EQ(ctrl_plat_boot(&env), CTRL_PLAT_READY);
    run(5);
    ASSERT_EQ(peer.word, kGigFull);
    EXPECT_EQ(counters.up + counters.down, 0u) << "L2 a PHY up at boot moves neither counter";
    flap(3000u);
    run(kPollMs + 10u);
    EXPECT_EQ(counters.down, 1u) << "L2 a 3 s loss moves LINK_DOWN and LINK_UP by one each";
    EXPECT_EQ(counters.up, 1u) << "L2 a 3 s loss moves LINK_DOWN and LINK_UP by one each";
    peer.latched_down = true;
    run(kPollMs + 10u);
    EXPECT_EQ(counters.down, 2u) << "L2 a loss that recovered between two polls moves LINK_DOWN and LINK_UP by one each";
    EXPECT_EQ(counters.up, 2u) << "L2 a loss that recovered between two polls moves LINK_DOWN and LINK_UP by one each";
    run(2u * kPollMs);
    EXPECT_EQ(counters.up + counters.down, 4u) << "L2 a steady link moves neither";
}

// REGISTER_UNSOLICITED_NOTIFICATION (IEEE 1722.1-2021 7.4.37) from a controller, as the datapath delivers it
std::vector<std::uint8_t> registration(std::uint64_t mac, std::uint64_t entity) {
    std::vector<std::uint8_t> b(38, 0u);
    const auto put = [&b](std::size_t at, std::uint64_t v, unsigned n) {
        for (unsigned k = 0; k < n; ++k) b[at + k] = static_cast<std::uint8_t>(v >> (8u * (n - k - 1u)));
    };
    put(0, mac, 6);
    put(6, 0x020000000081ull, 6);
    put(12, 0x22f0u, 2);
    b[14] = 0xfbu;
    put(16, 12u, 2);
    put(18, entity, 8);
    put(26, 0x1020304050607080ull, 8);
    put(34, 0x1234u, 2);
    put(36, 0x0024u, 2);
    return b;
}

TEST_F(Phy, L3EachEdgeNotifiesTheCounters) {
    ASSERT_EQ(ctrl_plat_boot(&env), CTRL_PLAT_READY);
    run(5);
    const auto reg = registration(ctrl_plat.config.entity->mac, ctrl_plat.config.entity->entity_id);
    ASSERT_TRUE(mbx_model_rx(&fabric, reg.data(), reg.size(), 0));
    run(20);
    notices.clear();
    flap(3000u);
    run(1500u);
    EXPECT_EQ(notices, (std::vector<std::pair<std::uint32_t, std::uint32_t>>{{0u, 1u}, {1u, 1u}}))
        << "L3 each link edge sends one unsolicited GET_COUNTERS, LINK_DOWN then LINK_UP moved by one";
}

TEST_F(Phy, L4ReturnEndsTheCeaseWithinAPoll) {
    ASSERT_EQ(ctrl_plat_boot(&env), CTRL_PLAT_READY);
    run(5);
    flap(3000u);
    const std::uint64_t back = nvm_fmodel_now_us();
    run(2u * kPollMs + 10u);
    ASSERT_EQ(edges.size(), 2u) << "L4 the port enable falls with the loss and rises with the return";
    EXPECT_FALSE(edges[0].second) << "L4 the port enable falls with the loss";
    EXPECT_TRUE(edges[1].second) << "L4 the port enable rises with the return";
    EXPECT_LE(edges[1].first - back, std::uint64_t{CTRL_PLAT_PHY_POLL_US} + 10000u)
        << "L4 the first poll after the link's return publishes it up: the gPTP plane's port enable rises within "
           "CTRL_PLAT_PHY_POLL_US of the return, ending its Pdelay_Req cease";
}

}  // namespace
