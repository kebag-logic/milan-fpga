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
//
// THE REBOOT (IEEE 1722.1-2021 7.4.43; #871; ctrl_plat.h). The reset port is a
// register on the host bus; a write of 1 to it is the reset's request:
//   B11 a REBOOT of the ENTITY is answered SUCCESS and notified to the other
//       registered controller. Every interface then sends ENTITY_DEPARTING
//       (Milan v1.2 5.6.3.3), and the port is written once, after all of them
//       have left the mailbox. No command is answered after the SUCCESS
//   B12 while the mailbox holds the response, the port is not written, nor is
//       ADP shut down; once the response leaves, it is
//   B13 too short, another type, another ENTITY index and another
//       controller's lock are refused as 7.4.43 states. Each notifies no one,
//       leaves the port unwritten and the entity in service
//   B14 an image with no reset port answers REBOOT NOT_IMPLEMENTED and stays
//       in service
//   B15 across the reset (the flash kept, everything else from reset, as the
//       reload does), the saved name and binding are restored and ADP
//       advertises again within its valid time (Milan v1.2 Table 5.50)
//   B16 a REBOOT during the journal write that saves a change: the store runs
//       on while the datapath's drain waits on F_NVM, so the write completes
//       and the change is restored after the reset (docs/design/REBOOT_RESET.md
//       section 4)
//   B17 once the reset port has fired, nothing is taken: a bind is neither
//       answered nor applied, and no journal write starts during the PHY hold

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

// One frame the model sent, with bus().log.size() when it left the mailbox.
struct Sent {
    std::size_t plat;
    mbx_model_tx frame;
};
std::vector<Sent> frames;

void take_frames() {
    while (frames.size() < fabric.tx_sent) {
        frames.push_back({bus().log.size(), *mbx_model_tx_frame(&fabric, static_cast<std::uint32_t>(frames.size()))});
    }
}
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

// Set, the mailbox's transmit stops at the ADP ring's next commit, before it is taken (B12)
bool hold_adp = false;

