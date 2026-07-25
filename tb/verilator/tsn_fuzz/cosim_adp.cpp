// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// tsn-gen <-> Verilator co-simulation server for adp_advertiser.
//
// ADP is TX-only in this design: the advertiser has no AXI-Stream ingress,
// it takes decoded event pulses (link up/down, discover received, GM change,
// ...). So the campaign drives EVENTS via control frames and validates the
// EMITTED ADPDU field by field against the entity-model inputs it was given
// — the discovery-side equivalent of a getter sweep, and the only way to
// prove every advertised field lands at its right wire offset.
//
// Built with -GDISC_DLY_BASE=4 -GDISC_DLY_MASK=3 (the adp TB's shrink) so the
// randomised discover-response delay is a few cycles instead of ~100 ms.
//
// Usage: Vadp_cosim <socket-path>
#include "Vadp_advertiser.h"
#include "verilated.h"
#include "cosim_axis.h"

static Vadp_advertiser* dut;

static void tick() {
    dut->clk_i = 0; dut->eval();
    dut->clk_i = 1; dut->eval();
}

static const uint8_t ENT_MAC[6] = {0x02, 0x00, 0x00, 0xff, 0xfe, 0x01};
static const uint64_t ENTITY_ID = 0x020000fffe000001ULL;
static const uint64_t MODEL_ID = 0x001B92FFFE0000AAULL;
static const uint64_t GM_ID = 0x0011223344556677ULL;

//! ADP event ids carried in a CTRL_EVENT frame's argument byte
enum {
    EV_LINK_UP = 0, EV_LINK_DOWN = 1, EV_DISCOVER = 2, EV_GM_CHANGE = 3,
    EV_INFO_CHANGED = 4, EV_SHUTDOWN = 5, EV_TICK = 6
};

static bool collect_frame(std::vector<uint8_t>& resp) {
    resp.clear();
    dut->m_axis_tready = 1;
    int idle = 0;
    for (int c = 0; c < 20000; c++) {
        dut->eval();
        if (dut->m_axis_tvalid && dut->m_axis_tready) {
            for (int l = 0; l < 8; l++)
                if ((dut->m_axis_tkeep >> l) & 1)
                    resp.push_back(static_cast<uint8_t>(dut->m_axis_tdata >> (8 * l)));
            bool last = dut->m_axis_tlast;
            tick();
            if (last) return true;
            idle = 0;
        } else {
            tick();
            if (++idle > 300) return !resp.empty();
        }
    }
    return !resp.empty();
}

static void clear_events() {
    dut->link_up_i = 0; dut->link_down_i = 0; dut->shutdown_i = 0;
    dut->gm_change_i = 0; dut->info_changed_i = 0; dut->rcv_discover_i = 0;
    dut->tick_i = 0;
}

static void apply_model() {
    dut->valid_time_i = 10;
    dut->entity_id_i = ENTITY_ID;
    dut->entity_model_id_i = MODEL_ID;
    dut->entity_capabilities_i = 0x00008588;
    dut->talker_stream_sources_i = 8;
    dut->talker_capabilities_i = 0x4801;
    dut->listener_stream_sinks_i = 8;
    dut->listener_capabilities_i = 0x4801;
    dut->controller_capabilities_i = 0;
    dut->gptp_grandmaster_id_i = GM_ID;
    dut->gptp_domain_number_i = 0;
    dut->current_configuration_index_i = 0;
    dut->identify_control_index_i = 0;
    dut->interface_index_i = 0;
    dut->association_id_i = 0;
    uint64_t m = 0;
    for (int i = 0; i < 6; i++) m = (m << 8) | ENT_MAC[i];
    dut->station_mac_i = m;
}

static std::vector<uint8_t> state_dump() {
    return tsn_state_frame({
        static_cast<uint32_t>(dut->available_index_o),
        static_cast<uint32_t>(dut->busy_o),
        static_cast<uint32_t>(dut->depart_cnt_o),
        static_cast<uint32_t>(dut->rearm_cnt_o),
        static_cast<uint32_t>(dut->depart_src_o),
    });
}

static void reset_dut() {
    dut->rst_n = 0;
    dut->enable_i = 1;
    dut->link_level_i = 1;
    dut->m_axis_tready = 1;
    clear_events();
    apply_model();
    for (int i = 0; i < 8; i++) tick();
    dut->rst_n = 1;
    for (int i = 0; i < 8; i++) tick();
}

//! pulse one event pin for a cycle, then let the advertiser run
static void pulse_event(int ev) {
    clear_events();
    switch (ev) {
    case EV_LINK_UP:      dut->link_level_i = 1; dut->link_up_i = 1; break;
    case EV_LINK_DOWN:    dut->link_level_i = 0; dut->link_down_i = 1; break;
    case EV_DISCOVER:     dut->rcv_discover_i = 1; break;
    case EV_GM_CHANGE:    dut->gm_change_i = 1; break;
    case EV_INFO_CHANGED: dut->info_changed_i = 1; break;
    case EV_SHUTDOWN:     dut->shutdown_i = 1; break;
    case EV_TICK:         dut->tick_i = 1; break;
    default: break;
    }
    tick();
    clear_events();
}

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    if (argc < 2) { fprintf(stderr, "usage: %s <socket-path>\n", argv[0]); return 1; }
    dut = new Vadp_advertiser;
    reset_dut();

    int rc = tsn_serve(argv[1], [](const std::vector<uint8_t>& cmd) -> Frames {
        Frames out;
        std::vector<uint8_t> f;
        if (!tsn_is_ctrl(cmd)) {
            // ADP has no ingress: any non-control frame is just a "run" request
            while (collect_frame(f)) out.push_back(f);
            return out;
        }
        switch (cmd[2]) {
        case CTRL_STATE:
            out.push_back(state_dump());
            return out;
        case CTRL_RESET:
            reset_dut();
            while (collect_frame(f)) out.push_back(f);   // link-up advertisement
            return out;
        case CTRL_TICK:
            for (int t = 0; t < cmd[3]; t++) {
                pulse_event(EV_TICK);
                for (int c = 0; c < 20; c++) tick();
            }
            while (collect_frame(f)) out.push_back(f);
            return out;
        case CTRL_EVENT:
            pulse_event(cmd[3]);
            while (collect_frame(f)) out.push_back(f);
            return out;
        default:
            return out;
        }
    });
    delete dut;
    return rc;
}
