// SPDX-License-Identifier: CERN-OHL-W-2.0
// Real ACMP talker with the parent's real MAAP shim; external block state controlled.
#define main upstream_suite_main_unused
#include "acmp_talker/sim_main.cpp"
#undef main
#include <stdexcept>
static void need(bool b,const char* m){if(!b)throw std::runtime_error(m);}
int main(int argc,char** argv){
  Verilated::commandArgs(argc,argv);
  try{
    Hn h;h.auto_grant=false;
    h.d->block_valid_i=0;
    h.configure_the_talker_and_release_reset();h.run(1000);
    need(h.mreqs.size()==8,"boot allocation walk missing");
    need(h.d->declaring_o==0,"startup advertised without demand");
    unsigned requests=h.mreqs.size();
    h.d->block_valid_i=1;h.d->now_ms_i=200;h.run(N_SRC * (MAAP_TMO + 64));
    need(h.mreqs.size()==requests+N_SRC,"automatic retry sweep missing");
    need(h.d->declaring_o==0,"unexpected declaration before probe");
    printf("FIRST_PROBE setup: boot ALLOC refused for 8 sources; block later valid; retry interval and bounded sweep elapsed\n");
    need(h.send(MT_PROBE,1,C1,105,L1,8,FL_FC),"probe not accepted");h.run(100);
    need(h.resps.size()==1 && h.resps[0].status==0,"first probe failed after acquisition bound");
    need(h.resps[0].da==0x91e0f0006818ULL && h.resps[0].sid==sid_of(1) && h.resps[0].vlan==VID,"first response tuple wrong");
    need(h.mreqs.size()==requests+N_SRC,"first probe unexpectedly reallocates");
    need((h.d->declaring_o&2)!=0,"first probe did not open the acquired DA gate");
    printf("FIRST_PROBE fixed: status=0, DA=91e0f0006818, source SID and VID valid; no probe-triggered ALLOC\n");
    need(h.send(MT_PROBE,1,C1,106,L1,8,FL_FC),"retry not accepted");h.run(100);
    need(h.resps.size()==2 && h.resps[1].status==0,"second probe not successful");
    need(h.resps[1].da==0x91e0f0006818ULL && h.resps[1].sid==sid_of(1) && h.resps[1].vlan==VID,"second response tuple wrong");
    printf("SECOND_PROBE control: status=0, DA=91e0f0006818, source SID valid; no LeaveAll input exists on this path\n");
    // Distinguish an allocation cold start from a normal undeclared/warm talker.
    Hn warm;warm.auto_grant=false;warm.d->block_valid_i=1;
    warm.configure_the_talker_and_release_reset();warm.run(1000);
    need(warm.d->declaring_o==0,"warm control advertised before first probe");
    need(warm.send(MT_PROBE,1,C1,107,L1,8,FL_FC),"warm probe not accepted");warm.run(100);
    need(warm.resps.size()==1 && warm.resps[0].status==0,"warm first probe failed");
    printf("WARM_DA control: first probe status=0 even though no Talker Advertise before probe\n");
    printf("PASS: late availability recovered within the acquisition bound; peer retry delay and bench allocator history are not modeled\n");return 0;
  }catch(const std::exception& e){printf("FAIL: %s\n",e.what());return 1;}
}
