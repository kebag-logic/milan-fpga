// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// test_unit_seams.cpp - the composition and the driver against GoogleMock's
// two ctrl seams, the mailbox HAL (mock_mbx_hal.hpp) and lwSRP's port layer
// (mock_shlan_port.hpp), where the host model cannot answer as a test needs
// (#665 lane FT):
//
//   U1  ctrl_app_start binds lwSRP's allocator to the app's own pool, through
//       the port layer, before the mailbox is touched, and a bitstream that
//       carries another contract opens nothing;
//   U2  mbx_open refuses an ID or CAPS word that differs from the contract the
//       firmware was built against in any one field, and reads nothing more;
//   U3  ctrl_loop_run turns for ever: a pass, then the wait when it owed
//       nothing, and again;
//   U4  the app gives the filter the entity's MAC as every interface's own
//       unicast MAC before a channel opens (lane FC).

#include <gmock/gmock.h>
#include <gtest/gtest.h>

#include <csetjmp>
#include <cstdint>

#include "ctrl_app.h"
#include "ctrl_loop.h"
#include "fw_gtest.hpp"
#include "mbx.h"
#include "mbx_wire.h"
#include "mock_mbx_hal.hpp"
#include "mock_shlan_port.hpp"
#include "unit_window.hpp"

FW_TALLY_LABEL("ctrl units on the HAL and port-layer mocks");

