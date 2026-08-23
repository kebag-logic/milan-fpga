// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// tsn-gen <-> Verilator co-simulation server for the gPTP fabric slice
// (KL_gptp_shadow + the real timestamp_counter + KL_gptp_txstamp, wired by
// the gptp_shadow TB's wrapper — the same slice the datapath splice
// instantiates, clocked at the bench's 2 MHz scaling).
//
// gPTP is a TIMER-DRIVEN plane: the engine transmits on its own schedule
// (Pdelay_Req every second, Announce/Sync when it is the grandmaster), not
// only in reply. So unlike the AAF server, every command's reply burst is
//
//     [ each frame the plane transmitted since the last command ... ]
//     [ the state dump, ALWAYS LAST ]
//
// and CTRL_TICK is how the driver buys the plane time: arg = blocks of
// 10,000 cycles (5 ms of bench time each). The driver tells wire frames
// from the dump by the dump's 0xC0 0x51 magic — no wire frame starts with
// it (802.1AS frames start with the 01:80:C2 multicast DA).
//
// CTRL_EVENT arms harness behaviors:
//   arg 1/0  pdelay auto-responder on/off — the proven sim_main.cpp
//            responder: answers the plane's Pdelay_Req with a fabric-timed
//            Resp + Resp_Follow_Up so the measured delay lands near
//            D_NOM = 600 ns and asCapable can climb
//   arg 3/2  TX lane backpressure on/off (tx_tready low/high)
//
// Usage: Vptp_cosim <socket-path>
#include "Vgptp_shadow_wrap.h"
#include "verilated.h"
#include "cosim_axis.h"

static Vgptp_shadow_wrap* dut;

static const uint64_t OUR_CID = 0x02A1B2FFFEC3D4E5ull;   // the engine's
static const uint64_t PEER_CID = 0x0080E1FFFE112233ull;  // the responder's
static const int64_t D_NOM = 600;                        // ns, one-way

static uint64_t cyc = 0;
static uint16_t last_txts_seq = 0xFFFF;
static uint32_t txts_cnt = 0;
static Frames txf;                       // every frame the plane transmitted
static std::vector<uint64_t> tx_sof_phc; // phc at each frame's first beat
static std::vector<uint8_t> cur;
static bool tx_first = true;
static size_t tx_ret = 0;                // frames already returned
static size_t pd_seen = 0;               // responder's scan cursor
static bool pd_on = false;
static int64_t pd_expect = 0;            // the last exchange's expected D

static uint64_t phc() { return dut->phc_ns_o; }

static void tick() {
    dut->clk_i = 0; dut->eval();
    dut->clk_i = 1; dut->eval();
    if (dut->dbg_txts_v_o) { last_txts_seq = dut->dbg_txts_seq_o; txts_cnt++; }
    if (dut->tx_tvalid_o && dut->tx_tready_i) {
        if (tx_first) { cur.clear(); tx_sof_phc.push_back(phc()); }
        for (int i = 0; i < 8; i++)
            if ((dut->tx_tkeep_o >> i) & 1)
                cur.push_back(static_cast<uint8_t>(dut->tx_tdata_o >> (8 * i)));
        if (dut->tx_tlast_o) { txf.push_back(cur); tx_first = true; }
        else                 { tx_first = false; }
    }
    cyc++;
}

static void run(uint64_t n) { while (n--) tick(); }

//! pack bytes into wide beats and drive the tap (harness is the DMA
//! consumer too: tready held high)
static void send_wide(const std::vector<uint8_t>& bytes) {
    size_t n = bytes.size();
    for (size_t off = 0; off < n; off += 8) {
        uint64_t d = 0; uint8_t k = 0;
        for (size_t i = 0; i < 8 && off + i < n; i++) {
            d |= static_cast<uint64_t>(bytes[off + i]) << (8 * i);
            k |= static_cast<uint8_t>(1u << i);
        }
        dut->rx_tdata_i = d;  dut->rx_tkeep_i = k;
        dut->rx_tvalid_i = 1; dut->rx_tready_i = 1;
        dut->rx_tlast_i = (off + 8 >= n);
        tick();
    }
    dut->rx_tvalid_i = 0;
    dut->rx_tlast_i = 0;
}

// ---- the auto-responder: sim_main.cpp's fabric-timed pdelay peer --------
static void put_u16(std::vector<uint8_t>& f, uint16_t v) {
    f.push_back(v >> 8); f.push_back(v & 0xFF);
}
static void put_u32(std::vector<uint8_t>& f, uint32_t v) {
    put_u16(f, v >> 16); put_u16(f, v & 0xFFFF);
}
static void put_u48(std::vector<uint8_t>& f, uint64_t v) {
    put_u16(f, (v >> 32) & 0xFFFF); put_u32(f, v & 0xFFFFFFFF);
}
static void put_u64(std::vector<uint8_t>& f, uint64_t v) {
    put_u32(f, v >> 32); put_u32(f, v & 0xFFFFFFFF);
}
static void put_ts(std::vector<uint8_t>& f, uint64_t ns) {
    put_u48(f, ns / 1000000000ull); put_u32(f, ns % 1000000000ull);
}

