#include <verilated.h>
#include "Vdut.h"
#if __has_include("Vdut__Dpi.h")
#include "Vdut__Dpi.h"
#define HAVE_DPI_HDR 1
#else
#define HAVE_DPI_HDR 0
#endif
#include <svdpi.h>
#include <cstdio>
extern "C" void sva_witness(const char* rule, svBit nv) { std::printf("witness %s %d\n", rule, static_cast<int>(nv)); }
int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  auto d = std::make_unique<Vdut>();
  std::printf("dpi header present=%d scope=%s\n", HAVE_DPI_HDR, svGetScopeFromName("TOP.dut.u_sva") ? "found" : "NULL");
  d->final();
  return 0;
}