extern "C" void mbx_hal_write32(std::uint32_t offset, std::uint32_t value) {
    mailbox.push_back({bus().log.size(), true, offset, value});
    if (hold_adp && offset == MBX_CH_BASE + MBX_CH_ADP * MBX_CH_STRIDE + MBX_CH_REG_TX_HEAD) {
        hold_adp = false;
        mbx_model_tx_pause(&fabric, true);
    }
    mbx_model_write(&fabric, offset, value, 0xFu);
    take_frames();
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
        fabric_from_reset();
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
    // Every bus and the mailbox from reset, as SetUp and the configuration reload start them
    void fabric_from_reset() {
        bus().reset();
        mailbox.clear();
        media.clear();
        frames.clear();
        hold_adp = false;
        other_contract = false;
        mbx_model_reset(&fabric);
        mbx_model_far_bind(&fabric, &side);
        for (unsigned i = 0; i < MBX_N_IF; ++i) mbx_model_set_link(&fabric, i, true);
    }
    // The reset a REBOOT ends in: the configuration reload starts the fabric, the CPU and its
    // memory from the bitstream, and the flash keeps its contents (docs/design/REBOOT_RESET.md)
    void reload() {
        TearDown();
        fabric_from_reset();
        nvm_fmodel_power_on();
    }
    // One loop pass, each of both clocks a millisecond on
    void pass_ms(unsigned ms = 1) {
        mbx_model_advance_ms(&fabric, ms);
        nvm_fmodel_advance_us(1000ull * ms);
        ctrl_plat_step();
        take_frames();
    }
    // An AEM command from a controller, as the datapath delivers it (IEEE 1722.1-2021 9.2.1)
    void aem(std::uint16_t cmd, const std::vector<std::uint8_t>& body, std::uint64_t controller,
             std::uint64_t mac) {
        std::vector<std::uint8_t> f(38 + body.size());
        auto put = [&f](std::size_t at, std::uint64_t v, unsigned n) {
            for (unsigned k = 0; k < n; ++k) f[at + k] = static_cast<std::uint8_t>(v >> (8 * (n - k - 1)));
        };
        put(0, ctrl_plat.config.entity->mac, 6);
        put(6, mac, 6);
        put(12, 0x22f0u, 2);
        f[14] = 0xfbu;
        put(16, 12u + body.size(), 2);
        put(18, ctrl_plat.config.entity->entity_id, 8);
        put(26, controller, 8);
        put(34, ++sequence, 2);
        put(36, cmd, 2);
        std::copy(body.begin(), body.end(), f.begin() + 38);
        ASSERT_TRUE(mbx_model_rx(&fabric, f.data(), f.size(), 0)) << "the command reaches the mailbox";
    }
    std::uint16_t sequence = 0;
    // The writes of the reset port, as bus().log positions
    std::vector<std::size_t> reboot_writes() const {
        std::vector<std::size_t> out;
        for (std::size_t k = 0; k < bus().log.size(); ++k) {
            if (bus().log[k].write && bus().log[k].address == kReboot) out.push_back(k);
        }
        return out;
    }
    static std::uint64_t field(const mbx_model_tx& f, std::size_t at, unsigned n) {
        std::uint64_t v = 0;
        for (unsigned k = 0; k < n; ++k) v = v << 8 | f.bytes[at + k];
        return v;
    }
    // The AECP frames sent from `from` on with command_type cmd (u included)
    std::vector<const Sent*> aecp_frames(std::size_t from, std::uint16_t cmd) const {
        std::vector<const Sent*> out;
        for (std::size_t k = from; k < frames.size(); ++k) {
            const auto& f = frames[k].frame;
            if (f.channel == MBX_CH_AECP && field(f, 36, 2) == cmd) out.push_back(&frames[k]);
        }
        return out;
    }
    // The ENTITY_DEPARTINGs sent from `from` on (IEEE 1722.1-2021 6.2.1, message_type 1)
    std::vector<const Sent*> departing(std::size_t from) const {
        std::vector<const Sent*> out;
        for (std::size_t k = from; k < frames.size(); ++k) {
            const auto& f = frames[k].frame;
            if (f.channel == MBX_CH_ADP && (f.bytes[15] & 0x0fu) == 1u) out.push_back(&frames[k]);
        }
        return out;
    }
    static constexpr std::uintptr_t kReboot = 0xf0001800u;
    static constexpr std::uint64_t kCtl = 0x0011223344556677ull, kCtlMac = 0x020000000081ull;
    static constexpr std::uint64_t kOther = 0x0099aabbccddeeffull, kOtherMac = 0x020000000082ull;
    static std::vector<std::uint8_t> entity0() { return {0, 0, 0, 0}; }
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
    // the loop's passes, 10 ms of both clocks apart, so each carries one centisecond
    for (unsigned k = 0; k < 2000u && nvm_store_status()->commits_ok == commits; ++k) {
        mbx_model_advance_ms(&fabric, 10u);
        nvm_fmodel_advance_us(10000u);
        ctrl_plat_step();
    }
    acmp_sink_view sink{};
    ASSERT_TRUE(acmp_view(&ctrl_plat.app.acmp.acmp, 0, &sink));
    EXPECT_TRUE(sink.bound) << "B10 the bind is taken";
    EXPECT_EQ(nvm_store_status()->commits_ok, commits + 1u)
        << "B10 the bind is written back by the store's service on the loop's tick";
    EXPECT_GT(nvm_fmodel_count()->programs, programs) << "B10 the bind reaches the flash";
}

// ---- THE REBOOT (#871) ------------------------------------------------------

namespace {

// SET_NAME's body for the ENTITY's entity_name (IEEE 1722.1-2021 7.4.17.1)
std::vector<std::uint8_t> entity_name(const std::string& name) {
    std::vector<std::uint8_t> b(8 + 64, 0);
    std::copy(name.begin(), name.end(), b.begin() + 8);
    return b;
}

// GET_NAME's answer for the ENTITY's entity_name, from the frames from `from` on
std::string answered_name(const std::vector<Sent>& sent, std::size_t from) {
    for (std::size_t k = from; k < sent.size(); ++k) {
        const auto& f = sent[k].frame;
        if (f.channel == MBX_CH_AECP && f.bytes[36] == 0 && f.bytes[37] == 17u && f.len >= 46u + 64u) {
            const char* name = reinterpret_cast<const char*>(f.bytes + 46);
            return std::string(name, strnlen(name, 64));
        }
    }
    return "<no GET_NAME response>";
}

}  // namespace

