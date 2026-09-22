#include <verilated.h>
#include "Vdut.h"
#include <cstdio>
#include <cstring>
#include <map>
#include <string>
static std::map<std::string,int> hits;
extern "C" void witness(const char* name) { hits[name]++; }
int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  const char* mode = "ok";
  const char* arg = Verilated::commandArgsPlusMatch("mode=");
  if (arg && *arg) mode = arg + 6;
  Vdut* d = new Vdut;
  auto tick = [&]() { d->clk = 0; d->eval(); d->clk = 1; d->eval(); };
  d->rst_n = 0; d->a = 0; d->b = 0; tick(); tick();
  d->rst_n = 1; tick();
  // stall: a=1 b=0 for 3 cycles then handshake b=1
  d->a = 1; d->b = 0; tick(); tick(); tick();
  d->b = 1; tick(); d->a = 0; d->b = 0; tick();
  if (!strcmp(mode, "bone")) { d->a = 1; d->b = 0; tick(); d->a = 0; d->b = 1; tick(); tick(); }
  if (!strcmp(mode, "drop")) { d->a = 1; d->b = 0; tick(); d->a = 0; tick(); tick(); }
  if (!strcmp(mode, "reset_after")) { d->a = 1; d->b = 0; tick(); d->rst_n = 0; d->a = 0; tick(); d->rst_n = 1; tick(); tick(); }
  if (!strcmp(mode, "reset_before")) { d->rst_n = 0; d->a = 1; d->b = 0; tick(); d->rst_n = 1; d->a = 0; tick(); tick(); }
  printf("mode=%s done; gotError=%d\n", mode, (int)Verilated::gotError());
  for (auto& kv : hits) printf("hit %s %d\n", kv.first.c_str(), kv.second);
  d->final(); delete d;
  return 0;
}
