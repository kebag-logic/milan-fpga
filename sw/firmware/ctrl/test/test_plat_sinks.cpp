// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// test_plat_sinks.cpp - each Stream Input's current format in its
// receive-monitor context (#946; plat/ctrl_plat.c's sink port, the face's
// acknowledged publication in aecp/aecp_face.c, plat/ctrl_plat_csr.c), on the
// host: ctrl_plat.c's boot and composition on the mailbox model, F1's flash
// model and the CSR window of plat_bus.hpp, at the generated shape it is built
// for (PLAT_TEST_SHAPE).
//
// The window is read as the datapath decodes it (REGISTER_MAP.md, 0x800
// window): a write to the selection names {dir, idx}, and with dir 0 the
// FMT_LO and FMT_HI writes land in listener context idx's words 2 and 3. The
// receive monitor judges every PDU of a stream above 0 against those words,
// and a PDU not in them counts UNSUPPORTED_FORMAT and is discarded (Milan v1.2
// Table 5.6, 4.4.2.2; KL_avtp_rx_monitor_ctx), so each AAF input above 0 must
// hold its current format there before a stream of its binding arrives:
//
//   S1  at READY every AAF STREAM_INPUT above 0 holds its current format,
//       written after the face's acknowledged commit and before ADP starts;
//       input 0 (the publication carries its format) and the CRF input are
//       never selected; the selection another writer left is written back
//   S2  SET_STREAM_FORMAT of an unbound input above 0 moves its context alone
//       to the new format, after that change's acknowledged commit; bound, the
//       input refuses it (STREAM_IS_RUNNING) and no context is written
//   S3  a commit the datapath never acknowledges writes no context
//   S4  the port drops a write for another interface, which has no window, and
//       counts it

#include <gtest/gtest.h>

#include <algorithm>
#include <cstdint>
#include <map>
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

FW_TALLY_LABEL("ctrl split platform sink formats (host model, " PLAT_TEST_SHAPE ")");

#ifndef PLAT_SINKS_MIN
#error "PLAT_SINKS_MIN, the AAF inputs above 0 the shape holds, comes from the arm (plat_arms.arm_platsinks)"
#endif

