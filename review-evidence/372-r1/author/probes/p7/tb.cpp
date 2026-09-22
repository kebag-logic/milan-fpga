#include <verilated.h>
#include "Vdut.h"
#include "Vdut__Dpi.h"
#include <svdpi.h>
#include <cstdio>
#include <map>
#include <string>
struct Ledger { std::map<std::string, std::pair<int,int>> m; };
static char key_token;
void sva_witness(const char* rule, svBit nv) {
  svScope s = svGetScope();
  auto* l = static_cast<Ledger*>(svGetUserData(s, &key_token));
  if (!l) { printf("NO LEDGER for scope %s rule %s\n", svGetNameFromScope(s), rule); return; }
  auto& e = l->m[std::string(svGetNameFromScope(s)) + ":" + rule];
  e.first++; if (nv) e.second++;
}
int main(int argc, char** argv) {
  const auto ctx = std::make_unique<VerilatedContext>();
  ctx->commandArgs(argc, argv);
  auto d = std::make_unique<Vdut>(ctx.get());
  Ledger ledger;
  const char* names[] = {"TOP.dut.u_sva", "TOP.dut.u_sva.u_a", "TOP.dut.u_sva.u_b", "TOP.dut.u_nope"};
  for (auto n : names) { svScope s = svGetScopeFromName(n); printf("scope %s -> %s\n", n, s ? "found" : "NULL"); if (s) svPutUserData(s, &key_token, &ledger); }
  auto tick = [&]() { d->clk = 0; d->eval(); ctx->timeInc(5); d->clk = 1; d->eval(); ctx->timeInc(5); };
  d->rst_n = 0; d->a = 0; d->b = 0; tick(); tick(); d->rst_n = 1; tick();
  d->a = 1; d->b = 0; tick(); tick(); tick(); d->b = 1; tick(); d->a = 0; d->b = 0; tick(); tick();
  d->a = 1; d->b = 0; tick(); d->b = 1; tick(); d->a = 0; d->b = 0; tick(); tick();
  for (auto& kv : ledger.m) printf("witness %s calls=%d nonvacuous=%d\n", kv.first.c_str(), kv.second.first, kv.second.second);
  d->final();
  return 0;
}
