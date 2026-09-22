#include <verilated.h>
#include "Vdut.h"
#include <cstdio>
#include <map>
#include <string>
static std::map<std::string,int> calls, nonvac;
extern "C" void witness_flag(const char* name, svBit nv) { calls[name]++; if (nv) nonvac[name]++; }
int main(int argc, char** argv) {
  const auto ctx = std::make_unique<VerilatedContext>();
  ctx->commandArgs(argc, argv);
  auto d = std::make_unique<Vdut>(ctx.get());
  int clocks = 0, ante = 0, nv_tb = 0; bool prev = false;
  auto tick = [&]() { bool cur = d->rst_n && d->a && !d->b; if (prev && d->rst_n) nv_tb++; prev = cur; if (cur) ante++;
     d->clk = 0; d->eval(); ctx->timeInc(5); d->clk = 1; d->eval(); ctx->timeInc(5); clocks++; };
  d->rst_n = 0; d->a = 0; d->b = 0; tick(); tick(); d->rst_n = 1; tick();
  d->a = 1; d->b = 0; tick(); tick(); tick(); d->b = 1; tick(); d->a = 0; d->b = 0; tick(); tick(); tick();
  d->a = 1; tick(); d->b = 1; tick(); d->a = 0; d->b = 0; tick(); tick();
  d->a = 1; tick(); d->rst_n = 0; d->a = 0; tick(); d->rst_n = 1; tick(); tick();
  printf("clocks=%d antecedent_cycles=%d nonvacuous_tb=%d\n", clocks, ante, nv_tb);
  for (auto& kv : calls) printf("calls %s %d nonvacuous %d\n", kv.first.c_str(), kv.second, nonvac[kv.first]);
  d->final();
  return 0;
}
