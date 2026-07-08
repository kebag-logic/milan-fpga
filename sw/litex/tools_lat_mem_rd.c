/* pointer-chase latency vs working-set size — reveals the L2 boundary + miss cost,
 * no PMU/perf needed. Randomized cyclic permutation defeats the prefetcher. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>
#include <string.h>
static uint64_t nsec(void){ struct timespec t; clock_gettime(CLOCK_MONOTONIC,&t);
  return (uint64_t)t.tv_sec*1000000000ull + t.tv_nsec; }
int main(void){
  size_t sizes[] = {8,16,24,32,48,64,96,128,256,512,1024,2048}; /* KB */
  int ns_ = sizeof(sizes)/sizeof(sizes[0]);
  printf("WS_KB  ns/access\n");
  for(int s=0;s<ns_;s++){
    size_t n = sizes[s]*1024/sizeof(void*);
    void **a = malloc(n*sizeof(void*));
    if(!a){ printf("%6zu  OOM\n", sizes[s]); continue; }
    /* build a random single cycle over all n slots */
    size_t *idx = malloc(n*sizeof(size_t));
    for(size_t i=0;i<n;i++) idx[i]=i;
    for(size_t i=n-1;i>0;i--){ size_t j=((i*2654435761u)^ (i>>3))%(i+1); size_t t=idx[i]; idx[i]=idx[j]; idx[j]=t; }
    for(size_t i=0;i<n;i++) a[idx[i]] = &a[idx[(i+1)%n]];
    /* warm + chase */
    void **p=&a[idx[0]];
    for(size_t i=0;i<n;i++) p=(void**)*p;
    size_t iters = 4000000;
    uint64_t t0=nsec();
    for(size_t i=0;i<iters;i++) p=(void**)*p;
    uint64_t t1=nsec();
    __asm__ volatile(""::"r"(p));
    printf("%6zu  %6.1f\n", sizes[s], (double)(t1-t0)/iters);
    free(a); free(idx);
  }
  return 0;
}
