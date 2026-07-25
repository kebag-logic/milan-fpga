// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// Shared co-simulation plumbing for the tsn-gen field campaign.
//
// Wire format: tsn-gen's packed 10-byte AxiStreamBeat (uint64 tdata
// little-lane, uint8 tkeep, uint8 tlast) — tdata[7:0] is the first wire byte,
// matching both the MAC and tsn-gen's packer.
//
// Session protocol (identical for every DUT here, and the reason the drivers
// can never desynchronise):
//
//   driver -> DUT   one frame
//   DUT -> driver   EVERY frame that frame produced, in order
//                   (reply first, then any unsolicited notification)
//   DUT -> driver   one empty beat = end-of-responses terminator
//
// So "silent", "one reply" and "reply + notification" are all unambiguous.
//
// CONTROL FRAMES: a frame of exactly 4 bytes starting 0xC0 0x51 is not wire
// traffic but a request to the harness — state dump, timer tick, reset. Real
// frames in this campaign are never that short (the shortest AECPDU frame is
// 30 bytes), so the encoding is unambiguous without a side channel, and the
// driver can observe DUT STATE (the point of a state-stability campaign)
// over the same socket.
#ifndef TSN_FUZZ_COSIM_AXIS_H
#define TSN_FUZZ_COSIM_AXIS_H

#include <cstdint>
#include <cstdio>
#include <cstring>
#include <functional>
#include <vector>
#include <sys/socket.h>
#include <sys/un.h>
#include <unistd.h>

struct __attribute__((packed)) AxiStreamBeat {
    uint64_t tdata;
    uint8_t tkeep;
    uint8_t tlast;
};
static_assert(sizeof(AxiStreamBeat) == 10, "beat must be 10 bytes");

//! control-frame magic + opcodes (see the header comment)
static const uint8_t CTRL_MAGIC0 = 0xC0, CTRL_MAGIC1 = 0x51;
enum { CTRL_STATE = 0x01, CTRL_TICK = 0x02, CTRL_RESET = 0x03, CTRL_EVENT = 0x04 };

using Frames = std::vector<std::vector<uint8_t>>;
//! handler(frame) -> the frames it produced. Control frames arrive here too.
using Handler = std::function<Frames(const std::vector<uint8_t>&)>;

inline bool tsn_read_all(int fd, void* p, size_t n) {
    auto* b = static_cast<uint8_t*>(p);
    while (n) {
        ssize_t r = read(fd, b, n);
        if (r <= 0) return false;
        b += r; n -= static_cast<size_t>(r);
    }
    return true;
}

inline bool tsn_write_all(int fd, const void* p, size_t n) {
    const auto* b = static_cast<const uint8_t*>(p);
    while (n) {
        ssize_t r = write(fd, b, n);
        if (r <= 0) return false;
        b += r; n -= static_cast<size_t>(r);
    }
    return true;
}

inline bool tsn_recv_frame(int fd, std::vector<uint8_t>& out) {
    out.clear();
    for (;;) {
        AxiStreamBeat beat;
        if (!tsn_read_all(fd, &beat, sizeof(beat))) return false;
        for (int i = 0; i < 8; i++)
            if (beat.tkeep & (1u << i))
                out.push_back(static_cast<uint8_t>(beat.tdata >> (i * 8)));
        if (beat.tlast) return true;
    }
}

inline bool tsn_send_frame(int fd, const std::vector<uint8_t>& f) {
    size_t n = f.size();
    if (n == 0) {                       // explicit zero-length frame
        AxiStreamBeat b{0, 0, 1};
        return tsn_write_all(fd, &b, sizeof(b));
    }
    for (size_t off = 0; off < n; off += 8) {
        AxiStreamBeat beat{};
        size_t chunk = (n - off < 8) ? (n - off) : 8;
        for (size_t i = 0; i < chunk; i++)
            beat.tdata |= static_cast<uint64_t>(f[off + i]) << (i * 8);
        beat.tkeep = static_cast<uint8_t>((1u << chunk) - 1u);
        beat.tlast = (off + 8 >= n) ? 1 : 0;
        if (!tsn_write_all(fd, &beat, sizeof(beat))) return false;
    }
    return true;
}

inline bool tsn_is_ctrl(const std::vector<uint8_t>& f) {
    return f.size() == 4 && f[0] == CTRL_MAGIC0 && f[1] == CTRL_MAGIC1;
}

//! pack a state dump as a frame: 4-byte magic header then big-endian u32s
inline std::vector<uint8_t> tsn_state_frame(const std::vector<uint32_t>& words) {
    std::vector<uint8_t> f{CTRL_MAGIC0, CTRL_MAGIC1, CTRL_STATE,
                           static_cast<uint8_t>(words.size())};
    for (uint32_t w : words)
        for (int i = 3; i >= 0; i--) f.push_back(static_cast<uint8_t>(w >> (8 * i)));
    return f;
}

//! Accept one client at a time and run the session protocol forever.
inline int tsn_serve(const char* path, const Handler& handler) {
    int srv = socket(AF_UNIX, SOCK_STREAM, 0);
    if (srv < 0) { perror("socket"); return 1; }
    struct sockaddr_un addr {};
    addr.sun_family = AF_UNIX;
    std::strncpy(addr.sun_path, path, sizeof(addr.sun_path) - 1);
    unlink(path);
    if (bind(srv, reinterpret_cast<sockaddr*>(&addr), sizeof(addr)) < 0) {
        perror("bind"); return 1;
    }
    if (listen(srv, 1) < 0) { perror("listen"); return 1; }
    fprintf(stderr, "[cosim] serving %s\n", path);
    for (;;) {
        int fd = accept(srv, nullptr, nullptr);
        if (fd < 0) break;
        std::vector<uint8_t> cmd;
        while (tsn_recv_frame(fd, cmd)) {
            Frames out = handler(cmd);
            bool alive = true;
            for (const auto& f : out) {
                if (!f.empty()) { alive = tsn_send_frame(fd, f); }
                if (!alive) break;
            }
            if (!alive) break;
            AxiStreamBeat term{0, 0, 1};          // end-of-responses
            if (!tsn_write_all(fd, &term, sizeof(term))) break;
        }
        close(fd);
    }
    return 0;
}

#endif  // TSN_FUZZ_COSIM_AXIS_H
