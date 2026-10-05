#include <cstdint>
#include <map>
#include <mutex>
#include <string>
#include <iostream>
enum class SICF {MediaUnlocked,StreamInterrupted,SeqNumMismatch,LateTimestamp,EarlyTimestamp,UnsupportedFormat,MediaLocked};
namespace la_em {using StreamInputCounters=std::map<SICF,std::uint32_t>;}
std::string ctrJson(la_em::StreamInputCounters const& c) {std::string s="{"; for(auto [k,v]:c) s+=std::to_string(int(k))+":"+std::to_string(v)+","; return s+"}";}
// Cache initialization, reset/wrap and increment behavior match the application.
struct ErrorInfo { std::uint32_t current{0}, clear{0}; };
static std::map<std::uint64_t, std::map<std::uint16_t, std::map<SICF, ErrorInfo>>> errors;
static std::mutex errorMutex;
static std::string errorUpdate(std::uint64_t eid, std::uint16_t idx,
                              la_em::StreamInputCounters const& c, std::string const& conn)
{
 std::lock_guard<std::mutex> lock(errorMutex);
 if (!errors.count(eid)) return "{}";
 auto& row=errors[eid][idx];
 la_em::StreamInputCounters increments, visible;
 for (auto const& [flag,v]:c) {
  bool selected=false;
  switch(flag) {
   case SICF::MediaUnlocked: selected=(conn=="Connected"); break;
   case SICF::StreamInterrupted: case SICF::SeqNumMismatch:
   case SICF::LateTimestamp: case SICF::EarlyTimestamp:
   case SICF::UnsupportedFormat: selected=true; break;
   default: break;
  }
  if (!selected) continue;
  auto& x=row[flag];
  if(v<x.current) x.clear=0;
  if(v>x.current) increments[flag]=v-x.current;
  x.current=v;
 }
 for(auto const& [flag,x]:row) if(x.current!=x.clear) visible[flag]=x.current-x.clear;
 return "\"increments\":"+ctrJson(increments)+",\"visible\":"+ctrJson(visible);
}


int main(){
 errors[1][0][SICF::MediaUnlocked]={7,7};
 errorUpdate(1,0,{{SICF::MediaUnlocked,8}},"NotConnected");
 if(errors[1][0][SICF::MediaUnlocked].current!=7) return 1;
 errorUpdate(1,0,{{SICF::MediaUnlocked,8}},"Connected");
 if(errors[1][0][SICF::MediaUnlocked].current!=8 || errors[1][0][SICF::MediaUnlocked].clear!=7) return 2;
 for(auto f:{SICF::StreamInterrupted,SICF::SeqNumMismatch,SICF::LateTimestamp,SICF::EarlyTimestamp,SICF::UnsupportedFormat}){
  errorUpdate(1,0,{{f,3}},"NotConnected");if(errors[1][0][f].current!=3) return 3;
 }
 errorUpdate(1,0,{{SICF::MediaUnlocked,0}},"Connected");
 if(errors[1][0][SICF::MediaUnlocked].current!=0 || errors[1][0][SICF::MediaUnlocked].clear!=0) return 4;
 errorUpdate(1,0,{{SICF::MediaUnlocked,1}},"FastConnecting");
 if(errors[1][0][SICF::MediaUnlocked].current!=0) return 5;
 errorUpdate(1,0,{{SICF::MediaLocked,15}},"Connected");
 if(errors[1][0].count(SICF::MediaLocked)) return 6;
 errors[1][0][SICF::SeqNumMismatch]={0xffffffff,9};
 errorUpdate(1,0,{{SICF::SeqNumMismatch,0}},"NotConnected");
 if(errors[1][0][SICF::SeqNumMismatch].clear!=0) return 7;
 if(errorUpdate(2,0,{{SICF::SeqNumMismatch,1}},"Connected")!="{}") return 8;
 std::cout<<"Eight rule controls PASS\n";
}
