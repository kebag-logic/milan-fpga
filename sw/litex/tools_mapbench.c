/* Per-4KB-page cost: (A) cold memcpy of a page vs (B) map-side page cycle
   (touch-fault + MADV_DONTNEED zap) — proxy for TCP_ZEROCOPY_RECEIVE's
   vm_insert+zap machinery. If B << A, page-flipping beats copying on this core. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <sys/mman.h>
#define PG 4096
static double now(){ struct timespec t; clock_gettime(CLOCK_MONOTONIC,&t); return t.tv_sec+t.tv_nsec/1e9; }
int main(){
  int N=512, iters=20;
  /* A: cold copy — src working set 32 MB >> L2 so every page read is DRAM-cold */
  size_t WS=32u<<20; char *src=malloc(WS), *dst=malloc(PG);
  memset(src,1,WS);
  double t0=now(); long pages=0;
  for(int it=0; it<iters; it++)
    for(size_t off=0; off+PG<=WS; off+=PG){ memcpy(dst,src+off,PG); pages++; }
  double perA=(now()-t0)/pages*1e6;
  /* B: map-side cycle — fault-in N pages then zap them, repeatedly */
  char *m=mmap(NULL,(size_t)N*PG,PROT_READ|PROT_WRITE,MAP_PRIVATE|MAP_ANONYMOUS,-1,0);
  t0=now(); long mp=0;
  for(int it=0; it<400; it++){
    for(int i=0;i<N;i++){ m[(size_t)i*PG]=1; mp++; }   /* fault + PTE set */
    madvise(m,(size_t)N*PG,MADV_DONTNEED);             /* zap + TLB flush */
  }
  double perB=(now()-t0)/mp*1e6;
  printf("cold-copy 4K: %.2f us/page | map-cycle 4K: %.2f us/page | ratio %.1fx\n",perA,perB,perA/perB);
  return 0;
}
