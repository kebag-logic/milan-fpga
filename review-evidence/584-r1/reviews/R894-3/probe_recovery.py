#!/usr/bin/env python3
"""Exercise the exact head's recovery grader with independent decoded-frame controls.

This is a grader probe, not a replacement for the published pin-level runs.
Run from the reviewed checkout; generated code and binary remain under scratch.
"""
from pathlib import Path
import hashlib
import subprocess

packet = Path(__file__).resolve().parent
work = packet / 'scratch' / 'grader'
work.mkdir(parents=True, exist_ok=True)
path = Path('tb/verilator/milan_dp_render/sim_ship8_render.cpp')
src = path.read_text()
print('Source SHA256:', hashlib.sha256(path.read_bytes()).hexdigest(), flush=True)
recovery = src[src.index('struct Recovery {'):src.index('\nclass Ship8Harness')]
start = src.index('Recovery Ship8Harness::grade_the_record(')
end = src.index('//! The render epoch is stream qualified:', start)
methods = src[start:end]
prefix = r'''
#include <array>
#include <vector>
#include <string>
#include <cstdio>
#include <cstdint>
#include <cassert>
constexpr int kBusSlots = 32;
constexpr long kMinFrames = 100, kFlushFrames = 6;
constexpr uint32_t kMarker = 0x800000u, kEventMask = 0x1ffffu;
struct DecodedFrame { std::array<uint32_t, 32> slot{}; };
struct Check {
 std::vector<std::string> failed;
 void that(const char* name, bool ok) { if (!ok) failed.emplace_back(name); }
};
'''
declaration = r'''
class Ship8Harness {
public:
 std::vector<DecodedFrame> decoded;
 long gap_faults=0, framing_faults=0;
 Check check;
 Recovery grade_the_record(long, bool, int, int, long);
 void prove_the_recovery(const Recovery&, const char*, const char*, bool, int, int, long);
};
'''
driver = r'''
uint32_t sample(int s,int c,long e) { return (kMarker|(s<<20)|(c<<17)|e)<<8; }
Ship8Harness control(bool fall) {
 Ship8Harness h;
 h.decoded.resize(244);
 if (fall) h.decoded[0].slot[0]=sample(0,1,999);
 for(int i=144;i<244;i++) h.decoded[i].slot[0]=sample(0,1,1000+i-144);
 return h;
}
void judge(const char* name, Ship8Harness h, bool fall, bool pass, const char* expected) {
 auto r=h.grade_the_record(122,fall,0,1,1000);
 h.prove_the_recovery(r,"CLOSED","RECOVERY",fall,0,1,1000);
 assert(h.check.failed.empty()==pass);
 if(!pass) {
  bool named=false;
  for(const auto& f:h.check.failed) {
   std::printf("  rejected by: %s\n", f.c_str());
   if(f.find(expected)!=std::string::npos) named=true;
  }
  assert(named);
 }
 std::printf("PASS probe: %s; held=%ld stale=%ld first=%ld\n",name,r.held,r.stale,r.first_event);
}
int main() {
 judge("bind fall permits one pre-loss frame before closure",control(true),true,true,"");
 judge("reset release starts silent",control(false),false,true,"");
 auto h=control(true);h.decoded[144].slot[0]=sample(0,1,999);
 judge("stale first word after rebind",h,true,false,"FRESHNESS: the first");
 h=control(false);h.decoded[150].slot[0]=sample(0,1,999);
 judge("stale later word during recovery",h,false,false,"every rendered slot-0 word");
 h=control(true);h.decoded[50].slot[0]=sample(0,1,999);
 judge("leak while unbound",h,true,false,"to the rebind all 32 slots are silent");
 h=control(false);h.decoded[0].slot[0]=sample(0,1,999);
 judge("stale frame after reset release",h,false,false,"silent from the reset");
 h=control(true);h.decoded[145].slot[0]=sample(2,1,1001);
 judge("wrong stream during recovery",h,true,false,"every rendered slot-0 word");
 h=control(true);h.decoded[145].slot[31]=1;
 judge("nonzero tail during recovery",h,true,false,"slots 1-31");
 h=control(true);h.decoded[145].slot[0]=0;
 judge("gap after rendering starts",h,true,false,"none after it");
 std::puts("9/9 independent decoded-frame controls PASS");
}
'''
(work/'probe.cpp').write_text(prefix+recovery+declaration+methods+driver)
subprocess.run(['g++','-std=c++17','-O0','-Wall','-Wextra',str(work/'probe.cpp'),'-o',str(work/'probe')],check=True)
subprocess.run([str(work/'probe')],check=True)