TEST_F(Boot, B11ARebootIsAnsweredNotifiedDepartsAndThenResets) {
    env.reboot = kReboot;
    ASSERT_EQ(ctrl_plat_boot(&env), CTRL_PLAT_READY);
    aem(36, {}, kOther, kOtherMac);
    for (unsigned k = 0; k < 50; ++k) pass_ms();
    const std::size_t from = frames.size();
    aem(42, entity0(), kCtl, kCtlMac);
    for (unsigned k = 0; k < 500 && reboot_writes().empty(); ++k) pass_ms();
    const auto resp = aecp_frames(from, 42), note = aecp_frames(from, 0x8000u | 42u);
    const auto gone = departing(from);
    const auto writes = reboot_writes();
    ASSERT_EQ(resp.size(), 1u) << "B11 the REBOOT is answered once";
    EXPECT_EQ(field(resp[0]->frame, 16, 2) >> 11, 0u) << "B11 a REBOOT of the ENTITY is SUCCESS";
    EXPECT_EQ(field(resp[0]->frame, 26, 8), kCtl) << "B11 the response goes to the requester";
    EXPECT_EQ(field(resp[0]->frame, 38, 4), 0u) << "B11 the response echoes ENTITY 0";
    ASSERT_EQ(note.size(), 1u) << "B11 the other registered controller is notified";
    EXPECT_EQ(field(note[0]->frame, 26, 8), kOther) << "B11 the other registered controller is notified";
    EXPECT_EQ(gone.size(), static_cast<std::size_t>(MBX_N_IF)) << "B11 every interface sends ENTITY_DEPARTING";
    ASSERT_EQ(writes.size(), 1u) << "B11 the reset port is written once";
    EXPECT_EQ(bus().log[writes[0]].value, 1u) << "B11 the reset port is written once";
    EXPECT_LE(resp[0]->plat, writes[0]) << "B11 the response leaves before the reset";
    EXPECT_LE(note[0]->plat, writes[0]) << "B11 the notification leaves before the reset";
    for (const auto* d : gone) {
        EXPECT_GE(d->plat, note[0]->plat) << "B11 ENTITY_DEPARTING follows the notification";
        EXPECT_LE(d->plat, writes[0]) << "B11 ENTITY_DEPARTING leaves before the reset";
    }
    const std::size_t after = frames.size();
    aem(7, entity0(), kCtl, kCtlMac);
    for (unsigned k = 0; k < 50; ++k) pass_ms();
    EXPECT_TRUE(aecp_frames(after, 7).empty()) << "B11 no command is answered after the SUCCESS";
    EXPECT_EQ(reboot_writes().size(), 1u) << "B11 the reset port is written once";
}

