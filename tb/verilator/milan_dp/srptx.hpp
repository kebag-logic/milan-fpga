// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// srptx.hpp - the split build's SRP transmit path to the wire (#867, #665),
// as twin_split.cpp's half runs it with --srptx. srptx_grade.py grades what
// this records.
//
// The path is the one the split SoC composes: lwSRP's MRPDU, the SRP adapter's
// record in the SRP channel's transmit ring, KL_mbx_tx, the byte crossing, the
// datapath's ctl_tx_mux, then the MAC. The bench sees four places on it:
//   - lwSRP's output: every MRPDU lwSRP handed the adapter in one transmit
//     opportunity, and the adapter's answer (0 sent, otherwise refused). The
//     binary links with --wrap for mrp_transmit, mrp_rx and
//     mrp_port_configure, so this is the library's own call at its own
//     boundary, and the adapter is not edited;
//   - lwSRP's timers: every arm of a participant's LeaveAll, periodic, Join
//     and Leave timer, and each expiry, read from the public cs field around
//     the real shlan_timer_tick (--wrap shlan_timer_arm, shlan_timer_tick);
//   - the mailbox: the SRP channel's TX_HEAD and TX_TAIL as the firmware
//     writes and reads them, and every LICENCE write;
//   - the MAC: every frame, with the time its first beat left.
//
// TIME. A modeled millisecond is one KL_mbx tick (twin_split.cpp). Inside it
// the bench clocks the RTL, so a time is the tick's millisecond plus the RTL
// time since the tick: 10 ns a mailbox cycle, 20 ns a datapath cycle. The
// firmware's own instructions take no simulated time; the CPU's cost is the
// CPU budget harness's figure (tb/verilator/ctrl_service_budget).
//
// Three scenarios, each a list of stimulus frames:
//   wire     the twin's stimulus, run to kWireMs, the production composition;
//   hold     the same, with a peer's LeaveAlls every 200 ms from 20 s, and the
//            MAC refusing every beat from kHoldFrom to kHoldTo, which fills
//            the SRP transmit ring (IEEE 802.1Q-2018 10.7.6.6: each rLA! makes the
//            Applicant send again);
//   licence  a peer Listener Ready for source 0, then the #608 case: the
//            peer's LeaveAll, no re-declaration, and its withdrawal while the
//            Registrar is in LV (IEEE 802.1Q-2018 Table 10-4; Milan v1.2
//            4.2.7.2.2).
//
// THE LICENCE SCENARIO'S FIXTURE. At this base every split source declares
// Talker Failed: the platform configures its sources unallocated, and the
// SRP adapter entry that re-declares a source once MAAP allocates is deferred
// until the adapter's transmit rework lands (#665; sw/firmware/ctrl/plat
// README, Not yet done). No talker can hold
// a licence, so nothing can stop. The licence scenario alone wraps
// srp_mbx_init and hands the adapter source 0 allocated at MAAP's pinned
// range, the address MAAP takes in this simulation, as that entry would. The
// fixture is the scenario's input, not the platform's, and srptx_grade.py
// names it in every finding of that scenario.
//
//   Vmilan_dp_twin_sp --srptx wire|hold|licence <capture.json> [--ms N]

#ifndef SRPTX_HPP
#define SRPTX_HPP

#include <algorithm>
#include <cstdint>
#include <cstdio>
#include <functional>
#include <map>
#include <set>
#include <string>
#include <vector>

#include "ports/timer.h"
#include "shish_lan/mrp.h"
#include "srp_mbx.h"
#include "twin.hpp"

