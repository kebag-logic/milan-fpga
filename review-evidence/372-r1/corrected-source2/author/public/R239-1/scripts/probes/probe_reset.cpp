// R239 scratch probe: the REAL axis_mux_rr_2in_1out with the REAL bound
// checker (tb/common/sva, unmodified), driven through reset edge cases the
// suite harness does not drive. Prints every assertion failure (the model's
// own %Error lines) and a per-edge record of every pass-action call.
//
//   R1  one-edge reset while m is stalled and the source KEEPS TVALID and its
//       payload through that reset edge (a synchronously reset upstream
//       drops TVALID only after the edge), TVALID low from the next edge.
//   R2  one-edge reset landing on an owner's TLAST handshake edge.
//   R3  two-edge reset while stalled, source keeps TVALID for both edges.
//
// Exit 0 always; the verdict is read from the printed lines.
#include <verilated.h>
#include "Vaxis_mux_rr_2in_1out.h"
#include "Vaxis_mux_rr_2in_1out__Dpi.h"
#include <cstdio>
#include <cstring>
#include <map>
#include <string>

static std::uint64_t g_cycle = 0;
static bool g_trace = false;
static std::map<std::string, std::uint64_t> g_calls;

void axis_sva_witness(const char* rule_name, svBit nonvacuous) {
    const char* scope = svGetNameFromScope(svGetScope());
    std::string key = std::string(scope) + "." + rule_name + (nonvacuous ? " flag=1" : " flag=0");
    ++g_calls[key];
    if (g_trace && std::strstr(rule_name, "ap_") == rule_name) {
        std::printf("    edge %llu pass-action %s.%s flag=%d\n", (unsigned long long)g_cycle, scope, rule_name,
                    nonvacuous ? 1 : 0);
    }
}

struct Pins {
    int rst_n = 0;
    int s0_valid = 0, s0_last = 0; std::uint64_t s0_data = 0; int s0_keep = 0;
    int s1_valid = 0, s1_last = 0; std::uint64_t s1_data = 0; int s1_keep = 0;
    int m_ready = 1;
};

static void tick(Vaxis_mux_rr_2in_1out* top, const Pins& p, const char* note) {
    top->rst_n = p.rst_n;
    top->s0_tvalid = p.s0_valid; top->s0_tdata = p.s0_data; top->s0_tkeep = p.s0_keep; top->s0_tlast = p.s0_last;
    top->s1_tvalid = p.s1_valid; top->s1_tdata = p.s1_data; top->s1_tkeep = p.s1_keep; top->s1_tlast = p.s1_last;
    top->m_tready = p.m_ready;
    top->clk = 0;
    top->eval();
    std::printf("  edge %2llu %-44s rst_n=%d s0v=%d s0rdy=%d m_v=%d m_rdy=%d\n", (unsigned long long)g_cycle, note,
                p.rst_n, top->s0_tvalid, top->s0_tready, top->m_tvalid, top->m_tready);
    top->clk = 1;
    top->eval();
    Verilated::threadContextp()->timeInc(1000);
    ++g_cycle;
}

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    const char* which = Verilated::commandArgsPlusMatch("case=");
    std::string c = which[0] ? std::string(which).substr(6) : "R1";
    g_trace = Verilated::commandArgsPlusMatch("trace")[0] != '\0';
    auto* top = new Vaxis_mux_rr_2in_1out;
    for (const char* s : {"TOP.axis_mux_rr_2in_1out.u_sva", "TOP.axis_mux_rr_2in_1out.u_sva.u_s0_stimulus",
                          "TOP.axis_mux_rr_2in_1out.u_sva.u_s1_stimulus", "TOP.axis_mux_rr_2in_1out.u_sva.u_m_dut"}) {
        std::printf("scope %s %s\n", s, svGetScopeFromName(s) ? "present" : "ABSENT");
    }
    std::printf("case %s\n", c.c_str());
    Pins p;
    p.rst_n = 0;
    for (int i = 0; i < 4; ++i) tick(top, p, "reset");
    p.rst_n = 1;
    tick(top, p, "released, idle");
    // s0 offers a 3-beat packet; the sink takes beat 0 then stalls beat 1.
    p.s0_valid = 1; p.s0_data = 0x11; p.s0_keep = 0xFF; p.s0_last = 0;
    tick(top, p, "s0 offers beat0 (grant edge)");
    tick(top, p, "beat0 taken");
    p.s0_data = 0x22;
    if (c == "R2") {
        tick(top, p, "beat1 taken");
        p.s0_data = 0x33; p.s0_last = 1;
        p.rst_n = 0;
        tick(top, p, "RESET on beat2 TLAST handshake edge");
        p.rst_n = 1; p.s0_valid = 0; p.s0_last = 0;
        tick(top, p, "released; source was reset");
        tick(top, p, "idle");
    } else {
        p.m_ready = 0;
        tick(top, p, "beat1 stalled");
        tick(top, p, "beat1 stalled");
        p.rst_n = 0;  // source keeps TVALID and payload at this reset edge
        tick(top, p, "RESET edge, s0 still offering beat1");
        if (c == "R3") tick(top, p, "RESET edge 2, s0 still offering beat1");
        p.rst_n = 1; p.s0_valid = 0;  // the upstream was reset with it
        tick(top, p, "released; s0 TVALID low, m stalled");
        tick(top, p, "idle");
        p.m_ready = 1;
        tick(top, p, "idle, sink ready");
    }
    std::printf("errors reported by the model: %u\n", Verilated::threadContextp()->errorCount());
    for (const auto& [k, v] : g_calls) {
        if (k.find(".ap_") != std::string::npos) std::printf("calls %-96s %llu\n", k.c_str(), (unsigned long long)v);
    }
    top->final();
    delete top;
    return 0;
}
