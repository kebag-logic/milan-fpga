// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Model implementation (design independent parts)

#include "Vmac_tx_chain_mii__pch.h"

//============================================================
// Constructors

Vmac_tx_chain_mii::Vmac_tx_chain_mii(VerilatedContext* _vcontextp__, const char* _vcname__)
    : Vmac_tx_chain_mii{_vcontextp__, _vcname__, true} {}

Vmac_tx_chain_mii::Vmac_tx_chain_mii(VerilatedContext* _vcontextp__, const char* _vcname__, bool _vcisRoot__)
    : VerilatedModel{*_vcontextp__}
    , vlSymsp{new Vmac_tx_chain_mii__Syms(contextp(), this, _vcname__, _vcisRoot__)}
    , m_evalLoop{*this, /*convergeLimit:*/ 10000}
    , sys_clk{vlSymsp->vlInst.TOP.__VprimaryPorts.sys_clk}
    , sys_rst{vlSymsp->vlInst.TOP.__VprimaryPorts.sys_rst}
    , dp_clk{vlSymsp->vlInst.TOP.__VprimaryPorts.dp_clk}
    , dp_rst{vlSymsp->vlInst.TOP.__VprimaryPorts.dp_rst}
    , eth_tx_clk{vlSymsp->vlInst.TOP.__VprimaryPorts.eth_tx_clk}
    , eth_rx_clk{vlSymsp->vlInst.TOP.__VprimaryPorts.eth_rx_clk}
    , eth_phy_rst{vlSymsp->vlInst.TOP.__VprimaryPorts.eth_phy_rst}
    , reinit{vlSymsp->vlInst.TOP.__VprimaryPorts.reinit}
    , eth_rst{vlSymsp->vlInst.TOP.__VprimaryPorts.eth_rst}
    , loopback{vlSymsp->vlInst.TOP.__VprimaryPorts.loopback}
    , dp_tdata{vlSymsp->vlInst.TOP.__VprimaryPorts.dp_tdata}
    , dp_tkeep{vlSymsp->vlInst.TOP.__VprimaryPorts.dp_tkeep}
    , dp_tvalid{vlSymsp->vlInst.TOP.__VprimaryPorts.dp_tvalid}
    , dp_tlast{vlSymsp->vlInst.TOP.__VprimaryPorts.dp_tlast}
    , dp_tready{vlSymsp->vlInst.TOP.__VprimaryPorts.dp_tready}
    , gmii_tx_en{vlSymsp->vlInst.TOP.__VprimaryPorts.gmii_tx_en}
    , gmii_tx_data{vlSymsp->vlInst.TOP.__VprimaryPorts.gmii_tx_data}
    , gmii_tx_er{vlSymsp->vlInst.TOP.__VprimaryPorts.gmii_tx_er}
    , phy_sink_valid{vlSymsp->vlInst.TOP.__VprimaryPorts.phy_sink_valid}
    , phy_sink_ready{vlSymsp->vlInst.TOP.__VprimaryPorts.phy_sink_ready}
    , phy_sink_data{vlSymsp->vlInst.TOP.__VprimaryPorts.phy_sink_data}
    , phy_sink_last{vlSymsp->vlInst.TOP.__VprimaryPorts.phy_sink_last}
    , maceth_tx_rst{vlSymsp->vlInst.TOP.__VprimaryPorts.maceth_tx_rst}
    , rootp{&(vlSymsp->vlInst.TOP)}
{
    // Register model with the context
    contextp()->addModel(this);
}

Vmac_tx_chain_mii::Vmac_tx_chain_mii(const char* _vcname__)
    : Vmac_tx_chain_mii(Verilated::threadContextp(), _vcname__)
{
}

//============================================================
// Destructor

Vmac_tx_chain_mii::~Vmac_tx_chain_mii() {
    delete vlSymsp;
}

//============================================================
// Evaluation function