namespace srptx {

constexpr std::uint64_t kMsrpGroup = 0x0180C200000Eull;   // IEEE 802.1Q-2018 35.2.2.1
constexpr std::uint64_t kMvrpGroup = 0x0180C2000021ull;   // IEEE 802.1Q-2018 11.2.3.1.3
//! the adapter's timers (srp_mbx.c): JoinTime 20 cs, LeaveTime 500 cs, LeaveAllTime 1000 cs
constexpr std::uint32_t kJoinCs = 20;
constexpr std::uint32_t kLeaveCs = 500;
constexpr std::uint32_t kLeaveAllCs = 1000;
constexpr std::uint32_t kPeriodicCs = 100;   // lwSRP's PeriodicTransmission timer (10.7.4.4)
//! the wire run: past forty LeaveAll draws of each participant
constexpr std::uint32_t kWireMs = 600000;
//! the hold run: the peer's LeaveAlls, and the window the MAC refuses
constexpr std::uint32_t kHoldLaFrom = 20000;
constexpr std::uint32_t kHoldLaTo = 30000;
constexpr std::uint32_t kHoldFrom = 22000;
constexpr std::uint32_t kHoldTo = 25000;
constexpr std::uint32_t kHoldMs = 40000;
//! the licence run: the peer's Listener Ready, its LeaveAll and its withdrawal,
//! between the split's own MSRP LeaveAlls at 14560 and 27910 ms
constexpr std::uint32_t kReadyMs = 3000;
constexpr std::uint32_t kPeerLeaveAllMs = 16000;
constexpr std::uint32_t kWithdrawMs = 18000;
constexpr std::uint32_t kLicenceMs = 26000;

// ---- the peer's MRPDUs (IEEE 802.1Q-2018 10.8.1.2, 10.8.2; 35.2.2) --------------

//! the AttributeEvents (IEEE 802.1Q-2018 10.8.2.10) the peer sends
constexpr std::uint8_t kNew = 0;
constexpr std::uint8_t kJoinIn = 1;
constexpr std::uint8_t kLv = 5;
constexpr std::uint8_t kReady = 2;   // 35.2.2.7.2, the Listener's FourPackedEvent

inline twin::Frame mrpdu(std::uint64_t group, std::uint16_t ethertype, const std::vector<std::uint8_t>& pdu) {
    twin::Frame f = twin::eth(group, twin::kPeerMac, ethertype, 14 + pdu.size());
    for (std::size_t k = 0; k < pdu.size(); ++k) f[14 + k] = pdu[k];
    return f;
}

//! One MSRP Message: AttributeType, AttributeLength, AttributeListLength, its
//! vectors and the AttributeList EndMark (35.2.2.x, 10.8.1.2).
inline std::vector<std::uint8_t> msrp_message(std::uint8_t type, std::uint8_t length,
                                              const std::vector<std::uint8_t>& vectors) {
    const std::size_t list = vectors.size() + 2;
    std::vector<std::uint8_t> m{type, length, static_cast<std::uint8_t>(list >> 8), static_cast<std::uint8_t>(list)};
    m.insert(m.end(), vectors.begin(), vectors.end());
    m.push_back(0);
    m.push_back(0);
    return m;
}

//! The peer's Listener declaration for one stream: one value, its event and Ready.
inline twin::Frame listener(std::uint64_t stream_id, std::uint8_t event) {
    std::vector<std::uint8_t> v{0x00, 0x01};
    for (unsigned k = 0; k < 8; ++k) v.push_back(static_cast<std::uint8_t>(stream_id >> (56 - 8 * k)));
    v.push_back(static_cast<std::uint8_t>(event * 36));
    v.push_back(static_cast<std::uint8_t>(kReady << 6));
    std::vector<std::uint8_t> pdu{0x00};
    const std::vector<std::uint8_t> m = msrp_message(3, 8, v);
    pdu.insert(pdu.end(), m.begin(), m.end());
    pdu.push_back(0);
    pdu.push_back(0);
    return mrpdu(kMsrpGroup, twin::kEtherMsrp, pdu);
}

//! The peer's MSRP LeaveAll and nothing else: a LeaveAll vector in a Message of
//! each MSRP AttributeType (10.8.2.6), as lwSRP sends its own.
inline twin::Frame msrp_leave_all() {
    std::vector<std::uint8_t> pdu{0x00};
    const std::uint8_t lengths[] = {25, 34, 8, 4};
    for (std::uint8_t type = 1; type <= 4; ++type) {
        std::vector<std::uint8_t> v{0x20, 0x00};
        v.resize(2 + lengths[type - 1], 0);
        const std::vector<std::uint8_t> m = msrp_message(type, lengths[type - 1], v);
        pdu.insert(pdu.end(), m.begin(), m.end());
    }
    pdu.push_back(0);
    pdu.push_back(0);
    return mrpdu(kMsrpGroup, twin::kEtherMsrp, pdu);
}

//! The peer's MVRP LeaveAll: one VID Message, its LeaveAll vector (11.2.3.1).
inline twin::Frame mvrp_leave_all() {
    return mrpdu(kMvrpGroup, twin::kEtherMvrp, {0x00, 0x01, 0x02, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00});
}

// ---- what the bench records -----------------------------------------------------

struct Lib {
    std::uint32_t ms;
    double us;
    std::uint16_t ethertype;
    unsigned opportunity;
    twin::Frame pdu;
    int rc;
    std::uint32_t ring_used;    // words in the SRP transmit ring when the adapter refused, else 0
    std::uint32_t record;       // the words the refused record needed
    std::uint32_t retries = 0;  // the same refusal again, at each poll until last_ms
    std::uint32_t last_ms = 0;
};

struct Opportunity {
    std::uint32_t ms;
    std::uint16_t ethertype;
    unsigned sends;
    unsigned accepted;
};

struct Timer {
    std::uint32_t ms;
    double us;
    std::uint16_t ethertype;
    std::string kind;    // leaveall, periodic, join, leave
    std::string event;   // arm, expire
    std::uint32_t cs;
    std::uintptr_t id;
};

struct Mac {
    std::uint32_t ms;
    double us;
    twin::Frame bytes;
};

struct Policer {
    std::uint32_t ms;
    std::uint32_t active;
    std::uint32_t admitted;
    std::uint32_t gate;
    bool aaf;
    bool crf_active;
    bool crf_emit;
};

struct Participant {
    std::uint16_t ethertype = 0;
    shlan_timer* la = nullptr;
};

struct Recorder {
    bool on = false;
    bool fixture = false;
    std::string scenario;
    std::uint32_t run_ms = 0;
    std::vector<std::pair<std::uint32_t, std::uint32_t>> holds;
    std::function<std::uint32_t()> ms;
    std::function<double()> us;
    // the context of the library call in progress
    const mrp_app* ctx = nullptr;
    bool configuring = false;
    unsigned opportunity = 0;
    std::map<const mrp_app*, Participant> apps;
    std::map<shlan_timer*, std::pair<std::uint16_t, std::string>> timers;
    std::string layout_error;
    // the SRP channel's ring, as the firmware last wrote TX_HEAD and read TX_TAIL
    std::uint16_t tx_head = 0;
    std::uint16_t tx_tail = 0;
    std::vector<Lib> lib;
    std::vector<Opportunity> opps;
    std::vector<Timer> timer_events;
    std::vector<std::pair<double, std::uint32_t>> licence_writes;
    std::vector<Mac> mac;
    std::map<std::pair<std::uint32_t, std::uint64_t>, unsigned> stream;   // (ms, stream_id) -> frames
    twin::Frame first_stream;                                              // the first stream frame, whole
    std::vector<Policer> policer;
    double intra_ms_max_us = 0;
    std::uint64_t talker_sid = 0;
    bool listener_declared = false;
};

inline Recorder& rec() {
    static Recorder r;
    return r;
}

inline std::uint16_t ethertype_of(const mrp_app* app) { return app && app->ops ? app->ops->ethertype : 0; }

inline bool held(std::uint32_t ms) {
    for (const auto& h : rec().holds)
        if (ms >= h.first && ms < h.second) return true;
    return false;
}

// ---- the mailbox side: the SRP ring's head and tail, and LICENCE ------------------

constexpr std::uint32_t kSrpTxHead = MBX_CH_BASE + MBX_CH_STRIDE * MBX_CH_SRP + MBX_CH_REG_TX_HEAD;
constexpr std::uint32_t kSrpTxTail = MBX_CH_BASE + MBX_CH_STRIDE * MBX_CH_SRP + MBX_CH_REG_TX_TAIL;
constexpr std::uint32_t kLicence = MBX_PUB_BASE + MBX_PUB_REG_LICENCE;   // interface 0's

//! Any channel's TX_HEAD: the doorbell of a committed record.
inline bool tx_head(std::uint32_t off) {
    return off >= MBX_CH_BASE && off < MBX_CH_BASE + MBX_CH_STRIDE * MBX_N_CH &&
           (off - MBX_CH_BASE) % MBX_CH_STRIDE == MBX_CH_REG_TX_HEAD;
}

inline void hal_write(std::uint32_t off, std::uint32_t v) {
    Recorder& r = rec();
    if (!r.on) return;
    if (off == kSrpTxHead) r.tx_head = static_cast<std::uint16_t>(v);
    if (off == kLicence) r.licence_writes.push_back({r.us(), v});
}

inline void hal_read(std::uint32_t off, std::uint32_t v) {
    if (rec().on && off == kSrpTxTail) rec().tx_tail = static_cast<std::uint16_t>(v);
}

// ---- the MAC side ---------------------------------------------------------------

inline std::uint64_t be(const twin::Frame& f, std::size_t at, unsigned n) {
    std::uint64_t v = 0;
    for (unsigned k = 0; k < n; ++k) v = v << 8 | f[at + k];
    return v;
}

//! One frame the MAC took, its first beat at `first_us`. A stream frame is
//! counted by its stream_id (IEEE 1722-2016 4.4.4.6); a control frame is kept.
//! In the licence scenario the peer answers each MSRP LeaveAll the split sends
//! with its Listener JoinIn while it still declares it (10.7.6.6: rLA! makes
//! its Applicant send again); the answer is returned for the bench to apply.
inline bool mac_frame(const twin::Frame& f, double first_us, twin::Frame* answer) {
    Recorder& r = rec();
    if (!r.on) return false;
    std::uint16_t t = 0;
    std::size_t at = 0;
    if (!twin::is_control(f)) {
        if (twin::ethertype(f, &t, &at) && t == twin::kEtherAvtp && at + 12 <= f.size()) {
            ++r.stream[{r.ms(), be(f, at + 4, 8)}];
            if (r.first_stream.empty()) r.first_stream = f;
        }
        return false;
    }
    r.mac.push_back({r.ms(), first_us, f});
    if (r.scenario != "licence" || !r.listener_declared || !twin::ethertype(f, &t, &at) || t != twin::kEtherMsrp)
        return false;
    // a LeaveAll in the frame's first Message (lwSRP flags every Message of its LeaveAll frame)
    if (at + 6 > f.size() || !(f[at + 5] & 0x20)) return false;
    *answer = listener(r.talker_sid, kJoinIn);
    return true;
}

//! The policer as the datapath has it at the end of each millisecond.
template <class Dut>
void sample(const Dut* d) {
    Recorder& r = rec();
    if (!r.on) return;
    const Policer p{r.ms(), d->p_active, d->p_admitted, d->p_stream_gate, d->p_aaf_gate != 0, d->p_crf_res_active != 0,
                    d->p_crf_emit != 0};
    const Policer* last = r.policer.empty() ? nullptr : &r.policer.back();
    if (!last || last->active != p.active || last->admitted != p.admitted || last->gate != p.gate ||
        last->aaf != p.aaf || last->crf_active != p.crf_active || last->crf_emit != p.crf_emit)
        r.policer.push_back(p);
}

// ---- the scenarios --------------------------------------------------------------

inline std::vector<twin::Stimulus> scenario(const std::string& name) {
    Recorder& r = rec();
    r.scenario = name;
    std::vector<twin::Stimulus> s;
    if (name == "wire" || name == "hold") s = twin::scenario();
    if (name == "wire") r.run_ms = kWireMs;
    if (name == "hold") {
        r.run_ms = kHoldMs;
        r.holds.push_back({kHoldFrom, kHoldTo});
        for (std::uint32_t ms = kHoldLaFrom; ms < kHoldLaTo; ms += 200) {
            s.push_back({ms, "MSRP LeaveAll, the peer", msrp_leave_all()});
            s.push_back({ms + 100, "MVRP LeaveAll, the peer", mvrp_leave_all()});
        }
    }
    if (name == "licence") {
        r.run_ms = kLicenceMs;
        r.fixture = true;
        s.push_back({kReadyMs, "MSRP Listener Ready New for source 0, the peer", listener(r.talker_sid, kNew)});
        s.push_back({kReadyMs + 200, "MSRP Listener Ready JoinIn for source 0, the peer", listener(r.talker_sid, kJoinIn)});
        s.push_back({kPeerLeaveAllMs, "MSRP LeaveAll, the peer, no re-declaration", msrp_leave_all()});
        s.push_back({kWithdrawMs, "MSRP Listener Ready Lv for source 0, the peer", listener(r.talker_sid, kLv)});
    }
    std::stable_sort(s.begin(), s.end(), [](const twin::Stimulus& a, const twin::Stimulus& b) { return a.ms < b.ms; });
    return s;
}

//! Applied to the bench: the licence scenario's peer declares its Listener
//! from its first Ready to its LeaveAll, after which it never declares again.
inline void applied(const std::string& what) {
    Recorder& r = rec();
    if (!r.on) return;
    if (what.rfind("MSRP Listener Ready New", 0) == 0) r.listener_declared = true;
    if (what.rfind("MSRP LeaveAll, the peer, no re-declaration", 0) == 0) r.listener_declared = false;
}

// ---- the capture ----------------------------------------------------------------

inline const char* proto(std::uint16_t ethertype) {
    return ethertype == twin::kEtherMsrp ? "MSRP" : ethertype == twin::kEtherMvrp ? "MVRP" : "?";
}

inline bool write(const char* path, const std::vector<twin::Capture::Applied>& applied) {
    const Recorder& r = rec();
    std::FILE* fh = std::fopen(path, "w");
    if (fh == nullptr) return false;
    std::fprintf(fh, "{\"scenario\": \"%s\", \"run_ms\": %u, \"fixture\": %s, \"port_mac\": \"%012llx\",\n",
                 r.scenario.c_str(), r.run_ms, r.fixture ? "true" : "false",
                 static_cast<unsigned long long>(twin::kEntityMac));
    std::fprintf(fh, " \"talker_sid\": \"%016llx\", \"ring_words\": %u, \"intra_ms_max_us\": %.4f,\n",
                 static_cast<unsigned long long>(r.talker_sid), MBX_CH_SRP_TX_WORDS, r.intra_ms_max_us);
    std::fprintf(fh, " \"layout_error\": \"%s\", \"first_stream\": \"%s\",\n \"holds\": [", r.layout_error.c_str(),
                 twin::hex(r.first_stream).c_str());
    for (std::size_t k = 0; k < r.holds.size(); ++k)
        std::fprintf(fh, "%s[%u, %u]", k ? ", " : "", r.holds[k].first, r.holds[k].second);
    std::fprintf(fh, "],\n \"timers_cs\": {\"join\": %u, \"leave\": %u, \"leaveall\": %u, \"periodic\": %u},\n",
                 kJoinCs, kLeaveCs, kLeaveAllCs, kPeriodicCs);
    std::fprintf(fh, " \"applied\": [");
    for (std::size_t k = 0; k < applied.size(); ++k)
        std::fprintf(fh, "%s\n  {\"ms\": %u, \"what\": \"%s\", \"hex\": \"%s\"}", k ? "," : "", applied[k].ms,
                     applied[k].what.c_str(), twin::hex(applied[k].frame).c_str());
    std::fprintf(fh, "],\n \"mac\": [");
    for (std::size_t k = 0; k < r.mac.size(); ++k)
        std::fprintf(fh, "%s\n  {\"ms\": %u, \"us\": %.4f, \"hex\": \"%s\"}", k ? "," : "", r.mac[k].ms, r.mac[k].us,
                     twin::hex(r.mac[k].bytes).c_str());
    std::fprintf(fh, "],\n \"lib\": [");
    for (std::size_t k = 0; k < r.lib.size(); ++k) {
        const Lib& l = r.lib[k];
        std::fprintf(fh, "%s\n  {\"ms\": %u, \"us\": %.4f, \"proto\": \"%s\", \"opportunity\": %u, \"rc\": %d, "
                     "\"ring_used\": %u, \"record\": %u, \"retries\": %u, \"last_ms\": %u, \"hex\": \"%s\"}", k ? "," : "",
                     l.ms, l.us, proto(l.ethertype), l.opportunity, l.rc, l.ring_used, l.record, l.retries, l.last_ms,
                     twin::hex(l.pdu).c_str());
    }
    std::fprintf(fh, "],\n \"opportunities\": [");
    for (std::size_t k = 0; k < r.opps.size(); ++k)
        std::fprintf(fh, "%s[%u, \"%s\", %u, %u]", k ? ", " : "", r.opps[k].ms, proto(r.opps[k].ethertype),
                     r.opps[k].sends, r.opps[k].accepted);
    std::fprintf(fh, "],\n \"timers\": [");
    for (std::size_t k = 0; k < r.timer_events.size(); ++k) {
        const Timer& t = r.timer_events[k];
        std::fprintf(fh, "%s\n  {\"ms\": %u, \"us\": %.4f, \"proto\": \"%s\", \"kind\": \"%s\", \"event\": \"%s\", "
                     "\"cs\": %u, \"id\": %llu}", k ? "," : "", t.ms, t.us, proto(t.ethertype), t.kind.c_str(),
                     t.event.c_str(), t.cs, static_cast<unsigned long long>(t.id));
    }
    std::fprintf(fh, "],\n \"licence_writes\": [");
    for (std::size_t k = 0; k < r.licence_writes.size(); ++k)
        std::fprintf(fh, "%s[%.4f, %u]", k ? ", " : "", r.licence_writes[k].first, r.licence_writes[k].second);
    std::fprintf(fh, "],\n \"policer\": [");
    for (std::size_t k = 0; k < r.policer.size(); ++k) {
        const Policer& p = r.policer[k];
        std::fprintf(fh, "%s\n  {\"ms\": %u, \"active\": %u, \"admitted\": %u, \"gate\": %u, \"aaf\": %d, "
                     "\"crf_active\": %d, \"crf_emit\": %d}", k ? "," : "", p.ms, p.active, p.admitted, p.gate,
                     p.aaf, p.crf_active, p.crf_emit);
    }
    std::fprintf(fh, "],\n \"stream\": [");
    bool first = true;
    for (const auto& e : r.stream) {
        std::fprintf(fh, "%s[%u, \"%016llx\", %u]", first ? "" : ", ", e.first.first,
                     static_cast<unsigned long long>(e.first.second), e.second);
        first = false;
    }
    std::fprintf(fh, "]}\n");
    return std::fclose(fh) == 0;
}

}  // namespace srptx

