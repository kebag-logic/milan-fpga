// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// test_plat_boot.cpp - the split platform's boot and composition (#665 S3;
// plat/ctrl_plat.c) on the host: the mailbox model behind mbx_hal.h, F1's
// flash model behind the flash port, and the CSR window and UART of
// plat_bus.hpp behind ctrl_plat_io.h, at the generated shape it is built for.
// Every access of the three goes into one order (Seq), so a test reads the
// boot's steps as the buses carry them (docs/ARCHITECTURE_HW_SW_SPLIT.md
// section 2, Milan v1.2 5.6.1):
//
//   B1  the boot reaches READY in step order: the identity read first, the
//       policy's fifteen writes, MAAP's invalid report taking the stream
//       window from the fabric allocator, then the mailbox; the face commit
//       before ADP's first timer; the banner first and the ready line last
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

#include <gtest/gtest.h>

#include <cstdint>
#include <cstring>
#include <string>
#include <vector>

#include "fw_gtest.hpp"
#include "plat_bus.hpp"

#include "ctrl_plat.h"
#include "ctrl_plat_policy_gen.h"
extern "C" {
#include "host/nvm_fmodel.h"
}
#include "mbx_hal.h"
#include "mbx_model.h"
// the store's shape header asserts in C11's spelling
#define _Static_assert static_assert
#include "nvm_store.h"
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

struct Far {
    bool ack = true;
    std::vector<std::size_t> commits;   // the mailbox access count at each F_COMMIT
    static mbx_model_reply answer(void*, unsigned, unsigned, const std::uint32_t*, std::uint64_t* data) {
        *data = 0;
        return MBX_MODEL_SILENT;
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
    std::vector<std::uint8_t> image;

    void SetUp() override {
        bus().reset();
        mailbox.clear();
        other_contract = false;
        mbx_model_reset(&fabric);
        mbx_model_far_bind(&fabric, &side);
        for (unsigned i = 0; i < MBX_N_IF; ++i) mbx_model_set_link(&fabric, i, true);
        nvm_fmodel_blank();
        nvm_fmodel_power_on();
        nvm_fmodel_window(NVM_SLOT_A, NVM_SLOT_B + NVM_SLOT_BYTES);
        nvm_fmodel_times(1000, 100);
        env.flash = &nvm_fmodel_port;
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

}  // namespace