namespace {

using plat_bus::bus;
using plat_bus::kCsr;

constexpr std::uint16_t kStreamInput = 5u;          // IEEE 1722.1-2021 Table 7-1
constexpr unsigned kFormatAt = 74u;                  // a STREAM_INPUT's current_format (7.2.6)
constexpr unsigned kInterfaceAt = 126u;              // its avb_interface_index
constexpr std::uint8_t kAaf = 0x02u;                 // IEEE 1722-2016 Table 6
constexpr std::uint32_t kOtherSelection = 0x103u;    // talker 3, as MAAP's destination writes leave it
constexpr std::uint64_t kTwoChannels = 0x0205022000806000ull;  // AAF PCM32 48 kHz 2ch, in the Base family
constexpr unsigned kSuccess = 0u, kStreamIsRunning = 12u, kInProgress = 25u;  // IEEE 1722.1-2021 Table 7-126

// One mailbox access, with the CSR accesses before it.
struct Mbx {
    std::size_t plat;   // bus().log.size() when it was made
    bool write;
    std::uint32_t offset;
    std::uint32_t value;
};

mbx_model fabric;
std::vector<Mbx> mailbox;

struct Far {
    bool ack = true;
    std::vector<std::size_t> commits;   // mailbox.size() at each F_COMMIT
    // SET_STREAM_FORMAT's verdict (GSI kind 0, selector 15) is 3, supported and every mapped channel kept; the
    // other GET_STREAM_INFO words are 0; every other window is silent
    static mbx_model_reply answer(void*, unsigned, unsigned w, const std::uint32_t* r, std::uint64_t* data) {
        *data = 0;
        if (w != MBX_WIN_GSI || (r[1] & 3u) != 0u) return MBX_MODEL_SILENT;
        if (((r[1] >> 4) & 15u) == 15u) *data = 3u;
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

// The listener contexts' format words as the window decodes the writes from bus log position `from` on: each
// context's {FMT_HI, FMT_LO}, the log position of its last format write, the listener selections in order, and
// whether each format pair was followed by the selection's write back to `restore`.
struct Window {
    std::map<unsigned, std::uint32_t> lo, hi;
    std::map<unsigned, std::size_t> at;
    std::vector<unsigned> selected;
    bool restored = true;
    std::uint64_t format(unsigned n) const {
        return static_cast<std::uint64_t>(hi.at(n)) << 32 | lo.at(n);
    }
    bool holds(unsigned n) const { return lo.count(n) != 0u && hi.count(n) != 0u; }
};

Window window(std::size_t from, std::uint32_t restore) {
    Window w;
    std::uint32_t sel = restore;
    bool owed = false;
    for (std::size_t k = from; k < bus().log.size(); ++k) {
        const auto& a = bus().log[k];
        if (!a.write || a.address < kCsr || a.address >= kCsr + 0x10000u) continue;
        const auto offset = static_cast<std::uint32_t>(a.address - kCsr);
        const unsigned idx = sel & 0xFu;
        const bool listener = (sel & 0x100u) == 0u;
        if (offset == CTRL_PLAT_CSR_STRM_SEL) {
            if (owed) w.restored = w.restored && a.value == restore;
            owed = false;
            sel = a.value;
            if ((sel & 0x100u) == 0u) w.selected.push_back(sel & 0xFu);
        } else if (offset == CTRL_PLAT_CSR_STRMW_FMT_LO && listener) {
            w.lo[idx] = a.value;
            w.at[idx] = k;
            owed = true;
        } else if (offset == CTRL_PLAT_CSR_STRMW_FMT_HI && listener) {
            w.hi[idx] = a.value;
            w.at[idx] = k;
            owed = true;
        }
    }
    w.restored = w.restored && !owed;
    return w;
}

std::uint64_t be(const std::uint8_t* p, unsigned n) {
    std::uint64_t v = 0;
    for (unsigned k = 0; k < n; ++k) v = v << 8 | p[k];
    return v;
}

}  // namespace

// mbx_hal.h on the model, every access in the shared order
extern "C" std::uint32_t mbx_hal_read32(std::uint32_t offset) {
    const std::uint32_t value = mbx_model_read(&fabric, offset);
    mailbox.push_back({bus().log.size(), false, offset, value});
    return value;
}

extern "C" void mbx_hal_write32(std::uint32_t offset, std::uint32_t value) {
    mailbox.push_back({bus().log.size(), true, offset, value});
    mbx_model_write(&fabric, offset, value, 0xFu);
}

extern "C" void mbx_hal_wait(void) {}

namespace {

struct Sinks : ::testing::Test {
    Far far{};
    mbx_model_far side{&far, Far::answer, Far::commit};
    ctrl_plat_env env{};
    nvm_flash flash{};