#ifdef VL_DEBUG
void Vmac_tx_chain_mii___024root___eval_debug_assertions(Vmac_tx_chain_mii___024root* vlSelf);
#endif  // VL_DEBUG
VL_ATTR_COLD void Vmac_tx_chain_mii___024root___eval_static(Vmac_tx_chain_mii___024root* vlSelf);
VL_ATTR_COLD void Vmac_tx_chain_mii___024root___eval_initial(Vmac_tx_chain_mii___024root* vlSelf);
VL_ATTR_COLD bool Vmac_tx_chain_mii___024root___eval_stl(Vmac_tx_chain_mii___024root* vlSelf, ::CData/*0:0*/ firstIteration);
void Vmac_tx_chain_mii___024root___eval_sample(Vmac_tx_chain_mii___024root* vlSelf);
bool Vmac_tx_chain_mii___024root___eval_ico(Vmac_tx_chain_mii___024root* vlSelf, ::CData/*0:0*/ firstIteration);
bool Vmac_tx_chain_mii___024root___eval_act(Vmac_tx_chain_mii___024root* vlSelf);
bool Vmac_tx_chain_mii___024root___eval_inact(Vmac_tx_chain_mii___024root* vlSelf);
bool Vmac_tx_chain_mii___024root___eval_nba(Vmac_tx_chain_mii___024root* vlSelf);
bool Vmac_tx_chain_mii___024root___eval_obs(Vmac_tx_chain_mii___024root* vlSelf);
bool Vmac_tx_chain_mii___024root___eval_react(Vmac_tx_chain_mii___024root* vlSelf);
void Vmac_tx_chain_mii___024root___eval_postponed(Vmac_tx_chain_mii___024root* vlSelf);
VL_ATTR_COLD void Vmac_tx_chain_mii___024root___eval_final(Vmac_tx_chain_mii___024root* vlSelf);
VL_ATTR_COLD void Vmac_tx_chain_mii___024root___eval_dump_triggers__stl(Vmac_tx_chain_mii___024root* vlSelf);
VL_ATTR_COLD void Vmac_tx_chain_mii___024root___eval_dump_triggers__ico(Vmac_tx_chain_mii___024root* vlSelf);
VL_ATTR_COLD void Vmac_tx_chain_mii___024root___eval_dump_triggers__act(Vmac_tx_chain_mii___024root* vlSelf);
VL_ATTR_COLD void Vmac_tx_chain_mii___024root___eval_dump_triggers__nba(Vmac_tx_chain_mii___024root* vlSelf);
VL_ATTR_COLD void Vmac_tx_chain_mii___024root___eval_dump_triggers__obs(Vmac_tx_chain_mii___024root* vlSelf);
VL_ATTR_COLD void Vmac_tx_chain_mii___024root___eval_dump_triggers__react(Vmac_tx_chain_mii___024root* vlSelf);

void Vmac_tx_chain_mii::eval_step() {
    VL_DEBUG_IF(VL_DBG_MSGF("+++++TOP Evaluate Vmac_tx_chain_mii::eval_step\n"); );
    m_evalLoop.eval();
}

void Vmac_tx_chain_mii::evalBegin() {
#ifdef VL_DEBUG
    // Debug assertions
    Vmac_tx_chain_mii___024root___eval_debug_assertions(&(vlSymsp->vlInst.TOP));
#endif  // VL_DEBUG
    vlSymsp->__Vm_deleter.deleteAll();
}

void Vmac_tx_chain_mii::evalEnd() {
    // Evaluate cleanup
    Verilated::endOfEval(vlSymsp->__Vm_evalMsgQp);
}

void Vmac_tx_chain_mii::evalStatic() {
    Vmac_tx_chain_mii___024root___eval_static(&(vlSymsp->vlInst.TOP));
}

void Vmac_tx_chain_mii::evalInitial() {
    Vmac_tx_chain_mii___024root___eval_initial(&(vlSymsp->vlInst.TOP));
}

bool Vmac_tx_chain_mii::evalStl(bool firstIteration) {
    return Vmac_tx_chain_mii___024root___eval_stl(&(vlSymsp->vlInst.TOP), firstIteration);
}

