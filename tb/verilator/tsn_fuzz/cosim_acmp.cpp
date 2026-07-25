// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// tsn-gen <-> Verilator co-simulation server for KL_acmp_listener.
//
// The ACMP listener is THE state machine of the campaign: LSM_UNBOUND ->
// PRB_W_AVAIL -> PRB_W_DELAY -> PRB_W_RESP -> SETTLED_*. Fuzzing its input
// PDUs is only half the test; the other half is watching `state_o` and the
// bind context afterwards, which is what the CTRL_STATE dump exposes.
//
// Built with -GCLK_FREQ_HZ_P=10000 (the acmp_lstn TB's scaling) so 1 ms is
// 10 cycles and the 200 ms / 4 s probe timers are reachable in simulation.
//
// Usage: Vacmp_cosim <socket-path>
#include "VKL_acmp_listener.h"
#include "verilated.h"
#include "cosim_axis.h"

static VKL_acmp_listener* dut;

static void tick() {
    dut->clk_i = 0; dut->eval();
    dut->clk_i = 1; dut->eval();
}

static const uint8_t ENT_MAC[6] = {0x02, 0x00, 0x00, 0xff, 0xfe, 0x01};
static const uint64_t ENTITY_ID = 0x020000fffe000001ULL;

//! harvest one TX frame; false = the listener stayed silent
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
            if (++idle > 400) return !resp.empty();
        }
    }
    return !resp.empty();
}

static void feed(const std::vector<uint8_t>& f) {
    int n = static_cast<int>(f.size());
    for (int off = 0; off < n; off += 8) {
        uint64_t d = 0; uint8_t keep = 0;
        for (int l = 0; l < 8; l++)
            if (off + l < n) { d |= static_cast<uint64_t>(f[off + l]) << (8 * l); keep |= (1 << l); }
        dut->rx_tvalid_i = 1; dut->rx_tdata_i = d; dut->rx_tkeep_i = keep;
        dut->rx_tlast_i = (off + 8 >= n);
        tick();
    }
    dut->rx_tvalid_i = 0; dut->rx_tlast_i = 0; dut->rx_tkeep_i = 0;
    tick(); tick();
}

static std::vector<uint8_t> state_dump() {
    return tsn_state_frame({
        static_cast<uint32_t>(dut->state_o),
        static_cast<uint32_t>(dut->acmp_status_o),
        static_cast<uint32_t>(dut->cmd_count_o),
        static_cast<uint32_t>(dut->probe_count_o),
        static_cast<uint32_t>(dut->tx_wedge_cnt_o),
        static_cast<uint32_t>(dut->stream_active_o),
        static_cast<uint32_t>(dut->lstn_declare_o),
        static_cast<uint32_t>(dut->probing_o),
        static_cast<uint32_t>(dut->tk_avail_o),
        static_cast<uint32_t>(dut->bound_sid_o >> 32),
        static_cast<uint32_t>(dut->bound_sid_o & 0xFFFFFFFFu),
        static_cast<uint32_t>(dut->bound_tuid_o),
    });
}

static void reset_dut() {
    dut->rst_n = 0;
    dut->enable_i = 1;
    dut->tick_1s_i = 0;
    dut->rx_tvalid_i = 0; dut->rx_tlast_i = 0; dut->rx_tkeep_i = 0;
    dut->m_axis_tready = 1;
    dut->ta_registered_i = 0; dut->ta_failed_i = 0;
    dut->tbl_req_i = 0; dut->tbl_idx_i = 0;
    dut->rest_req_i = 0;
    dut->entity_id_i = ENTITY_ID;
    uint64_t m = 0;
    for (int i = 0; i < 6; i++) m = (m << 8) | ENT_MAC[i];
    dut->station_mac_i = m;
    for (int i = 0; i < 8; i++) tick();
    dut->rst_n = 1;
    for (int i = 0; i < 8; i++) tick();
}

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    if (argc < 2) { fprintf(stderr, "usage: %s <socket-path>\n", argv[0]); return 1; }
    dut = new VKL_acmp_listener;
    reset_dut();

    int rc = tsn_serve(argv[1], [](const std::vector<uint8_t>& cmd) -> Frames {
        Frames out;
        if (tsn_is_ctrl(cmd)) {
            switch (cmd[2]) {
            case CTRL_STATE:
                out.push_back(state_dump());
                return out;
            case CTRL_TICK: {                       // cmd[3] one-second ticks
                for (int t = 0; t < cmd[3]; t++) {
                    dut->tick_1s_i = 1; tick();
                    dut->tick_1s_i = 0;
                    for (int c = 0; c < 40; c++) tick();
                }
                std::vector<uint8_t> f;
                while (collect_frame(f)) out.push_back(f);   // timer-driven TX
                return out;
            }
            case CTRL_RESET:
                reset_dut();
                out.push_back(state_dump());
                return out;
            case CTRL_EVENT:                        // cmd[3]: SRP state bits
                dut->ta_registered_i = (cmd[3] >> 0) & 1;
                dut->ta_failed_i = (cmd[3] >> 1) & 1;
                for (int c = 0; c < 40; c++) tick();
                out.push_back(state_dump());
                return out;
            default:
                return out;
            }
        }
        feed(cmd);
        std::vector<uint8_t> f;
        while (collect_frame(f)) out.push_back(f);
        return out;
    });
    delete dut;
    return rc;
}