// ---- lwSRP's boundary, through the linker's --wrap ----------------------------------

extern "C" {
int __real_mrp_transmit(struct mrp_app* app, uint8_t port_id, uint8_t* pdu, size_t capacity, mrp_send_fn send,
                        void* ctx);
int __real_mrp_rx(struct mrp_app* app, uint8_t port_id, const uint8_t* pdu, size_t pdu_len);
int __real_mrp_port_configure(struct mrp_app* app, uint8_t port_id, uint32_t join_cs, uint32_t leave_cs,
                              uint32_t leaveall_cs, uint32_t seed, bool point_to_point);
void __real_shlan_timer_arm(struct shlan_timer* t, uint32_t centiseconds);
void __real_shlan_timer_tick(void);
bool __real_srp_mbx_init(struct srp_mbx* m, const struct srp_mbx_config* config);
}

namespace srptx {

//! The adapter's send callback, recorded: the MRPDU lwSRP built and the answer.
struct Trampoline {
    mrp_send_fn send;
    void* ctx;
    const mrp_app* app;
    unsigned sends = 0;
    unsigned accepted = 0;
};

inline int trampoline(void* raw, uint8_t port, const uint8_t* pdu, size_t len) {
    auto* t = static_cast<Trampoline*>(raw);
    const int rc = t->send(t->ctx, port, pdu, len);
    Recorder& r = rec();
    const std::uint32_t used = static_cast<std::uint16_t>(r.tx_head - r.tx_tail);
    const std::uint32_t record = MBX_TX_HDR_WORDS + (static_cast<std::uint32_t>(len) + 14u + 3u) / 4u;
    // a refusal repeated with the same MRPDU, as each poll retries it, counts on the first
    Lib* last = r.lib.empty() ? nullptr : &r.lib.back();
    if (rc != 0 && last != nullptr && last->rc == rc && last->ethertype == ethertype_of(t->app) &&
        last->pdu == twin::Frame(pdu, pdu + len)) {
        ++last->retries;
        last->last_ms = r.ms();
        last->ring_used = std::min(last->ring_used, used);
    } else {
        r.lib.push_back({r.ms(), r.us(), ethertype_of(t->app), r.opportunity, twin::Frame(pdu, pdu + len), rc,
                         rc != 0 ? used : 0u, rc != 0 ? record : 0u, 0u, r.ms()});
    }
    ++t->sends;
    if (rc == 0) ++t->accepted;
    return rc;
}

inline void timer_event(shlan_timer* t, const char* event, std::uint32_t cs) {
    Recorder& r = rec();
    const auto found = r.timers.find(t);
    if (found == r.timers.end()) return;
    r.timer_events.push_back({r.ms(), r.us(), found->second.first, found->second.second, event, cs,
                              reinterpret_cast<std::uintptr_t>(t)});
}

}  // namespace srptx

