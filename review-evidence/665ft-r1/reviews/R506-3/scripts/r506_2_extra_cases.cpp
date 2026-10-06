// R506-2 probe: listener behaviours the README states that tally_cases.cpp does not plant.
#include <gtest/gtest.h>
#include <csignal>
#include <cstdlib>
#include "fw_gtest.hpp"
FW_TALLY_LABEL("firmware tally listener (planted cases)");
namespace {
volatile int one = 1;
class FailingEnv final : public ::testing::Environment {
 public:
    void SetUp() override {
        if (std::getenv("R506_ENV_FAIL") != nullptr) ADD_FAILURE() << "a planted failure in a global environment";
    }
};
::testing::Environment* const env = ::testing::AddGlobalTestEnvironment(new FailingEnv);
}  // namespace
TEST(Pass, One) { EXPECT_EQ(one, 1); }
TEST(Sig, Fpe) { static_cast<void>(std::raise(SIGFPE)); }
TEST(Sig, Bus) { static_cast<void>(std::raise(SIGBUS)); }
TEST(Sig, Ill) { static_cast<void>(std::raise(SIGILL)); }
class TearDownFails : public ::testing::Test {
 protected:
    static void TearDownTestSuite() { ADD_FAILURE() << "a planted failure in a suite's tear-down"; }
};
TEST_F(TearDownFails, Body) { EXPECT_EQ(one, 1); }
TEST(DISABLED_WholeSuite, NeverRuns) { EXPECT_EQ(one, 1); }
