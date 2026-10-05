#include "VKL_mbx_axil.h"
#include "verilated.h"
#include <cstdio>
int main(){VKL_mbx_axil d;d.clk_i=0;d.rst_n=0;d.eval();d.clk_i=1;d.eval();d.clk_i=0;d.rst_n=1;d.eval();
unsigned ar0=d.s_arready_o;d.s_arvalid_i=1;d.eval();unsigned ar1=d.s_arready_o;
printf("WITHOUT_CLOCK_EDGE ARVALID 0->1: ARREADY %u->%u\n",ar0,ar1);
d.s_arvalid_i=0;d.s_awvalid_i=1;d.s_wvalid_i=0;d.eval();unsigned aw0=d.s_awready_o,w0=d.s_wready_o;d.s_wvalid_i=1;d.eval();
printf("WITHOUT_CLOCK_EDGE WVALID 0->1 with AWVALID=1: AWREADY %u->%u WREADY %u->%u\n",aw0,d.s_awready_o,w0,d.s_wready_o);
return (ar0!=ar1||aw0!=d.s_awready_o||w0!=d.s_wready_o)?1:0;}