extern "C" int __wrap_mrp_transmit(struct mrp_app* app, uint8_t port_id, uint8_t* pdu, size_t capacity,
                                   mrp_send_fn send, void* ctx) {
    srptx::Recorder& r = srptx::rec();
    if (!r.on) return __real_mrp_transmit(app, port_id, pdu, capacity, send, ctx);
    const mrp_app* saved = r.ctx;
    r.ctx = app;
    srptx::Trampoline t{send, ctx, app};
    const int result = __real_mrp_transmit(app, port_id, pdu, capacity, &srptx::trampoline, &t);
    r.ctx = saved;
    if (t.accepted) r.opps.push_back({r.ms(), srptx::ethertype_of(app), t.sends, t.accepted});
    ++r.opportunity;
    return result;
}

extern "C" int __wrap_mrp_rx(struct mrp_app* app, uint8_t port_id, const uint8_t* pdu, size_t pdu_len) {
    srptx::Recorder& r = srptx::rec();
    const mrp_app* saved = r.ctx;
    r.ctx = app;
    const int result = __real_mrp_rx(app, port_id, pdu, pdu_len);
    r.ctx = saved;
    return result;
}

extern "C" int __wrap_mrp_port_configure(struct mrp_app* app, uint8_t port_id, uint32_t join_cs, uint32_t leave_cs,
                                         uint32_t leaveall_cs, uint32_t seed, bool point_to_point) {
    srptx::Recorder& r = srptx::rec();
    const mrp_app* saved = r.ctx;
    r.ctx = app;
    r.configuring = true;
    const int result = __real_mrp_port_configure(app, port_id, join_cs, leave_cs, leaveall_cs, seed, point_to_point);
    r.configuring = false;
    r.ctx = saved;
    return result;
}

