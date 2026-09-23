// Reviewer disposable probe driver: one line per action-block call, tagged with the edge index.
#include <verilated.h>
#include "Vsem_probe.h"
#include "Vsem_probe__Dpi.h"
#include <cstdio>
static int g_edge = -1;
void note(const char* name, int passed, svBit flag) {
    std::printf("edge %2d %-14s %s flag=%d\n", g_edge, name, passed ? "PASS-action" : "FAIL-action", flag ? 1 : 0);
}
int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    Vsem_probe top;
    //            edge:   0  1  2  3  4  5  6  7  8  9 10
    const int rst[]  = { 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1 };
    const int av[]   = { 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0 };
    const int bv[]   = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0 };
    const char* why[] = {"reset", "reset", "run, a=1 (attempt starts)", "RESET edge completes the edge-2 attempt, b=0",
                         "RESET edge, a=1 (attempt starts in reset)", "run, b=0: completes the edge-4 attempt",
                         "run, a=1", "run, b=0: completes edge-6 attempt (must FAIL)", "run, a=1",
                         "run, b=1: completes edge-8 attempt (non-vacuous pass)", "run, idle"};
    for (int e = 0; e < 11; ++e) {
        top.rst_n = rst[e]; top.a = av[e]; top.b = bv[e];
        top.clk = 0; top.eval();
        g_edge = e;
        std::printf("-- edge %2d: %s\n", e, why[e]);
        top.clk = 1; top.eval();
        Verilated::threadContextp()->timeInc(1);
    }
    return 0;
}
