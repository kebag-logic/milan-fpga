#include <verilated.h>
#include "Vdut.h"
#include <cstdio>
#include <cstring>
int main(int argc, char** argv) {
  const auto ctx = std::make_unique<VerilatedContext>();
  ctx->commandArgs(argc, argv);
  const char* mode = "ok";
  const char* arg = ctx->commandArgsPlusMatch("mode=");
  if (arg && *arg) mode = arg + 6;
  auto d = std::make_unique<Vdut>(ctx.get());
  auto tick = [&]() { d->clk = 0; d->eval(); ctx->timeInc(5); d->clk = 1; d->eval(); ctx->timeInc(5); };
  d->rst_n = 0; d->a = 0; d->b = 0; tick(); tick(); d->rst_n = 1; tick();
  if (!strcmp(mode, "ab")) { d->a = 1; d->b = 1; tick(); tick(); }
  if (!strcmp(mode, "bone")) { d->a = 1; d->b = 0; tick(); d->a = 0; d->b = 1; tick(); tick(); }
  printf("mode=%s done\n", mode);
  d->final();
  return 0;
}