//! Each arm names its timer. mrp_port_configure arms only the LeaveAll timer
//! (lwSRP mrp_mad.c), so that arm finds the participant's; its periodic and Join
//! timers follow it in the participant's state, and a Join arm inside its own
//! mrp_transmit that is not there is refused as a changed layout. An arm of
//! LeaveTime inside a library call is an attribute's Leave timer.
extern "C" void __wrap_shlan_timer_arm(struct shlan_timer* t, uint32_t centiseconds) {
    srptx::Recorder& r = srptx::rec();
    __real_shlan_timer_arm(t, centiseconds);
    if (!r.on || r.ctx == nullptr) {
        if (r.on) srptx::timer_event(t, "arm", centiseconds);
        return;
    }
    const std::uint16_t et = srptx::ethertype_of(r.ctx);
    srptx::Participant& p = r.apps[r.ctx];
    p.ethertype = et;
    if (r.configuring) {
        if (p.la != t) {
            p.la = t;
            r.timers[t] = {et, "leaveall"};
            r.timers[t + 1] = {et, "periodic"};
            r.timers[t + 2] = {et, "join"};
        }
    } else if (centiseconds == srptx::kJoinCs && p.la != nullptr && t != p.la + 2) {
        r.layout_error = "a Join timer arm outside its participant's state: lwSRP's port layout changed";
    } else if (centiseconds == srptx::kLeaveCs && r.timers.find(t) == r.timers.end()) {
        r.timers[t] = {et, "leave"};
    }
    srptx::timer_event(t, "arm", centiseconds);
}

