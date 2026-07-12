/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * tsn-gen <-> Verilator co-simulation harness for KL_aecp_top.
 *
 * A AF_UNIX socket SERVER that speaks tsn-gen's AxiStreamBeat wire format
 * (packed 10 bytes: uint64 tdata little-endian, uint8 tkeep, uint8 tlast,
 * tb/verilator/aecp <- tsn-gen/traffic-gen/inc/tsn/axi_stream_beat.h). For each
 * command frame received it drives the bytes into the DUT's RX monitor tap,
 * runs the clock until the AECP listener emits its response on m_axis, and
 * writes the response back over the same connection as AxiStreamBeats.
 *
 * The DUT is the REAL RTL (KL_aecp_top); tsn-gen generates the spec-shaped AECP
 * command stimulus and decodes/validates the responses. Byte order on the wire
 * is little-lane (tdata[7:0] = first wire byte), matching both the MAC and
 * tsn-gen's packer.
 *
 * Usage: Vaecp_cosim <socket-path>
 */
#include "VKL_aecp_top.h"
#include "verilated.h"
#include <cstdio>
#include <cstdint>
#include <cstring>
#include <vector>
#include <sys/socket.h>
#include <sys/un.h>
#include <unistd.h>

struct __attribute__((packed)) AxiStreamBeat { uint64_t tdata; uint8_t tkeep; uint8_t tlast; };
static_assert(sizeof(AxiStreamBeat) == 10, "beat must be 10 bytes");

static VKL_aecp_top* dut;
static void tick() { dut->clk_i = 0; dut->eval(); dut->clk_i = 1; dut->eval(); }

// entity identity (mirrors tb/verilator/aecp/sim_main.cpp + the board CSR setup)
static const uint8_t ENT_MAC[6] = {0x02,0x00,0x00,0xff,0xfe,0x01};
static const uint64_t ENTITY_ID = 0x020000fffe000001ULL;

static bool read_all(int fd, void* p, size_t n) {
    auto* b = (uint8_t*)p;
    while (n) { ssize_t r = read(fd, b, n); if (r <= 0) return false; b += r; n -= (size_t)r; }
    return true;
}
static bool write_all(int fd, const void* p, size_t n) {
    auto* b = (const uint8_t*)p;
    while (n) { ssize_t r = write(fd, b, n); if (r <= 0) return false; b += r; n -= (size_t)r; }
    return true;
}

// read one framed packet (beats until tlast) -> wire bytes (little-lane)
static bool recv_frame(int fd, std::vector<uint8_t>& out) {
    out.clear();
    for (;;) {
        AxiStreamBeat beat;
        if (!read_all(fd, &beat, sizeof(beat))) return false;
        for (int i = 0; i < 8; i++)
            if (beat.tkeep & (1u << i)) out.push_back((uint8_t)(beat.tdata >> (i * 8)));
        if (beat.tlast) return true;
    }
}
// write a wire-byte frame as beats (little-lane)
static bool send_frame(int fd, const std::vector<uint8_t>& f) {
    size_t n = f.size();
    for (size_t off = 0; off < n; off += 8) {
        AxiStreamBeat beat{}; size_t chunk = (n - off < 8) ? (n - off) : 8;
        for (size_t i = 0; i < chunk; i++) beat.tdata |= (uint64_t)f[off + i] << (i * 8);
        beat.tkeep = (uint8_t)((1u << chunk) - 1u);
        beat.tlast = (off + 8 >= n) ? 1 : 0;
        if (!write_all(fd, &beat, sizeof(beat))) return false;
    }
    return true;
}

// drive one command frame into the RX tap; capture the response frame (empty if none)
static void run_command(const std::vector<uint8_t>& cmd, std::vector<uint8_t>& resp) {
    int n = (int)cmd.size();
    for (int off = 0; off < n; off += 8) {
        uint64_t d = 0; uint8_t keep = 0;
        for (int l = 0; l < 8; l++) if (off + l < n) { d |= (uint64_t)cmd[off + l] << (8 * l); keep |= (1 << l); }
        dut->rx_tvalid_i = 1; dut->rx_tdata_i = d; dut->rx_tkeep_i = keep;
        dut->rx_tlast_i = (off + 8 >= n); tick();
    }
    dut->rx_tvalid_i = 0; dut->rx_tlast_i = 0; dut->rx_tkeep_i = 0;

    resp.clear();
    dut->m_axis_tready = 1;
    int idle = 0;
    for (int c = 0; c < 8000; c++) {
        dut->eval();
        if (dut->m_axis_tvalid && dut->m_axis_tready) {
            for (int l = 0; l < 8; l++) if ((dut->m_axis_tkeep >> l) & 1) resp.push_back((uint8_t)(dut->m_axis_tdata >> (8 * l)));
            bool last = dut->m_axis_tlast; tick();
            if (last) return;
            idle = 0;
        } else { tick(); if (++idle > 600) return; }
    }
}

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    if (argc < 2) { fprintf(stderr, "usage: %s <socket-path>\n", argv[0]); return 1; }
    const char* path = argv[1];

    dut = new VKL_aecp_top;
    dut->rst_n = 0; dut->enable_i = 1; dut->rx_tvalid_i = 0; dut->m_axis_tready = 1;
    dut->entity_id_i = ENTITY_ID; dut->entity_model_id_i = 0;
    dut->entity_caps_i = 0x00008588; dut->talker_sources_i = 8; dut->talker_caps_i = 0x4801;
    dut->listener_sinks_i = 8; dut->listener_caps_i = 0x4801; dut->controller_caps_i = 0;
    dut->available_index_i = 0; dut->association_id_i = 0;
    dut->gptp_gm_id_i = 0x0011223344556677ULL; dut->gptp_domain_i = 0;
    { uint64_t m = 0; for (int i = 0; i < 6; i++) m = (m << 8) | ENT_MAC[i]; dut->station_mac_i = m; }
    for (int i = 0; i < 8; i++) tick();
    dut->rst_n = 1;
    for (int i = 0; i < 4; i++) tick();

    int srv = socket(AF_UNIX, SOCK_STREAM, 0);
    struct sockaddr_un addr{}; addr.sun_family = AF_UNIX;
    std::strncpy(addr.sun_path, path, sizeof(addr.sun_path) - 1);
    unlink(path);
    if (bind(srv, (sockaddr*)&addr, sizeof(addr)) < 0) { perror("bind"); return 1; }
    if (listen(srv, 1) < 0) { perror("listen"); return 1; }
    fprintf(stderr, "[cosim] KL_aecp_top listening on %s (entity 0x%016llx)\n",
            path, (unsigned long long)ENTITY_ID);

    for (;;) {
        int fd = accept(srv, nullptr, nullptr);
        if (fd < 0) break;
        std::vector<uint8_t> cmd, resp;
        while (recv_frame(fd, cmd)) {
            run_command(cmd, resp);
            fprintf(stderr, "[cosim] cmd %zuB -> resp %zuB\n", cmd.size(), resp.size());
            if (!resp.empty()) { if (!send_frame(fd, resp)) break; }
        }
        close(fd);
    }
    delete dut; return 0;
}