    void SetUp() override {
        bus().reset();
        bus().csr[CTRL_PLAT_CSR_STRM_SEL] = kOtherSelection;
        mailbox.clear();
        mbx_model_reset(&fabric);
        mbx_model_far_bind(&fabric, &side);
        for (unsigned i = 0; i < MBX_N_IF; ++i) mbx_model_set_link(&fabric, i, true);
        nvm_fmodel_blank();
        nvm_fmodel_power_on();
        nvm_fmodel_window(NVM_SLOT_A, NVM_SLOT_B + NVM_SLOT_BYTES);
        nvm_fmodel_times(1000, 100);
        flash = {nvm_fmodel_port.read, nvm_fmodel_port.program, nvm_fmodel_port.erase, nvm_fmodel_port.busy,
                 nvm_fmodel_port.now_us, nvm_fmodel_port.ctx};
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
    // SRP keeps its one instance as its timer's owner (srp_mbx.h), so each case destroys it
    void TearDown() override {
        srp_mbx_destroy(&ctrl_plat.srp);
        mbx_model_far_bind(&fabric, nullptr);
    }
    // The current configuration's STREAM_INPUTs, by index: the descriptor's current format and interface.
    struct Input {
        std::uint64_t format;
        unsigned interface;
    };
    std::map<unsigned, Input> inputs() const {
        std::map<unsigned, Input> out;
        const aecp_model* model = ctrl_plat.aecp.core.cfg.model;
        for (std::size_t n = 0; n < model->count; ++n) {
            const aecp_descriptor& d = model->descriptors[n];
            if (d.type == kStreamInput && d.configuration == ctrl_plat.aecp.core.configuration &&
                d.length >= kInterfaceAt + 2u) {
                out[d.index] = {be(d.value + kFormatAt, 8), static_cast<unsigned>(be(d.value + kInterfaceAt, 2))};
            }
        }
        return out;
    }
    // The AAF inputs above 0 on interface 0, which each have a receive-monitor context of their own.
    std::vector<unsigned> contexts() const {
        std::vector<unsigned> out;
        for (const auto& [n, in] : inputs()) {
            if (n != 0u && (in.format >> 56) == kAaf && in.interface == 0u) out.push_back(n);
        }
        return out;
    }
    // Whether the CSR access at bus log position p follows an acknowledged commit with no mailbox write
    // between: the last mailbox write before it is an F_COMMIT the face made, and a read after that commit,
    // its acknowledgement's, precedes p too (mbx_face_commit).
    bool after_acknowledged_commit(std::size_t p) const {
        std::size_t last = mailbox.size();
        for (std::size_t k = 0; k < mailbox.size() && mailbox[k].plat <= p; ++k) {
            if (mailbox[k].write) last = k;
        }
        if (last == mailbox.size()) return false;
        bool commit = false;
        for (const std::size_t c : far.commits) commit = commit || c == last + 1u;
        return commit && last + 1u < mailbox.size() && !mailbox[last + 1u].write && mailbox[last + 1u].plat <= p;
    }
    // The bus log position at the first write to TMR_CMD arming interface 0's ADP slot (ADP starts).
    std::size_t adp_start() const {
        for (const auto& a : mailbox) {
            const std::uint32_t slot = (a.value >> MBX_TMR_CMD_SLOT_LSB) & ((1u << MBX_TMR_CMD_SLOT_WIDTH) - 1u);
            const std::uint32_t op = (a.value >> MBX_TMR_CMD_OP_LSB) & ((1u << MBX_TMR_CMD_OP_WIDTH) - 1u);
            if (a.write && a.offset == MBX_REG_TMR_CMD && slot == CTRL_APP_ADP_FIRST_SLOT && op == MBX_TMR_OP_ARM) {
                return a.plat;
            }
        }
        return bus().log.size();
    }
    // SET_STREAM_FORMAT (IEEE 1722.1-2021 7.4.9.1) of STREAM_INPUT n, as the datapath delivers it; the
    // response's status once it is final, or -1 for none within the turns
    int set_format(unsigned n, std::uint64_t format, std::uint16_t seq) {
        std::vector<std::uint8_t> f(50, 0);
        const auto put = [&](std::size_t at, std::uint64_t v, unsigned bytes) {
            for (unsigned k = 0; k < bytes; ++k) f[at + k] = static_cast<std::uint8_t>(v >> (8u * (bytes - 1u - k)));
        };
        put(0, ctrl_plat.config.entity->mac, 6);
        put(6, 0x020000000081ull, 6);
        put(12, 0x22f0u, 2);
        f[14] = 0xfbu;                   // AECP, AEM_COMMAND
        put(16, 24u, 2);                 // control_data_length: controller, sequence, command and 12 payload bytes
        put(18, ctrl_plat.config.entity->entity_id, 8);
        put(26, 0x1020304050607080ull, 8);
        put(34, seq, 2);
        put(36, 0x0008u, 2);             // SET_STREAM_FORMAT
        put(38, kStreamInput, 2);
        put(40, n, 2);
        put(42, format, 8);
        const std::uint32_t before = fabric.tx_sent;
        if (!mbx_model_rx(&fabric, f.data(), f.size(), 0)) return -1;
        for (unsigned turn = 0; turn < 400u; ++turn) {
            ctrl_plat_step();
            for (std::uint32_t k = before; k < fabric.tx_sent; ++k) {
                const auto* t = mbx_model_tx_frame(&fabric, k);
                if (t == nullptr || t->len < 50u || t->bytes[14] != 0xfbu || (t->bytes[15] & 0xfu) != 1u ||
                    be(t->bytes + 34, 2) != seq || be(t->bytes + 36, 2) != 0x0008u) {
                    continue;
                }
                const auto status = static_cast<int>(be(t->bytes + 16, 2) >> 11);
                if (status != static_cast<int>(kInProgress)) return status;
            }
        }
        return -1;
    }
};

TEST_F(Sinks, S1EveryAafInputAboveZeroHoldsItsFormatAtReady) {
    ASSERT_EQ(ctrl_plat_boot(&env), CTRL_PLAT_READY) << "S1 the boot reaches its ready state";
    const auto all = inputs();
    const auto want = contexts();
    EXPECT_GE(want.size(), static_cast<std::size_t>(PLAT_SINKS_MIN))
        << "S1 the shape holds its AAF inputs above 0 (" PLAT_TEST_SHAPE ")";
    ASSERT_FALSE(far.commits.empty()) << "S1 the face is committed before AECP opens";
    const std::size_t adp = adp_start();
    const Window w = window(0, kOtherSelection);
    for (const unsigned n : want) {
        if (!w.holds(n)) {
            ADD_FAILURE() << "S1 every AAF input above 0 holds its current format: input " << n << " holds none";
            continue;
        }
        EXPECT_EQ(w.format(n), all.at(n).format) << "S1 every AAF input above 0 holds its current format: input " << n;
        EXPECT_TRUE(after_acknowledged_commit(w.at.at(n)))
            << "S1 written after the face's acknowledged commit: input " << n;
        EXPECT_LT(w.at.at(n), adp) << "S1 written before ADP starts: input " << n;
    }
    for (const unsigned n : w.selected) {
        EXPECT_NE(n, 0u) << "S1 input 0 is never selected (the publication carries its format)";
        EXPECT_TRUE(all.count(n) == 0u || (all.at(n).format >> 56) == kAaf)
            << "S1 the CRF input has no receive-monitor context: input " << n;
    }
    for (const auto& [n, word] : w.lo) {
        (void)word;
        EXPECT_NE(std::find(want.begin(), want.end(), n), want.end()) << "S1 no other listener context is written: "
                                                                       << n;
    }
    EXPECT_TRUE(w.restored) << "S1 the selection another writer left is written back";
    EXPECT_EQ(bus().word(CTRL_PLAT_CSR_STRM_SEL), kOtherSelection) << "S1 the selection another writer left is kept";
}

TEST_F(Sinks, S2SetStreamFormatMovesOnlyThatContextAndABoundInputRefuses) {
    ASSERT_EQ(ctrl_plat_boot(&env), CTRL_PLAT_READY);
    const auto want = contexts();
    if (want.empty()) {
        // no AAF input above 0 at this shape: input 0's SET_STREAM_FORMAT, its first, is a change the face
        // publishes (the override is set), and it writes no context
        const std::size_t from = bus().log.size();
        const std::size_t commits = far.commits.size();
        EXPECT_EQ(set_format(0u, inputs().at(0).format, 0x0201u), static_cast<int>(kSuccess))
            << "S2 SET_STREAM_FORMAT of input 0 is accepted";
        EXPECT_GT(far.commits.size(), commits) << "S2 input 0's change is published";
        EXPECT_TRUE(window(from, kOtherSelection).selected.empty()) << "S2 input 0's change writes no context";
        return;
    }
    const unsigned n = want.back();
    const std::uint64_t was = inputs().at(n).format;
    ASSERT_NE(was, kTwoChannels);
    std::size_t from = bus().log.size();
    ASSERT_EQ(set_format(n, kTwoChannels, 0x0201u), static_cast<int>(kSuccess))
        << "S2 SET_STREAM_FORMAT of an unbound input is accepted";
    Window w = window(from, kOtherSelection);
    ASSERT_TRUE(w.holds(n)) << "S2 SET_STREAM_FORMAT's new format reaches input " << n << "'s context";
    EXPECT_EQ(w.format(n), kTwoChannels) << "S2 SET_STREAM_FORMAT's new format reaches input " << n << "'s context";
    EXPECT_EQ(w.lo.size(), 1u) << "S2 that input's context alone is written";
    EXPECT_TRUE(after_acknowledged_commit(w.at.at(n))) << "S2 written after the change's acknowledged commit";
    EXPECT_TRUE(w.restored) << "S2 the selection another writer left is written back";
    // a controller binds input n, as the datapath delivers it; the input then refuses a format
    acmp_test::Pdu bind;
    bind.msg = spec::MSG_BIND_RX_COMMAND;
    bind.controller = acmp_test::kCtl1;
    bind.talker = acmp_test::kTkA;
    bind.listener = ctrl_plat.config.entity->entity_id;
    bind.listener_uid = static_cast<std::uint16_t>(n);
    const auto frame = acmp_test::acmpdu(bind);
    ASSERT_TRUE(mbx_model_rx(&fabric, frame.data(), frame.size(), 0)) << "S2 the bind reaches the mailbox";
    acmp_sink_view sink{};
    for (unsigned turn = 0; turn < 400u && !sink.bound; ++turn) {
        ctrl_plat_step();
        ASSERT_TRUE(acmp_view(&ctrl_plat.app.acmp.acmp, static_cast<uint16_t>(n), &sink));
    }
    ASSERT_TRUE(sink.bound) << "S2 the bind is taken";
    from = bus().log.size();
    EXPECT_EQ(set_format(n, was, 0x0202u), static_cast<int>(kStreamIsRunning))
        << "S2 a bound input refuses SET_STREAM_FORMAT";
    EXPECT_TRUE(window(from, kOtherSelection).selected.empty()) << "S2 a refused change writes no context";
}

TEST_F(Sinks, S3AnUnacknowledgedCommitWritesNoContext) {
    far.ack = false;
    EXPECT_EQ(ctrl_plat_boot(&env), CTRL_PLAT_AECP) << "S3 no acknowledgement, no AECP";
    EXPECT_FALSE(far.commits.empty()) << "S3 the face was offered";
    EXPECT_TRUE(window(0, kOtherSelection).selected.empty()) << "S3 a commit never acknowledged writes no context";
}

TEST_F(Sinks, S4AnotherInterfacesWriteIsDroppedAndCounted) {
    ASSERT_EQ(ctrl_plat_boot(&env), CTRL_PLAT_READY);
    ASSERT_NE(ctrl_plat.face.sink, nullptr) << "S4 the platform binds the face's sink port";
    const std::size_t at = bus().log.size();
    const std::uint32_t dropped = ctrl_plat.csr_dropped;
    ctrl_plat.face.sink(ctrl_plat.face.sink_ctx, 1u, 3u, 0x0205022002006000ull);
    EXPECT_EQ(bus().log.size(), at) << "S4 another interface's write reaches no window";
    EXPECT_EQ(ctrl_plat.csr_dropped, dropped + 1u) << "S4 and is counted";
    ctrl_plat.face.sink(ctrl_plat.face.sink_ctx, 0u, 3u, 0x0205022002006000ull);
    const Window w = window(at, kOtherSelection);
    ASSERT_TRUE(w.holds(3u)) << "S4 interface 0's write reaches its window";
    EXPECT_EQ(w.format(3u), 0x0205022002006000ull) << "S4 interface 0's write reaches its window";
    EXPECT_EQ(ctrl_plat.csr_dropped, dropped + 1u) << "S4 interface 0's write is not counted";
}

}  // namespace
