#include <verilated.h>
#include "Vtop.h"
#include <cstdio>
int main(int argc, char** argv) {
  const auto ctx = std::make_unique<VerilatedContext>();
  ctx->commandArgs(argc, argv);
  auto d = std::make_unique<Vtop>(ctx.get());
  int cyc = 0;
  auto tick = [&]() { d->clk = 0; d->eval(); ctx->timeInc(5); d->clk = 1; d->eval(); ctx->timeInc(5); cyc++;
                      if (ctx->errorCount() > 0) { printf("harness: error count %d after cycle %d, stopping\n", ctx->errorCount(), cyc); d->final(); std::exit(3); } };
  d->rst_n = 0; d->a = 0; d->b = 0; tick(); tick(); d->rst_n = 1; tick();
  d->a = 1; d->b = 1; tick(); tick(); tick();
  printf("end without stop\n");
  d->final();
  return 0;
}
