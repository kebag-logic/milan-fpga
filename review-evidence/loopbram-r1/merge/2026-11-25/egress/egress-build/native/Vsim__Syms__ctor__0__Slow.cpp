// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table implementation internals

#include "Vsim__pch.h"

void Vsim__Syms::Vsim__Syms__ctor__0() {
    // Check resources
    Verilated::stackCheck(2699);
    // Setup sub module instances
    TOP__KL_mbx_pkg.ctor(this, "KL_mbx_pkg");
    TOP__sim.ctor(this, "sim");
    TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.ctor(this, "sim.VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952");
    TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.ctor(this, "sim.VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.vexiis_0_logic_core");
    TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__integer_RegFilePlugin_logic_regfile_fpga.ctor(this, "sim.VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.vexiis_0_logic_core.integer_RegFilePlugin_logic_regfile_fpga");
    // Configure time unit / time precision
    _vm_contextp__->timeunit(-9);
    _vm_contextp__->timeprecision(-12);
    // Setup each module's pointers to their submodules
    TOP.__PVT__KL_mbx_pkg = &TOP__KL_mbx_pkg;
    TOP.sim = &TOP__sim;
    TOP__sim.VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952 = &TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952;
    TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.vexiis_0_logic_core = &TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core;
    TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.integer_RegFilePlugin_logic_regfile_fpga = &TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__integer_RegFilePlugin_logic_regfile_fpga;
    // Setup each module's pointer back to symbol table (for public functions)
    TOP.__Vconfigure(true);
    TOP__KL_mbx_pkg.__Vconfigure(true);
    TOP__sim.__Vconfigure(true);
    TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__Vconfigure(true);
    TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.__Vconfigure(true);
    TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__integer_RegFilePlugin_logic_regfile_fpga.__Vconfigure(true);
    // Setup scopes
    __Vscopep_sim__KL_mbx__u_evt = new VerilatedScope{this, "sim.KL_mbx.u_evt", "u_evt", "<null>", 0, VerilatedScope::SCOPE_OTHER};
    __Vscopep_sim__KL_mbx__u_rx = new VerilatedScope{this, "sim.KL_mbx.u_rx", "u_rx", "<null>", 0, VerilatedScope::SCOPE_OTHER};
    __Vscopep_sim__KL_mbx__u_rx__verdict__unnamedblk11__unnamedblk12 = new VerilatedScope{this, "sim.KL_mbx.u_rx.verdict.unnamedblk11.unnamedblk12", "unnamedblk12", "<null>", -9, VerilatedScope::SCOPE_OTHER};
    __Vscopep_sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core = new VerilatedScope{this, "sim.VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.vexiis_0_logic_core", "vexiis_0_logic_core", "<null>", 0, VerilatedScope::SCOPE_OTHER};
    __Vscopep_sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__integer_RegFilePlugin_logic_regfile_fpga = new VerilatedScope{this, "sim.VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.vexiis_0_logic_core.integer_RegFilePlugin_logic_regfile_fpga", "integer_RegFilePlugin_logic_regfile_fpga", "<null>", 0, VerilatedScope::SCOPE_OTHER};
    // Setup export functions - final: 0
    // Setup export functions - final: 1
    // Setup public variables
    __Vscopep_sim__KL_mbx__u_evt->varInsert("wr_addr_o", &(TOP__sim.KL_mbx__DOT__u_evt__DOT__wr_addr_o), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD|VLVF_CONTINUOUSLY, 0, 1 ,5,0);
    __Vscopep_sim__KL_mbx__u_evt->varInsert("wr_data_o", &(TOP__sim.KL_mbx__DOT__u_evt__DOT__wr_data_o), false, VLVT_UINT32, VLVD_NODIR|VLVF_PUB_RD|VLVF_CONTINUOUSLY, 0, 1 ,31,0);
    __Vscopep_sim__KL_mbx__u_evt->varInsert("wr_en_o", &(TOP__sim.KL_mbx__DOT__u_evt__DOT__wr_en_o), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD|VLVF_CONTINUOUSLY, 0, 0);
    __Vscopep_sim__KL_mbx__u_rx->varInsert("ch_r", &(TOP__sim.KL_mbx__DOT__u_rx__DOT__ch_r), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD, 0, 1 ,2,0);
    __Vscopep_sim__KL_mbx__u_rx->varInsert("commit_w", &(TOP__sim.KL_mbx__DOT__u_rx__DOT__commit_w), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD|VLVF_CONTINUOUSLY, 0, 0);
    __Vscopep_sim__KL_mbx__u_rx->varInsert("hold_w", &(TOP__sim.KL_mbx__DOT__u_rx__DOT__hold_w), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD|VLVF_CONTINUOUSLY, 0, 0);
    __Vscopep_sim__KL_mbx__u_rx->varInsert("rel_w", &(TOP__sim.KL_mbx__DOT__u_rx__DOT__rel_w), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD, 1, 0 ,0,4);
    __Vscopep_sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core->varInsert("FetchL1Plugin_logic_bus_cmd_payload_address", &(TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.FetchL1Plugin_logic_bus_cmd_payload_address), false, VLVT_UINT32, VLVD_NODIR|VLVF_PUB_RD|VLVF_CONTINUOUSLY|VLVF_NET, 0, 1 ,31,0);
    __Vscopep_sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core->varInsert("FetchL1Plugin_logic_bus_cmd_ready", &(TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.FetchL1Plugin_logic_bus_cmd_ready), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD|VLVF_CONTINUOUSLY|VLVF_NET, 0, 0);
    __Vscopep_sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core->varInsert("FetchL1Plugin_logic_bus_cmd_valid", &(TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.FetchL1Plugin_logic_bus_cmd_valid), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD|VLVF_CONTINUOUSLY|VLVF_NET, 0, 0);
    __Vscopep_sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core->varInsert("FetchL1Plugin_logic_bus_rsp_payload_error", &(TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.FetchL1Plugin_logic_bus_rsp_payload_error), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD|VLVF_CONTINUOUSLY|VLVF_NET, 0, 0);
    __Vscopep_sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core->varInsert("FetchL1Plugin_logic_bus_rsp_valid", &(TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.FetchL1Plugin_logic_bus_rsp_valid), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD|VLVF_CONTINUOUSLY|VLVF_NET, 0, 0);
    __Vscopep_sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core->varInsert("LsuPlugin_logic_bus_cmd_payload_address", &(TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.LsuPlugin_logic_bus_cmd_payload_address), false, VLVT_UINT32, VLVD_NODIR|VLVF_PUB_RD|VLVF_CONTINUOUSLY|VLVF_NET, 0, 1 ,31,0);
    __Vscopep_sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core->varInsert("LsuPlugin_logic_bus_cmd_payload_write", &(TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.LsuPlugin_logic_bus_cmd_payload_write), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD|VLVF_CONTINUOUSLY|VLVF_NET, 0, 0);
    __Vscopep_sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core->varInsert("LsuPlugin_logic_bus_cmd_ready", &(TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.LsuPlugin_logic_bus_cmd_ready), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD|VLVF_CONTINUOUSLY|VLVF_NET, 0, 0);
    __Vscopep_sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core->varInsert("LsuPlugin_logic_bus_cmd_valid", &(TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.LsuPlugin_logic_bus_cmd_valid), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD|VLVF_CONTINUOUSLY|VLVF_NET, 0, 0);
    __Vscopep_sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core->varInsert("LsuPlugin_logic_bus_rsp_payload_error", &(TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.LsuPlugin_logic_bus_rsp_payload_error), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD|VLVF_CONTINUOUSLY|VLVF_NET, 0, 0);
    __Vscopep_sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core->varInsert("LsuPlugin_logic_bus_rsp_valid", &(TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.LsuPlugin_logic_bus_rsp_valid), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD|VLVF_CONTINUOUSLY|VLVF_NET, 0, 0);
    __Vscopep_sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core->varInsert("PrivilegedPlugin_logic_harts_0_int_m_external", &(TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.PrivilegedPlugin_logic_harts_0_int_m_external), false, VLVT_UINT8, VLVD_IN|VLVF_PUB_RW|VLVF_NET, 0, 0);
    __Vscopep_sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core->varInsert("PrivilegedPlugin_logic_harts_0_int_m_software", &(TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.PrivilegedPlugin_logic_harts_0_int_m_software), false, VLVT_UINT8, VLVD_IN|VLVF_PUB_RW|VLVF_NET, 0, 0);
    __Vscopep_sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core->varInsert("PrivilegedPlugin_logic_harts_0_int_m_timer", &(TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.PrivilegedPlugin_logic_harts_0_int_m_timer), false, VLVT_UINT8, VLVD_IN|VLVF_PUB_RW|VLVF_NET, 0, 0);
    __Vscopep_sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core->varInsert("WhiteboxerPlugin_logic_commits_ports_0_pc", &(TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.WhiteboxerPlugin_logic_commits_ports_0_pc), false, VLVT_UINT32, VLVD_NODIR|VLVF_PUB_RD|VLVF_CONTINUOUSLY|VLVF_NET, 0, 1 ,31,0);
    __Vscopep_sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core->varInsert("WhiteboxerPlugin_logic_commits_ports_0_valid", &(TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.WhiteboxerPlugin_logic_commits_ports_0_valid), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD|VLVF_CONTINUOUSLY|VLVF_NET, 0, 0);
    __Vscopep_sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core->varInsert("WhiteboxerPlugin_logic_trap_ports_0_cause", &(TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.WhiteboxerPlugin_logic_trap_ports_0_cause), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD|VLVF_CONTINUOUSLY|VLVF_NET, 0, 1 ,4,0);
    __Vscopep_sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core->varInsert("WhiteboxerPlugin_logic_trap_ports_0_interrupt", &(TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.WhiteboxerPlugin_logic_trap_ports_0_interrupt), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD|VLVF_CONTINUOUSLY|VLVF_NET, 0, 0);
    __Vscopep_sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core->varInsert("WhiteboxerPlugin_logic_trap_ports_0_valid", &(TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.WhiteboxerPlugin_logic_trap_ports_0_valid), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD|VLVF_CONTINUOUSLY|VLVF_NET, 0, 0);
    __Vscopep_sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core->varInsert("integer_write_0_address", &(TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.integer_write_0_address), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET, 0, 1 ,4,0);
    __Vscopep_sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core->varInsert("integer_write_0_data", &(TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.integer_write_0_data), false, VLVT_UINT32, VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET, 0, 1 ,31,0);
    __Vscopep_sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core->varInsert("integer_write_0_uopId", &(TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.integer_write_0_uopId), false, VLVT_UINT16, VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET, 0, 1 ,15,0);
    __Vscopep_sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core->varInsert("integer_write_0_valid", &(TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core.integer_write_0_valid), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET, 0, 0);
    __Vscopep_sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__integer_RegFilePlugin_logic_regfile_fpga->varInsert("asMem_ram", &(TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__vexiis_0_logic_core__integer_RegFilePlugin_logic_regfile_fpga.asMem_ram), false, VLVT_UINT32, VLVD_NODIR|VLVF_PUB_RW, 1, 1 ,0,31 ,31,0);
}
