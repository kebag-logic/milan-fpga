#include <verilated.h>
#include "Vdut.h"
#include <cstdio>
#include <map>
#include <string>
static std::map<std::string,int> hits;
extern "C" void witness(const char* name) { hits[name]++; }
int main(int argc, char** argv) {
  const auto ctx = std::make_unique<VerilatedContext>();
  ctx->commandArgs(argc, argv);
  auto d = std::make_unique<Vdut>(ctx.get());
  int clocks = 0, ante = 0;
  auto tick = [&]() { if (d->rst_n && d->a && !d->b) ante++; d->clk = 0; d->eval(); ctx->timeInc(5); d->clk = 1; d->eval(); ctx->timeInc(5); clocks++; };
  d->rst_n = 0; d->a = 0; d->b = 0; tick(); tick(); d->rst_n = 1; tick();
  d->a = 1; d->b = 0; tick(); tick(); tick(); d->b = 1; tick(); d->a = 0; d->b = 0; tick(); tick(); tick();
  d->a = 1; tick(); d->b = 1; tick(); d->a = 0; d->b = 0; tick(); tick();
  printf("clocks=%d antecedent_cycles=%d\n", clocks, ante);
  for (auto& kv : hits) printf("hit %s %d\n", kv.first.c_str(), kv.second);
  d->final();
  return 0;
}