extern "C" void __wrap_shlan_timer_tick(void) {
    srptx::Recorder& r = srptx::rec();
    if (!r.on) {
        __real_shlan_timer_tick();
        return;
    }
    std::vector<shlan_timer*> due;
    for (const auto& e : r.timers)
        if (e.first->cs == 1) due.push_back(e.first);
    __real_shlan_timer_tick();
    for (shlan_timer* t : due) srptx::timer_event(t, "expire", 0);
}

//! The licence scenario's fixture (the header's note): source 0 allocated at
//! MAAP's pinned range on every interface, as the deferred adapter entry
//! would declare it once MAAP allocates. srp_mbx_init copies its sources.
extern "C" bool __wrap_srp_mbx_init(struct srp_mbx* m, const struct srp_mbx_config* config) {
    if (!srptx::rec().fixture) return __real_srp_mbx_init(m, config);
    static srp_source sources[MBX_N_IF][CTRL_SRP_SOURCES];
    srp_mbx_config fixed = *config;
    for (unsigned i = 0; i < MBX_N_IF; ++i) {
        for (unsigned n = 0; n < CTRL_SRP_SOURCES; ++n) sources[i][n] = config->sources[i][n];
        sources[i][0].allocated = true;
        for (unsigned k = 0; k < 6; ++k)
            sources[i][0].value.dest_mac[k] = static_cast<std::uint8_t>(twin::kMaapPreferred >> (40 - 8 * k));
        fixed.sources[i] = sources[i];
    }
    return __real_srp_mbx_init(m, &fixed);
}

#endif  // SRPTX_HPP
