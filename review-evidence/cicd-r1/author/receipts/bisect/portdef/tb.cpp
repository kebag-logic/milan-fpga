#include "Vtop.h"
#include <cstdio>
int main() { Vtop t; t.pcm_chans_i = 0x86; for (int sel = 0; sel < 2; ++sel) { t.sel_i = sel; for (int i = 0; i < 2; ++i) { t.clk_i = 0; t.eval(); t.clk_i = 1; t.eval(); } std::printf("sel %d q %d\n", sel, t.q_o); } }
