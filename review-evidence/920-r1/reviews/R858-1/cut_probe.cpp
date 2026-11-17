// Reviewer probe: power loss at every service boundary of joined/chained saves.
#include "nvm_suite.hpp"
#include "nvm_c.hpp"
#include <set>
#include <cstdio>
namespace fw_test { const char* tally_label() { return "joined and chained save power cuts"; } }
namespace nvm_test {
static std::string num(long long n) { return std::to_string(n); }
static std::vector<std::string> concat(std::vector<std::string> a, std::initializer_list<std::string> b) {
    a.insert(a.end(), b.begin(), b.end());
    return a;
}
TEST_F(NvmModel, JoinedAndNextSaveCutAtEveryStep) {
    const auto ids = rids();
    const unsigned low = ids.front(), high = ids.back();
    const auto golden = fx().payloads("golden");
    const auto first = with(golden, {{low, value(low, 71)}, {high, value(high, 72)}});
    const auto second = with(first, {{high, value(high, 73)}});
    const std::vector<std::string> start = {
        "--slot-b", "g", "--boot",
        "--set", set_word(high, value(high, 72)),
        "--until-phase", num(NVM_P_CAPTURE), "--service", "1",
        "--set", set_word(low, value(low, 71)),
        "--set", set_word(high, value(high, 73))};
    for (const Port port : {Port::Model, Port::Litespi}) {
        Files reference = fx().files({{"g", "golden@5"}});
        const auto before = go(port, reference, start);
        const auto complete = go(port, reference, concat(start, {"--until-idle"}));
        ASSERT_EQ(complete.at("ok"), 2);
        const auto limit = static_cast<unsigned>(complete.at("steps") - before.at("steps") + 1);
        ASSERT_LT(limit, 10000u);
        std::set<long long> phases, sequences;
        unsigned cases = 0;
        for (unsigned cut = 0; cut < limit; ++cut) {
            SCOPED_TRACE(::testing::Message() << port_name(port) << " cut=" << cut);
            Files f = fx().files({{"g", "golden@5"}});
            const auto r = go(port, f, concat(start, {
                "--service", num(cut), "--dump-slot-a", "a", "--dump-slot-b", "b"}));
            phases.insert(r.at("phase"));
            const auto boot = go(port, f, {"--slot-a", "a", "--slot-b", "b", "--boot", "--dump-state", "state"});
            ASSERT_EQ(boot.at("terminal"), NVM_T_COMPLETE);
            const auto seq = boot.at("seq");
            ASSERT_GE(seq, 5); ASSERT_LE(seq, 7);
            sequences.insert(seq);
            expect_state(f, "state", seq == 5 ? golden : seq == 6 ? first : second,
                         "complete snapshot after the power loss");
            ++cases;
            if (r.at("ok") == 2 && r.at("phase") == NVM_P_IDLE) {
                EXPECT_EQ(r.at("dirty"), 0); EXPECT_EQ(r.at("pending"), 0);
                break;
            }
        }
        EXPECT_EQ(cases, limit);
        EXPECT_EQ(sequences, (std::set<long long>{5, 6, 7}));
        for (int phase = NVM_P_IDLE; phase <= NVM_P_VERIFY; ++phase)
            EXPECT_TRUE(phases.count(phase)) << "unexamined phase " << phase;
        std::printf("CUT RECEIPT port=%s boundaries=%u distinct_snapshots=%zu distinct_phases=%zu\n",
                    port_name(port), cases, sequences.size(), phases.size());
    }
}
}
