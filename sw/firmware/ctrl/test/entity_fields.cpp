// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// entity_fields.cpp - the ENTITY_AVAILABLE the ADP slice builds from one
// shape's generated entity header (adp_entity_gen.h, from adp_entity.py),
// field by field against what the fabric is programmed and compiled with for
// the same shape (#665 lanes F0 and FT). Built once per shipped config.
//
// entity_expect_gen.hpp is written by the host test's entity arm
// (ctrl_arms.py) from the fabric's own sources: boot_policy.fabric_constants,
// the builder's ADP shape include and the processor's ADP_ENTITY_CAPS_C, with
// each field's place in the 82-byte frame (IEEE 1722.1-2021 Figure 6-1, after
// the 14-byte Ethernet header). Nothing here restates a value.

#include <gtest/gtest.h>

#include <cstddef>
#include <cstdint>
#include <ios>

#include "adp.h"
#include "adp_entity_gen.h"
#include "entity_expect_gen.hpp"
#include "fw_gtest.hpp"

FW_TALLY_LABEL(entity_expect::kLabel);

namespace {

bool no_send(void*, unsigned, const std::uint8_t*, std::size_t) {
    return false;
}
void no_timer(void*, unsigned, std::uint32_t) {}
void no_stop(void*, unsigned) {}

void zero_gptp(void*, unsigned, std::uint64_t* gm_id, std::uint8_t* domain) {
    *gm_id = 0;
    *domain = 0;
}

bool link_down(void*, unsigned) {
    return false;
}
std::uint32_t zero_seed(void*) {
    return 0;
}

//! The ENTITY_AVAILABLE this shape's entity header makes the ADP slice build.
const std::uint8_t* firmware_frame() {
    static const adp_entity entity = ADP_ENTITY_GEN_INIT;
    static const adp_ports ports = {nullptr, no_send, no_timer, no_stop, zero_gptp, link_down, zero_seed};
    static std::uint8_t frame[ADP_FRAME_BYTES];
    adp a;
    adp_init(&a, &entity, &ports, 0, 0);
    adp_build(&a, ADP_MSG_ENTITY_AVAILABLE, 0, frame);
    return frame;
}

class EntityField : public ::testing::TestWithParam<entity_expect::Field> {};

TEST_P(EntityField, MatchesTheFabric) {
    const entity_expect::Field& f = GetParam();
    const std::uint8_t* frame = firmware_frame();
    std::uint64_t got = 0;
    for (unsigned k = 0; k < f.bytes; ++k) {
        got = (got << 8) | frame[f.at + k];
    }
    EXPECT_EQ(got, f.want) << entity_expect::kConfig << ": " << f.name << " is 0x" << std::hex << std::uppercase << got
                           << " in the firmware ADPDU, 0x" << f.want << " in the fabric";
}

INSTANTIATE_TEST_SUITE_P(Fabric, EntityField, ::testing::ValuesIn(entity_expect::kFields),
                         [](const ::testing::TestParamInfo<entity_expect::Field>& info) { return info.param.name; });

}  // namespace