TEST_F(Boot, B12TheResetWaitsForTheResponseToLeave) {
    env.reboot = kReboot;
    ASSERT_EQ(ctrl_plat_boot(&env), CTRL_PLAT_READY);
    for (unsigned k = 0; k < 50; ++k) pass_ms();
    const std::size_t from = frames.size();
    mbx_model_tx_pause(&fabric, true);
    aem(42, entity0(), kCtl, kCtlMac);
    for (unsigned k = 0; k < 300; ++k) pass_ms();
    EXPECT_TRUE(aecp_frames(from, 42).empty()) << "B12 the mailbox holds the response";
    EXPECT_TRUE(reboot_writes().empty()) << "B12 no reset while the mailbox holds the response";
    EXPECT_TRUE(ctrl_plat.app.adp.ifs[0].adp.enabled) << "B12 nor is ADP shut down";
    // the response leaves, and the mailbox then holds what ADP commits next: its ENTITY_DEPARTINGs
    hold_adp = true;
    mbx_model_tx_pause(&fabric, false);
    take_frames();
    for (unsigned k = 0; k < 300; ++k) pass_ms();
    EXPECT_FALSE(hold_adp) << "B12 the mailbox holds ENTITY_DEPARTING";
    EXPECT_FALSE(ctrl_plat.app.adp.ifs[0].adp.enabled) << "B12 the response has left, so ADP is shut down";
    EXPECT_TRUE(departing(from).empty()) << "B12 the mailbox holds ENTITY_DEPARTING";
    EXPECT_TRUE(reboot_writes().empty()) << "B12 no reset while the mailbox holds ENTITY_DEPARTING";
    mbx_model_tx_pause(&fabric, false);
    take_frames();
    for (unsigned k = 0; k < 500 && reboot_writes().empty(); ++k) pass_ms();
    const auto resp = aecp_frames(from, 42);
    const auto gone = departing(from);
    const auto writes = reboot_writes();
    ASSERT_EQ(resp.size(), 1u) << "B12 the response leaves";
    ASSERT_EQ(writes.size(), 1u) << "B12 once the response leaves, the reset port is written";
    EXPECT_LE(resp[0]->plat, writes[0]) << "B12 the response leaves before the reset";
    ASSERT_EQ(gone.size(), static_cast<std::size_t>(MBX_N_IF)) << "B12 ENTITY_DEPARTING leaves";
    for (const auto* d : gone) EXPECT_LE(d->plat, writes[0]) << "B12 ENTITY_DEPARTING leaves before the reset";
}

TEST_F(Boot, B13RefusalsLeaveTheEntityInService) {
    env.reboot = kReboot;
    ASSERT_EQ(ctrl_plat_boot(&env), CTRL_PLAT_READY);
    aem(36, {}, kOther, kOtherMac);
    for (unsigned k = 0; k < 20; ++k) pass_ms();
    struct Case {
        std::vector<std::uint8_t> body;
        unsigned status;
        const char* what;
    };
    const std::vector<Case> cases = {
        {{0, 0}, 7u, "B13 BAD_ARGUMENTS short of Figure 7-68's four bytes"},
        {{0, 5, 0, 0}, 11u, "B13 NOT_SUPPORTED for a STREAM_INPUT"},
        {{0, 0x0b, 0, 0}, 11u, "B13 NOT_SUPPORTED for a MEMORY_OBJECT, which this entity lacks"},
        {{0, 0, 0, 1}, 2u, "B13 NO_SUCH_DESCRIPTOR for another ENTITY index"},
        {{}, 3u, "B13 ENTITY_LOCKED under another controller's lock"},
    };
    for (const auto& c : cases) {
        if (c.status == 3u) {
            aem(1, std::vector<std::uint8_t>(16, 0), kOther, kOtherMac);
            for (unsigned k = 0; k < 20; ++k) pass_ms();
        }
        const std::size_t from = frames.size();
        aem(42, c.status == 3u ? entity0() : c.body, kCtl, kCtlMac);
        for (unsigned k = 0; k < 30; ++k) pass_ms();
        const auto resp = aecp_frames(from, 42);
        ASSERT_EQ(resp.size(), 1u) << c.what;
        EXPECT_EQ(field(resp[0]->frame, 16, 2) >> 11, c.status) << c.what;
        EXPECT_EQ(field(resp[0]->frame, 16, 2) & 0x7ffu, 16u) << c.what << ", at cdl 16";
        EXPECT_TRUE(aecp_frames(from, 0x8000u | 42u).empty()) << c.what << ", notifying no one";
        aem(7, entity0(), kCtl, kCtlMac);
        for (unsigned k = 0; k < 30; ++k) pass_ms();
        EXPECT_EQ(aecp_frames(from, 7).size(), 1u) << c.what << ", leaving the entity in service";
    }
    EXPECT_TRUE(reboot_writes().empty()) << "B13 a refused REBOOT resets nothing";
    EXPECT_TRUE(departing(0).empty()) << "B13 a refused REBOOT sends no ENTITY_DEPARTING";
}