void Vmac_tx_chain_mii::evalSample() {
    Vmac_tx_chain_mii___024root___eval_sample(&(vlSymsp->vlInst.TOP));
}

bool Vmac_tx_chain_mii::evalIco(bool firstIteration) {
    return Vmac_tx_chain_mii___024root___eval_ico(&(vlSymsp->vlInst.TOP), firstIteration);
}

bool Vmac_tx_chain_mii::evalAct() {
    return Vmac_tx_chain_mii___024root___eval_act(&(vlSymsp->vlInst.TOP));
}

bool Vmac_tx_chain_mii::evalInact() {
    return Vmac_tx_chain_mii___024root___eval_inact(&(vlSymsp->vlInst.TOP));
}

bool Vmac_tx_chain_mii::evalNba() {
    return Vmac_tx_chain_mii___024root___eval_nba(&(vlSymsp->vlInst.TOP));
}

bool Vmac_tx_chain_mii::evalObs() {
    return Vmac_tx_chain_mii___024root___eval_obs(&(vlSymsp->vlInst.TOP));
}

bool Vmac_tx_chain_mii::evalReact() {
    return Vmac_tx_chain_mii___024root___eval_react(&(vlSymsp->vlInst.TOP));
}

void Vmac_tx_chain_mii::evalPostponed() {
    Vmac_tx_chain_mii___024root___eval_postponed(&(vlSymsp->vlInst.TOP));
}

void Vmac_tx_chain_mii::evalFinal() {
    Vmac_tx_chain_mii___024root___eval_final(&(vlSymsp->vlInst.TOP));
}

VL_ATTR_COLD void Vmac_tx_chain_mii::dumpTriggersStl() {
    Vmac_tx_chain_mii___024root___eval_dump_triggers__stl(&(vlSymsp->vlInst.TOP));
}

VL_ATTR_COLD void Vmac_tx_chain_mii::dumpTriggersIco() {
    Vmac_tx_chain_mii___024root___eval_dump_triggers__ico(&(vlSymsp->vlInst.TOP));
}

VL_ATTR_COLD void Vmac_tx_chain_mii::dumpTriggersAct() {
    Vmac_tx_chain_mii___024root___eval_dump_triggers__act(&(vlSymsp->vlInst.TOP));
}

VL_ATTR_COLD void Vmac_tx_chain_mii::dumpTriggersNba() {
    Vmac_tx_chain_mii___024root___eval_dump_triggers__nba(&(vlSymsp->vlInst.TOP));
}

VL_ATTR_COLD void Vmac_tx_chain_mii::dumpTriggersObs() {
    Vmac_tx_chain_mii___024root___eval_dump_triggers__obs(&(vlSymsp->vlInst.TOP));
}

VL_ATTR_COLD void Vmac_tx_chain_mii::dumpTriggersReact() {
    Vmac_tx_chain_mii___024root___eval_dump_triggers__react(&(vlSymsp->vlInst.TOP));
}

//============================================================
// Events and timing
bool Vmac_tx_chain_mii::eventsPending() { return false; }

uint64_t Vmac_tx_chain_mii::nextTimeSlot() {
    VL_FATAL_MT(__FILE__, __LINE__, "", "No delays in the design");
    return 0;
}

//============================================================
// Utilities

const char* Vmac_tx_chain_mii::name() const {
    return vlSymsp->name();
}

//============================================================
// Invoke final blocks

VL_ATTR_COLD void Vmac_tx_chain_mii::final() {
    contextp()->executingFinal(true);
    evalFinal();
    contextp()->executingFinal(false);
}

//============================================================
// Implementations of abstract methods from VerilatedModel

const char* Vmac_tx_chain_mii::hierName() const { return vlSymsp->name(); }
const char* Vmac_tx_chain_mii::modelName() const { return "Vmac_tx_chain_mii"; }
unsigned Vmac_tx_chain_mii::threads() const { return 1; }
void Vmac_tx_chain_mii::prepareClone() const { contextp()->prepareClone(); }
void Vmac_tx_chain_mii::atClone() const {
    contextp()->threadPoolpOnClone();
}
