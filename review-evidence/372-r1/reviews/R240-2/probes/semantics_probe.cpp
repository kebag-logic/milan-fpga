#include "Vsemantics_probe.h"
#include "Vsemantics_probe__Dpi.h"
#include <verilated.h>
#include <cstdio>
#include <map>
#include <string>
#include <vector>

struct Event { unsigned edge; std::string rule; bool value; };
static unsigned edge = 0;
static std::vector<Event> events;
void probe_result(const char* rule, svBit value) {
    events.push_back({edge, rule, value != 0});
    std::printf("edge=%u rule=%s value=%d\n", edge, rule, value);
}
void axis_sva_witness(const char* rule, svBit flag) { probe_result(rule, flag); }

int main(int argc, char** argv) {
    VerilatedContext context;
    context.commandArgs(argc, argv);
    Vsemantics_probe top(&context);
    struct Stimulus { unsigned rst, valid, ready, data; };
    const Stimulus stimulus[] = {
        {0,0,0,0}, {1,0,0,0}, {1,1,0,1}, {0,1,0,2},
        {1,0,0,3}, {1,1,0,4}, {1,1,0,4}, {0,0,0,5},
        {0,1,0,6}, {1,0,0,7}, {1,1,0,8}, {1,1,1,8}
    };
    for (const auto& s : stimulus) {
        ++edge;
        top.clk = 0;
        top.rst_n = s.rst; top.valid = s.valid; top.ready = s.ready;
        top.data = s.data; top.keep = 1; top.last = 0;
        top.eval();
        top.clk = 1; top.eval(); context.timeInc(1000);
    }
    const std::map<unsigned, bool> expected = {
        {2,0}, {3,0}, {5,0}, {6,0}, {7,1}, {10,0}, {11,0}, {12,1}
    };
    unsigned failures = 0;
    const char* rules[] = {"ap_tvalid_held_until_handshake", "ap_tdata_stable_until_handshake",
                          "ap_tkeep_stable_until_handshake", "ap_tlast_stable_until_handshake"};
    for (const auto* rule : rules) {
        std::map<unsigned, bool> got;
        for (const auto& e : events) if (e.rule == rule) got.emplace(e.edge, e.value);
        if (got != expected) { ++failures; std::printf("FAIL checker rule %s\n", rule); }
    }
    for (const auto* rule : {"past_one", "stable_one"}) {
        unsigned count = 0;
        for (const auto& e : events) if (e.rule == rule) {
            ++count;
            if (e.value != (e.edge > 1)) ++failures;
        }
        if (count != 12) ++failures;
    }
    for (unsigned at : {5U, 10U}) {
        bool seen = false;
        for (const auto& e : events) if (e.rule == "bad_flag" && e.edge == at && e.value) seen = true;
        if (!seen) ++failures;
    }
    for (const auto& e : events) if (e.rule == "unexpected_fail") ++failures;
    if (context.errorCount()) ++failures;
    std::printf("SEMANTICS %s: 4 exact reset-action timelines; first past/stable zero; bad flags on release; failures=%u\n",
                failures ? "FAIL" : "PASS", failures);
    top.final();
    return failures ? 1 : 0;
}