static std::vector<uint8_t> ptp_hdr(uint8_t mtype, uint16_t seq, uint16_t flags,
                                    uint16_t body_len) {
    std::vector<uint8_t> f;
    put_u48(f, 0x0180C200000Eull);
    put_u48(f, 0x0080E1112233ull);
    put_u16(f, 0x88F7);
    f.push_back(0x10 | mtype); f.push_back(0x02);
    put_u16(f, 34 + body_len);
    f.push_back(0); f.push_back(0);
    put_u16(f, flags);
    put_u64(f, 0);
    put_u32(f, 0);
    put_u64(f, PEER_CID); put_u16(f, 1);
    put_u16(f, seq);
    f.push_back(0x05); f.push_back(0x7F);
    return f;
}

static void service_pdelay() {
    while (pd_seen < txf.size()) {
        size_t i = pd_seen;
        if (txf[i].size() <= 14 || (txf[i][14] & 0xF) != 0x2) { pd_seen++; continue; }
        pd_seen++;
        if (!pd_on) continue;
        uint16_t seq = static_cast<uint16_t>((txf[i][44] << 8) | txf[i][45]);
        uint64_t t1 = tx_sof_phc[i];         // = the boundary stamp
        run(300);                            // a real turnaround, > 2*D_NOM
        uint64_t t2 = 5000000ull + phc();
        std::vector<uint8_t> f = ptp_hdr(0x3, seq, 0x0200, 20);
        put_ts(f, t2); put_u64(f, OUR_CID); put_u16(f, 1);
        // residence = (fabric turnaround) - 2*D_NOM, computed at send time;
        // the tap stamps t4 within a beat of the first wide beat below
        uint64_t resid = (phc() - t1) - 2 * static_cast<uint64_t>(D_NOM);
        uint64_t t3 = t2 + resid;
        uint64_t t4_est = phc() + 8;         // the next tick's beat 0
        pd_expect = static_cast<int64_t>((t4_est - t1) - resid) / 2;
        send_wide(f);
        run(50);
        std::vector<uint8_t> g = ptp_hdr(0xA, seq, 0x0000, 20);
        put_ts(g, t3); put_u64(g, OUR_CID); put_u16(g, 1);
        send_wide(g);
        run(50);
    }
}

static void run_svc(uint64_t n) {
    while (n--) { tick(); if ((n & 255) == 0) service_pdelay(); }
}

//! Every observable the campaign grades by. Order is the contract with
//! fuzz_ptp.py's STATE tuple — append only, never reorder.
static std::vector<uint8_t> state_dump() {
    return tsn_state_frame({
        static_cast<uint32_t>(dut->pub_flags_o),
        static_cast<uint32_t>(dut->pub_gm_id_o >> 32),
        static_cast<uint32_t>(dut->pub_gm_id_o),
        static_cast<uint32_t>(dut->pub_parent_id_o >> 32),
        static_cast<uint32_t>(dut->pub_parent_id_o),
        static_cast<uint32_t>(dut->pub_pdelay_ns_o),
        static_cast<uint32_t>(dut->pub_offset_o),
        static_cast<uint32_t>(dut->dbg_tap_drop_o),
        static_cast<uint32_t>(dut->dbg_rx_drop_o),
        static_cast<uint32_t>(phc() >> 32),
        static_cast<uint32_t>(phc()),
        static_cast<uint32_t>(txf.size()),
        static_cast<uint32_t>(last_txts_seq),
        txts_cnt,
        static_cast<uint32_t>(pd_expect),
        static_cast<uint32_t>(dut->dbg_prog_run_o),
    });
}

static void reset_dut() {
    dut->rst_n = 0;
    dut->rx_tvalid_i = 0; dut->rx_tlast_i = 0; dut->rx_tdata_i = 0;
    dut->rx_tkeep_i = 0;  dut->rx_tready_i = 1;
    dut->tx_tready_i = 1;
    for (int i = 0; i < 8; i++) tick();
    dut->rst_n = 1;
    for (int i = 0; i < 8; i++) tick();
    // harness bookkeeping restarts with the plane
    txf.clear(); tx_sof_phc.clear(); cur.clear();
    tx_first = true; tx_ret = 0; pd_seen = 0;
    last_txts_seq = 0xFFFF; txts_cnt = 0; pd_expect = 0;
}

//! reply burst: the plane's new TX frames, then the dump — dump LAST
static Frames reply() {
    Frames out;
    for (; tx_ret < txf.size(); tx_ret++) out.push_back(txf[tx_ret]);
    out.push_back(state_dump());
    return out;
}

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    if (argc < 2) { fprintf(stderr, "usage: %s <socket-path>\n", argv[0]); return 1; }
    dut = new Vgptp_shadow_wrap;
    reset_dut();

    int rc = tsn_serve(argv[1], [](const std::vector<uint8_t>& cmd) -> Frames {
        if (tsn_is_ctrl(cmd)) {
            switch (cmd[2]) {
            case CTRL_STATE:
                return reply();
            case CTRL_RESET:
                reset_dut();
                return reply();
            case CTRL_TICK:                       // arg × 10,000 cycles
                for (int t = 0; t < cmd[3]; t++) run_svc(10000);
                return reply();
            case CTRL_EVENT:
                switch (cmd[3]) {
                case 0: pd_on = false; break;
                case 1: pd_on = true;  service_pdelay(); break;
                case 2: dut->tx_tready_i = 1; break;
                case 3: dut->tx_tready_i = 0; break;
                default: break;
                }
                return reply();
            default:
                return Frames{};
            }
        }
        send_wide(cmd);
        run_svc(3000);           // parse + dispatch + any response TX
        return reply();
    });
    delete dut;
    return rc;
}
