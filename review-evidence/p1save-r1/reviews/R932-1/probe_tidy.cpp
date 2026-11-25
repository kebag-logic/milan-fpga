#include <iostream>
#include "fw_gtest.hpp"
#include "nvm_c.hpp"
#include "nvm_suite.hpp"
FW_TALLY_LABEL("maintenance capture fault probe");

namespace nvm_test {
namespace {
std::vector<std::string> prefix() {
    unsigned rb = static_cast<unsigned>(fx().num("bind_rid"));
    return {"--slot-a", "a", "--slot-b", "b", "--boot", "--set", set_word(rb, value(rb, 7)),
            "--until-idle", "--until-phase", std::to_string(NVM_P_CAPTURE)};
}
Files initial() { return fx().files({{"a", "slot/g5+full"}, {"b", "golden@6/minor1"}}); }

TEST_P(NvmBoth, maintenance_capture_first_failure) {
    Files f = initial();
    auto args = prefix();
    unsigned rb = static_cast<unsigned>(fx().num("bind_rid2"));
    args.insert(args.end(), {"--set", set_word(rb, value(rb, 8)), "--fault", "erase-refuse:1",
                            "--until-phase", std::to_string(NVM_P_IDLE)});
    const auto r = go(port(), f, args, {"ls_refused"});
    std::cout << "CAPTURED_CHANGE_FIRST_FAILURE " << r.text() << '\n';
    EXPECT_EQ(r.at("pending"), 1);
    EXPECT_EQ(r.at("stale"), 1) << "A captured change failed to reach durable storage";
    EXPECT_EQ(r.at("attempts"), 1) << "The failed captured work set owes one attempt";
}

TEST_P(NvmBoth, maintenance_capture_retry_count) {
    Files f = initial();
    auto args = prefix();
    unsigned rb = static_cast<unsigned>(fx().num("bind_rid2"));
    args.insert(args.end(), {"--set", set_word(rb, value(rb, 8)), "--fault", "erase-refuse:99", "--until-idle"});
    const auto r = go(port(), f, args, {"ls_refused"});
    std::cout << "CAPTURED_CHANGE_ALL_FAILURES " << r.text() << '\n';
    for (std::size_t i = 0; i < r.fail_at.size(); ++i) std::cout << "FAILURE_US " << i << ' ' << r.fail_at[i] << '\n';
    EXPECT_EQ(r.at("failed"), 3) << "DR2c allows three attempts including the first";
    if (r.fail_at.size() > 1) {
        EXPECT_GE(r.fail_at[1] - r.fail_at[0], 1000000u);
    }
}

TEST_P(NvmBoth, maintenance_without_change_control) {
    Files f = initial();
    auto args = prefix();
    args.insert(args.end(), {"--fault", "erase-refuse:1", "--until-phase", std::to_string(NVM_P_IDLE)});
    const auto r = go(port(), f, args, {"ls_refused"});
    std::cout << "EMPTY_MAINTENANCE_CONTROL " << r.text() << '\n';
    EXPECT_EQ(r.at("pending"), 0);
    EXPECT_EQ(r.at("stale"), 0);
    EXPECT_EQ(r.at("attempts"), 0);
}
}
}