TEST_F(Boot, B14WithoutAResetPortRebootIsNotImplemented) {
    ASSERT_EQ(env.reboot, 0u);
    ASSERT_EQ(ctrl_plat_boot(&env), CTRL_PLAT_READY);
    const std::size_t from = frames.size();
    aem(42, entity0(), kCtl, kCtlMac);
    for (unsigned k = 0; k < 50; ++k) pass_ms();
    const auto resp = aecp_frames(from, 42);
    ASSERT_EQ(resp.size(), 1u) << "B14 the REBOOT is answered";
    EXPECT_EQ(field(resp[0]->frame, 16, 2) >> 11, 1u) << "B14 without a reset port REBOOT is NOT_IMPLEMENTED";
    aem(7, entity0(), kCtl, kCtlMac);
    for (unsigned k = 0; k < 30; ++k) pass_ms();
    EXPECT_EQ(aecp_frames(from, 7).size(), 1u) << "B14 and the entity stays in service";
    EXPECT_TRUE(departing(0).empty()) << "B14 and sends no ENTITY_DEPARTING";
}

TEST_F(Boot, B15TheResetRestoresTheSavedStateAndAdvertisesAgain) {
    env.reboot = kReboot;
    ASSERT_EQ(ctrl_plat_boot(&env), CTRL_PLAT_READY);
    aem(16, entity_name("after the reboot"), kCtl, kCtlMac);
    acmp_test::Pdu bind;
    bind.msg = spec::MSG_BIND_RX_COMMAND;
    bind.controller = acmp_test::kCtl1;
    bind.talker = acmp_test::kTkA;
    bind.listener = ctrl_plat.config.entity->entity_id;
    const auto frame = acmp_test::acmpdu(bind);
    ASSERT_TRUE(mbx_model_rx(&fabric, frame.data(), frame.size(), 0));
    for (unsigned k = 0; k < 400 && (nvm_store_status()->dirty != 0 || nvm_store_status()->pending != 0 ||
                                     nvm_store_status()->commits_ok == 0u); ++k) {
        pass_ms(10);
    }
    ASSERT_GT(nvm_store_status()->commits_ok, 0u) << "B15 the name and the binding are saved";
    aem(42, entity0(), kCtl, kCtlMac);
    for (unsigned k = 0; k < 500 && reboot_writes().empty(); ++k) pass_ms();
    ASSERT_EQ(reboot_writes().size(), 1u) << "B15 the REBOOT fires the reset port";
    reload();
    ASSERT_EQ(ctrl_plat_boot(&env), CTRL_PLAT_READY) << "B15 the image boots again after the reset";
    acmp_sink_view sink{};
    ASSERT_TRUE(acmp_view(&ctrl_plat.app.acmp.acmp, 0, &sink));
    EXPECT_TRUE(sink.bound) << "B15 the binding is restored";
    const std::size_t from = frames.size();
    aem(17, std::vector<std::uint8_t>(8, 0), kCtl, kCtlMac);
    auto available = [] {
        return std::any_of(frames.begin(), frames.end(), [](const Sent& s) {
            return s.frame.channel == MBX_CH_ADP && (s.frame.bytes[15] & 0x0fu) == 0u;
        });
    };
    unsigned ms = 0;
    for (; ms < 20000u && !available(); ms += 10) pass_ms(10);
    EXPECT_LT(ms, 20000u) << "B15 ADP advertises again within its valid time";
    EXPECT_EQ(answered_name(frames, from), "after the reboot") << "B15 the saved name is restored";
}

