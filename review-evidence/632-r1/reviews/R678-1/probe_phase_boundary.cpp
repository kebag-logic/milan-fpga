#include "VKL_mmcm_drp_servo.h"
#include "VKL_mmcm_drp_servo___024root.h"
#include <cstdio>
#include <memory>
#include <cstdint>
#include <cstdlib>
#define R(n) d->rootp->KL_mmcm_drp_servo__DOT__##n
int main(int argc,char**argv){
 Verilated::commandArgs(argc,argv);
 const int magnitude=(argc>1)?std::atoi(argv[1]):10416;
 auto d=std::make_unique<VKL_mmcm_drp_servo>();
 d->sel_i=1;d->ref_locked_i=1;d->ref_rate_valid_i=1;d->ph_en_i=1;d->mmcm_locked_i=1;
 auto edge=[&](){d->clk_i=0;d->clk_audio_i=0;d->ps_clk_i=0;d->eval();d->clk_i=1;d->clk_audio_i=1;d->ps_clk_i=1;d->ptp_now_i+=20;d->eval();};
 d->rst_n=0;for(int i=0;i<8;i++)edge(); d->rst_n=1;
 R(state_r)=4;R(lock_cnt_r)=4;R(win_valid_r)=1;
 unsigned windows=0;bool bad_settle=false;int sample=0;int restarts=0;bool bad_mr=false; int after_restart=-1; int64_t ix0=0;
 for(int i=0;i<120000;i++){
  d->ref_restart_p_i=0;d->dom_ev_p_i=(i%64==0);d->dom_ns_i=1000000;
  d->ref_ts_p_i=(i%64==2);
  if(d->ref_ts_p_i){d->ref_ts_ns_i=(++sample%2)?1000000-magnitude:1000000+magnitude;}
  // An isolated detector test: keep the rate state at its reachable LOCKED value,
  // and give each boundary exactly the nominal rate span. No physical-plant claim.
  R(state_r)=4;R(lock_cnt_r)=4;
  if(R(tick_p_w)&&R(tick_cnt_r)==511){
   R(win_start_r)=R(ptp_q_r)-512000000ULL;
   windows++;
   if(windows==7){R(ph_theta_r)=3000;R(ph_theta_v_r)=1;d->ref_restart_p_i=1;restarts++; ix0=(int64_t(int32_t(R(integ_r)<<8)>>8)*256)+R(integ_frac_r); after_restart=0;}
  }
  edge();
  if(windows>=2 && windows<7 && d->ph_settled_o){bad_settle=true;}
  if(d->ref_restart_p_i){
   std::printf("restart boundary: phase_valid=%u held=%u snapped_phase=%d pp_run=%u\n",R(ph_theta_v_r),R(ph_hold_w),(int16_t)R(pp_ph_r),R(pp_run_r));
   bad_mr=R(ph_theta_v_r)==0 && R(pp_ph_r)==3000 && R(pp_run_r);
  }
  if(after_restart>=0 && ++after_restart==8){
   int64_t ix1=(int64_t(int32_t(R(integ_r)<<8)>>8)*256)+R(integ_frac_r);
   int64_t phase_delta=ix1-ix0-int64_t(int32_t(R(ew_r)))*128;
   std::printf("committed phase contribution after restart=%lld/256 trim units; expected zero\n",(long long)phase_delta);
   bad_mr=bad_mr && phase_delta==6000;
  }
  if(i%8192==0)std::printf("cycle=%d windows=%u count=%u theta=%d settled=%u\n",i,windows,R(ph_wcnt_r),(int16_t)R(ph_theta_r),d->ph_settled_o);
 }
 std::printf("Each sampled phase has magnitude %d ns; 5-percent bound=1041.667 ns.\n",magnitude);
 std::printf("settled_seen=%d stale_restart_snapshot=%d restart_count=%d\n",bad_settle,bad_mr,restarts);
 return !(bad_settle&&bad_mr);
}
