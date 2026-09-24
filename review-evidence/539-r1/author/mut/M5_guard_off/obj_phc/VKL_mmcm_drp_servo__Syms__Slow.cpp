// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table implementation internals

#include "VKL_mmcm_drp_servo__pch.h"

VKL_mmcm_drp_servo__Syms::VKL_mmcm_drp_servo__Syms(VerilatedContext* contextp, const char* namep, VKL_mmcm_drp_servo* modelp)
    : VerilatedSyms{contextp}
    // Setup internal state of the Syms class
    , __Vm_modelp{modelp}
    // Setup top module instance
    , TOP{this, namep}
{
    // Check resources
    Verilated::stackCheck(420);
    // Setup sub module instances
    // Configure time unit / time precision
    _vm_contextp__->timeunit(-12);
    _vm_contextp__->timeprecision(-12);
    // Setup each module's pointers to their submodules
    // Setup each module's pointer back to symbol table (for public functions)
    TOP.__Vconfigure(true);
    // Setup scopes
    __Vscopep_KL_mmcm_drp_servo = new VerilatedScope{this, "KL_mmcm_drp_servo", "KL_mmcm_drp_servo", "<null>", 0, VerilatedScope::SCOPE_OTHER};
    __Vscopep_KL_mmcm_drp_servo__servo_engine__disc_tally = new VerilatedScope{this, "KL_mmcm_drp_servo.servo_engine.disc_tally", "disc_tally", "<null>", 0, VerilatedScope::SCOPE_OTHER};
    __Vscopep_KL_mmcm_drp_servo__servo_engine__dispatch = new VerilatedScope{this, "KL_mmcm_drp_servo.servo_engine.dispatch", "dispatch", "<null>", 0, VerilatedScope::SCOPE_OTHER};
    __Vscopep_KL_mmcm_drp_servo__u_batch_hs = new VerilatedScope{this, "KL_mmcm_drp_servo.u_batch_hs", "u_batch_hs", "<null>", 0, VerilatedScope::SCOPE_OTHER};
    __Vscopep_KL_mmcm_drp_servo__u_tick_cdc = new VerilatedScope{this, "KL_mmcm_drp_servo.u_tick_cdc", "u_tick_cdc", "<null>", 0, VerilatedScope::SCOPE_OTHER};
    __Vscopep_TOP = new VerilatedScope{this, "TOP", "TOP", "<null>", 0, VerilatedScope::SCOPE_OTHER};
    // Setup export functions - final: 0
    // Setup export functions - final: 1
    // Setup public variables
    __Vscopep_KL_mmcm_drp_servo->varInsert("CFG_C0R1_MASK_P", const_cast<void*>(static_cast<const void*>(&(TOP.KL_mmcm_drp_servo__DOT__CFG_C0R1_MASK_P))), true, VLVT_UINT16, VLVD_NODIR|VLVF_PUB_RW, 0, 1 ,15,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("CFG_C0R1_P", const_cast<void*>(static_cast<const void*>(&(TOP.KL_mmcm_drp_servo__DOT__CFG_C0R1_P))), true, VLVT_UINT16, VLVD_NODIR|VLVF_PUB_RW, 0, 1 ,15,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("CFG_C0R2_MASK_P", const_cast<void*>(static_cast<const void*>(&(TOP.KL_mmcm_drp_servo__DOT__CFG_C0R2_MASK_P))), true, VLVT_UINT16, VLVD_NODIR|VLVF_PUB_RW, 0, 1 ,15,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("CFG_C0R2_P", const_cast<void*>(static_cast<const void*>(&(TOP.KL_mmcm_drp_servo__DOT__CFG_C0R2_P))), true, VLVT_UINT16, VLVD_NODIR|VLVF_PUB_RW, 0, 1 ,15,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("CLK_FREQ_HZ_P", const_cast<void*>(static_cast<const void*>(&(TOP.KL_mmcm_drp_servo__DOT__CLK_FREQ_HZ_P))), true, VLVT_UINT32, VLVD_NODIR|VLVF_PUB_RW|VLVF_DPI_CLAY, 0, 1 ,31,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("DADDR_C0R1_C", const_cast<void*>(static_cast<const void*>(&(TOP.KL_mmcm_drp_servo__DOT__DADDR_C0R1_C))), true, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 1 ,6,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("DADDR_C0R2_C", const_cast<void*>(static_cast<const void*>(&(TOP.KL_mmcm_drp_servo__DOT__DADDR_C0R2_C))), true, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 1 ,6,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("DADDR_POWER_C", const_cast<void*>(static_cast<const void*>(&(TOP.KL_mmcm_drp_servo__DOT__DADDR_POWER_C))), true, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 1 ,6,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("DISC_MAX_C", const_cast<void*>(static_cast<const void*>(&(TOP.KL_mmcm_drp_servo__DOT__DISC_MAX_C))), true, VLVT_UINT32, VLVD_NODIR|VLVF_PUB_RW|VLVF_DPI_CLAY, 0, 1 ,31,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("ECLAMP_C", const_cast<void*>(static_cast<const void*>(&(TOP.KL_mmcm_drp_servo__DOT__ECLAMP_C))), true, VLVT_UINT32, VLVD_NODIR|VLVF_PUB_RW|VLVF_DPI_CLAY|VLVF_SIGNED, 0, 1 ,31,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("GAIN_NUM_P", const_cast<void*>(static_cast<const void*>(&(TOP.KL_mmcm_drp_servo__DOT__GAIN_NUM_P))), true, VLVT_UINT32, VLVD_NODIR|VLVF_PUB_RW|VLVF_DPI_CLAY, 0, 1 ,31,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("GUARD_THR_C", const_cast<void*>(static_cast<const void*>(&(TOP.KL_mmcm_drp_servo__DOT__GUARD_THR_C))), true, VLVT_UINT32, VLVD_NODIR|VLVF_PUB_RW|VLVF_DPI_CLAY|VLVF_SIGNED, 0, 1 ,31,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("KI_SHIFT_P", const_cast<void*>(static_cast<const void*>(&(TOP.KL_mmcm_drp_servo__DOT__KI_SHIFT_P))), true, VLVT_UINT32, VLVD_NODIR|VLVF_PUB_RW|VLVF_DPI_CLAY, 0, 1 ,31,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("KP_SHIFT_P", const_cast<void*>(static_cast<const void*>(&(TOP.KL_mmcm_drp_servo__DOT__KP_SHIFT_P))), true, VLVT_UINT32, VLVD_NODIR|VLVF_PUB_RW|VLVF_DPI_CLAY, 0, 1 ,31,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("LOCK_THR_P", const_cast<void*>(static_cast<const void*>(&(TOP.KL_mmcm_drp_servo__DOT__LOCK_THR_P))), true, VLVT_UINT32, VLVD_NODIR|VLVF_PUB_RW|VLVF_DPI_CLAY|VLVF_SIGNED, 0, 1 ,31,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("LOCK_WIN_P", const_cast<void*>(static_cast<const void*>(&(TOP.KL_mmcm_drp_servo__DOT__LOCK_WIN_P))), true, VLVT_UINT32, VLVD_NODIR|VLVF_PUB_RW|VLVF_DPI_CLAY, 0, 1 ,31,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("NOM_WIN_NS_P", const_cast<void*>(static_cast<const void*>(&(TOP.KL_mmcm_drp_servo__DOT__NOM_WIN_NS_P))), true, VLVT_UINT64, VLVD_NODIR|VLVF_PUB_RW|VLVF_DPI_CLAY, 0, 1 ,63,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("NORM_SHIFT_P", const_cast<void*>(static_cast<const void*>(&(TOP.KL_mmcm_drp_servo__DOT__NORM_SHIFT_P))), true, VLVT_UINT32, VLVD_NODIR|VLVF_PUB_RW|VLVF_DPI_CLAY, 0, 1 ,31,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("POWER_ALL_C", const_cast<void*>(static_cast<const void*>(&(TOP.KL_mmcm_drp_servo__DOT__POWER_ALL_C))), true, VLVT_UINT16, VLVD_NODIR|VLVF_PUB_RW, 0, 1 ,15,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("PS_TOUT_CYC_P", const_cast<void*>(static_cast<const void*>(&(TOP.KL_mmcm_drp_servo__DOT__PS_TOUT_CYC_P))), true, VLVT_UINT32, VLVD_NODIR|VLVF_PUB_RW|VLVF_DPI_CLAY, 0, 1 ,31,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("RELOCK_TOUT_P", const_cast<void*>(static_cast<const void*>(&(TOP.KL_mmcm_drp_servo__DOT__RELOCK_TOUT_P))), true, VLVT_UINT32, VLVD_NODIR|VLVF_PUB_RW|VLVF_DPI_CLAY, 0, 1 ,31,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("SLEW_MAX_P", const_cast<void*>(static_cast<const void*>(&(TOP.KL_mmcm_drp_servo__DOT__SLEW_MAX_P))), true, VLVT_UINT32, VLVD_NODIR|VLVF_PUB_RW|VLVF_DPI_CLAY|VLVF_SIGNED, 0, 1 ,31,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("STEP_DET_NS_C", const_cast<void*>(static_cast<const void*>(&(TOP.KL_mmcm_drp_servo__DOT__STEP_DET_NS_C))), true, VLVT_UINT32, VLVD_NODIR|VLVF_PUB_RW, 0, 1 ,31,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("TICK_CYC_P", const_cast<void*>(static_cast<const void*>(&(TOP.KL_mmcm_drp_servo__DOT__TICK_CYC_P))), true, VLVT_UINT32, VLVD_NODIR|VLVF_PUB_RW|VLVF_DPI_CLAY, 0, 1 ,31,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("U_MAX_P", const_cast<void*>(static_cast<const void*>(&(TOP.KL_mmcm_drp_servo__DOT__U_MAX_P))), true, VLVT_UINT32, VLVD_NODIR|VLVF_PUB_RW|VLVF_DPI_CLAY|VLVF_SIGNED, 0, 1 ,31,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("WIN_LOG2_P", const_cast<void*>(static_cast<const void*>(&(TOP.KL_mmcm_drp_servo__DOT__WIN_LOG2_P))), true, VLVT_UINT32, VLVD_NODIR|VLVF_PUB_RW|VLVF_DPI_CLAY, 0, 1 ,31,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("WIN_TICKS_C", const_cast<void*>(static_cast<const void*>(&(TOP.KL_mmcm_drp_servo__DOT__WIN_TICKS_C))), true, VLVT_UINT32, VLVD_NODIR|VLVF_PUB_RW|VLVF_DPI_CLAY, 0, 1 ,31,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("acc_r", &(TOP.KL_mmcm_drp_servo__DOT__acc_r), false, VLVT_UINT32, VLVD_NODIR|VLVF_PUB_RW|VLVF_SIGNED, 0, 1 ,31,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("arst_n_w", &(TOP.KL_mmcm_drp_servo__DOT__arst_n_w), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET, 0, 0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("arst_sync_r", &(TOP.KL_mmcm_drp_servo__DOT__arst_sync_r), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 1 ,1,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("auto_repair_i", &(TOP.KL_mmcm_drp_servo__DOT__auto_repair_i), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW|VLVF_NET, 0, 0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("clk_audio_i", &(TOP.KL_mmcm_drp_servo__DOT__clk_audio_i), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW|VLVF_NET, 0, 0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("clk_i", &(TOP.KL_mmcm_drp_servo__DOT__clk_i), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW|VLVF_NET, 0, 0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("clk_src_i", &(TOP.KL_mmcm_drp_servo__DOT__clk_src_i), false, VLVT_UINT16, VLVD_NODIR|VLVF_PUB_RW|VLVF_NET, 0, 1 ,15,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("crf_locked_i", &(TOP.KL_mmcm_drp_servo__DOT__crf_locked_i), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW|VLVF_NET, 0, 0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("crf_rate_i", &(TOP.KL_mmcm_drp_servo__DOT__crf_rate_i), false, VLVT_UINT32, VLVD_NODIR|VLVF_PUB_RW|VLVF_SIGNED|VLVF_NET, 0, 1 ,31,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("crf_src_idx_i", &(TOP.KL_mmcm_drp_servo__DOT__crf_src_idx_i), false, VLVT_UINT16, VLVD_NODIR|VLVF_PUB_RW|VLVF_NET, 0, 1 ,15,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("disc_cnt_r", &(TOP.KL_mmcm_drp_servo__DOT__disc_cnt_r), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 1 ,5,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("disc_run_r", &(TOP.KL_mmcm_drp_servo__DOT__disc_run_r), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 1 ,1,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("drp_addr_o", &(TOP.KL_mmcm_drp_servo__DOT__drp_addr_o), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 1 ,6,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("drp_di_o", &(TOP.KL_mmcm_drp_servo__DOT__drp_di_o), false, VLVT_UINT16, VLVD_NODIR|VLVF_PUB_RW, 0, 1 ,15,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("drp_do_i", &(TOP.KL_mmcm_drp_servo__DOT__drp_do_i), false, VLVT_UINT16, VLVD_NODIR|VLVF_PUB_RW|VLVF_NET, 0, 1 ,15,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("drp_en_o", &(TOP.KL_mmcm_drp_servo__DOT__drp_en_o), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("drp_fault_r", &(TOP.KL_mmcm_drp_servo__DOT__drp_fault_r), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("drp_pass_r", &(TOP.KL_mmcm_drp_servo__DOT__drp_pass_r), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("drp_rdy_i", &(TOP.KL_mmcm_drp_servo__DOT__drp_rdy_i), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW|VLVF_NET, 0, 0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("drp_we_o", &(TOP.KL_mmcm_drp_servo__DOT__drp_we_o), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("dstate_r", &(TOP.KL_mmcm_drp_servo__DOT__dstate_r), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 1 ,3,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("ew_r", &(TOP.KL_mmcm_drp_servo__DOT__ew_r), false, VLVT_UINT32, VLVD_NODIR|VLVF_PUB_RW|VLVF_SIGNED, 0, 1 ,31,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("exp_mask_w", &(TOP.KL_mmcm_drp_servo__DOT__exp_mask_w), false, VLVT_UINT16, VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET, 0, 1 ,15,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("exp_val_w", &(TOP.KL_mmcm_drp_servo__DOT__exp_val_w), false, VLVT_UINT16, VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET, 0, 1 ,15,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("guard_hit_w", &(TOP.KL_mmcm_drp_servo__DOT__guard_hit_w), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET, 0, 0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("hs_data_r", &(TOP.KL_mmcm_drp_servo__DOT__hs_data_r), false, VLVT_UINT16, VLVD_NODIR|VLVF_PUB_RW, 0, 1 ,14,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("hs_rcv_w", &(TOP.KL_mmcm_drp_servo__DOT__hs_rcv_w), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW|VLVF_NET, 0, 0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("hs_send_r", &(TOP.KL_mmcm_drp_servo__DOT__hs_send_r), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("integ_r", &(TOP.KL_mmcm_drp_servo__DOT__integ_r), false, VLVT_UINT32, VLVD_NODIR|VLVF_PUB_RW|VLVF_SIGNED, 0, 1 ,23,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("lock_cnt_r", &(TOP.KL_mmcm_drp_servo__DOT__lock_cnt_r), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 1 ,2,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("locked_sync_r", &(TOP.KL_mmcm_drp_servo__DOT__locked_sync_r), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 1 ,1,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("mismatch_r", &(TOP.KL_mmcm_drp_servo__DOT__mismatch_r), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("mmcm_locked_i", &(TOP.KL_mmcm_drp_servo__DOT__mmcm_locked_i), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW|VLVF_NET, 0, 0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("mmcm_locked_s_w", &(TOP.KL_mmcm_drp_servo__DOT__mmcm_locked_s_w), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET, 0, 0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("mmcm_rst_o", &(TOP.KL_mmcm_drp_servo__DOT__mmcm_rst_o), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("pend_r", &(TOP.KL_mmcm_drp_servo__DOT__pend_r), false, VLVT_UINT16, VLVD_NODIR|VLVF_PUB_RW, 0, 1 ,14,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("pend_v_r", &(TOP.KL_mmcm_drp_servo__DOT__pend_v_r), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("pp_d_r", &(TOP.KL_mmcm_drp_servo__DOT__pp_d_r), false, VLVT_UINT64, VLVD_NODIR|VLVF_PUB_RW|VLVF_SIGNED, 0, 1 ,63,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("pp_du_r", &(TOP.KL_mmcm_drp_servo__DOT__pp_du_r), false, VLVT_UINT32, VLVD_NODIR|VLVF_PUB_RW|VLVF_SIGNED, 0, 1 ,31,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("pp_ig_r", &(TOP.KL_mmcm_drp_servo__DOT__pp_ig_r), false, VLVT_UINT32, VLVD_NODIR|VLVF_PUB_RW|VLVF_SIGNED, 0, 1 ,23,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("pp_isum_r", &(TOP.KL_mmcm_drp_servo__DOT__pp_isum_r), false, VLVT_UINT32, VLVD_NODIR|VLVF_PUB_RW|VLVF_SIGNED, 0, 1 ,31,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("pp_locerr_r", &(TOP.KL_mmcm_drp_servo__DOT__pp_locerr_r), false, VLVT_UINT32, VLVD_NODIR|VLVF_PUB_RW|VLVF_SIGNED, 0, 1 ,31,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("pp_rate_r", &(TOP.KL_mmcm_drp_servo__DOT__pp_rate_r), false, VLVT_UINT32, VLVD_NODIR|VLVF_PUB_RW|VLVF_SIGNED, 0, 1 ,31,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("pp_run_r", &(TOP.KL_mmcm_drp_servo__DOT__pp_run_r), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("pp_seq_r", &(TOP.KL_mmcm_drp_servo__DOT__pp_seq_r), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 1 ,2,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("pp_spann_r", &(TOP.KL_mmcm_drp_servo__DOT__pp_spann_r), false, VLVT_UINT64, VLVD_NODIR|VLVF_PUB_RW|VLVF_SIGNED, 0, 1 ,63,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("pp_thr_r", &(TOP.KL_mmcm_drp_servo__DOT__pp_thr_r), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("pp_un_r", &(TOP.KL_mmcm_drp_servo__DOT__pp_un_r), false, VLVT_UINT32, VLVD_NODIR|VLVF_PUB_RW|VLVF_SIGNED, 0, 1 ,31,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("pp_ut_r", &(TOP.KL_mmcm_drp_servo__DOT__pp_ut_r), false, VLVT_UINT32, VLVD_NODIR|VLVF_PUB_RW|VLVF_SIGNED, 0, 1 ,23,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("ps_busy_ps_r", &(TOP.KL_mmcm_drp_servo__DOT__ps_busy_ps_r), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("ps_busy_s_w", &(TOP.KL_mmcm_drp_servo__DOT__ps_busy_s_w), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET, 0, 0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("ps_clk_i", &(TOP.KL_mmcm_drp_servo__DOT__ps_clk_i), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW|VLVF_NET, 0, 0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("ps_cmd_w", &(TOP.KL_mmcm_drp_servo__DOT__ps_cmd_w), false, VLVT_UINT16, VLVD_NODIR|VLVF_PUB_RW|VLVF_NET, 0, 1 ,14,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("ps_cnt_r", &(TOP.KL_mmcm_drp_servo__DOT__ps_cnt_r), false, VLVT_UINT16, VLVD_NODIR|VLVF_PUB_RW, 0, 1 ,13,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("ps_dir_r", &(TOP.KL_mmcm_drp_servo__DOT__ps_dir_r), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("ps_done_i", &(TOP.KL_mmcm_drp_servo__DOT__ps_done_i), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW|VLVF_NET, 0, 0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("ps_en_o", &(TOP.KL_mmcm_drp_servo__DOT__ps_en_o), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("ps_fault_ps_r", &(TOP.KL_mmcm_drp_servo__DOT__ps_fault_ps_r), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("ps_fault_s_w", &(TOP.KL_mmcm_drp_servo__DOT__ps_fault_s_w), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET, 0, 0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("ps_hold_r", &(TOP.KL_mmcm_drp_servo__DOT__ps_hold_r), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("ps_incdec_o", &(TOP.KL_mmcm_drp_servo__DOT__ps_incdec_o), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("ps_invert_i", &(TOP.KL_mmcm_drp_servo__DOT__ps_invert_i), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW|VLVF_NET, 0, 0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("ps_req_w", &(TOP.KL_mmcm_drp_servo__DOT__ps_req_w), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW|VLVF_NET, 0, 0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("ps_wd_r", &(TOP.KL_mmcm_drp_servo__DOT__ps_wd_r), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 1 ,7,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("psbusy_sync_r", &(TOP.KL_mmcm_drp_servo__DOT__psbusy_sync_r), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 1 ,1,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("psfault_sync_r", &(TOP.KL_mmcm_drp_servo__DOT__psfault_sync_r), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 1 ,1,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("psrst_n_w", &(TOP.KL_mmcm_drp_servo__DOT__psrst_n_w), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET, 0, 0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("psrst_sync_r", &(TOP.KL_mmcm_drp_servo__DOT__psrst_sync_r), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 1 ,1,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("pstate_r", &(TOP.KL_mmcm_drp_servo__DOT__pstate_r), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 1 ,1,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("ptp_jump_r", &(TOP.KL_mmcm_drp_servo__DOT__ptp_jump_r), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("ptp_now_i", &(TOP.KL_mmcm_drp_servo__DOT__ptp_now_i), false, VLVT_UINT64, VLVD_NODIR|VLVF_PUB_RW|VLVF_NET, 0, 1 ,63,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("ptp_q_r", &(TOP.KL_mmcm_drp_servo__DOT__ptp_q_r), false, VLVT_UINT64, VLVD_NODIR|VLVF_PUB_RW, 0, 1 ,63,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("rd_second_r", &(TOP.KL_mmcm_drp_servo__DOT__rd_second_r), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("rd_val_r", &(TOP.KL_mmcm_drp_servo__DOT__rd_val_r), false, VLVT_UINT16, VLVD_NODIR|VLVF_PUB_RW, 0, 1 ,15,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("relock_r", &(TOP.KL_mmcm_drp_servo__DOT__relock_r), false, VLVT_UINT32, VLVD_NODIR|VLVF_PUB_RW, 0, 1 ,17,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("repairing_r", &(TOP.KL_mmcm_drp_servo__DOT__repairing_r), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("rst_n", &(TOP.KL_mmcm_drp_servo__DOT__rst_n), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW|VLVF_NET, 0, 0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("rst_settle_r", &(TOP.KL_mmcm_drp_servo__DOT__rst_settle_r), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 1 ,3,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("servo_sel_w", &(TOP.KL_mmcm_drp_servo__DOT__servo_sel_w), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET, 0, 0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("state_r", &(TOP.KL_mmcm_drp_servo__DOT__state_r), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 1 ,2,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("status_o", &(TOP.KL_mmcm_drp_servo__DOT__status_o), false, VLVT_UINT32, VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY, 0, 1 ,31,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("step_hit_w", &(TOP.KL_mmcm_drp_servo__DOT__step_hit_w), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET, 0, 0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("tick_a_r", &(TOP.KL_mmcm_drp_servo__DOT__tick_a_r), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("tick_cnt_r", &(TOP.KL_mmcm_drp_servo__DOT__tick_cnt_r), false, VLVT_UINT16, VLVD_NODIR|VLVF_PUB_RW, 0, 1 ,9,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("tick_div_r", &(TOP.KL_mmcm_drp_servo__DOT__tick_div_r), false, VLVT_UINT16, VLVD_NODIR|VLVF_PUB_RW, 0, 1 ,14,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("tick_p_w", &(TOP.KL_mmcm_drp_servo__DOT__tick_p_w), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW|VLVF_NET, 0, 0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("trim_w", &(TOP.KL_mmcm_drp_servo__DOT__trim_w), false, VLVT_UINT16, VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_SIGNED|VLVF_NET, 0, 1 ,15,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("u_cmd_r", &(TOP.KL_mmcm_drp_servo__DOT__u_cmd_r), false, VLVT_UINT32, VLVD_NODIR|VLVF_PUB_RW|VLVF_SIGNED, 0, 1 ,23,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("u_gain_r", &(TOP.KL_mmcm_drp_servo__DOT__u_gain_r), false, VLVT_UINT32, VLVD_NODIR|VLVF_PUB_RW|VLVF_SIGNED, 0, 1 ,31,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("verified_r", &(TOP.KL_mmcm_drp_servo__DOT__verified_r), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("win_skip_r", &(TOP.KL_mmcm_drp_servo__DOT__win_skip_r), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 1 ,1,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("win_start_r", &(TOP.KL_mmcm_drp_servo__DOT__win_start_r), false, VLVT_UINT64, VLVD_NODIR|VLVF_PUB_RW, 0, 1 ,63,0);
    __Vscopep_KL_mmcm_drp_servo->varInsert("win_valid_r", &(TOP.KL_mmcm_drp_servo__DOT__win_valid_r), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 0);
    __Vscopep_KL_mmcm_drp_servo__servo_engine__disc_tally->varInsert("n_v", &(TOP.KL_mmcm_drp_servo__DOT__servo_engine__DOT__disc_tally__DOT__n_v), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 1 ,6,0);
    __Vscopep_KL_mmcm_drp_servo__servo_engine__dispatch->varInsert("a_v", &(TOP.KL_mmcm_drp_servo__DOT__servo_engine__DOT__dispatch__DOT__a_v), false, VLVT_UINT32, VLVD_NODIR|VLVF_PUB_RW|VLVF_SIGNED, 0, 1 ,31,0);
    __Vscopep_KL_mmcm_drp_servo__servo_engine__dispatch->varInsert("b_v", &(TOP.KL_mmcm_drp_servo__DOT__servo_engine__DOT__dispatch__DOT__b_v), false, VLVT_UINT32, VLVD_NODIR|VLVF_PUB_RW|VLVF_SIGNED, 0, 1 ,31,0);
    __Vscopep_KL_mmcm_drp_servo__u_batch_hs->varInsert("DEST_SYNC_FF", const_cast<void*>(static_cast<const void*>(&(TOP.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__DEST_SYNC_FF))), true, VLVT_UINT32, VLVD_NODIR|VLVF_PUB_RW|VLVF_DPI_CLAY|VLVF_SIGNED, 0, 1 ,31,0);
    __Vscopep_KL_mmcm_drp_servo__u_batch_hs->varInsert("SRC_SYNC_FF", const_cast<void*>(static_cast<const void*>(&(TOP.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__SRC_SYNC_FF))), true, VLVT_UINT32, VLVD_NODIR|VLVF_PUB_RW|VLVF_DPI_CLAY|VLVF_SIGNED, 0, 1 ,31,0);
    __Vscopep_KL_mmcm_drp_servo__u_batch_hs->varInsert("WIDTH", const_cast<void*>(static_cast<const void*>(&(TOP.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__WIDTH))), true, VLVT_UINT32, VLVD_NODIR|VLVF_PUB_RW|VLVF_DPI_CLAY|VLVF_SIGNED, 0, 1 ,31,0);
    __Vscopep_KL_mmcm_drp_servo__u_batch_hs->varInsert("ack_sync", &(TOP.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__ack_sync), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 1 ,2,0);
    __Vscopep_KL_mmcm_drp_servo__u_batch_hs->varInsert("ack_tog", &(TOP.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__ack_tog), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 0);
    __Vscopep_KL_mmcm_drp_servo__u_batch_hs->varInsert("data_hold", &(TOP.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__data_hold), false, VLVT_UINT16, VLVD_NODIR|VLVF_PUB_RW, 0, 1 ,14,0);
    __Vscopep_KL_mmcm_drp_servo__u_batch_hs->varInsert("dest_clk", &(TOP.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__dest_clk), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW|VLVF_NET, 0, 0);
    __Vscopep_KL_mmcm_drp_servo__u_batch_hs->varInsert("dest_out", &(TOP.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__dest_out), false, VLVT_UINT16, VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET, 0, 1 ,14,0);
    __Vscopep_KL_mmcm_drp_servo__u_batch_hs->varInsert("dest_out_r", &(TOP.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__dest_out_r), false, VLVT_UINT16, VLVD_NODIR|VLVF_PUB_RW, 0, 1 ,14,0);
    __Vscopep_KL_mmcm_drp_servo__u_batch_hs->varInsert("dest_req", &(TOP.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__dest_req), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET, 0, 0);
    __Vscopep_KL_mmcm_drp_servo__u_batch_hs->varInsert("dest_req_r", &(TOP.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__dest_req_r), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 0);
    __Vscopep_KL_mmcm_drp_servo__u_batch_hs->varInsert("dest_rst_n", &(TOP.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__dest_rst_n), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW|VLVF_NET, 0, 0);
    __Vscopep_KL_mmcm_drp_servo__u_batch_hs->varInsert("req_edge", &(TOP.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__req_edge), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET, 0, 0);
    __Vscopep_KL_mmcm_drp_servo__u_batch_hs->varInsert("req_sync", &(TOP.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__req_sync), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 1 ,2,0);
    __Vscopep_KL_mmcm_drp_servo__u_batch_hs->varInsert("req_tog", &(TOP.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__req_tog), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 0);
    __Vscopep_KL_mmcm_drp_servo__u_batch_hs->varInsert("src_clk", &(TOP.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__src_clk), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW|VLVF_NET, 0, 0);
    __Vscopep_KL_mmcm_drp_servo__u_batch_hs->varInsert("src_in", &(TOP.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__src_in), false, VLVT_UINT16, VLVD_NODIR|VLVF_PUB_RW|VLVF_NET, 0, 1 ,14,0);
    __Vscopep_KL_mmcm_drp_servo__u_batch_hs->varInsert("src_rcv", &(TOP.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__src_rcv), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET, 0, 0);
    __Vscopep_KL_mmcm_drp_servo__u_batch_hs->varInsert("src_rst_n", &(TOP.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__src_rst_n), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW|VLVF_NET, 0, 0);
    __Vscopep_KL_mmcm_drp_servo__u_batch_hs->varInsert("src_send", &(TOP.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__src_send), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW|VLVF_NET, 0, 0);
    __Vscopep_KL_mmcm_drp_servo__u_batch_hs->varInsert("src_send_d", &(TOP.KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__src_send_d), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 0);
    __Vscopep_KL_mmcm_drp_servo__u_tick_cdc->varInsert("DEST_SYNC_FF", const_cast<void*>(static_cast<const void*>(&(TOP.KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__DEST_SYNC_FF))), true, VLVT_UINT32, VLVD_NODIR|VLVF_PUB_RW|VLVF_DPI_CLAY|VLVF_SIGNED, 0, 1 ,31,0);
    __Vscopep_KL_mmcm_drp_servo__u_tick_cdc->varInsert("dest_clk", &(TOP.KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__dest_clk), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW|VLVF_NET, 0, 0);
    __Vscopep_KL_mmcm_drp_servo__u_tick_cdc->varInsert("dest_pulse", &(TOP.KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__dest_pulse), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET, 0, 0);
    __Vscopep_KL_mmcm_drp_servo__u_tick_cdc->varInsert("dest_rst_n", &(TOP.KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__dest_rst_n), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW|VLVF_NET, 0, 0);
    __Vscopep_KL_mmcm_drp_servo__u_tick_cdc->varInsert("src_clk", &(TOP.KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__src_clk), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW|VLVF_NET, 0, 0);
    __Vscopep_KL_mmcm_drp_servo__u_tick_cdc->varInsert("src_level", &(TOP.KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__src_level), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 0);
    __Vscopep_KL_mmcm_drp_servo__u_tick_cdc->varInsert("src_pulse", &(TOP.KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__src_pulse), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW|VLVF_NET, 0, 0);
    __Vscopep_KL_mmcm_drp_servo__u_tick_cdc->varInsert("src_rst_n", &(TOP.KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__src_rst_n), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW|VLVF_NET, 0, 0);
    __Vscopep_KL_mmcm_drp_servo__u_tick_cdc->varInsert("sync", &(TOP.KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__sync), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 1 ,2,0);
    __Vscopep_TOP->varInsert("auto_repair_i", &(TOP.auto_repair_i), false, VLVT_UINT8, VLVD_IN|VLVF_PUB_RW|VLVF_NET, 0, 0);
    __Vscopep_TOP->varInsert("clk_audio_i", &(TOP.clk_audio_i), false, VLVT_UINT8, VLVD_IN|VLVF_PUB_RW|VLVF_NET, 0, 0);
    __Vscopep_TOP->varInsert("clk_i", &(TOP.clk_i), false, VLVT_UINT8, VLVD_IN|VLVF_PUB_RW|VLVF_NET, 0, 0);
    __Vscopep_TOP->varInsert("clk_src_i", &(TOP.clk_src_i), false, VLVT_UINT16, VLVD_IN|VLVF_PUB_RW|VLVF_NET, 0, 1 ,15,0);
    __Vscopep_TOP->varInsert("crf_locked_i", &(TOP.crf_locked_i), false, VLVT_UINT8, VLVD_IN|VLVF_PUB_RW|VLVF_NET, 0, 0);
    __Vscopep_TOP->varInsert("crf_rate_i", &(TOP.crf_rate_i), false, VLVT_UINT32, VLVD_IN|VLVF_PUB_RW|VLVF_SIGNED|VLVF_NET, 0, 1 ,31,0);
    __Vscopep_TOP->varInsert("crf_src_idx_i", &(TOP.crf_src_idx_i), false, VLVT_UINT16, VLVD_IN|VLVF_PUB_RW|VLVF_NET, 0, 1 ,15,0);
    __Vscopep_TOP->varInsert("drp_addr_o", &(TOP.drp_addr_o), false, VLVT_UINT8, VLVD_OUT|VLVF_PUB_RW, 0, 1 ,6,0);
    __Vscopep_TOP->varInsert("drp_di_o", &(TOP.drp_di_o), false, VLVT_UINT16, VLVD_OUT|VLVF_PUB_RW, 0, 1 ,15,0);
    __Vscopep_TOP->varInsert("drp_do_i", &(TOP.drp_do_i), false, VLVT_UINT16, VLVD_IN|VLVF_PUB_RW|VLVF_NET, 0, 1 ,15,0);
    __Vscopep_TOP->varInsert("drp_en_o", &(TOP.drp_en_o), false, VLVT_UINT8, VLVD_OUT|VLVF_PUB_RW, 0, 0);
    __Vscopep_TOP->varInsert("drp_rdy_i", &(TOP.drp_rdy_i), false, VLVT_UINT8, VLVD_IN|VLVF_PUB_RW|VLVF_NET, 0, 0);
    __Vscopep_TOP->varInsert("drp_we_o", &(TOP.drp_we_o), false, VLVT_UINT8, VLVD_OUT|VLVF_PUB_RW, 0, 0);
    __Vscopep_TOP->varInsert("mmcm_locked_i", &(TOP.mmcm_locked_i), false, VLVT_UINT8, VLVD_IN|VLVF_PUB_RW|VLVF_NET, 0, 0);
    __Vscopep_TOP->varInsert("mmcm_rst_o", &(TOP.mmcm_rst_o), false, VLVT_UINT8, VLVD_OUT|VLVF_PUB_RW, 0, 0);
    __Vscopep_TOP->varInsert("ps_clk_i", &(TOP.ps_clk_i), false, VLVT_UINT8, VLVD_IN|VLVF_PUB_RW|VLVF_NET, 0, 0);
    __Vscopep_TOP->varInsert("ps_done_i", &(TOP.ps_done_i), false, VLVT_UINT8, VLVD_IN|VLVF_PUB_RW|VLVF_NET, 0, 0);
    __Vscopep_TOP->varInsert("ps_en_o", &(TOP.ps_en_o), false, VLVT_UINT8, VLVD_OUT|VLVF_PUB_RW, 0, 0);
    __Vscopep_TOP->varInsert("ps_incdec_o", &(TOP.ps_incdec_o), false, VLVT_UINT8, VLVD_OUT|VLVF_PUB_RW, 0, 0);
    __Vscopep_TOP->varInsert("ps_invert_i", &(TOP.ps_invert_i), false, VLVT_UINT8, VLVD_IN|VLVF_PUB_RW|VLVF_NET, 0, 0);
    __Vscopep_TOP->varInsert("ptp_now_i", &(TOP.ptp_now_i), false, VLVT_UINT64, VLVD_IN|VLVF_PUB_RW|VLVF_NET, 0, 1 ,63,0);
    __Vscopep_TOP->varInsert("rst_n", &(TOP.rst_n), false, VLVT_UINT8, VLVD_IN|VLVF_PUB_RW|VLVF_NET, 0, 0);
    __Vscopep_TOP->varInsert("status_o", &(TOP.status_o), false, VLVT_UINT32, VLVD_OUT|VLVF_PUB_RW|VLVF_CONTINUOUSLY, 0, 1 ,31,0);
}

VKL_mmcm_drp_servo__Syms::~VKL_mmcm_drp_servo__Syms() {
    // Tear down scopes
    VL_DO_CLEAR(delete __Vscopep_KL_mmcm_drp_servo, __Vscopep_KL_mmcm_drp_servo = nullptr);
    VL_DO_CLEAR(delete __Vscopep_KL_mmcm_drp_servo__servo_engine__disc_tally, __Vscopep_KL_mmcm_drp_servo__servo_engine__disc_tally = nullptr);
    VL_DO_CLEAR(delete __Vscopep_KL_mmcm_drp_servo__servo_engine__dispatch, __Vscopep_KL_mmcm_drp_servo__servo_engine__dispatch = nullptr);
    VL_DO_CLEAR(delete __Vscopep_KL_mmcm_drp_servo__u_batch_hs, __Vscopep_KL_mmcm_drp_servo__u_batch_hs = nullptr);
    VL_DO_CLEAR(delete __Vscopep_KL_mmcm_drp_servo__u_tick_cdc, __Vscopep_KL_mmcm_drp_servo__u_tick_cdc = nullptr);
    VL_DO_CLEAR(delete __Vscopep_TOP, __Vscopep_TOP = nullptr);
    // Tear down sub module instances
}
