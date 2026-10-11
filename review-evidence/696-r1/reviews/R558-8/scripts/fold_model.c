/* Independent model of the KL_maap first draw at head 32582421 (constants
 * transcribed from hdl/ieee1722/maap/KL_maap.sv:147,151,163-178,193-198).
 * Checks the recorded separation criterion for every seed exhaustively by
 * linearity, plus the zero-sum fallback pairs, by brute force over seeds. */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
static const uint32_t OFF[16]={ /* row 0 .. row 15 */
 0x00000081,0x10400000,0x08100040,0x10080002,0x04000220,0x48002000,0x80080040,0x80808000,
 0x20008001,0x00111000,0x08200000,0x10000084,0x00044800,0x02100008,0x00020104,0x01000410};
static const uint32_t PRB[6]={0x24200880,0x00000409,0x02841420,0x49008050,0x804A4200,0x10112104};
static uint32_t step(uint32_t s){return (s<<1)|(((s>>31)^(s>>21)^(s>>1)^s)&1);}
static int par(uint32_t x){return __builtin_parity(x);}
static uint32_t ofold(uint32_t s){uint32_t r=0;for(int i=0;i<16;i++)r|=(uint32_t)par(s&OFF[i])<<i;return r;}
static uint32_t pfold(uint32_t s){uint32_t r=0;for(int i=0;i<6;i++)r|=(uint32_t)par(s&PRB[i])<<i;return r;}
static uint32_t rand_offset(uint32_t rnd,uint32_t cnt){uint32_t o=rnd>=0xFE00?rnd-0xFE00:rnd; if(o>0xFE00-cnt)o=0xFE00-cnt; return o;}
static uint32_t seedfix(uint32_t s){return s?s:0xACE1;}
static uint32_t first_word(uint32_t sum){return ofold(step(seedfix(sum)));}
static uint32_t first_probe(uint32_t sum){return pfold(step(seedfix(sum)));}
static int rank(uint32_t *cols,int n){uint32_t b[32]={0};int r=0;for(int k=0;k<n;k++){uint32_t v=cols[k];for(int bit=31;bit>=0;bit--){if(!((v>>bit)&1))continue;if(!b[bit]){b[bit]=v;r++;break;}v^=b[bit];}}return r;}
int main(void){
  uint32_t oc[32],pc[32],both[32],hi[16];
  for(int k=0;k<32;k++){oc[k]=ofold(step(1u<<k));pc[k]=pfold(step(1u<<k));both[k]=oc[k]|(pc[k]<<16);}
  for(int k=0;k<16;k++)hi[k]=oc[16+k];
  int r_off=rank(oc,32),r_hi=rank(hi,16),r_both=rank(both,32);
  printf("rank offset map %d, bits16..31 %d, joint 22-bit %d\n",r_off,r_hi,r_both);
  /* all carry runs x all 65536 words x counts 1..8 (image is full when r_off==16) */
  long bad=0,pbad=0,minspare=1<<16; int runs=0;
  for(int i=0;i<32;i++)for(int j=i;j<32;j++){
    uint32_t run=(uint32_t)((((uint64_t)1)<<(j+1))-(((uint64_t)1)<<i)); runs++;
    uint32_t d=0,pd=0; for(int k=0;k<32;k++)if((run>>k)&1){d^=oc[k];pd^=pc[k];}
    if(!pd)pbad++;
    for(uint32_t w=0;w<65536;w++)for(uint32_t c=1;c<=8;c++){
      long a=rand_offset(w,c),b=rand_offset(w^d,c),g=labs(a-b);
      if(g<(long)c)bad++; if(g-(long)c<minspare)minspare=g-(long)c;}
  }
  printf("carry runs %d: overlapping (run,word,count) %ld; equal probe draws %ld; least spare %ld\n",runs,bad,pbad,minspare);
  /* zero-sum fallback pairs: sums s and s+2^i where one of them is 0 */
  int zbad=0,zpeq=0;
  for(int i=0;i<32;i++){
    uint32_t pairs[2][2]={{0u,1u<<i},{(uint32_t)(0u-(1u<<i)),0u}};
    for(int p=0;p<2;p++){uint32_t a=pairs[p][0],b=pairs[p][1];
      for(uint32_t c=1;c<=8;c++){long x=rand_offset(first_word(a),c),y=rand_offset(first_word(b),c);
        if(labs(x-y)<(long)c){zbad++; printf("  zero-fallback overlap i=%d sums %08x/%08x count %u: 0x%04lx 0x%04lx\n",i,a,b,c,x,y);}}
      if(first_probe(a)==first_probe(b))zpeq++;}
  }
  printf("zero-fallback pairs: overlapping (pair,count) %d, equal first probe draws %d\n",zbad,zpeq);
  /* brute-force sample: random sums s, every i, compare directly (no linearity assumption) */
  uint32_t x=0x1234567u; long sb=0,sp=0,n=0;
  for(int t=0;t<200000;t++){x=x*1664525u+1013904223u; for(int i=0;i<32;i++){uint32_t a=x,b=x+(1u<<i); if(!a||!b)continue; n++;
     long u=rand_offset(first_word(a),8),v=rand_offset(first_word(b),8); if(labs(u-v)<8)sb++; if(first_probe(a)==first_probe(b))sp++;}}
  printf("direct sample %ld pairs 2^i apart: overlapping %ld, equal first probe %ld\n",n,sb,sp);
  /* fixed datapath pairs and R558-6 pairs, count 8 */
  struct {uint32_t a,b;} fx[]={{1,2},{1,0x10001},{0xa1234+7,0x5b1234+7},{0x11001234,0x22001234}};
  for(int k=0;k<4;k++)printf("fixed %08x/%08x -> 0x%04x 0x%04x\n",fx[k].a,fx[k].b,rand_offset(first_word(fx[k].a),8),rand_offset(first_word(fx[k].b),8));
  return (r_off==16&&r_hi==16&&r_both==22&&bad==0&&pbad==0)?0:1;
}
