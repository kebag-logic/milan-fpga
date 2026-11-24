#include "Vtop.h"
#include <cstdio>
int main() { Vtop t; t.pcm_chans_i = 0x86; t.sel_i = 1; for (int i = 0; i < 2; ++i) { t.clk_i = 0; t.eval(); t.clk_i = 1; t.eval(); } std::printf("a %d b %d c %d\n", t.a_o, t.b_o, t.c_o); }