TEST_F(Boot, B16ARebootDuringTheJournalWriteKeepsTheChange) {
    env.reboot = kReboot;
    nvm_fmodel_times(200000, 2000);
    ASSERT_EQ(ctrl_plat_boot(&env), CTRL_PLAT_READY);
    const unsigned erases = nvm_fmodel_count()->erases, commits = nvm_store_status()->commits_ok;
    aem(16, entity_name("kept"), kCtl, kCtlMac);
    for (unsigned k = 0; k < 4000 && nvm_fmodel_count()->erases == erases; ++k) pass_ms();
    ASSERT_GT(nvm_fmodel_count()->erases, erases) << "B16 the change's journal write has started";
    ASSERT_EQ(nvm_store_status()->commits_ok, commits) << "B16 and has not completed";
    aem(42, entity0(), kCtl, kCtlMac);
    for (unsigned k = 0; k < 500 && reboot_writes().empty(); ++k) pass_ms();
    ASSERT_EQ(reboot_writes().size(), 1u) << "B16 the REBOOT fires the reset port";
    // KL_reboot_ctrl's drain: until no live writer or nothing accepted outside a slot, at most 10,000 ms
    unsigned drained = 0;
    auto settled = [] {
        mbx_model_face v{};
        mbx_model_face_view(&fabric, 0, &v);
        const bool backed = (v.nvm >> MBX_F_NVM_BACKED_LSB) & 1u, dirty = (v.nvm >> MBX_F_NVM_DIRTY_LSB) & 1u,
                   pend = (v.nvm >> MBX_F_NVM_PEND_LSB) & 1u;
        return !backed || (!dirty && !pend);
    };
    for (; drained < 10000u && !settled(); drained += 10) pass_ms(10);
    EXPECT_LT(drained, 10000u) << "B16 the drain ends because the write completed, not at its deadline";
    EXPECT_EQ(nvm_store_status()->commits_ok, commits + 1u) << "B16 the write in progress completes";
    nvm_fmodel_advance_us(3500000);
    reload();
    ASSERT_EQ(ctrl_plat_boot(&env), CTRL_PLAT_READY) << "B16 the image boots again after the reset";
    const std::size_t from = frames.size();
    aem(17, std::vector<std::uint8_t>(8, 0), kCtl, kCtlMac);
    for (unsigned k = 0; k < 50; ++k) pass_ms();
    EXPECT_EQ(answered_name(frames, from), "kept") << "B16 the change made before the REBOOT is kept";
}

TEST_F(Boot, B17NothingIsTakenOnceTheResetPortFired) {
    env.reboot = kReboot;
    ASSERT_EQ(ctrl_plat_boot(&env), CTRL_PLAT_READY);
    aem(42, entity0(), kCtl, kCtlMac);
    for (unsigned k = 0; k < 500 && reboot_writes().empty(); ++k) pass_ms();
    ASSERT_EQ(reboot_writes().size(), 1u) << "B17 the REBOOT fires the reset port";
    const std::size_t from = frames.size();
    const unsigned erases = nvm_fmodel_count()->erases, commits = nvm_store_status()->commits_ok;
    acmp_test::Pdu bind;
    bind.msg = spec::MSG_BIND_RX_COMMAND;
    bind.controller = acmp_test::kCtl1;
    bind.talker = acmp_test::kTkA;
    bind.listener = ctrl_plat.config.entity->entity_id;
    const auto frame = acmp_test::acmpdu(bind);
    ASSERT_TRUE(mbx_model_rx(&fabric, frame.data(), frame.size(), 0));
    // the PHY hold's 3,500 ms, past the store's debounce and a write's
    for (unsigned k = 0; k < 350; ++k) pass_ms(10);
    acmp_sink_view sink{};
    ASSERT_TRUE(acmp_view(&ctrl_plat.app.acmp.acmp, 0, &sink));
    EXPECT_FALSE(sink.bound) << "B17 a bind after the reset port fired is not taken";
    EXPECT_TRUE(std::none_of(frames.begin() + static_cast<std::ptrdiff_t>(from), frames.end(),
                             [](const Sent& s) { return s.frame.channel == MBX_CH_ACMP; }))
        << "B17 a bind after the reset port fired is not answered";
    EXPECT_EQ(nvm_fmodel_count()->erases, erases) << "B17 no journal write starts during the PHY hold";
    EXPECT_EQ(nvm_store_status()->commits_ok, commits) << "B17 no journal write starts during the PHY hold";
}

}  // namespace