namespace {

using ::testing::_;
using ::testing::AnyNumber;
using ::testing::Eq;
using ::testing::InSequence;
using ::testing::NiceMock;
using ::testing::Return;

//! The ID and CAPS words of the contract this firmware was built against.
const std::uint32_t kId = unit::contract_id();
const std::uint32_t kCaps = unit::contract_caps();

const adp_entity kEntity = {0x1122334455667788ull, 0x99AABBCCDDEEFF01ull, 0x001B921122AAull, 0xC588u, 8u, 0x4801u,
                            8u, 0x4801u, 5u};

alignas(std::max_align_t) std::uint8_t arena[1024];
const ctrl_pool_class kClasses[] = {{32u, 8u}};

//! A window that answers the contract's ID and CAPS and reads 0 elsewhere.
void answer_contract(NiceMock<MockMbxHal>& hal, std::uint32_t id = kId, std::uint32_t caps = kCaps) {
    ON_CALL(hal, read32(_)).WillByDefault(Return(0u));
    ON_CALL(hal, read32(MBX_REG_ID)).WillByDefault(Return(id));
    ON_CALL(hal, read32(MBX_REG_CAPS)).WillByDefault(Return(caps));
}

ctrl_app_config config() {
    return ctrl_app_config{&kEntity, 2, arena, sizeof arena, kClasses, 1, nullptr, nullptr, nullptr, nullptr};
}

TEST(AppComposition, U1BindsTheAppPoolBehindLwsrpBeforeTheMailbox) {
    static ctrl_app app;
    NiceMock<MockMbxHal> hal;
    MockShlanPort port;
    answer_contract(hal);
    const ctrl_app_config cfg = config();
    EXPECT_CALL(hal, read32(_)).Times(AnyNumber());
    {
        InSequence order;
        EXPECT_CALL(port, bind_pool(Eq(&app.pool))).Times(1);
        EXPECT_CALL(hal, read32(MBX_REG_ID)).Times(1);
    }
    EXPECT_CALL(hal, write32(_, _)).Times(AnyNumber());
    EXPECT_TRUE(ctrl_app_start(&app, &cfg)) << "U1 the app starts on a window that carries its contract";
}

TEST(AppComposition, U1AnotherContractOpensNothing) {
    static ctrl_app app;
    NiceMock<MockMbxHal> hal;
    NiceMock<MockShlanPort> port;
    answer_contract(hal, kId ^ (1u << MBX_ID_MAJOR_LSB));
    const ctrl_app_config cfg = config();
    EXPECT_CALL(hal, write32(_, _)).Times(0);
    EXPECT_FALSE(ctrl_app_start(&app, &cfg)) << "U1 a bitstream carrying another contract is refused, nothing written";
}

// ADP sends the entity's one MAC on every interface, so the app gives it to
// the filter as every interface's own unicast MAC, before a channel opens
// (#665 lane FC).
TEST(AppComposition, U4EveryInterfaceOwnsTheEntityMacBeforeAChannelOpens) {
    static ctrl_app app;
    NiceMock<MockMbxHal> hal;
    NiceMock<MockShlanPort> port;
    unit::Window w(hal);
    const ctrl_app_config cfg = config();
    ASSERT_TRUE(ctrl_app_start(&app, &cfg));
    std::size_t opened = w.writes.size();
    for (std::size_t k = w.writes.size(); k-- > 0;) {
        if (w.writes[k].first == MBX_REG_FILTER_EN) {
            opened = k;
        }
    }
    for (unsigned i = 0; i < MBX_N_IF; ++i) {
        const std::uint32_t lo = MBX_IFF_BASE + MBX_IFF_STRIDE * i + MBX_IFF_REG_OWN_MAC_LO;
        const std::uint32_t hi = MBX_IFF_BASE + MBX_IFF_STRIDE * i + MBX_IFF_REG_OWN_MAC_HI;
        EXPECT_TRUE(w.at(lo) == static_cast<std::uint32_t>(kEntity.mac) &&
                    w.at(hi) == static_cast<std::uint32_t>(kEntity.mac >> 32))
            << "U4 interface " << i << "'s OWN_MAC is the entity's MAC";
        bool before = false;
        for (std::size_t k = 0; k < opened; ++k) {
            before = before || w.writes[k].first == hi;
        }
        EXPECT_TRUE(before) << "U4 and is written before any channel opens";
    }
}

TEST(AppComposition, U1AnUncarvablePoolStartsNothing) {
    static ctrl_app app;
    MockMbxHal hal;
    MockShlanPort port;
    ctrl_app_config cfg = config();
    cfg.arena_bytes = 1;
    EXPECT_CALL(port, bind_pool(_)).Times(0);
    EXPECT_CALL(hal, read32(_)).Times(0);
    EXPECT_FALSE(ctrl_app_start(&app, &cfg)) << "U1 an arena too small for the classes starts nothing";
}

//! One field of ID or CAPS made to differ from the contract.
struct Field {
    const char* name;
    bool caps;
    std::uint32_t lsb;
};

class ContractField : public ::testing::TestWithParam<Field> {};

TEST_P(ContractField, U2RefusedAndNothingMoreRead) {
    NiceMock<MockMbxHal> hal;
    const Field& f = GetParam();
    answer_contract(hal, f.caps ? kId : kId ^ (1u << f.lsb), f.caps ? kCaps ^ (1u << f.lsb) : kCaps);
    EXPECT_CALL(hal, read32(_)).Times(0);
    EXPECT_CALL(hal, read32(MBX_REG_ID)).Times(1);
    EXPECT_CALL(hal, read32(MBX_REG_CAPS)).Times(1);
    EXPECT_FALSE(mbx_open()) << "U2 " << f.name << " differs from the contract: mbx_open refuses";
}

INSTANTIATE_TEST_SUITE_P(IdAndCaps, ContractField,
                         ::testing::Values(Field{"magic", false, MBX_ID_MAGIC_LSB},
                                           Field{"major", false, MBX_ID_MAJOR_LSB},
                                           Field{"n_ch", true, MBX_CAPS_N_CH_LSB},
                                           Field{"n_if", true, MBX_CAPS_N_IF_LSB},
                                           Field{"n_timers", true, MBX_CAPS_N_TIMERS_LSB},
                                           Field{"evt_words", true, MBX_CAPS_EVT_WORDS_LOG2_LSB}),
                         [](const ::testing::TestParamInfo<Field>& info) { return info.param.name; });

TEST(LoopRun, U3TurnsForEverAndSleepsWhenNothingIsOwed) {
    static ctrl_loop loop;
    NiceMock<MockMbxHal> hal;
    answer_contract(hal);
    ASSERT_TRUE(mbx_open());
    ctrl_loop_init(&loop);
    std::jmp_buf out;
    EXPECT_CALL(hal, wait()).Times(3);
    hal.escape_after(3, &out);
    if (setjmp(out) == 0) {
        ctrl_loop_run(&loop);
    }
    EXPECT_EQ(loop.stats.passes, 3u) << "U3 every turn is one pass, and a pass that owed nothing then sleeps";
}

}  // namespace
