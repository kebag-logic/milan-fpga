// Disposable reviewer probe: counts the bound checker's DPI witness calls when the
// checker is bound onto the mux instance inside ptp_ts_top (original sim_main.cpp).
#include "svdpi.h"
#include <cstdio>
#include <map>
#include <string>
namespace {
struct Tally { unsigned long long calls = 0, nonvacuous = 0; };
struct Ledger {
    std::map<std::string, Tally> tallies;
    ~Ledger() {
        for (const auto& [key, tally] : tallies)
            std::printf("probe-witness %s calls=%llu nonvacuous=%llu\n", key.c_str(), tally.calls, tally.nonvacuous);
        std::printf("probe-witness pairs=%zu\n", tallies.size());
    }
};
Ledger ledger;
}
extern "C" void axis_sva_witness(const char* rule_name, svBit nonvacuous) {
    Tally& tally = ledger.tallies[std::string(svGetNameFromScope(svGetScope())) + "." + rule_name];
    ++tally.calls;
    if (nonvacuous) ++tally.nonvacuous;
}
