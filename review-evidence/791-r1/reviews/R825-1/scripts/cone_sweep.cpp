// cone_sweep.cpp: drive pma_cone (cone_extract.py) at every word address of the 32-bit space and compare the
// fetch and word-load fault terms with the SoC's regions (spec.h: FETCH_OK / LOAD_OK ranges). Independent of
// the PR's decode.py. Prints admitted spans and the first mismatches; exit 0 when both ports are exact.
#include "Vpma_cone.h"
#include "spec.h"
#include <cstdint>
#include <cstdio>
static bool in(const Range* r, int n, uint64_t a) { for (int i = 0; i < n; ++i) if (a >= r[i].lo && a < r[i].hi) return true; return false; }
int main() {
  Vpma_cone m;
  m.LsuCachelessPlugin_logic_onPma_port_cmd_size = 2;  // word
  m.LsuCachelessPlugin_logic_onPma_port_cmd_op = 0;    // load
  uint64_t bad[2] = {0, 0}; bool prev[2] = {false, false}; uint64_t start[2] = {0, 0};
  const char* nm[2] = {"fetch", "load"};
  for (uint64_t a = 0; a < (1ull << 32); a += 4) {
    m.FetchL1Plugin_logic_ctrl_pmaPort_cmd_address = (uint32_t)a;
    m.LsuCachelessPlugin_logic_onPma_port_cmd_address = (uint32_t)a;
    m.eval();
    bool adm[2] = {!m.FetchL1Plugin_logic_ctrl_pmaPort_rsp_fault_o, !m.LsuCachelessPlugin_logic_onPma_port_rsp_fault_o};
    bool want[2] = {in(FETCH_OK, N_FETCH, a), in(LOAD_OK, N_LOAD, a)};
    for (int p = 0; p < 2; ++p) {
      if (adm[p] != want[p] && bad[p]++ < 3)
        printf("MISMATCH %s 0x%08llx admitted=%d want=%d\n", nm[p], (unsigned long long)a, adm[p], want[p]);
      if (adm[p] && !prev[p]) start[p] = a;
      if (!adm[p] && prev[p]) printf("SPAN %s [0x%08llx, 0x%08llx)\n", nm[p], (unsigned long long)start[p], (unsigned long long)a);
      prev[p] = adm[p];
    }
  }
  for (int p = 0; p < 2; ++p) {
    if (prev[p]) printf("SPAN %s [0x%08llx, 0x100000000)\n", nm[p], (unsigned long long)start[p]);
    printf("RESULT %s: %llu word address(es) of 2^30 differ from the SoC regions -> %s\n", nm[p],
           (unsigned long long)bad[p], bad[p] ? "INEXACT" : "EXACT");
  }
  return (bad[0] || bad[1]) ? 1 : 0;
}
