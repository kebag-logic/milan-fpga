// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table implementation internals

#include "Vmilan_datapath__pch.h"

Vmilan_datapath__Syms::Vmilan_datapath__Syms(VerilatedContext* contextp, const char* namep, Vmilan_datapath* modelp)
    : VerilatedSyms{contextp}
    // Setup internal state of the Syms class
    , __Vm_modelp{modelp}
    // Setup top module instance
    , TOP{this, namep}
{
    // Check resources
    Verilated::stackCheck(8232);
    // Setup sub module instances
    TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_rx.ctor(this, "milan_datapath.ptp_timestamp.m_axis_rx");
    TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx.ctor(this, "milan_datapath.ptp_timestamp.m_axis_tx");
    TOP__milan_datapath__DOT__ptp_timestamp__DOT__s_axis_rx.ctor(this, "milan_datapath.ptp_timestamp.s_axis_rx");
    TOP__milan_datapath__DOT__ptp_timestamp__DOT__s_axis_tx.ctor(this, "milan_datapath.ptp_timestamp.s_axis_tx");
    TOP__milan_datapath__DOT__ptp_timestamp__DOT__ts_m_axis_rx.ctor(this, "milan_datapath.ptp_timestamp.ts_m_axis_rx");
    TOP__milan_datapath__DOT__ptp_timestamp__DOT__ts_m_axis_tx.ctor(this, "milan_datapath.ptp_timestamp.ts_m_axis_tx");
    TOP__milan_datapath__DOT__ptp_timestamp__DOT__ts_rx_buffered.ctor(this, "milan_datapath.ptp_timestamp.ts_rx_buffered");
    TOP__milan_datapath__DOT__ptp_timestamp__DOT__ts_switch_to_fifo.ctor(this, "milan_datapath.ptp_timestamp.ts_switch_to_fifo");
    TOP__milan_datapath__DOT__ptp_timestamp__DOT__ts_tx_buffered.ctor(this, "milan_datapath.ptp_timestamp.ts_tx_buffered");
    TOP__milan_datapath__DOT__rx_axis_ptp_to_filt.ctor(this, "milan_datapath.rx_axis_ptp_to_filt");
    TOP__milan_datapath__DOT__rx_axis_to_dma.ctor(this, "milan_datapath.rx_axis_to_dma");
    TOP__milan_datapath__DOT__rx_axis_to_ts.ctor(this, "milan_datapath.rx_axis_to_ts");
    TOP__milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__m_axis_fifo.ctor(this, "milan_datapath.traffic_controller.classifier.m_axis_fifo");
    TOP__milan_datapath__DOT__traffic_controller__DOT__classifier_to_queue.ctor(this, "milan_datapath.traffic_controller.classifier_to_queue");
    TOP__milan_datapath__DOT__traffic_controller__DOT__queue_to_shaper.ctor(this, "milan_datapath.traffic_controller.queue_to_shaper");
    TOP__milan_datapath__DOT__ts_metadata_axis.ctor(this, "milan_datapath.ts_metadata_axis");
    TOP__milan_datapath__DOT__tx_axis_dp_to_arb.ctor(this, "milan_datapath.tx_axis_dp_to_arb");
    TOP__milan_datapath__DOT__tx_axis_shaper_to_ts.ctor(this, "milan_datapath.tx_axis_shaper_to_ts");
    TOP__milan_datapath__DOT__tx_axis_to_mac.ctor(this, "milan_datapath.tx_axis_to_mac");
    TOP__milan_datapath__DOT__tx_axis_to_shaper.ctor(this, "milan_datapath.tx_axis_to_shaper");
    // Configure time unit / time precision
    _vm_contextp__->timeunit(-9);
    _vm_contextp__->timeprecision(-12);
    // Setup each module's pointers to their submodules
    TOP.__PVT__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_rx = &TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_rx;
    TOP.__PVT__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx = &TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx;
    TOP.__PVT__milan_datapath__DOT__ptp_timestamp__DOT__s_axis_rx = &TOP__milan_datapath__DOT__ptp_timestamp__DOT__s_axis_rx;
    TOP.__PVT__milan_datapath__DOT__ptp_timestamp__DOT__s_axis_tx = &TOP__milan_datapath__DOT__ptp_timestamp__DOT__s_axis_tx;
    TOP.__PVT__milan_datapath__DOT__ptp_timestamp__DOT__ts_m_axis_rx = &TOP__milan_datapath__DOT__ptp_timestamp__DOT__ts_m_axis_rx;
    TOP.__PVT__milan_datapath__DOT__ptp_timestamp__DOT__ts_m_axis_tx = &TOP__milan_datapath__DOT__ptp_timestamp__DOT__ts_m_axis_tx;
    TOP.__PVT__milan_datapath__DOT__ptp_timestamp__DOT__ts_rx_buffered = &TOP__milan_datapath__DOT__ptp_timestamp__DOT__ts_rx_buffered;
    TOP.__PVT__milan_datapath__DOT__ptp_timestamp__DOT__ts_switch_to_fifo = &TOP__milan_datapath__DOT__ptp_timestamp__DOT__ts_switch_to_fifo;
    TOP.__PVT__milan_datapath__DOT__ptp_timestamp__DOT__ts_tx_buffered = &TOP__milan_datapath__DOT__ptp_timestamp__DOT__ts_tx_buffered;
    TOP.__PVT__milan_datapath__DOT__rx_axis_ptp_to_filt = &TOP__milan_datapath__DOT__rx_axis_ptp_to_filt;
    TOP.__PVT__milan_datapath__DOT__rx_axis_to_dma = &TOP__milan_datapath__DOT__rx_axis_to_dma;
    TOP.__PVT__milan_datapath__DOT__rx_axis_to_ts = &TOP__milan_datapath__DOT__rx_axis_to_ts;
    TOP.__PVT__milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__m_axis_fifo = &TOP__milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__m_axis_fifo;
    TOP.__PVT__milan_datapath__DOT__traffic_controller__DOT__classifier_to_queue = &TOP__milan_datapath__DOT__traffic_controller__DOT__classifier_to_queue;
    TOP.__PVT__milan_datapath__DOT__traffic_controller__DOT__queue_to_shaper = &TOP__milan_datapath__DOT__traffic_controller__DOT__queue_to_shaper;
    TOP.__PVT__milan_datapath__DOT__ts_metadata_axis = &TOP__milan_datapath__DOT__ts_metadata_axis;
    TOP.__PVT__milan_datapath__DOT__tx_axis_dp_to_arb = &TOP__milan_datapath__DOT__tx_axis_dp_to_arb;
    TOP.__PVT__milan_datapath__DOT__tx_axis_shaper_to_ts = &TOP__milan_datapath__DOT__tx_axis_shaper_to_ts;
    TOP.__PVT__milan_datapath__DOT__tx_axis_to_mac = &TOP__milan_datapath__DOT__tx_axis_to_mac;
    TOP.__PVT__milan_datapath__DOT__tx_axis_to_shaper = &TOP__milan_datapath__DOT__tx_axis_to_shaper;
    // Setup each module's pointer back to symbol table (for public functions)
    TOP.__Vconfigure(true);
    TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_rx.__Vconfigure(true);
    TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx.__Vconfigure(false);
    TOP__milan_datapath__DOT__ptp_timestamp__DOT__s_axis_rx.__Vconfigure(false);
    TOP__milan_datapath__DOT__ptp_timestamp__DOT__s_axis_tx.__Vconfigure(false);
    TOP__milan_datapath__DOT__ptp_timestamp__DOT__ts_m_axis_rx.__Vconfigure(false);
    TOP__milan_datapath__DOT__ptp_timestamp__DOT__ts_m_axis_tx.__Vconfigure(false);
    TOP__milan_datapath__DOT__ptp_timestamp__DOT__ts_rx_buffered.__Vconfigure(false);
    TOP__milan_datapath__DOT__ptp_timestamp__DOT__ts_switch_to_fifo.__Vconfigure(false);
    TOP__milan_datapath__DOT__ptp_timestamp__DOT__ts_tx_buffered.__Vconfigure(false);
    TOP__milan_datapath__DOT__rx_axis_ptp_to_filt.__Vconfigure(false);
    TOP__milan_datapath__DOT__rx_axis_to_dma.__Vconfigure(false);
    TOP__milan_datapath__DOT__rx_axis_to_ts.__Vconfigure(false);
    TOP__milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__m_axis_fifo.__Vconfigure(false);
    TOP__milan_datapath__DOT__traffic_controller__DOT__classifier_to_queue.__Vconfigure(true);
    TOP__milan_datapath__DOT__traffic_controller__DOT__queue_to_shaper.__Vconfigure(false);
    TOP__milan_datapath__DOT__ts_metadata_axis.__Vconfigure(false);
    TOP__milan_datapath__DOT__tx_axis_dp_to_arb.__Vconfigure(false);
    TOP__milan_datapath__DOT__tx_axis_shaper_to_ts.__Vconfigure(false);
    TOP__milan_datapath__DOT__tx_axis_to_mac.__Vconfigure(false);
    TOP__milan_datapath__DOT__tx_axis_to_shaper.__Vconfigure(false);
    // Setup scopes
    __Vscopep_milan_datapath = new VerilatedScope{this, "milan_datapath", "milan_datapath", "<null>", 0, VerilatedScope::SCOPE_OTHER};
    __Vscopep_milan_datapath__acmp_listener_sm__u_ctx = new VerilatedScope{this, "milan_datapath.acmp_listener_sm.u_ctx", "u_ctx", "<null>", -9, VerilatedScope::SCOPE_OTHER};
    __Vscopep_milan_datapath__acmp_listener_sm__u_ctx__probe_byte = new VerilatedScope{this, "milan_datapath.acmp_listener_sm.u_ctx.probe_byte", "probe_byte", "<null>", -9, VerilatedScope::SCOPE_OTHER};
    __Vscopep_milan_datapath__aecp_listener__u_parser = new VerilatedScope{this, "milan_datapath.aecp_listener.u_parser", "u_parser", "<null>", -9, VerilatedScope::SCOPE_OTHER};
    __Vscopep_milan_datapath__traffic_controller__classifier__class_map = new VerilatedScope{this, "milan_datapath.traffic_controller.classifier.class_map", "class_map", "<null>", -9, VerilatedScope::SCOPE_OTHER};
    __Vscopep_milan_datapath__traffic_controller__classifier__class_map__classify = new VerilatedScope{this, "milan_datapath.traffic_controller.classifier.class_map.classify", "classify", "<null>", -9, VerilatedScope::SCOPE_OTHER};
    // Setup export functions - final: 0
    // Setup export functions - final: 1
    // Setup public variables
    __Vscopep_milan_datapath->varInsert("aaf_stream_en_w", &(TOP.milan_datapath__DOT__aaf_stream_en_w), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD|VLVF_CONTINUOUSLY|VLVF_NET, 0, 1 ,7,0);
    __Vscopep_milan_datapath->varInsert("rend_pcm_tvalid_w", &(TOP.milan_datapath__DOT__rend_pcm_tvalid_w), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RD|VLVF_NET, 0, 0);
}

