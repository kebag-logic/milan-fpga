// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// test_nvm_shapes.cpp - the store built against a shape header the builder
// does not emit (#665 lane FT): the shipping 1x1 shape with one constant
// changed (nvm_bench.DOCTORED), so a branch only such a build reaches runs.
// Built twice, one binary per edit, and each binary runs its own test:
//
//   NVM_DOCTORED_MAPIN   an input map of 256 entries, which the codec's byte
//                        table cannot hold: the record walk disagrees with
//                        the compile-time sizes, and the store disables
//                        persistence (DR3b);
//   NVM_DOCTORED_NONAME  a shape with no name record: the D3 walk reaches its
//                        end without passing a name, and the settle step runs
//                        there, once, after the last map.

#include <gtest/gtest.h>

#include "fw_gtest.hpp"
#include "nvm_c.hpp"
#include "nvm_suite.hpp"

#if defined(NVM_DOCTORED_MAPIN)
FW_TALLY_LABEL("ctrl_nvm saved-state store, a build whose record walk and sizes disagree");
#elif defined(NVM_DOCTORED_NONAME)
FW_TALLY_LABEL("ctrl_nvm saved-state store, a shape with no name record");
#endif

namespace nvm_test {
namespace {

#if defined(NVM_DOCTORED_MAPIN)

// DR3b: a build whose record walk and sizes disagree reads no slot, writes
// none, and runs on its defaults; AECP is released over a proven model and
// held over an unproven one.
TEST_F(NvmModel, shape_mismatch_disables_persistence) {
    ASSERT_EQ(nvm_shape_consistent(), 0) << "(the doctored build's walk disagrees with its sizes)";
    const nvm_rec r = nvm_rec_first();
    Files f;
    Result res = go(port(), f, {"--blank", "--boot", "--set", set_word(r.id, Bytes(r.plen, 0x5Au)), "--run-ms", "3000"});
    EXPECT_TRUE(res.at("terminal") == NVM_T_DEFAULTS && res.at("cause") == NVM_C_SHAPE && res.at("releases") == 1 &&
                res.at("phase") == NVM_P_OFF && res.at("steps") == 0 && res.at("erases") == 0 &&
                res.at("sm_applies") == 0 && res.at("dirty") == 0)
        << "a walk that disagrees with the sizes disables persistence: " << res.text();
    res = go(port(), f, {"--blank", "--not-ready", "--boot"});
    EXPECT_TRUE(res.at("terminal") == NVM_T_CLOSED && res.at("cause") == NVM_C_MODEL && res.at("releases") == 0 &&
                res.at("phase") == NVM_P_OFF)
        << "and over an unproven model nothing is released: " << res.text();
}

#elif defined(NVM_DOCTORED_NONAME)

// The settle step judges every restored format against the final maps once,
// before the first name; with no name it runs after the last record, and a
// settle that cannot be judged rolls the D3 walk back there.
TEST_F(NvmModel, settle_after_the_last_record) {
    Files f;
    Result r = go(port(), f, {"--blank", "--boot", "--set-pattern", "1", "--until-idle", "--dump-slot-a", "a.bin"});
    ASSERT_EQ(r.at("ok"), 1) << "(a container of the doctored shape is committed): " << r.text();
    r = go(port(), f, {"--slot-a", "a.bin", "--boot"});
    EXPECT_TRUE(r.at("terminal") == NVM_T_COMPLETE && r.at("sm_settles") == 1 && r.at("applied") == NVM_N_REC)
        << "the settle step runs once, after the last record: " << r.text();
    r = go(port(), f, {"--slot-a", "a.bin", "--settle-fault", "--boot"});
    EXPECT_TRUE(r.at("terminal") == NVM_T_DEFAULTS && r.at("cause") == NVM_C_SETTLE && r.at("sm_rollbacks") == 1 &&
                r.at("releases") == 1)
        << "a settle that cannot be judged there rolls the D3 walk back: " << r.text();
}

#endif

}  // namespace
}  // namespace nvm_test