Vmilan_datapath__Syms::~Vmilan_datapath__Syms() {
    // Tear down scopes
    VL_DO_CLEAR(delete __Vscopep_milan_datapath, __Vscopep_milan_datapath = nullptr);
    VL_DO_CLEAR(delete __Vscopep_milan_datapath__acmp_listener_sm__u_ctx, __Vscopep_milan_datapath__acmp_listener_sm__u_ctx = nullptr);
    VL_DO_CLEAR(delete __Vscopep_milan_datapath__acmp_listener_sm__u_ctx__probe_byte, __Vscopep_milan_datapath__acmp_listener_sm__u_ctx__probe_byte = nullptr);
    VL_DO_CLEAR(delete __Vscopep_milan_datapath__aecp_listener__u_parser, __Vscopep_milan_datapath__aecp_listener__u_parser = nullptr);
    VL_DO_CLEAR(delete __Vscopep_milan_datapath__traffic_controller__classifier__class_map, __Vscopep_milan_datapath__traffic_controller__classifier__class_map = nullptr);
    VL_DO_CLEAR(delete __Vscopep_milan_datapath__traffic_controller__classifier__class_map__classify, __Vscopep_milan_datapath__traffic_controller__classifier__class_map__classify = nullptr);
    // Tear down sub module instances
    TOP__milan_datapath__DOT__tx_axis_to_shaper.dtor();
    TOP__milan_datapath__DOT__tx_axis_to_mac.dtor();
    TOP__milan_datapath__DOT__tx_axis_shaper_to_ts.dtor();
    TOP__milan_datapath__DOT__tx_axis_dp_to_arb.dtor();
    TOP__milan_datapath__DOT__ts_metadata_axis.dtor();
    TOP__milan_datapath__DOT__traffic_controller__DOT__queue_to_shaper.dtor();
    TOP__milan_datapath__DOT__traffic_controller__DOT__classifier_to_queue.dtor();
    TOP__milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__m_axis_fifo.dtor();
    TOP__milan_datapath__DOT__rx_axis_to_ts.dtor();
    TOP__milan_datapath__DOT__rx_axis_to_dma.dtor();
    TOP__milan_datapath__DOT__rx_axis_ptp_to_filt.dtor();
    TOP__milan_datapath__DOT__ptp_timestamp__DOT__ts_tx_buffered.dtor();
    TOP__milan_datapath__DOT__ptp_timestamp__DOT__ts_switch_to_fifo.dtor();
    TOP__milan_datapath__DOT__ptp_timestamp__DOT__ts_rx_buffered.dtor();
    TOP__milan_datapath__DOT__ptp_timestamp__DOT__ts_m_axis_tx.dtor();
    TOP__milan_datapath__DOT__ptp_timestamp__DOT__ts_m_axis_rx.dtor();
    TOP__milan_datapath__DOT__ptp_timestamp__DOT__s_axis_tx.dtor();
    TOP__milan_datapath__DOT__ptp_timestamp__DOT__s_axis_rx.dtor();
    TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx.dtor();
    TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_rx.dtor();
}
